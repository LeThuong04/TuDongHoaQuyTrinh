from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from bs4 import BeautifulSoup
import schedule
import requests
from uuid import uuid4

def initDriver():
    # Khởi tạo và trả về một instance của Chrome WebDriver
    return webdriver.Chrome()

def aiPage(driver):
    # Điều hướng đến mục tin tức AI trên trang vnexpress.net
    driver.get("https://vnexpress.net/")
    parent = driver.find_element(By.CSS_SELECTOR, "#wrap-main-nav > nav > ul > li.khoahoccongnghe")
    ActionChains(driver).move_to_element(parent).perform()
    element = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#wrap-main-nav > nav > ul > li.khoahoccongnghe > ul > li:nth-child(4)"))
    )
    element.click()
    time.sleep(2)

def getLinks(driver, page):
    # Lấy danh sách link bài viết từ một trang cụ thể
    driver.get(f"https://vnexpress.net/cong-nghe/ai-p{page}")
    time.sleep(2)
    articles = driver.find_elements(By.CSS_SELECTOR, ".title-news a")
    return [article.get_attribute("href") for article in articles]

def hasNextPage(driver):
    # Kiểm tra xem có trang tiếp theo hay không
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, ".next-page")
        return next_button.is_enabled() and next_button.is_displayed()
    except:
        return False

def getImageUrl(soup):
    # Lấy URL của hình ảnh từ trang bài viết
    image_container = soup.find('div', class_='fig-picture')
    if not image_container:
        return "Không có hình ảnh"
    
    image_url = image_container.get('data-src')
    if image_url:
        return image_url
        
    image = image_container.find('img')
    return image.get('data-src') or image.get('src') or "Không có hình ảnh" if image else "Không có hình ảnh"

def scrapeArticle(link):
    # Thu thập nội dung từ một bài viết cụ thể
    try:
        news = requests.get(link)
        soup = BeautifulSoup(news.content, "html.parser")
        
        title = soup.find('h1', class_='title-detail')
        title = title.text.strip() if title else "Không có tiêu đề"
        
        summary = soup.find('p', class_='description')
        summary = summary.text.strip() if summary else ""
        
        body = soup.find("article", class_="fck_detail")
        content = body.get_text(strip=True) if body else ""
        
        image_url = getImageUrl(soup)
        
        return [title, summary, content, image_url]
    except Exception as e:
        print(f"Lỗi khi thu thập bài viết {link}: {e}")
        return ["Không có tiêu đề", "", "", "Không có hình ảnh"]

def saveToExcel(data):
    # Lưu dữ liệu thu thập được vào file Excel
    df = pd.DataFrame(data, columns=['Tiêu đề', 'Tóm tắt', 'Nội dung', 'Hình ảnh'])
    df.to_excel(f'vnexpress_{uuid4()}.xlsx', index=False)

def job():
    # Hàm chính để thu thập tất cả bài viết AI từ vnexpress.net
    print("Đang lưu dữ liệu")
    driver = initDriver()
    try:
        aiPage(driver)
        article_data = []
        page = 1
        
        while page :
            links = getLinks(driver, page)
            for link in links:
                article_data.append(scrapeArticle(link))
            
            if not hasNextPage(driver):
                break
            page += 1
        
        saveToExcel(article_data)
    finally:
        driver.quit()

if __name__ == "__main__":
    schedule.every().day.at("06:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
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

driver = webdriver.Chrome()

def job():
    print("đang lưu dữ liệu")
    
    driver.get("https://vnexpress.net/")

    parent = driver.find_element(By.CSS_SELECTOR, "#wrap-main-nav > nav > ul > li.khoahoccongnghe")
    ActionChains(driver).move_to_element(parent).perform()
    element = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#wrap-main-nav > nav > ul > li.khoahoccongnghe > ul > li:nth-child(4)"))
    )

    element.click()
    time.sleep(2)

    article_data = []

    #5. Lấy tất cả dữ liệu của 5 trang đầu (lấy tất cả chưa hiểu nên em lấy 5 trang đầu ) 
    for page in range(1,5):
        driver.get(f"https://vnexpress.net/cong-nghe/ai-p{page}")
        time.sleep(2)

        #lấy link bài 
        class_link = ".title-news a"
        articles = driver.find_elements(By.CSS_SELECTOR, class_link)
        links = [article.get_attribute("href") for article in articles]
        
        for link in links:
            news = requests.get(link)
            soup = BeautifulSoup(news.content, "html.parser")
            # lấy tiêu đề
            title = soup.find('h1', class_='title-detail')
            title = title.text.strip() if title else "Không có tiêu đề"
            # lấy tóm tắt
            summary = soup.find('p', class_='description')
            summary = summary.text.strip() if summary else ""
            # lấy nội dung
            body = soup.find("article", class_="fck_detail")
            try:
                content = body.get_text(strip=True) if body else ""
            except:
                content = ""
            # lấy hình ảnh
            try:
                image_container = soup.find('div', class_='fig-picture')
                if image_container:
                    image_url = image_container.get('data-src', '')
                    if  image_url == '':
                        image = image_container.find('img')
                        if image and 'data-src' in image.attrs:
                            image_url = image['data-src']
                        elif image and 'src' in image.attrs:
                            image_url = image['src']
                        else:
                            image_url = "Không có hình ảnh"
                    else:
                        image_url = "Không có hình ảnh"
                else:
                    image_url = "Không có hình ảnh"
            except Exception as e:
                print(f"Lỗi khi lấy hình ảnh từ {link}: {e}")
                image_url = "Không có hình ảnh"
            article_data.append([title, summary, content, image_url])
            
    #6. Lưu dữ liệu vào file excel
    df = pd.DataFrame(article_data, columns=['Tiêu đề', 'Tóm tắt', 'Nội dung', 'Hình ảnh'])
    df.to_excel('vnexpress.xlsx', index=False)
    driver.quit()
#7. Set lịch chạy vào lúc 6h sáng hằng ngày.

schedule.every().day.at("06:00").do(job)
# job()
while True:
    schedule.run_pending() 
    time.sleep(1)


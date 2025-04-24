# Công Cụ Thu Thập Dữ Liệu Từ VNExpress

Script tự động thu thập bài viết từ báo VNExpress. Công cụ này trích xuất tiêu đề, tóm tắt, nội dung chính và URL hình ảnh của các bài báo rồi lưu vào file Excel

# Tính Năng

- Thu thập bài viết từ 5 trang đầu tiên của chuyên mục "Công Nghệ"
- Trích xuất các thông tin:
  - Tiêu đề 
  - Phần tóm tắt
  - Nội dung chính
  - URL hình ảnh 
- Lưu dữ liệu vào file Excel `vnexpress.xlsx`
- Tự động chạy vào lúc 6:00 sáng và 12:00 trưa hàng ngày

# Yêu Cầu thư viện

Các thư viện Python cần thiết:
- `selenium`
- `pandas`
- `beautifulsoup4`
- `schedule`
- `requests`



# Cài Đặt

1. **Cài đặt thư viện**  
   Chạy lệnh sau trong terminal:
   ```bash
   pip install selenium pandas beautifulsoup4 schedule requests
2 Chạy file code:
    Chạy lệnh sau trong terminal:
    python btl.py
# Công Cụ Thu Thập Dữ Liệu Từ VNExpress

Script Python tự động thu thập bài viết từ chuyên mục AI của báo VNExpress. Công cụ này trích xuất tiêu đề, tóm tắt, nội dung chính và URL hình ảnh của các bài báo, sau đó lưu vào file Excel.

## Tính Năng

- Thu thập bài viết từ 5 trang đầu tiên của chuyên mục "Công Nghệ - AI" trên VNExpress.
- Trích xuất các thông tin:
  - **Tiêu đề**: Tiêu đề bài viết.
  - **Tóm tắt**: Phần mô tả ngắn của bài viết.
  - **Nội dung chính**: Toàn bộ nội dung chi tiết của bài báo.
  - **URL hình ảnh**: Đường dẫn đến hình ảnh minh họa (nếu có).
- Lưu dữ liệu vào file Excel với tên định dạng `vnexpress_<UUID>.xlsx`.
- Lên lịch chạy tự động vào **6:00 sáng** và **12:00 trưa** hàng ngày.

## Yêu Cầu Thư Viện

Các thư viện Python cần thiết:
- `selenium` (để điều khiển trình duyệt và thu thập link bài viết)
- `pandas` (để lưu dữ liệu vào file Excel)
- `beautifulsoup4` (để phân tích HTML và trích xuất nội dung)
- `schedule` (để lên lịch chạy tự động)
- `requests` (để tải nội dung trang bài viết)
- Trình duyệt Chrome và **ChromeDriver** tương thích (cần cài đặt riêng).

## Cài Đặt

1. **Cài đặt thư viện Python**  
   Mở terminal và chạy lệnh sau để cài đặt các thư viện cần thiết:
   ```bash
   pip install selenium pandas beautifulsoup4 schedule requests
   ```

2. **Cài đặt ChromeDriver**  
   - Tải ChromeDriver tương thích với phiên bản trình duyệt Chrome của bạn từ [trang chính thức](https://chromedriver.chromium.org/downloads).
   - Đặt file `chromedriver` vào thư mục trong biến PATH của hệ thống hoặc chỉ định đường dẫn trong code nếu cần.

3. **Chuẩn bị môi trường**  
   - Đảm bảo trình duyệt Chrome đã được cài đặt trên máy tính.
   - Kiểm tra kết nối internet ổn định để truy cập trang VNExpress.

4. **Chạy script**  
   - Lưu code vào file, ví dụ `btl.py`.
   - Mở terminal, di chuyển đến thư mục chứa file và chạy lệnh:
     ```bash
     python btl.py
     ```

## Cách Sử Dụng

- Script sẽ tự động chạy vào **6:00 sáng** và **12:00 trưa** hàng ngày theo lịch đã thiết lập.
- Mỗi lần chạy, script sẽ:
  - Thu thập bài viết từ 5 trang đầu tiên của chuyên mục AI.
  - Lưu dữ liệu vào file Excel mới với tên duy nhất (sử dụng UUID).
- Để chạy thủ công, bạn có thể bỏ phần lịch trình (`schedule`) và gọi hàm `mainJob()` trực tiếp.

## Lưu Ý

- Đảm bảo ChromeDriver và Chrome có phiên bản tương thích để tránh lỗi.
- File Excel đầu ra sẽ được lưu trong cùng thư mục với script.
- Nếu trang VNExpress thay đổi cấu trúc HTML, cần cập nhật các bộ chọn CSS (`CSS_SELECTOR`) trong code.
- Script hiện tại giới hạn ở 5 trang để test; để thu thập tất cả trang, xóa hằng số `MAX_PAGES` và logic kiểm tra liên quan trong hàm `mainJob`.
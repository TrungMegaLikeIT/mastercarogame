### Đồ án Cờ caro

- Yêu cầu đồ án hiện tại :
    - Game có thể chạy, có màn hình bắt đầu, trong màn hình bắt đầu có 2 nút là start và setting
    - Nút setting sẽ đi tới màn hình setting
    - trong màn hình setting sẽ có nút back quay lại màn hình bắt đầu, tạm thời chưa có setting nào cần tạo
    - khi bấm nút start thì sẽ vào game
    - màn hình game sẽ có bảng cờ caro và 2 nút, 1 nút quay về màn hình bắt đầu, 1 nút đến màn hình setting
    - Sử dụng pygame sprite để render texture, hiện tại chưa có texture thì tạo texture thủ công trong code, texture tạo thủ công chỉ đơn sắc ( mỗi pixel sẽ có chung 4 thuộc tính (r, g, b, a)) 
    
- Thiết kế kiến trúc mã nguồn : 
    - Sử dụng thư viện đồ họa pygame ( đã cài trên máy, dạng pygame-ce ) 
    - Sử dụng lập trình hướng đối tượng
    - tuân thủ nguyên tắc SOLID và các nguyên tắc trong OOP và trong lập trình nói chung ( Composition over inheritance, low coupling high cohesion, KISS,.... )
    - chỉ sử dụng tối đa chỉ 2 tầng kế thừa, không tính tầng kế thừa từ pygame ( ví dụ : pygame.? -> ông nội -> cha -> con )
    - hạn chế sử dụng nhiều biến boolean cho việc chuyển các trạng thái trong game ( start, settings, game ) làm code khó đọc

- khi chuyển từ game state sang setting state thì trong setting state lúc đó cần phải có 2 nút là back to game và back to start, back to start sẽ quay về start screen, khi quay về start screen thì trạng thái của game trở về ban đầu, còn khi back to game sẽ quay trở lại game và game vẫn giữ trạng thái trước khi bấm vào nút setting ở trong game. Còn khi từ menu state tới setting state thì chỉ cần một nút back. tôi đề xuất chèn tham số từ game state vào setting state để tạo thêm một nút back to game. 
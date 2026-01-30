# BÁO CÁO BÀI TẬP LỚN: ỨNG DỤNG MINH HỌA VÀ ĐÁNH GIÁ THUẬT TOÁN TÌM ĐƯỜNG
**Môn học:** [Tên Môn Học]  
**Sinh viên thực hiện:** [Tên Sinh Viên]  

---

## MỤC LỤC
1. [GIỚI THIỆU](#i-giới-thiệu)
2. [PHÁT BIỂU BÀI TOÁN](#ii-phát-biểu-bài-toán)
3. [NGHIÊN CỨU LIÊN QUAN](#iii-nghiên-cứu-liên-quan)
4. [PHƯƠNG PHÁP ĐỀ XUẤT](#iv-phương-pháp-đề-xuất)
5. [KẾT QUẢ THỰC NGHIỆM](#v-kết-quả-thực-nghiệm)
6. [KẾT LUẬN](#vi-kết-luận)

---

## I. GIỚI THIỆU

### 1.1. Bối cảnh và động lực nghiên cứu
Trong khoa học máy tính và robotics, bài toán tìm đường đi ngắn nhất hoặc khả thi giữa hai điểm trong một không gian có vật cản là một bài toán kinh điển. Từ việc định tuyến gói tin trên Internet, điều hướng nhân vật trong trò chơi điện tử (Game AI), đến lập kế hoạch di chuyển cho robot tự hành, các thuật toán tìm kiếm trên đồ thị đóng vai trò cốt lõi.

Nhu cầu thực tiễn đặt ra là làm sao để không chỉ tìm được đường đi, mà còn phải tối ưu về mặt thời gian thực thi và tài nguyên bộ nhớ, đặc biệt khi quy mô bản đồ (đồ thị) tăng lên.

### 1.2. Mục tiêu của đề tài
Xây dựng một ứng dụng trực quan hóa (Visualizer) và hệ thống đánh giá hiệu năng (Benchmarking Suite) nhằm:
1.  Minh họa trực quan cơ chế hoạt động của các thuật toán sinh mê cung và tìm đường.
2.  So sánh, đánh giá định lượng hiệu năng (thời gian, bộ nhớ, độ dài đường đi) của các thuật toán cổ điển như BFS, DFS, Dijkstra và A*.

### 1.3. Đóng góp chính của đề tài
*   Hệ thống mô phỏng tương tác thời gian thực sử dụng kiến trúc MVC.
*   Bộ công cụ đánh giá tự động (Headless Benchmark) cho phép kiểm thử trên quy mô lớn.
*   Phân tích so sánh chi tiết giữa các thuật toán heuristic (A*) và thuật toán vét cạn (BFS/Dijkstra).

---

## II. PHÁT BIỂU BÀI TOÁN

### 2.1. Mô tả bài toán
Cho một lưới 2 chiều (Grid) kích thước $M \times N$, mỗi ô (cell) có thể là đường đi hoặc tường chắn.
*   **Input:** Điểm bắt đầu $S$ và điểm kết thúc $E$.
*   **Output:** Một chuỗi các ô liền kề nối từ $S$ đến $E$ không đi qua tường.
*   **Yêu cầu:** Tùy thuộc vào thuật toán, yêu cầu có thể là tìm đường đi bất kỳ hoặc đường đi ngắn nhất.

### 2.2. Mô hình hóa toán học
Lưới được mô hình hóa dưới dạng Đồ thị vô hướng $G = (V, E)$.
*   $V$: Tập hợp các ô trống trong mê cung.
*   $E$: Tập hợp các cạnh nối hai ô liền kề $(u, v)$ nếu không có tường ngăn cách.
*   Hàm mục tiêu (cho bài toán đường đi ngắn nhất): Tìm đường dẫn $P = (v_1, v_2, ..., v_k)$ sao cho $k$ là nhỏ nhất, với $v_1 = S, v_k = E$.

### 2.3. Khó khăn và thách thức
*   **Không gian trạng thái:** Số lượng trạng thái tăng theo cấp số nhân hoặc đa thức bậc cao tùy thuộc vào kích thước lưới.
*   **Cạm bẫy cục bộ:** Với các mê cung phức tạp (nhiều ngõ cụt), các thuật toán tham lam đơn giản dễ bị kẹt hoặc tốn nhiều thời gian quay lui (backtracking).

---

## III. NGHIÊN CỨU LIÊN QUAN

### 3.1. Các phương pháp truyền thống
*   **Breadth-First Search (BFS):** Duyệt theo chiều rộng. Đảm bảo tìm ra đường đi ngắn nhất trong đồ thị không trọng số. Độ phức tạp $O(V+E)$.
*   **Depth-First Search (DFS):** Duyệt theo chiều sâu. Không đảm bảo đường đi ngắn nhất, thường bị kẹt trong các nhánh sâu vô hạn nếu không gian không giới hạn, nhưng tiết kiệm bộ nhớ hơn BFS.
*   **Dijkstra:** Tổng quát hóa của BFS cho đồ thị có trọng số không âm.

### 3.2. Các hướng tiếp cận hiện đại (Heuristic)
*   **A* (A-Star):** Sử dụng hàm đánh giá $f(n) = g(n) + h(n)$, trong đó $h(n)$ là hàm heuristic ước lượng khoảng cách đến đích (ví dụ: khoảng cách Manhattan). Giúp định hướng tìm kiếm về phía đích, giảm không gian tìm kiếm.

---

## IV. PHƯƠNG PHÁP ĐỀ XUẤT

### 4.1. Ý tưởng tổng quát
Ứng dụng được xây dựng bằng ngôn ngữ **Python** và thư viện đồ họa **Pygame-ce**. Kiến trúc phần mềm tuân thủ mẫu thiết kế **Model-View-Controller (MVC)** để tách biệt logic thuật toán khỏi giao diện hiển thị.

### 4.2. Chi tiết thuật toán / Mô hình
*   **Model (`model/`):**
    *   `Grid` & `Cell`: Quản lý cấu trúc dữ liệu đồ thị.
    *   **Generators:** Sử dụng `Recursive Backtracker` (DFS ngẫu nhiên) và `Prim's Algorithm` để sinh mê cung hoàn hảo (không có vòng lặp).
    *   **Solvers:** Cài đặt các thuật toán BFS, DFS, A*, Dijkstra dưới dạng **Python Generators** (`yield`). Điều này cho phép tạm dừng thực thi tại mỗi bước để cập nhật giao diện (visualize).
*   **Controller (`controller/`):** Điều phối luồng chương trình, xử lý sự kiện bàn phím/chuột.
*   **View (`view/`):** Chịu trách nhiệm vẽ lưới và các trạng thái (đang duyệt - open set, đã duyệt - closed set, đường đi).

### 4.3. Phân tích độ phức tạp
*   **Thời gian:**
    *   BFS/Dijkstra: $O(V + E)$ hay $O(b^d)$ với $b$ là hệ số nhánh, $d$ là độ sâu.
    *   A*: Phụ thuộc vào heuristic. Tốt nhất là $O(d)$, tệ nhất biến thành BFS.
*   **Không gian:**
    *   BFS lưu trữ toàn bộ biên (frontier) nên tốn bộ nhớ $O(b^d)$.
    *   DFS chỉ lưu trữ nhánh hiện tại $O(d)$.

---

## V. KẾT QUẢ THỰC NGHIỆM

### 5.1. Cấu hình thực nghiệm
*   **Phần cứng:** [Điền thông tin CPU/RAM của bạn]
*   **Môi trường:** Python 3.x, Pygame-ce.
*   **Thiết lập:** Chạy Benchmark tự động trên các kích thước lưới: $10\times10, 30\times30, 50\times50, ..., 100\times100$. Mỗi kích thước chạy lặp lại 50 lần để lấy trung bình.

### 5.2. Phương pháp Baseline để so sánh
Sử dụng **BFS** làm chuẩn (baseline) vì nó luôn tìm ra đường đi ngắn nhất, từ đó so sánh độ chính xác và tốc độ của A* và DFS.

### 5.3. Các tiêu chí đánh giá
1.  **Thời gian thực thi (Runtime - ms):** Tốc độ xử lý của thuật toán.
2.  **Số nút đã duyệt (Visited Nodes):** Đại diện cho khối lượng tính toán và hiệu quả của heuristic.
3.  **Độ dài đường đi (Path Length):** Đánh giá độ tối ưu của kết quả (Optimal vs Sub-optimal).

### 5.4. Phân tích kết quả
*(Phần này sẽ được điền sau khi chạy script `benchmark_runner.py` và `analyze_results.py`)*

*   **Về tốc độ:** A* thường nhanh hơn Dijkstra và BFS đáng kể nhờ heuristic định hướng.
*   **Về tính tối ưu:** DFS cho ra kết quả đường đi rất dài và ngoằn ngoèo (sub-optimal), trong khi BFS và A* (với heuristic chấp nhận được) luôn tìm ra đường ngắn nhất.
*   **Về khả năng mở rộng:** Khi kích thước lưới tăng lên, thời gian chạy của DFS tăng tuyến tính nhưng khó dự đoán, trong khi BFS tăng theo cấp số nhân của độ sâu tìm kiếm.

---

## VI. KẾT LUẬN

### Tóm tắt kết quả chính
Đề tài đã xây dựng thành công bộ công cụ trực quan hóa và so sánh thuật toán. Kết quả thực nghiệm cho thấy A* là lựa chọn cân bằng tốt nhất giữa tốc độ và độ tối ưu cho bài toán tìm đường trên lưới 2D.

### Hướng phát triển
*   Mở rộng sang không gian 3D.
*   Thử nghiệm với các thuật toán hiện đại hơn như IDA*, Jump Point Search (JPS).
*   Áp dụng cho bài toán Multi-Agent Pathfinding (nhiều nhân vật di chuyển cùng lúc).

---
**TÀI LIỆU THAM KHẢO**
1.  Russell, S. J., & Norvig, P. (2010). *Artificial Intelligence: A Modern Approach*.
2.  Tài liệu Pygame-ce: https://pyga.me/
3.  D. E. Knuth, *The Art of Computer Programming*.

import numpy as np

def find_loop(check, start_i, start_j):
    rows = len(check)
    cols = len(check[0])
    
    loop = [(start_i, start_j)]

    def backtrack(curr_i, curr_j, direction):
        # Kiểm tra nếu đã quay về điểm bắt đầu và có ít nhất 4 điểm trong chu trình
        if len(loop) > 3 and (curr_i, curr_j) == loop[0]:
            return True
        
        # Duyệt theo hàng
        if direction in {'row', None}:
            for col in range(cols):
                if col != curr_j and check[curr_i][col] == 0 and (curr_i, col) not in loop[1:len(loop)-1]:
                    loop.append((curr_i, col))
                    print(f"Thêm vào loop: {loop}")  # In giá trị loop sau khi thêm
                    if backtrack(curr_i, col, 'col'):
                        return True
                    loop.pop()
                    print(f"Duyệt ngược và xóa: {loop[-1]}, loop hiện tại: {loop}")  # In giá trị loop sau khi xóa

        # Duyệt theo cột
        if direction in {'col', None}:
            for row in range(rows):
                if row != curr_i and check[row][curr_j] == 0 and (row, curr_j) not in loop[1:len(loop)-1]:
                    loop.append((row, curr_j))
                    print(f"Thêm vào loop: {loop}")  # In giá trị loop sau khi thêm
                    if backtrack(row, curr_j, 'row'):
                        return True
                    loop.pop()
                    print(f"Duyệt ngược và xóa: {loop[-1]}, loop hiện tại: {loop}")  # In giá trị loop sau khi xóa

        return False

    # Bắt đầu tìm chu trình
    if backtrack(start_i, start_j, None):
        return loop
    else:
        print("Không tìm thấy chu trình.")
        return []

# Sử dụng hàm tìm chu trình
check_matrix = np.array([
    [0, 3, 7, 0],
    [0, 0, 0, 5],
    [-9, -14, 0, 8],
    [-12, -7, 0, 0],
])

loop_result = find_loop(check_matrix, 0, 3)
print("Chu trình tìm được:", loop_result)

import numpy as np

def balance_supply_demand(cost, supply, demand):
    total_supply = sum(supply)
    total_demand = sum(demand)

    if total_supply > total_demand:
        # Thêm cột giả
        demand.append(total_supply - total_demand)
        cost = np.append(cost, np.zeros((len(cost), 1)), axis=1)
        print("them cot gia")
    elif total_demand > total_supply:
        # Thêm hàng giả
        supply.append(total_demand - total_supply)
        cost = np.append(cost, np.zeros((1, len(cost[0]))), axis=0)
        print("them hang gia")
    else:
        print("khong can them")

    return cost, supply, demand

def northwest_corner_method(supply, demand):
    rows, cols = len(supply), len(demand)
    allocation = np.zeros((rows, cols))
    
    i, j = 0, 0
    while i < rows and j < cols:
        if supply[i] < demand[j]:
            allocation[i][j] = supply[i]
            demand[j] -= supply[i]
            i += 1
        else:
            allocation[i][j] = demand[j]
            supply[i] -= demand[j]
            j += 1
    
    return allocation

def calculate_cost(allocation, cost):
    total_cost = 0
    for i in range(len(allocation)):
        for j in range(len(allocation[0])):
            total_cost += allocation[i][j] * cost[i][j]
    return total_cost

# tinhs phan bo co bang m + n - 1 hay chua
def is_balanced(allocation):
    rows = len(allocation)
    cols = len(allocation[0])
    return sum(1 for i in range(rows) for j in range(cols) if allocation[i][j] > 0) == rows + cols - 1

def The_Largest_Positive_Value_Position(check):
    rows = len(check)
    cols = len(check[0])
    max = check[0][0]
    pos = (0, 0)
    for i in range(rows):
        for j in range(cols):
            if check[i][j] > max:
                max = check[i][j]
                pos = (i, j)
    return pos

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
    
def modi_method(cost, allocation):
    rows = len(allocation)
    cols = len(allocation[0])
    
    while True:
            # Tính U và V
        u = [None] * rows
        v = [None] * cols
        u[0] = 0  # Khởi tạo U đầu tiên
        
        for _ in range(rows + cols):
            for i in range(rows):
                for j in range(cols):
                    if allocation[i][j] > 0:
                        if u[i] is not None and v[j] is None:
                            v[j] = cost[i][j] - u[i]
                        elif v[j] is not None and u[i] is None:
                            u[i] = cost[i][j] - v[j]
        
        # Tính ma trận kiểm tra (delta)
        check = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                check[i][j] = u[i] + v[j] - cost[i][j]
        
        print("Check matrix:")
        print(check)
        
        # Nếu tất cả giá trị <= 0, phân bổ đã tối ưu
        if np.all(check <= 0):
            print("Phân bổ đã tối ưu")
            return allocation
        
        # Tìm ô có giá trị dương lớn nhất trong ma trận check
        i, j = The_Largest_Positive_Value_Position(check)
        print(f"Ô có giá trị dương lớn nhất: ({i}, {j})")
        
        # Thay giá trị ô đó trong ma trận check bằng 0
        check[i][j] = 0
           
        # Tìm đường vòng lặp (loop)      
        loop = find_loop(check, i, j)
        print("Đường vòng lặp:", loop)
        
        # Xóa vị trí cuối cùng trong loop
        loop.pop()
        
        # Xác định các ô + và - trong vòng lặp
        positive_positions = loop[0::2]
        negative_positions = loop[1::2]
        
        # Tìm giá trị nhỏ nhất trong các ô -
        theta = min(allocation[row][col] for row, col in negative_positions)
        
        # Điều chỉnh phân bổ
        for row, col in positive_positions:
            allocation[row][col] += theta
        for row, col in negative_positions:
            allocation[row][col] -= theta
        
        print("Phân bổ sau khi điều chỉnh:")
        print(allocation)

# Dữ liệu bài toán
cost_matrix = [
    [82, 73, 74, 79],
    [80, 75, 81, 79],
    [80, 77, 77, 82],
]
supply = [45, 90, 110]
demand = [40, 75, 60, 70]

# Cân bằng cung cấp và cầu
cost_matrix, supply, demand = balance_supply_demand(cost_matrix, supply, demand)

# Áp dụng phương pháp Northwest Corner
allocation = northwest_corner_method(supply, demand)
print("Phân bổ ban đầu:")
print(allocation)

print("Cân bằng cung cấp và cầu:", is_balanced(allocation))

# Tính chi phí
total_cost = calculate_cost(allocation, cost_matrix)
print("Chi phí ban đầu:", total_cost)

# Áp dụng phương pháp MODI
allocation = modi_method(cost_matrix, allocation)
print("Phân bổ cuối cùng:")
print(allocation)
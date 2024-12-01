from qiskit import QuantumCircuit, Aer, execute

# Tạo mạch với 7 qubit (4 input, 1 ancilla, 2 output)
qc = QuantumCircuit(7)

# Gán trạng thái input: 01 (qubit 0, 1) và 10 (qubit 2, 3)
qc.x(1)  # |01> cho qubit 0 và 1
qc.x(2)  # |10> cho qubit 2 và 3

# Thực hiện phép nhân: Toffoli để tính tích
qc.ccx(1, 2, 4)  # q1 AND q2 -> q4 (ancilla)
qc.cx(4, 5)      # Kết quả lưu vào qubit 5 (output thấp nhất)
qc.cx(3, 6)      # Dịch và lưu kết quả cao hơn vào qubit 6

# Đo trạng thái output
qc.measure_all()

# Chạy mô phỏng
simulator = Aer.get_backend('aer_simulator')
result = execute(qc, simulator).result()
counts = result.get_counts()

print("Kết quả:", counts)

import matplotlib.pyplot as plt

# 数据
x = [10, 30, 50, 100, 200]
y = [0.4222222222222222, 0.43448275862068964, 0.39918367346938777, 0.338989898989899, 0.22613065326633167]

# 使用plt绘图
plt.plot(x, y)
plt.title('Evaluation result')
plt.xlabel('data amount')
plt.ylabel('Kendall tau distance')
plt.show()
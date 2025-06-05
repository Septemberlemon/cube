import matplotlib.pyplot as plt


# 年份列表
years = list(range(2000, 2025))

# 出生人口数据（单位：百万）
births = [
    17.71, 16.47, 16.47, 15.94, 15.83,
    16.12, 15.84, 15.94, 16.04, 15.99,
    15.88, 16.04, 16.35, 16.40, 16.87,
    16.55, 17.86, 17.23, 15.23, 14.65,
    12.00, 10.62, 9.56, 9.02, 9.54
]

# 创建图表
plt.figure(figsize=(12, 6))
plt.plot(years, births, marker='o', linestyle='-', color='teal', label='出生人口（百万）')

# 设置Y轴从0开始，防止比例压缩
plt.ylim(0, max(births) + 1)  # 从0到最高值+1，确保上下留白

# 添加标题和标签
plt.title('2000–2024 年中国出生人口趋势', fontsize=16)
plt.xlabel('年份', fontsize=12)
plt.ylabel('出生人口（百万）', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(years, rotation=45)
plt.legend()

# 显示图表
plt.tight_layout()
plt.show()

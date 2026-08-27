n = int(input())

# 读取 n 个整数成绩，按空格分割
scores = list(map(int, input().split()))

# 初始化变量
total_sum = 0
max_score = 0
pass_count = 0

# 遍历成绩进行统计
for score in scores:
    total_sum += score
    if score > max_score:
        max_score = score
    if score >= 60:
        pass_count += 1

# 计算平均分（保留 1 位小数）
average = total_sum / n

# 输出结果
print("{:.1f}".format(average))
print(max_score)
print(pass_count)

sentence = input()
words = sentence.split()

# 统计单词次数
word_counts = {}
for word in words:
    word_counts[word] = word_counts.get(word, 0) + 1

# 将字典项转为列表
items = list(word_counts.items())

# 排序：
# 次数降序（-x[1]），次数相同时按单词升序（x[0]）
items.sort(key=lambda x: (-x[1], x[0]))

# 输出结果
for word, count in items:
    print(word, count)

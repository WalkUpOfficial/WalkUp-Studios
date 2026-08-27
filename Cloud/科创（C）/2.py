words = input().split()

if not words:
    # 如果没有单词，根据题意一般不出现，可输出空或特定值
    print("")
else:
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1

    max_count = 0
    for word in words:
        if counts[word] > max_count:
            max_count = counts[word]

    # 按原顺序找第一个计数等于 max_count 的单词
    result = ""
    for word in words:
        if counts[word] == max_count:
            result = word
            break

    print(result)

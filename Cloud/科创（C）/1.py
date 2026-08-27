n = int(input())
temperatures = list(map(int, input().split()))

if n == 0:
    print(0)
else:
    cur = 1  # 当前递增段长度
    ans = 1  # 最大递增段长度

    for i in range(1, n):
        if temperatures[i] > temperatures[i - 1]:
            cur += 1
        else:
            cur = 1
        if cur > ans:
            ans = cur

    print(ans)

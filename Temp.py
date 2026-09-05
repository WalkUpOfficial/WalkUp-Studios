def count_even(lst):
    cnt = 0
    for num in lst:
        if num % 2 == 0:
            cnt += 1
    return cnt
data = [12, 5, 8, 19, 22, 33, 40]
print(count_even(data))
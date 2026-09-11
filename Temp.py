import sys

sys.set_int_max_str_digits(999999999)

num = 99999999

for i in str(num**num):
    print(i, end='')
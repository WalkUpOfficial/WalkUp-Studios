# 读取起始时间
t1 = input()
t2 = input()

h1, m1 = map(int, t1.split(':'))
h2, m2 = map(int, t2.split(':'))

total1 = h1 * 60 + m1
total2 = h2 * 60 + m2

angle1 = total1 * 0.5
angle2 = total2 * 0.5

diff = angle2 - angle1 
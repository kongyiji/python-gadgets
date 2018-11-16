# -*- coding: utf-8 -*-

deduct_insurance = eval(input('请输入缴纳五险一金后的工资：'))
threshold = 5000
money = deduct_insurance - threshold
tax = 0

calc_tables = (
    (80000, 0.45, 15160),
    (55000, 0.35, 7160),
    (35000, 0.3, 4410),
    (25000, 0.25, 2660),
    (12000, 0.2, 1410),
    (3000, 0.1, 210),
    (0, 0.03, 0)
)


for table in calc_tables:
    if money > table[0]:
        tax = money * table[1] - table[2]


result = f'需要缴纳个税：{tax}, 税后工资：{deduct_insurance - tax}'
print(result)
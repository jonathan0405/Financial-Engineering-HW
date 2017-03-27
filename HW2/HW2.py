# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 21:40:03 2017

@author: Jonathan
"""
from dateutil.relativedelta import relativedelta
import datetime

Price = 100
Bond_Maturity_Date = datetime.date(1995, 3, 1)
Bond_Settlement_Date = datetime.date(1993, 7, 1)
Bond_Yeild = 0.03
Coupon_Rate = 0.1

input_year = int(input(">>> 輸入Bond_Maturity_Date Year: "))
input_month = int(input(">>> 輸入Bond_Maturity_Date Month: "))
input_day = int(input(">>> 輸入Bond_Maturity_Date Day: "))
Bond_Maturity_Date = Bond_Maturity_Date.replace(year = input_year, month = input_month, day = input_day)
print(Bond_Maturity_Date)

input_year = int(input(">>> 輸入Bond_Settlement_Date Year: "))
input_month = int(input(">>> 輸入Bond_Settlement_Date Month: "))
input_day = int(input(">>> 輸入Bond_Settlement_Date Day: "))
Bond_Settlement_Date = Bond_Settlement_Date.replace(year = input_year, month = input_month, day = input_day)
print(Bond_Settlement_Date)

Bond_Yeild = float(input(">>> 輸入Bond_Yeild: "))
Coupon_Rate = float(input(">>> 輸入Coupon_Rate: "))

print("Calculate with 30/360 method...")
coupon_day = Bond_Maturity_Date
coupon_day = coupon_day.replace(year = Bond_Settlement_Date.year)

if Bond_Settlement_Date > coupon_day:
    month_rel = relativedelta(months=6)
    coupon_day = coupon_day + month_rel
    
Days = 0
Days = Days + (coupon_day.year - Bond_Settlement_Date.year)*360
Days = Days + (coupon_day.month - Bond_Settlement_Date.month)*30
Days = Days + (coupon_day.day - Bond_Settlement_Date.day)

w = Days/180

Days = 0
Days = Days + (Bond_Maturity_Date.year - Bond_Settlement_Date.year)*360
Days = Days + (Bond_Maturity_Date.month - Bond_Settlement_Date.month)*30
Days = Days + (Bond_Maturity_Date.day - Bond_Settlement_Date.day)
n = int((Days/30/6)) + 1

Value = 0
for i in range(n):
    Value = Value + (Price*Coupon_Rate/2)/((1+(Bond_Yeild/2))**(i+w))
Value = Value + (Price)/((1+(Bond_Yeild/2))**(w+n-1))
Dirty_Price = Value
print('Dirty Price:%.4f' % Dirty_Price)

Accrued_Interest = (Price*Coupon_Rate/2)*(1-w)
Clean_Price = Value - Accrued_Interest
print('Clean Price:%.4f' % Clean_Price)

print("Calculate with Actual/Actual method...")
coupon_day = Bond_Maturity_Date
coupon_day = coupon_day.replace(year = Bond_Settlement_Date.year)

if Bond_Settlement_Date > coupon_day:
    month_rel = relativedelta(months=6)
    coupon_day = coupon_day + month_rel
    
Days = 0
Days = Days + (coupon_day.year - Bond_Settlement_Date.year)*360
Days = Days + (coupon_day.month - Bond_Settlement_Date.month)*30
Days = Days + (coupon_day.day - Bond_Settlement_Date.day)

Period = coupon_day - Bond_Settlement_Date
month_rel = relativedelta(months = -6)
coupon_day_prev = coupon_day
coupon_day_prev = coupon_day_prev + month_rel
w = Period.days/(coupon_day - coupon_day_prev).days

Value = 0
for i in range(n):
    Value = Value + (Price*Coupon_Rate/2)/((1+(Bond_Yeild/2))**(i+w))
Value = Value + (Price)/((1+(Bond_Yeild/2))**(w+n-1))
Dirty_Price = Value
print('Dirty Price:%.4f' % Dirty_Price)

Accrued_Interest = (Price*Coupon_Rate/2)*(1-w)
Clean_Price = Value - Accrued_Interest
print('Clean Price:%.4f' % Clean_Price)
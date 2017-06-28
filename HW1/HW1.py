# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 22:23:11 2017

@author: Jonathan
"""

def find_IRR(High, Low, C, x, k):
    while High-Low >= 0.0001:
        Middle = (Low+High)/2
        Value = 0     
        for i in range(1,len(C)+1):
            Discount = 1
            for j in range(1,i+1):
                Discount = Discount/(1+Middle)    
            Value = Value + Discount*C[i-1]
        Value = Value - x
        if k > 0:
            if Value > 0:
                High = Middle
            else:
                Low = Middle
        else:
            if Value < 0:
                High = Middle
            else:
                Low = Middle
    return High
    
def diff(r, C, x):
    value=0
    for i in range(1,len(C)+1):
        discount = 1
        for j in range(1,i+1):
            discount = discount/(1+r)
        value = value + discount*C[i-1]
    value = value - x
    return value
    
def diff1(r, C, x):
    value=0
    for i in range(1,len(C)+1):
        discount = 1
        for j in range(1,i+1):
            discount = discount/(1+r)
        value = value + discount*(-i)*C[i-1]/(1+r)
    return value
    
def newtons_Method(input_value):
    f0=diff(input_value, C, x)    
    while f0 != 0:
        input_value = input_value - f0/diff1(input_value, C, x)
        f0 = diff(input_value, C, x)
    return input_value
    
if __name__ == '__main__':
    C=[]
    '''
    n = int(input(">>> 輸入期數: "))
    x = int(input(">>> 輸入初期投入: "))
    for i in range(n):
        C.append(int(input(">>> 輸入第"+str(i+1)+"期報酬: ")))
    '''
    x = -9702
    C=[-19700,10000]
    
    High = 1
    Low = 0
    Rate1 = find_IRR(High,Low,C,x,1)
    
    High2 = Rate1
    Low2 = 0
    Rate2 = find_IRR(High2,Low2,C,x,0)
              
    print('Yeild Rate with Bisection method:%.4f' % Rate1)
    print('Yeild Rate with Bisection method:%.4f' % Rate2)
    
    input_value1 = 0.01
    input_value2 = 0.1
    
    Newtons_rate1 = newtons_Method(input_value1)
    Newtons_rate2 = newtons_Method(input_value2)
    
    print('Yeild Rate with Newtons method:%.4f' % Newtons_rate1)
    print('Yeild Rate with Newtons method:%.4f' % Newtons_rate2)
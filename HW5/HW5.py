# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 22:56:10 2017

@author: Jonathan
"""
def cal_static_spread(par, n, c, yield_spread, yield_rate):
    r = [yield_rate[0]]
    risk_r = [yield_rate[0] + yield_spread]

    for i in range(1,n):
        #12
        bond_value = 0
        risk_bond_value = 0
        for j in range(i+1):
            #01+012
            bond_value += c/(1 + yield_rate[i])**(j + 1)
            risk_bond_value += c/(1 + yield_rate[i] + yield_spread)**(j + 1)
            if j==i:
                bond_value += par/(1 + yield_rate[i])**(j + 1)
                risk_bond_value += par/(1 + yield_rate[i] + yield_spread)**(j + 1)
        rbond = 0
        riskbond = 0
        for j in range(i):
            #0+01
            rbond += c/(1 + r[j])**(j+1)
            riskbond += c/(1 + r[j])**(j+1)
        rbond = bond_value - rbond
        riskbond = risk_bond_value - riskbond
        newR=((c+par)/rbond)**(1/(i+1))
        risk_newR = ((c + par)/riskbond)**(1/(i+1))
        r.append(newR-1)
        risk_r.append(risk_newR - r[i] - 1)
            
    risk_r[0] = risk_r[0] - r[0]
    high = risk_r[-1]
    low = risk_r[0]
    while(abs(high - low) >= 0.0000000001):
        middle = (high + low)/2
        value = 0
        for j in range(n):
            value += c/(1 + r[j] + middle)**(j + 1)
            if j == i:
                value += par/(1 + r[j] + middle)**(j + 1)
        if value - risk_bond_value > 0:
            low = middle
        else:
            high = middle
    print(middle)

if __name__ == '__main__':
    par = 100
    n = int(input(">>> 輸入期數: "))
    c = int(input(">>> 輸入債息: "))
    yield_rate = [None] * n
    for i in range(n): 
        tmp_input = float(input(">>> 輸入第"+str(i+1)+"期Yeild Rate: "))
        yield_rate[i] = tmp_input
    yield_spread = float(input(">>> 輸入Yeild Spread: "))
    cal_static_spread(par, n, c, yield_spread, yield_rate)
    
    
    
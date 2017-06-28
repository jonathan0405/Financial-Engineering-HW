# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 22:56:10 2017

@author: Jonathan
"""

def Macaulay_Duration(period, coupon_rate, m_yield):
    coupon = 100*coupon_rate
    duration = 0
    presentValue = 0
    for i in range(period):
        duration = duration + (i+1)*coupon/(1 + m_yield)**(i+1)
        presentValue = presentValue + coupon/(1 + m_yield)**(i+1)
        if (i+1) == period:
            duration = duration + (i+1)*100/(1 + m_yield)**(i+1)
            presentValue = presentValue + 100/(1 + m_yield)**(i+1)
    duration = duration/presentValue
    return duration
    
def Modified_Duration(period, coupon_rate, m_yield):    
    modified_duration = Macaulay_Duration(period, coupon_rate, m_yield)/(1+m_yield)
    return modified_duration
    
if __name__ == '__main__':
    #Macaulay Duration
    print("設定期數6期,Face_value=100,Market_yeild=0.08")
    print('當債券支付的債息為0,則存續期間為:%.4f' % Macaulay_Duration(6, 0, 0.08))
    print('當債券支付的債息為0.08,則存續期間為:%.4f' % Macaulay_Duration(6, 0.08, 0.08))
    print("->債息提高，存續期間下降，因本金佔現值的比例變小")
    print('當債券支付的債息為0.01,則存續期間為:%.4f' % Macaulay_Duration(6, 0.01, 0.08))
    print("->債息下降，存續期間上升，因本金佔現值的比例變大")
    #Modified Duration
    print('當殖利率變動一個basis point時，價格變動的百分比為：' + 
          str(-Modified_Duration(6, 0.08, 0.08)*0.0001*100)[:10] + '%')  
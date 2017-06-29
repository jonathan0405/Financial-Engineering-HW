# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:08:56 2017

@author: Jonathan
"""

import csv
from lxml import html
import numpy as np
from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import urllib.request

class McListBox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""
    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()
    def _setup_widgets(self):
        s = """僅顯示買賣成交價完整之價格資料"""
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
            padding=(10, 2, 10, 6), text=s)
        msg.pack(fill='x')
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=data_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
    def _build_tree(self):
        for col in data_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))
        for item in data_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                #if self.tree.column(data_header[ix],width=None)<col_w:
                #    self.tree.column(data_header[ix], width=col_w)
                
def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))

def Put_Call_Parity(call, put, taiex, strike):
    if put != 0:
        putprice = call + strike*pv - taiex[1]
        callprice = taiex[1] + put - strike*pv
        if putprice != put:
            if putprice < put:
                arbitrage = abs(put - putprice)+(taiex[0] - taiex[1]) - 3
                return 'Put_Call_Parity: Sell a put, Sell a Taiex, Buy a call. Arbitrage:'+str(arbitrage)
            else:
                arbitrage = abs(put - putprice) - 3
                return 'Put_Call_Parity: Buy a put, Buy a taiex, Sell a call. Aarbitrage:'+str(arbitrage)
    else:
        return 'Put_Call_Parity: Price is missing.'
        
def Put_Call_Future_Parity(call, put ,future, strike):
    if put != 0:
        putprice = call + strike*pv - future[0]*pv
        callprice = -strike*pv + put + future[0]*pv
        if putprice != put:
            if putprice < put:
                arbitrage = abs(putprice - put) - 3
                return 'Put_Call_Future_Parity: Sell a put, Sell a future, Buy a call. Arbitrage:'+str(arbitrage)
            else:
                arbitrage = abs(putprice - put)-(future[1] - future[0]) - 3
                return 'Put_Call_Future_Parity: Buy a put, Buy a future, Sell a call. Arbitrage:'+str(arbitrage)
    else:
        return 'Put_Call_Future_Parity: Price is missing.'
        
def Theorem_3(call, put, taiex, strike):
    if call > Taiex[0]:
        arbitrage = (call - Taiex[0]) - 2
        return 'Theorem 3: Short a call, Long the stock. Arbitrage:'+str(arbitrage)
    if put > strike:
        arbitrage = put - 1
        return 'Theorem 3: Short a put. Arbitrage:'+str(arbitrage)
    else:
        return 'Theorem 3: No arbitrage.'
        
def Theorem_4(call, put, taiex, strike):
    if call < max((taiex[1] - strike*pv),0):
        arbitrage = (max((taiex[1] - strike*pv), 0) - call) + (taiex[0] - taiex[1]) - 2
        return 'Theorem 4: Long a call, Shorting the stock. Arbitrage:'+str(arbitrage)
    else:
        return 'Theorem 4: No arbitrage.'
        
def Theorem_6(call, put, taiex, strike):
    if put != 0:
        if put < max((strike*pv - taiex[1]), 0):
            arbitrage = (max((strike*pv - taiex[1]),0) - put - 2)
            return 'Theorem 6: Long a put. Long the stock. Arbitage:', arbitrage
        else:
            return 'Theorem 6: No arbitrage.'
    else:
        return 'Theorem 6: Price is missing.'
    
def get_value(td):
    try:
        result = td.cssselect('a')[0] if td.cssselect('a') else td
        result = float(result.text.strip())
    except Exception:
        result = False
    finally:
        return result
    
def get_str(td):
    try:
        result = td.cssselect('a')[0] if td.cssselect('a') else td
        result = str(result.text.strip())
    except Exception:
        result = False
    finally:
        return result
    
def Internet_callback():
    body = html.fromstring(urllib.request.urlopen('http://tw.screener.finance.yahoo.net/future/aa03?opmr=optionfull&opcm=WTXO').read())
    datas = body.cssselect('tr')[4:]
    title = body.cssselect('tr')[1]
    
    st = []
    msgs = ""
    for row in title:
        st = st + [ get_str(td) for td in row.cssselect('td')]
        msgs.join(st[0])
        
    TAIEX = st[1].split('（')[0]
    for ag in st:
        msgs = msgs + str(ag)
        
    global pv
    rt = float(e.get())/12
    pv = np.exp(-rt)
    
    for row in datas:
        values = [ get_value(td) for td in row.cssselect('td')]
        if values[2] and values[10]:
            Strike_Price.append(int(values[7]))
            Call.append(float(values[2]))
            Buy_Call.append(float(values[0]))
            Write_Call.append(float(values[1]))
            Put.append(float(values[10]))
            Buy_Put.append(float(values[8]))
            Write_Put.append(float(values[9]))
            data_list.append([int(values[7]), float(values[2]), float(values[0]), float(values[1]), 
                              float(values[10]), float(values[8]), float(values[9]), float(TAIEX), 
                              float(TAIEX), float(TAIEX), float(TAIEX), e.get()])
       
    Taiex.append(float(TAIEX))
    Taiex.append(float(TAIEX))
    Future.append(float(TAIEX))
    Future.append(float(TAIEX))
    disp_result()
    label1.configure(text=msgs)
            
    return msgs    

def local_callback():
    try:
        with open('data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                
                data_list.append([float(row[0]), float(row[1]), float(row[2]), float(row[3]), 
                                  float(row[4]), float(row[5]), float(row[6]), float(row[7]), 
                                  float(row[8]), float(row[9]), float(row[10]), e.get()])
                Strike_Price.append(float(row[0]))
                Call.append(float(row[1]))
                Buy_Call.append(float(row[2]))
                Write_Call.append(float(row[3]))
                Put.append(float(row[4]))
                Buy_Put.append(float(row[5]))
                Write_Put.append(float(row[6]))            
                if Taiex == []:
                    Taiex.append(float(row[7]))
                    Taiex.append(float(row[8]))
                    Future.append(float(row[9]))
                    Future.append(float(row[10]))
                    global pv
                    rt = float(e.get())/12                
                    pv = np.exp(-rt)
        label1.configure(text="祝你賺大錢")  
    except Exception:
        label1.configure(text="請檢查資料")
    finally:
          
        disp_result()        
        
def disp_result():
    for i in range(len(Strike_Price)):
        Lb1.insert('end', "Strike Price: "+str(Strike_Price[i]))
        Lb1.itemconfigure('end', background="lightpink")
        Lb1.insert('end', Put_Call_Parity(Call[i], Put[i], Taiex, Strike_Price[i]))
        Lb1.itemconfigure('end', background="lavenderblush")
        Lb1.insert('end', Put_Call_Future_Parity(Call[i], Put[i], Future, Strike_Price[i]))
        Lb1.itemconfigure('end', background="lavenderblush")
        Lb1.insert('end', Theorem_3(Call[i], Put[i], Taiex, Strike_Price[i]))
        Lb1.itemconfigure('end', background="lavenderblush")
        Lb1.insert('end', Theorem_4(Call[i], Put[i], Taiex, Strike_Price[i]))
        Lb1.itemconfigure('end', background="lavenderblush")
        Lb1.insert('end', Theorem_6(Call[i], Put[i], Taiex, Strike_Price[i]))
        Lb1.itemconfigure('end', background="lavenderblush")
        Lb1.insert('end', " ")
        Lb1.itemconfigure('end', background="whitesmoke")
    
    if(len(Strike_Price)==0):
        Lb1.insert('end', "非交易時間 或 連線資料異常")
        Lb1.itemconfigure('end', background="lightpink")
        
    btn_file.config(state = DISABLED)
    btn_internet.config(state = DISABLED)
    mc_listbox = McListBox()
    Lb1.pack()

if __name__ == '__main__':
    data_header = ['履約價', '買權-成交價', '買權-買價', '買權-賣價', '賣權-成交價', '賣權-買價', 
                   '賣權-賣價', '台指-買價', '台指-賣價', '台指期-買價', '台指期-賣價', '利率']
    data_list = []
    
    root = tk.Tk()
    root.iconbitmap('favicon.ico')
    root.title("2017財務工程導論 期末作業")   
    root.geometry('{}x{}'.format(1000, 700))
    Lb1 = tk.Listbox(root, width = 200, height = 30)
    label=tk.Label(root, text="輸入利率")
    e = StringVar()
    E1 = tk.Entry(root, textvariable=e)
    e.set("0.01844")
    label1=tk.Label(root, text="選擇資料來源")
    btn_file = tk.Button(root, text="讀檔(本機data.csv)", command=local_callback)
    btn_internet = tk.Button(root, text="從網路下載TXO即時資料", command=Internet_callback)
    
    label.pack()
    E1.pack()    
    label1.pack()
    btn_file.pack()
    btn_internet.pack()    
    
    Strike_Price = []
    Call = []
    Buy_Call = []
    Write_Call = []
    Put = []
    Buy_Put = []
    Write_Put = []
    Taiex = []
    Future = []
    pv = 0
    
    root.mainloop()
    
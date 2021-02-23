from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import csv
import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.request import urlopen
import io
import pandas as pd
#from choosepage import ChoosePage
import choosepage
import webbrowser

class Climb_Frame(Frame): 
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master #定義內部變數root
        self.createPage()
    def createPage(self):
        self.page1 = Frame(self,width=960,height = 580)
        self.page1.pack(padx=10,pady=10)
        Button(self.page1,text="返回",command=lambda:self.clear_frame()).grid(row=0,stick=W,padx=390,pady=10)
        Button(self.page1,text = "爬蟲開始",command=lambda:self.start_climb()).grid(row = 0,padx = 500)
        self.canvas = Canvas(self.page1,width = 300,height = 30,bg = "gray")
    def clear_frame(self):
        self.canvas.destroy()
        self.page1.destroy()
        self.destroy()
        choosepage.ChoosePage(self.root)
    def start_climb(self):
        Label(self.page1, text = "csv檔案資料製作完成").grid(row=3, stick=W,padx = 370, pady=10)
        Button(self.page1,text = "價格排序",command=lambda:self.sortPrice(5)).grid(row=3,stick=W,padx = 500,pady=10)
        start = time.time()
        for page in range(5):
            keyword1 = '日檢'
            keyword2 = 'N2'
            keyword3 = '單字'
            #設定網址
            print(page)
            if page==0:
                url = 'https://shopee.tw/search?keyword={}%20{}%20{}'.format(keyword1,keyword2,keyword3)
            else:
                url = 'https://shopee.tw/search?keyword={}%20{}%20{}&page={}'.format(keyword1,keyword2,keyword3,page)
            
            headers = {'user-agent': 'Googlebot'}
            r = requests.get(url, headers=headers) 
            soup = BeautifulSoup(r.text, 'html.parser')
        
            #設定抓取內容
            pictures = soup.find_all("div",class_="_39-Tsj _1tDEiO")
            pictures_link = [i.find('img').get('src') for i in pictures]
            contents = soup.find_all("div", class_="_1NoI8_ _16BAGk")
            prices = soup.find_all("div", class_="_1w9jLI _37ge-4 _2ZYSiu")
            all_items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
            links = [i.find('a').get('href') for i in all_items]
            #print(len(prices))
            #因為有些是價格範圍，所以要特別取出來
            price1 = []
            price2 = []
            for i in range(len(prices)):
                a = []
                for item in prices[i]:
                    a.extend(list(item))
                    if len(a)>6:
                        price2.pop()
                        price2.append(a[6])
                    else:
                        if len(a)==2:
                            price1.append(a[1])
                            price2.append(a[1])
            #寫入csv檔案
            with open('output_{}.csv'.format(page), 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['商品', '價格1', '價格2', '網址', '圖片']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
    
                for i in range(len(price1)):
                    #download_img(picture_link[i]) #新增擺放圖片的資料夾
                    writer.writerow({'商品': list(contents[i])[0], 
                                         '價格1': price1[i], '價格2': price2[i], 
                                         '網址': 'https://shopee.tw/'+links[i],
                                         '圖片':pictures_link[i]})
                    time.sleep(0.2)
        end = time.time()
        print(end-start)
    def sortPrice(self,page):
        #開啟csv檔案，讀成list
        for num in range(int(page)):
            with open ('output_{}.csv'.format(num), 'r', newline='', encoding='utf-8-sig') as csvFile:
                rows = csv.reader(csvFile)
                lists = []
                for row in rows:
                    lists.append(row)
            #按照價格做排序(由小到大)
            items = lists[1:]
            goods = {}
            for i in range(len(items)):
                url = items[i][3]
                name = url.split('-i')[0].split('https://shopee.tw//')[1]
                img = items[i][4]
                price1 = items[i][1]
                price2 = items[i][2]
                
                # 要對千元以上的數字進行處理 (網頁表示為'1,013')
                if ',' in price1:
                    price = []
                    price.append(price1.split(',')[0])
                    price.append(price1.split(',')[1])
                    price1 = int(''.join(price))
                else:
                    price1 = int(price1)
                if ',' in price2:
                    price = []
                    price.append(price2.split(',')[0])
                    price.append(price2.split(',')[1])
                    price2 = int(''.join(price))
                else:
                    price2 = int(price2)
                
                if name in goods:
                    goods[name+' '] = [price1, price2, url, img]
                else:
                    goods[name] = [price1, price2, url, img]
            sortGoods = sorted(goods.items(), key=lambda x:x[1][0])
            
            #寫入csv檔案
            with open('sorted{}.csv'.format(num), 'w', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['商品', '價格1', '價格2', '網址', '圖片']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(len(items)):
                    writer.writerow({'商品': sortGoods[i][0], '價格1': sortGoods[i][1][0], '價格2': sortGoods[i][1][1], '網址': sortGoods[i][1][2], '圖片': sortGoods[i][1][3]})
        Label(self.page1, text = "排序已完成").grid(row=4, stick=W,padx = 400, pady=10)
class Tree_Frame(Frame):
    def __init__(self,master = None):
        Frame.__init__(self,master)
        self.root = master #定義內部變數root
        self.var = StringVar()
        self.var1 = BooleanVar()
        self.createPage()
        self.putimage = []
        #self.website = []
    def createPage(self):
        Combobox(self, textvariable = self.var,value = ('1', '2', '3', '4','5')).grid(row=0,stick=W,padx = 280, pady=10)
        self.var.set('請選擇')
        Button(self,text = "開始",command =self.show_tree).grid(row = 0,stick=W,padx = 460)
        self.var1.set(False)
        Checkbutton(self,text="價格排序",variable = self.var1).grid(row=0,stick=W,padx=560)
        Button(self,text="返回",command=lambda:self.clear_frame2()).grid(row=0,padx = 640)
    def clear_frame2(self):
        self.destroy()
        choosepage.ChoosePage(self.root)
    def readImage(self,url):
        img_bytes = urlopen(url).read()#讀取url
        data_stream = io.BytesIO(img_bytes)
        self.pil_image = Image.open(data_stream)    
    def show_tree(self):
        print("Now in pandas")
        csvfile = ''
        Style().configure("Treeview",rowheight = 130)    
        #建立捲動條
        scrollbar = Scrollbar(self,orient="vertical")
        scrollbar.place(x=920,y=40,width=20,height = 540)
        #建立treeview(此height 代表顯示欄位數量 非欄位寬(rowheight))
        tree = Treeview(self,height = 4,columns = ("商品","價格"),
                        yscrollcommand=scrollbar.set)
        #設定欄位寬度與顯示位置
        tree.column("#0",anchor = W,width = 160)
        tree.column("#1",anchor = W,width = 600)
        tree.column("#2",anchor = CENTER,width = 80) 
        #建立欄位開頭
        tree.heading("#0", text = "圖片")
        tree.heading("#1", text = "商品")
        tree.heading("#2", text = "價格")
        
        tree.grid(row = 3,stick = S+W,padx = 80)
        page = self.var.get()
        if page == '1':
            if self.var1.get() == True:
                csvfile = './sorted0.csv'
            else:
                csvfile = './output_0.csv'
        elif page == '2':
            if self.var1.get() == True:
                csvfile = './sorted1.csv'
            else:
                csvfile = './output_1.csv'
        elif page =='3':
            if self.var1.get() == True:
                csvfile = './sorted2.csv'
            else:
                csvfile = './output_2.csv'
        elif page == '4':
            if self.var1.get() == True:
                csvfile = './sorted3.csv'
            else:
                csvfile = './output_3.csv'
        elif page == '5':
            if self.var1.get() == True:
                csvfile = './sorted4.csv'
            else:
                csvfile = './output_4.csv'
        data = pd.read_csv(csvfile)
        for i in range(0,data.shape[0]):
            self.readImage(data.iloc[i][4])#跳去副函式 iloc[i][0]為圖片網址
            pil_image2 = self.pil_image.resize((120,120),Image.ANTIALIAS)#resize 修改大小
            imgobj = ImageTk.PhotoImage(pil_image2) #photoImage轉換
            self.putimage.append(imgobj) #放進list
            tree.image = self.putimage[len(self.putimage)-1]#定義存在
            if data.iloc[i][1]!=data.iloc[i][2]:
                price = '{}~{}'.format(data.iloc[i][1],data.iloc[i][2])
            else:
                price = data.iloc[i][1]
            tree.insert("",'end',image = self.putimage[-1],text="",values=(data.iloc[i][0],
                                                price,data.iloc[i][3]))
            tree.update()
            time.sleep(0.1)
        tree.bind("<Double-1>",self.double_click)
        scrollbar.config(command=tree.yview)

    def double_click(self,event):
        e = event.widget
        iid = e.identify("item",event.x,event.y)
        url = e.item(iid,"values")[2]
        #預設瀏覽器位置(r'瀏覽器路徑')
        #mozillapath = r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
        
        #宣告瀏覽器名稱
        #webbrowser.register('Firefox',None,webbrowser.BackgroundBrowser(mozillapath))
        
        #開啟網頁 new = 1 開啟新分頁 2 = 開啟新tab
        #webbrowser.get('Firefox').open(url,new=1,autoraise=True)
        
        #開啟網頁(使用電腦預設的瀏覽器)
        webbrowser.open(url,new=1,autoraise=True)
        
  
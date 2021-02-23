from tkinter import *
import show

class ChoosePage(object):
    def __init__(self, master=None):
        self.root = master #定義內部變數root
        self.root.geometry('%dx%d' % (1000, 580)) #設定視窗大小
        self.createPage()
    
    def createPage(self):
        self.page = Frame(self.root,width=500,height = 500)
        self.page.pack(padx=10,pady=10)
        #self.root.config(bg ="yellow")
        self.climbPage = show.Climb_Frame(self.root)
        self.treePage = show.Tree_Frame(self.root)
        Button(self.page,text = "爬蟲",command = lambda:self.find_climbPage()).grid(row=0,padx=10,pady=10)
        Button(self.page,text="印出圖表",command = lambda:self.find_treePage()).grid(row=0,column=1,padx=10,pady=10)
        
    def find_climbPage(self):
        self.page.destroy()
        self.treePage.pack_forget()
        self.climbPage.pack()
       
    def find_treePage(self):
        self.page.destroy()
        self.climbPage.destroy()
        self.treePage.pack()
        

        
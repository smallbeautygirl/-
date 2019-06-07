import tkinter as tk
from tkinter import *
import tkinter.font as font

def sign_in():
    SigninWindow = Toplevel()
    SigninWindow.geometry("800x600")
    SigninWindow.title("Sign In")
    #img_welcome = tk.PhotoImage(file = '1.gif')
    #ImageWelcomeLabel = tk.Label(SigninWindow,image = img_welcome)
    #ImageWelcomeLabel.pack()
    canvas = tk.Canvas(SigninWindow, height=200, width=500)#创建画布
    image_file = tk.PhotoImage(file='1.gif')#加载图片文件
    image = canvas.create_image(0,0, anchor='nw', image=image_file)#将图片置于画布上
    canvas.pack(side='top')#放置画布（为上端）
def create_account():
    SigninWindow = tk.Tk()
    SigninWindow.geometry("800x600")
    SigninWindow.title("Create Account")


window = tk.Tk()
window.title("Pokemon Fight!!")

#full screen
w = window.winfo_screenwidth()
h = window.winfo_screenheight()
window.geometry("%dx%d" %(w, h))

window.resizable(True, True)#設定視窗是否可以縮放
window.minsize(400, 200)

# define font
myFont = font.Font(family='Arial', size=20)

#create label
GamenameLabel = tk.Label(window,text='Pokemon Fight!!',bg='#ffe153',font=('Arial',30),width=20,height=3)
GamenameLabel.pack(pady=250)# 固定窗口位置

SignButton = tk.Button(window,text='sign in',width = 15,height = 2,command = sign_in)
SignButton['font'] = myFont# apply font to the button label
SignButton.pack(pady=10)

CreateButton = tk.Button(window,text='create account',width = 15,height = 2,command = create_account)
CreateButton['font'] = myFont# apply font to the button label
CreateButton.pack(pady=10)

ExitButton = tk.Button(window,text='Exit',width=15, height=2,command=window.destroy)
ExitButton['font'] = myFont# apply font to the button label
ExitButton.pack()

#img_gif = tk.PhotoImage(file = '1.gif')
#ImageLabel = tk.Label(window,image = img_gif)
#ImageLabel.pack(anchor=NE)
window.mainloop()
import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as font
import socket
from playsound import playsound
from PIL import ImageTk, Image
import time
import threading
import os
bufferSize = 1024
which = 0
def sign_in():
    global SigninWindow
    SigninWindow = Toplevel()
    SigninWindow.geometry("800x600")
    SigninWindow.title("Sign In")

    SigninLabel = Label(SigninWindow,text = "Sign in",bg='#ffe153',font=('Arial',30),width=15,height=2).pack(pady=100)
    
    signin = "sign in"
    clientSocket.send(signin.encode())
    
    global username
    global password
    #set text variables
    username = StringVar()
    password = StringVar()
    #set username label
    usernameLabel = Label(SigninWindow,text="Username",font=('Arial',20))
    usernameLabel.pack()
    # Set username entry
    # The Entry widget is a standard Tkinter widget used to enter or display a single line of text.
    usernameEntry = Entry(SigninWindow,textvariable=username)
    usernameEntry.pack()

    # Set password label
    passwordLabel = Label(SigninWindow,text = "Password",font=('Arial',20))
    passwordLabel.pack()
    # Set password entry
    passwordEntry = Entry(SigninWindow, textvariable=password, show='*')
    passwordEntry.pack()

    Button(SigninWindow, text="Sign in",font=('Arial',20), width=10, height=1, command=Signin_verify).pack(pady=20)
def Signin_verify():
    #get username and password
    username1 = username.get()
    password1 = password.get()
    #send username and password
    clientSocket.send(username1.encode())
    print(username1)
    time.sleep( 0.1 )
    clientSocket.send(password1.encode())
    print(password1)
    check = clientSocket.recv(bufferSize).decode()
    if check == "true":
        print ("Exist")
        Signin_success()
    else :
        print("Not Exist")
    SigninWindow.destroy()
def Signin_success():
    global Signin_successWindow
    Signin_successWindow = Toplevel()
    Signin_successWindow.title("Success")
    Signin_successWindow.geometry("250x150")
    Label(Signin_successWindow, text="Sign in Success",font=('Arial',15)).pack(pady=40)
    # create OK button
    Button(Signin_successWindow, text="OK", command = delete_login_success,font=('Arial',20)).pack(pady=5)
def delete_login_success():
    Signin_successWindow.destroy()
    showRules()
def showRules():
    global ruleWindow
    ruleWindow = Toplevel()
    ruleWindow.title("!!Rule!!")
    #full screen
    rw = ruleWindow.winfo_screenwidth()
    rh = ruleWindow.winfo_screenheight()
    ruleWindow.geometry("%dx%d" %(rw, rh))

    ruleWindow.resizable(True, True)#設定視窗是否可以縮放
    ruleWindow.minsize(400, 200)

    ruleLabel = Label(ruleWindow,text ="遊戲規則",bg='#ffe153',font=('Arial',40),width=15,height=2)
    ruleLabel.pack(pady=100)

    contentLabel = Label(ruleWindow,text = "Welcome to Pokemon Fight!!!",font=('Arial',25))
    contentLabel.place(x = 750,y=300)
    c2 = Label(ruleWindow,text ="Here is the rule :",font=('Arial',25))
    c2.place(x = 750,y=350)
    c3 = Label(ruleWindow,text = "1. You need to wait another player join the game",font=('Arial',25))
    c3.place(x = 650,y=400)
    c4 = Label(ruleWindow,text ="2. Choose one field that you want to go",font=('Arial',25))
    c4.place(x = 650,y=450)
    c5 = Label(ruleWindow,text ="3. Choose one pokemon to join the fight",font=('Arial',25))
    c5.place(x = 650,y=500)
    c6 = Label(ruleWindow,text ="4. Each pokemon has different HP and skill.",font=('Arial',25))
    c6.place(x = 650,y=550)
    c7 = Label(ruleWindow,text ="Each round the player will take turn to choose a skill for attack or defence",font=('Arial',25))
    c7.place(x = 650,y=600)
    c8 = Label(ruleWindow,text ="Until one player's HP becomes to zero, then game over.",font=('Arial',25))
    c8.place(x = 650,y=650)
    c9 = Label(ruleWindow,text ="5. If you won three games, you can upgrade your level.",font=('Arial',25))
    c9.place(x = 650,y=700)
    c10 = Label(ruleWindow,text ="The maximum level is ten",font=('Arial',25))
    c10.place(x = 650,y=750)
    # create OK button
    Button(ruleWindow, text="OK", command=delete_showrule,width=15, height=1,font=('Arial',25)).place(x = 800,y=900)
def delete_showrule():
    ruleWindow.destroy()
    selectAll()
def selectAll():
    global selectWindow
    selectWindow = Toplevel()
    selectWindow.title("!!Select!!")
    #full screen
    sw = selectWindow.winfo_screenwidth()
    sh = selectWindow.winfo_screenheight()
    selectWindow.geometry("%dx%d" %(sw, sh))

    selectWindow.resizable(True, True)#設定視窗是否可以縮放
    selectWindow.minsize(400, 200)

    select = "select"
    clientSocket.send(select.encode())
    print(select)

    fieldLabel = Label(selectWindow,text = "Choose which field you want to go :",bg='#ffe153',font=('Arial',30),width=30,height=2).place(x = 650,y = 100)

    varField = IntVar()
    varField.set(1)#預設值1 = grassland
    grassland = Radiobutton(selectWindow,variable = varField,value = 1,text = "Grassland",font=('Arial',25),command = Grassland).place(x = 750,y=250)
    polar = Radiobutton(selectWindow,variable = varField,value = 2,text = "Polar",font=('Arial',25),command = Polar).place(x = 750,y=300)
    electrical = Radiobutton(selectWindow,variable = varField,value = 3,text = "Electrical field",font=('Arial',25),command = Electrical).place(x = 750,y=350)
    pokemonLabel = Label(selectWindow,text = "Choose one of your pokemon :",bg='#ffe153',font=('Arial',30),width=30,height=2).place(x = 650,y = 450)
# recvData from server
class recvData(threading.Thread):
    def __init__(self,clientSocket,windowName,who):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.windowName = windowName
        self.who=who#看是誰
    def run(self):
        while True:
            data = self.clientSocket.recv(bufferSize).decode()
            print("data: " + data)
            if data[1] == 'H':
                print("HP")
                if self.who == 0:#11111
                    if which ==0:#11111按的
                        hp1 = Label(self.windowName,text=data[2:]+" ",font=('Arial', 25)).place(x=1430, y=650)
                    else: #22222按的
                        hp2 = Label(self.windowName,text=data[2:]+" ",font=('Arial', 25)).place(x=180, y=650)
                elif self.who == 1:#22222
                    if which ==0:#11111按的
                        hp3 = Label(self.windowName,text=data[2:]+" ",font=('Arial', 25)).place(x=180, y=650)
                    else: #22222按的
                        hp4 = Label(self.windowName,text=data[2:]+" ",font=('Arial', 25)).place(x=1430, y=650)
            elif data[1] == 'E':
                print("EPS")
                if self.who == 0:#11111
                    if which ==0:#11111按的
                        hp1 = Label(self.windowName,text=data[2:]+" ",font=('Arial', 25)).place(x=1810, y=650)
                    else: #22222按的
                        hp2 = Label(self.windowName,text=data[2:]+" ",font=('Arial', 25)).place(x=560, y=650)
                elif self.who == 1:#22222
                    if which ==0:#11111按的
                        hp3 = Label(self.windowName,text=data[2:]+" ",font=('Arial', 25)).place(x=560, y=650)
                    else: #22222按的
                        hp4 = Label(self.windowName,text=data[2:]+" ",font=('Arial', 25)).place(x=1810, y=650)
            elif data[0] == 'w':
                print("win")
                winlabel=Label(self.windowName,text="You Win!!!",font=('Arial', 60)).place(x=750, y=320)
            elif data[0] == 'l':
                print("lose")
                loselabel=Label(self.windowName,text="You Lose!!!",font=('Arial', 60)).place(x=750, y=320)
def start(windowName,field,role,hp,atk,eps):
    context1 = clientSocket.recv(bufferSize)
    print(context1.decode())
    l1 = Label(windowName,text = context1,font=('Arial',30)).place(x=20,y = 30)
    global grassImg
    global myAction1
    global myAction2
    global myAction3
    if field == 1:
        if role == 2:
            grassImg = PhotoImage(file="treecko.png")
            myAction1 = "Bullet Seed"
            myAction2 ="Pound"
            myAction3="Grass Knot"
        elif role == 3:
            grassImg = PhotoImage(file="bulbasaur.png")
        elif role == 4:
            grassImg = PhotoImage(file="exeggutor.png")
        elif role == 5:
            grassImg = PhotoImage(file="victreebel.png")
        else:
            grassImg = PhotoImage(file="turtwig.png")
            myAction1 = "Razor Leaf"
            myAction2 = "Seed Bomb"
            myAction3 = "Energy Ball"
    elif field == 2:
        if role == 2:
            grassImg = PhotoImage(file="piloswine.png")
        elif role == 3:
            grassImg = PhotoImage(file="articuno.png")
        elif role == 4:
            grassImg = PhotoImage(file="lapras.png")
        elif role == 5:
            grassImg = PhotoImage(file="snover.png")
        else:
            grassImg = PhotoImage(file="spheal.png")
    else:
        if role == 2:
            grassImg = PhotoImage(file="ampharos.png")
        elif role == 3:
            grassImg = PhotoImage(file="electabuzz.png")
        elif role == 4:
            grassImg = PhotoImage(file="zapdos.png")
        elif role == 5:
            grassImg = PhotoImage(file="jolteon.png")
        else:
            grassImg = PhotoImage(file="pikachu.png")

    grassImgLabel = Label(windowName, image=grassImg)
    grassImgLabel.image = grassImg
    grassImgLabel.place(x=200, y=450)
    label11 = Label(windowName, text="HP : ",font=('Arial', 25)).place(x=100, y=650)
    label12=Label(windowName, text=hp,font=('Arial', 25)).place(x=180, y=650)
    label13=Label(windowName, text=" ATK : " + atk,font=('Arial', 25)).place(x=270, y=650)
    label14=Label(windowName, text=" EPS : ",font=('Arial', 25)).place(x=450, y=650)
    label15=Label(windowName, text=eps,font=('Arial', 25)).place(x=560, y=650)
    # vs
    vsImgop = Image.open("vs.png")
    vsImgrs = vsImgop.resize((250, 250), Image.ANTIALIAS)
    vsImg = ImageTk.PhotoImage(vsImgrs)
    vsImgLabel = Label(windowName, image=vsImg)
    vsImgLabel.image = vsImg
    vsImgLabel.place(x=800, y=450)
    # playsound('fightBGM.mp3')
    otherrole = clientSocket.recv(bufferSize)
    print(otherrole.decode())
    otherrole = otherrole.decode()

    global otherImg
    if field == 1:
        if otherrole == "2":
            otherImg = PhotoImage(file="treecko.png")
        elif otherrole == "3":
            otherImg = PhotoImage(file="bulbasaur.png")
        elif otherrole == "4":
            otherImg = PhotoImage(file="exeggutor.png")
        elif otherrole == "5":
            otherImg = PhotoImage(file="victreebel.png")
        else:
            otherImg = PhotoImage(file="turtwig.png")
    elif field == 2:
        if otherrole == "2":
            otherImg = PhotoImage(file="piloswine.png")
        elif otherrole == "3":
            otherImg = PhotoImage(file="articuno.png")
        elif otherrole == "4":
            otherImg = PhotoImage(file="lapras.png")
        elif otherrole == "5":
            otherImg = PhotoImage(file="snover.png")
        else:
            otherImg = PhotoImage(file="spheal.png")
    else:
        if otherrole == "2":
            otherImg = PhotoImage(file="ampharos.png")
        elif otherrole == "3":
            otherImg = PhotoImage(file="electabuzz.png")
        elif otherrole == "4":
            otherImg = PhotoImage(file="zapdos.png")
        elif otherrole == "5":
            otherImg = PhotoImage(file="jolteon.png")
        else:
            otherImg = PhotoImage(file="pikachu.png")
    otherImgLabel = Label(windowName, image=otherImg)
    otherImgLabel.image = otherImg
    otherImgLabel.place(x=1400, y=450)

    otherHP = clientSocket.recv(bufferSize)
    print(otherHP.decode())
    otherATK = clientSocket.recv(bufferSize)
    print(otherATK.decode())
    otherEPS = clientSocket.recv(bufferSize)
    print(otherEPS.decode())

    # labe2 = Label(windowName, text="HP : " + otherHP.decode() + " ATK : " + otherATK.decode() + " EPS : " + otherEPS.decode(),font=('Arial', 25)).place(x=1400, y=650)
    label21 = Label(windowName, text="HP : ",font=('Arial', 25)).place(x=1350, y=650)
    label22=Label(windowName, text=otherHP.decode(),font=('Arial', 25)).place(x=1430, y=650)
    label23=Label(windowName, text=" ATK : " + otherATK.decode(),font=('Arial', 25)).place(x=1520, y=650)
    label24=Label(windowName, text=" EPS : ",font=('Arial', 25)).place(x=1700, y=650)
    label25=Label(windowName, text=otherEPS.decode(),font=('Arial', 25)).place(x=1810, y=650)
    # 顯示攻擊的東東
    global varATK
    varATK = IntVar()
    varATK.set(1)#預設值1 = Turtwig
    myActionLabel1 = Radiobutton(windowName,variable = varATK,value = 1,text = myAction1,font=('Arial',30)).place(x = 300,y = 130)
    myActionLabel2 = Radiobutton(windowName,variable = varATK,value = 2,text = myAction2,font=('Arial',30)).place(x = 300,y = 180)
    myActionLabel3 = Radiobutton(windowName,variable = varATK,value = 3,text = myAction3,font=('Arial',30)).place(x = 300,y = 230)
    ATKButton = Button(windowName,text = "Fight!!",font=('Arial',30),command = reallyStart).place(x = 400,y=300)
    if username.get() == "11111":
        who =0
    else:
        who =1
    recvData(clientSocket,windowName,who).start()
def reallyStart():
    print("really")
    print(username.get())
    if username.get() == "11111":
        clientSocket.send("0".encode()) # player 1
        which = 0
    else:
        clientSocket.send("1".encode()) # player 2
        which =1
    clientSocket.send(str(varATK.get()).encode())
        
def GOGrassland():
    print(varA.get())
    clientSocket.send("1".encode())
    print("grassland")
    selectWindow.destroy()
    global GOWindow
    GOWindow = Toplevel()
    GOWindow.title("Grassland")
    #full screen
    gw = GOWindow.winfo_screenwidth()
    gh = GOWindow.winfo_screenheight()
    GOWindow.geometry("%dx%d" %(gw, gh))

    GOWindow.resizable(True, True)#設定視窗是否可以縮放
    GOWindow.minsize(400, 200)

    # Background
    grassbgop = Image.open("grassland.png")
    grassbgrs = grassbgop.resize((gw, 250), Image.ANTIALIAS)
    grassbg = ImageTk.PhotoImage(grassbgrs)
    img2 = tk.Label(GOWindow, image=grassbg)
    img2.image = grassbg
    img2.place(x=0, y=770)

    time.sleep( 0.1 )
    clientSocket.send(str(varA.get()).encode())
    print(varA.get())
    grassHp = clientSocket.recv(3).decode()
    print(grassHp)
    grassAtk =clientSocket.recv(3).decode()
    print(grassAtk)
    grassEps = clientSocket.recv(3).decode()
    print(grassEps)

    start(GOWindow,1,varA.get(),grassHp,grassAtk,grassEps)
def GOPolar():
    selectWindow.destroy()    
    global PolarWindow
    PolarWindow = Toplevel()
    PolarWindow.title("Polar")
    #full screen
    gw = PolarWindow.winfo_screenwidth()
    gh = PolarWindow.winfo_screenheight()
    PolarWindow.geometry("%dx%d" %(gw, gh))

    PolarWindow.resizable(True, True)#設定視窗是否可以縮放
    PolarWindow.minsize(400, 200)

    #Background
    polarbgop = Image.open("polar.png")
    polarbgrs = polarbgop.resize((gw, 300), Image.ANTIALIAS)
    polarbg = ImageTk.PhotoImage(polarbgrs)
    img2 = tk.Label(PolarWindow, image=polarbg)
    img2.image = polarbg
    img2.place(x=0, y=670)

    clientSocket.send("2".encode())
    print("polar")
    time.sleep( 0.1 )
    clientSocket.send(str(varB.get()).encode())
    print(varB.get())
    polarHp = clientSocket.recv(3).decode()
    print(polarHp)
    polarAtk =clientSocket.recv(3).decode()
    print(polarAtk)
    polarEps = clientSocket.recv(3).decode()
    print(polarEps)

    start(PolarWindow,2,varB.get(),polarHp,polarAtk,polarEps)
def GOElectrical():
    selectWindow.destroy()

    clientSocket.send("3".encode())
    print("electrical field")

    global ElectricalWindow
    ElectricalWindow = Toplevel()
    ElectricalWindow.title("Electrical")
    #full screen
    gw = ElectricalWindow.winfo_screenwidth()
    gh = ElectricalWindow.winfo_screenheight()
    ElectricalWindow.geometry("%dx%d" %(gw, gh))

    ElectricalWindow.resizable(True, True)#設定視窗是否可以縮放
    ElectricalWindow.minsize(400, 200)

    #Background
    electbgop = Image.open("electrical.png")
    electbgrs = electbgop.resize((gw, 200), Image.ANTIALIAS)
    electbg = ImageTk.PhotoImage(electbgrs)
    img2 = tk.Label(ElectricalWindow, image=electbg)
    img2.image = electbg
    img2.place(x=0, y=770)
    time.sleep( 0.1 )
    clientSocket.send(str(varC.get()).encode())
    print(varC.get())
    electHp = clientSocket.recv(3).decode()
    print(electHp)
    electAtk =clientSocket.recv(3).decode()
    print(electAtk)
    electEps = clientSocket.recv(3).decode()
    print(electEps)

    start(ElectricalWindow,1,varC.get(),electHp,electAtk,electEps)
def Grassland():
    global varA
    varA = IntVar()
    varA.set(1)#預設值1 = Turtwig
    Turtwig = Radiobutton(selectWindow,variable = varA,value = 1,text = "Turtwig",font=('Arial',25),command = showTurtwig).place(x = 750,y = 600)
    Treecko = Radiobutton(selectWindow,variable = varA,value = 2,text = "Treecko",font=('Arial',25),command = showTreecko).place(x = 750,y = 650)
    Bulbasaur = Radiobutton(selectWindow,variable = varA,value = 3,text = "Bulbasaur",font=('Arial',25),command = showBulbasaur).place(x = 750,y = 700)
    Exeggutor = Radiobutton(selectWindow,variable = varA,value = 4,text = "Exeggutor",font=('Arial',25),command = showExeggutor).place(x = 750,y = 750)
    Victreebel = Radiobutton(selectWindow,variable = varA,value = 5,text = "Victreebel",font=('Arial',25),command = showVictreebel).place(x = 750,y = 800)    
    goButton = Button(selectWindow,text = "GO!!",width=15, height=1,font=('Arial',25),command = GOGrassland).place(x = 800,y=900)
def Polar():
    global varB
    varB = IntVar()
    varB.set(1)#預設值1 = Spheal
    Spheal= Radiobutton(selectWindow,variable = varB,value = 1,text = "Spheal",font=('Arial',25),command = showSpheal).place(x = 750,y = 600)
    Piloswine = Radiobutton(selectWindow,variable = varB,value = 2,text = "Piloswine",font=('Arial',25),command = showPiloswine).place(x = 750,y = 650)
    Articuno = Radiobutton(selectWindow,variable = varB,value = 3,text = "Articuno",font=('Arial',25),command = showArticuno).place(x = 750,y = 700)
    Lapras = Radiobutton(selectWindow,variable = varB,value = 4,text = "Lapras",font=('Arial',25),command = showLapras).place(x = 750,y = 750)
    Snover = Radiobutton(selectWindow,variable = varB,value = 5,text = "Snover",font=('Arial',25),command = showSnover).place(x = 750,y = 800)  
    goButton = Button(selectWindow,text = "GO!!",width=15, height=1,font=('Arial',25),command = GOPolar).place(x = 800,y=900)
def Electrical():
    global varC
    varC = IntVar()
    varC.set(1)#預設值1 = Pikachu
    Pikachu = Radiobutton(selectWindow,variable = varC,value = 1,text = "Pikachu",font=('Arial',25),command = showPikachu).place(x = 750,y = 600)
    Ampharos = Radiobutton(selectWindow,variable = varC,value = 2,text = "Ampharos",font=('Arial',25),command = showAmpharos).place(x = 750,y = 650)
    Electabuzz = Radiobutton(selectWindow,variable = varC,value = 3,text = "Electabuzz",font=('Arial',25),command = showElectabuzz).place(x = 750,y = 700)
    Zapdos = Radiobutton(selectWindow,variable = varC,value = 4,text = "Zapdos",font=('Arial',25),command = showZapdos).place(x = 750,y = 750)
    Jolteon = Radiobutton(selectWindow,variable = varC,value = 5,text = "Jolteon",font=('Arial',25),command = showJolteon).place(x = 750,y = 800)  
    goButton = Button(selectWindow,text = "GO!!",width=15, height=1,font=('Arial',25),command = GOElectrical).place(x = 800,y=900)
# Grassland
def showTurtwig():
    turImg = PhotoImage(file = "turtwig.png")
    turImgLabel = Label(selectWindow,image = turImg)
    turImgLabel.image = turImg
    turImgLabel.place(x = 1100,y = 600)
    # clientSocket.send("turtwig".encode())
def showTreecko():
    treImg = PhotoImage(file = "treecko.png")
    treImgLabel = Label(selectWindow,image = treImg)
    treImgLabel.image = treImg
    treImgLabel.place(x = 1100,y = 600)
    # clientSocket.send("treecko".encode())
def showBulbasaur():
    bulImg = PhotoImage(file = "bulbasaur.png")
    bulImgLabel = Label(selectWindow,image = bulImg)
    bulImgLabel.image = bulImg
    bulImgLabel.place(x = 1100,y = 600)
    # clientSocket.send("bulbasaur".encode())
def showExeggutor():
    exeImg = PhotoImage(file = "exeggutor.png")
    exeImgLabel = Label(selectWindow,image = exeImg)
    exeImgLabel.image = exeImg
    exeImgLabel.place(x = 1100,y = 600)
    # clientSocket.send("exeggutor".encode())
def showVictreebel():
    vicImg = PhotoImage(file = "victreebel.png")
    vicImgLabel = Label(selectWindow,image = vicImg)
    vicImgLabel.image = vicImg
    vicImgLabel.place(x = 1100,y = 600)
    # clientSocket.send("victreebel".encode())
# electrical field
def showPikachu():
    pikaImg = PhotoImage(file = "pikachu.png")
    pikaImgLabel = Label(selectWindow,image = pikaImg)
    pikaImgLabel.image = pikaImg
    pikaImgLabel.place(x = 1100,y = 600)
    # playsound('pikachuScream.mp3')
def showAmpharos():
    ampImg = PhotoImage(file = "ampharos.png")
    ampImgLabel = Label(selectWindow,image = ampImg)
    ampImgLabel.image = ampImg
    ampImgLabel.place(x = 1100,y = 600)
def showElectabuzz():
    eleImg = PhotoImage(file = "electabuzz.png")
    eleImgLabel = Label(selectWindow,image = eleImg)
    eleImgLabel.image = eleImg
    eleImgLabel.place(x = 1100,y = 600)
def showZapdos():
    zapImg = PhotoImage(file = "zapdos.png")
    zapImgLabel = Label(selectWindow,image = zapImg)
    zapImgLabel.image = zapImg
    zapImgLabel.place(x = 1100,y = 600)
def showJolteon():
    jolImg = PhotoImage(file = "jolteon.png")
    jolImgLabel = Label(selectWindow,image = jolImg)
    jolImgLabel.image = jolImg
    jolImgLabel.place(x = 1100,y = 600)
    #polar
def showSpheal():
    sphImg = PhotoImage(file = "spheal.png")
    sphImgLabel = Label(selectWindow,image = sphImg)
    sphImgLabel.image = sphImg
    sphImgLabel.place(x = 1100,y = 600)
def showPiloswine():
    pilImg = PhotoImage(file = "piloswine.png")
    pilImgLabel = Label(selectWindow,image = pilImg)
    pilImgLabel.image = pilImg
    pilImgLabel.place(x = 1100,y = 600)
def showArticuno():
    artImg = PhotoImage(file = "articuno.png")
    artImgLabel = Label(selectWindow,image = artImg)
    artImgLabel.image = artImg
    artImgLabel.place(x = 1100,y = 600)
def showLapras():
    lapImg = PhotoImage(file = "lapras.png")
    lapImgLabel = Label(selectWindow,image = lapImg)
    lapImgLabel.image = lapImg
    lapImgLabel.place(x = 1100,y = 600)
def showSnover():
    snoImg = PhotoImage(file = "snover.png")
    snoImgLabel = Label(selectWindow,image = snoImg)
    snoImgLabel.image = snoImg
    snoImgLabel.place(x = 1100,y = 600)
def create_account():
    createWindow =Toplevel() #tk.Tk()
    createWindow.geometry("800x600")
    createWindow.title("Create Account")
    create = "create"
    clientSocket.send(create.encode())

def bye():
    window.destroy()
    os._exit(0)

#建立連線
port = 9999
host = "127.0.0.1"

clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    clientSocket.connect((host,port))
except:
    print ("connect error!!")

#建立main window
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
CreateButton['font'] = myFont# apSignply font to the button label
CreateButton.pack(pady=10)

ExitButton = tk.Button(window,text='Exit',width=15, height=2,command=bye)
ExitButton['font'] = myFont# apply font to the button label
ExitButton.pack()

img_gif = tk.PhotoImage(file = '1.gif')
ImageLabel = tk.Label(window,image = img_gif)
ImageLabel.image = img_gif
ImageLabel.place(x =1500,y = 750)
window.mainloop()
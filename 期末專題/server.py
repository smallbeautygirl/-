import socket,traceback
import threading
import Pokemon
from Pokemon import Sopheal
from Pokemon import Piloswine
from Pokemon import Articuno
from Pokemon import Lapras
from Pokemon import Snover
from Pokemon import Pikachu
from Pokemon import Ampharos
from Pokemon import Electabuzz
from Pokemon import Zapdos
from Pokemon import Jolteon
from Pokemon import Turtwig
from Pokemon import Treecko
from Pokemon import Bulbasaur
from Pokemon import Exeggutor
from Pokemon import Victreebel
import time
currentPlayer = 0
class clientInformation():
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.win = 0
    def setWin(win):
        self.win = win   
#set some default users
user1 = clientInformation("11111","11111")
user2 = clientInformation("22222","22222")
database = [user1,user2]
storeRole = []
mainField =[]
bufferSize = 1024
storeHP =[]#int
storeATK =[]#int
storeEPS =[]#int
storeFD =[]
#建立socket物件(1)
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#設定和得到socket選項(2)
serverSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#繫結socket(3)
serverSocket.bind(("127.0.0.1",9999))
#偵聽連線(4)
serverSocket.listen(5)
# 紀錄 Client 傳送資料的 Thread
clientThreads = []
# 紀錄 Client 連線資訊
clientsocketConn = {}
import random
import time

class Pokemon:
    def __init__(self, hp, atk, eps,socket):
        self.hp = hp
        self.atk = atk
        self.eps = eps
        self.socket = socket
        if random.randint(0, 1):  # 1 plus
            self.hp += random.randint(0, 50)
            self.atk += random.randint(0, 50)
            self.eps += random.randint(0, 50)
        else:  # 0 minus
            self.hp -= random.randint(0, 50)
            self.atk -= random.randint(0, 50)
            self.eps -= random.randint(0, 50)
            while self.hp <= 0 or self.atk <= 0 or self.eps <= 0:
                if self.hp <= 0:
                    self.hp = hp
                    self.hp -= random.randint(0, 50)
                elif self.atk <= 0:
                    self.atk = atk
                    self.atk -= random.randint(0, 50)
                else:
                    self.eps = eps
                    self.eps -= random.randint(0, 50)

        dict = {"HP": self.hp, "ATK": self.atk, "EPS": self.eps}
        print(dict)
        self.socket.send(str(self.hp).encode())
        time.sleep( 0.07 )
        self.socket.send(str(self.atk).encode())
        time.sleep( 0.07 )
        self.socket.send(str(self.eps).encode())
        storeHP.append(self.hp)
        storeATK.append(self.atk)
        storeEPS.append(self.eps)
    def attack(self, damage, play):
        print("123")
        currentPlayer+=1
        currentPlayer%=2
        play = (play + 1) % 2  # change to opponent
        if storeEPS[play] > 0:  # can defend
            if storeEPS[play] - damage < 0:  # damage > eps
                damage -= storeEPS[play]  # rest damage
                storeEPS[play] = 0
                if storeHP[play] - damage < 0:
                    storeHP[play] = 0
                else:
                    storeHP[play] -= damage
            else:
                storeEPS[play] -= damage
        else:  # can't defend
            if storeHP[play] - damage < 0:
                storeHP[play] = 0
            else:
                storeHP[play] -= damage
        storeFD[0].send(storeHP[play].encode())
        print(storeHP[play])
        time.sleep(0.07)
        storeFD[1].send(storeHP[play].encode())
        print(storeHP[play])
        time.sleep(0.07)
        storeFD[0].send(storeEPS[play].encode())
        print(storeEPS[play])
        time.sleep(0.07)
        storeFD[1].send(storeEPS[play].encode())
        print(storeEPS[play])
        time.sleep(0.07)
def attack(damage, play):
    print("123")
    play = (play + 1) % 2  # change to opponent
    if storeEPS[play] > 0:  # can defend
        if storeEPS[play] - damage < 0:  # damage > eps
            damage -= storeEPS[play]  # rest damage
            storeEPS[play] = 0
            if storeHP[play] - damage < 0:
                storeHP[play] = 0
            else:
                storeHP[play] -= damage
        else:
            storeEPS[play] -= damage
    else:  # can't defend
        if storeHP[play] - damage < 0:
            storeHP[play] = 0
        else:
            storeHP[play] -= damage
    if play == 1:
        temp="0"#11111按得
    elif play==0:
        temp="1"#22222按的
    storeFD[0].send((temp+"H"+str(storeHP[play])).encode())
    print(storeHP[play])
    time.sleep(0.07)
    storeFD[1].send((temp+"H"+str(storeHP[play])).encode())
    print(storeHP[play])
    time.sleep(0.07)
    storeFD[0].send((temp+"E"+str(storeEPS[play])).encode())
    print(storeEPS[play])
    time.sleep(0.07)
    storeFD[1].send((temp+"E"+str(storeEPS[play])).encode())
    print(storeEPS[play])
    time.sleep(0.07)
# ##Grassland## #


class Turtwig(Pokemon):
    def __init__(self, hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)

    def skill(self):
        print("1. Razor Leaf\t2. Seed Bomb\t3. Energy Ball")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, att, play):
        if att == "1":  # razor leaf
            damage = storeATK[play] + random.randint(0, 10)
        elif att == "2": # Seed bomb
            damage = storeATK[play]* 5

        print("[damage] : ", damage)
        attack(damage, play)

    def defend_skill(self):
        if self.eps + 15 > 100:
            self.eps = 100
        else:
            self.eps += 15
        print("[EPS + 15]", self.eps)


class Treecko(Pokemon):
    def __init__(self, hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)

    def skill(self):
        print("1. Bullet Seed\t2. Pound\t3. Grass Knot")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, att, play):
        if att == "1":  # Bullet Seed
            damage = storeATK[play] + random.randint(0, 10)
        elif att == "2": # Pound
            damage = storeATK[play] + random.randint(0, 5)

        print("[damage] : ", damage)
        attack(damage, play)

    def defend_skill(self):
        if self.eps + 20 > 100:
            self.eps = 100
        else:
            self.eps += 20
        print("[EPS + 20]", self.eps)

class Bulbasaur(Pokemon):
    def __init__(self,hp, atk, eps, socket):
        super().__init__( hp, atk, eps, socket)

    def skill(self):
        print("1. Power Whip\t2. Tackle\t3. Vine Whip")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # Power whip
            damage = self.atk * 4
        elif a == "2": # Tackle
            damage = self.atk * 2

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

    def defend_skill(self):
        if self.eps + 10 > 100:
            self.eps = 100
        else:
            self.eps += 10
        print("[EPS + 10]", self.eps)


class Exeggutor(Pokemon):
    def __init__(self, hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)
        print("Exeggutor")
    def skill(self):
        print("1. Dragon Pulse\t2. Solar Beam\t3. Confusion")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # Dragon pulse
            damage = self.atk * 2
        elif a == "2": # solar beam
            damage = self.atk * 4

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

    def defend_skill(self):
        if self.eps + 15 > 100:
            self.eps = 100
        else:
            self.eps += 15
        print("[EPS + 15]", self.eps)


class Victreebel(Pokemon):
    def __init__(self, hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)

    def skill(self):
        print("1. Acid\t2. Solar Beam\t3. Razor Leaf")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # Acid
            damage = self.atk + random.randint(0, 5)
        elif a == "2": # Solar beam
            damage = self.atk * 4

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

    def defend_skill(self):
        if self.eps + 10 > 100:
            self.eps = 100
        else:
            self.eps += 10
        print("[EPS + 10]", self.eps)


# ##End of Grassland## #
# ##Polar## #


class Sopheal(Pokemon):
    def __init__(self,hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)

    def skill(self):
        print("1. Water Gun\t2. Aurora Beam\t3. Rock Smash")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # water gun
            damage = self.atk + random.randint(0, 5)
        elif a == "2": # Paurora Beam
            damage = self.atk * 2

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

    def defend_skill(self):
        if self.eps + 10 > 100:
            self.eps = 100
        else:
            self.eps += 10
        print("[EPS + 10]", self.eps)


class Piloswine(Pokemon):
    def __init__(self,hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)

    def skill(self):
        print("1. Powder Snow\t2. Bulldoze\t3. Avalanche")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # Powder snow
            damage = self.atk + random.randint(0, 5)
        elif a == "2": # Bulldoze
            damage = self.atk * 2

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

    def defend_skill(self):
        if self.eps + 10 > 100:
            self.eps = 100
        else:
            self.eps += 10
        print("[EPS + 10]", self.eps)


class Articuno(Pokemon):
    def __init__(self,hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)

    def skill(self):
        print("1. Frost Breath\t2. Blizzard\t3. Ice Beam")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # Frost Breath
            damage = self.atk + random.randint(0, 10)
        elif a == "2": # Blizzard
            damage = self.atk * 4

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

    def defend_skill(self):
        if self.eps + 10 > 100:
            self.eps = 100
        else:
            self.eps += 10
        print("[EPS + 10]", self.eps)


class Lapras(Pokemon):
    def __init__(self,hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)

    def skill(self):
        print("1. Water Gun\t2. Hydro Pump\t3. Frost Breath")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # water gun
            damage = self.atk + random.randint(0, 5)
        elif a == "2": # hydro pump
            damage = self.atk * 4

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

    def defend_skill(self):
        if self.eps + 8 > 100:
            self.eps = 100
        else:
            self.eps += 8
        print("[EPS + 8]", self.eps)


class Snover(Pokemon):
    def __init__(self,hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)

    def skill(self):
        print("1. Ice Shard\t2. Ice Beam\t3. Energy Ball")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # Ice Shard
            damage = self.atk + random.randint(0, 5)
        elif a == "2": # Ice Beam
            damage = self.atk * 3

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

    def defend_skill(self):
        if self.eps + 10 > 100:
            self.eps = 100
        else:
            self.eps += 10
        print("[EPS + 10]", self.eps)


# ##End of Polar## #

# ##Electrical## #


class Pikachu(Pokemon):
    def __init__(self,hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)

    def skill(self):
        print("1. Thunder Shock\t2. Thunderbolt\t3. Quick Attack")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # Thunder Shock
            damage = self.atk + random.randint(0, 5)
        elif a == "2": # Thunderbolt
            damage = self.atk * 2

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

    def defend_skill(self):
        if self.eps + 10 > 100:
            self.eps = 100
        else:
            self.eps += 10
        print("[EPS + 10]", self.eps)


class Ampharos(Pokemon):
    def __init__(self,hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)

    def skill(self):
        print("1. Charge Beam\t2. Thunder\t3. Volt Switch")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # Charge Beam
            damage = self.atk + random.randint(0, 5)
        elif a == "2": # Thunder
            damage = self.atk * 2

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

    def defend_skill(self):
        if self.eps + 5 > 100:
            self.eps = 100
        else:
            self.eps += 5
        print("[EPS + 5]", self.eps)


class Electabuzz(Pokemon):
    def __init__(self,hp, atk, eps, socket):
        super().__init__( hp, atk, eps, socket)

    def skill(self):
        print("1. Thunder Punch\t2. Thunderbolt\t3. Thunder Shock")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # Thunder Punch
            damage = self.atk * 2
        elif a == "2": # Thunderbolt
            damage = self.atk * 3

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

    def defend_skill(self):
        if self.eps + 10 > 100:
            self.eps = 100
        else:
            self.eps += 10
        print("[EPS + 10]", self.eps)


class Zapdos(Pokemon):
    def __init__(self,  hp, atk, eps, socket):
        super().__init__( hp, atk, eps, socket)

    def skill(self):
        print("1. Thunderbolt\t2. Zap Cannon\t3. Charge Beam")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # Thunderbolt
            damage = self.atk * 2
        elif a == "2": # Zap cannon
            damage = self.atk * 4

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

    def defend_skill(self):
        if self.eps + 10 > 100:
            self.eps = 100
        else:
            self.eps += 10
        print("[EPS + 10]", self.eps)


class Jolteon(Pokemon):
    def __init__(self, hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)

    def skill(self):
        print("1. Discharge\t2. Thunder\t3. Volt Switch")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # Discharge
            damage = self.atk + random.randint(0, 10)
        elif a == "2": # Thunder
            damage = self.atk * 3

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

    def defend_skill(self):
        if self.eps + 10 > 100:
            self.eps = 100
        else:
            self.eps += 10
        print("[EPS + 10]", self.eps)


# ##End of Electrical## #
def create(thefield, thepoke, socket):  # create pokemon constructor
    # opponentDist = {"HP" : 100, "ATK" : 15, "EPS" : 10}
    if thefield == "2":  # polar
        if thepoke == "1":
            spheal = Sopheal(100, 15, 10, socket)
            # print(spheal.)
            # while opponentDist["HP"] != 0:
            #     a = spheal.skill()
            #     if a == "3":
            #         spheal.defend_skill()
            #     else:
            #         spheal.attack_skill(a, opponentDist)
        elif thepoke == "2":
            piloswine = Piloswine(130, 10, 15, socket)
            # while opponentDist["HP"] != 0:
            #     a = piloswine.skill()
            #     if a == "3":
            #         piloswine.defend_skill()
            #     else:
            #         piloswine.attack_skill(a, opponentDist)
        elif thepoke == "3":
            articuno = Articuno(130, 15, 10, socket)
            # while opponentDist["HP"] != 0:
            #     a = articuno.skill()
            #     if a == "3":
            #         articuno.defend_skill()
            #     else:
            #         articuno.attack_skill(a, opponentDist)
        elif thepoke == "4":
            lapras = Lapras(150, 15, 10, socket)
            # while opponentDist["HP"] != 0:
            #     a = lapras.skill()
            #     if a == "3":
            #         lapras.defend_skill()
            #     else:
            #         lapras.attack_skill(a, opponentDist)
        elif thepoke == "5":
            snover = Snover(110, 10, 15, socket)
            # while opponentDist["HP"] != 0:
            #     a = snover.skill()
            #     if a == "3":
            #         snover.defend_skill()
            #     else:
            #         snover.attack_skill(a, opponentDist)
    elif thefield == "3":  # electrical
        if thepoke == "1":
            pikachu = Pikachu(80, 15, 15, socket)
        #     while opponentDist["HP"] != 0:
        #         a = pikachu.skill()
        #         if a == "3":
        #             pikachu.defend_skill()
        #         else:
        #             pikachu.attack_skill(a, opponentDist)
        # elif thepoke == "2":
            ampharos = Ampharos(135, 15, 10, socket)
            # while opponentDist["HP"] != 0:
            #     a = ampharos.skill()
            #     if a == "3":
            #         ampharos.defend_skill()
            #     else:
            #         ampharos.attack_skill(a, opponentDist)
        elif thepoke == "3":
            electabuzz = Electabuzz(110, 10, 12, socket)
            # while opponentDist["HP"] != 0:
            #     a = electabuzz.skill()
            #     if a == "3":
            #         electabuzz.defend_skill()
            #     else:
            #         electabuzz.attack_skill(a, opponentDist)
        elif thepoke == "4":
            zapdos = Zapdos(140, 15, 12, socket)
            # while opponentDist["HP"] != 0:
            #     a = zapdos.skill()
            #     if a == "3":
            #         zapdos.defend_skill()
            #     else:
            #         zapdos.attack_skill(a, opponentDist)
        elif thepoke == "5":
            jolteon = Jolteon(110, 10, 10, socket)
            # while opponentDist["HP"] != 0:
            #     a = jolteon.skill()
            #     if a == "3":
            #         jolteon.defend_skill()
            #     else:
            #         jolteon.attack_skill(a, opponentDist)
    else:  # grassland
        if thepoke == "1":
            turtwig = Turtwig(100, 15, 10, socket)  # set value
            # while opponentDist["HP"] != 0:
            #     a = turtwig.skill()
            #     if a == "3":
            #         turtwig.defend_skill()
            #     else:
            #         turtwig.attack_skill(a, opponentDist)
        elif thepoke == "2":
            treecko = Treecko(90, 10, 12, socket)
            # while opponentDist["HP"] != 0:
            #     a = treecko.skill()
            #     if a == "3":
            #         treecko.defend_skill()
            #     else:
            #         treecko.attack_skill(a, opponentDist)
        elif thepoke == "3":
            bulbasaur = Bulbasaur(95, 8, 20, socket)
            # while opponentDist["HP"] != 0:
            #     a = bulbasaur.skill()
            #     if a == "3":
            #         bulbasaur.defend_skill()
            #     else:
            #         bulbasaur.attack_skill(a, opponentDist)
        elif thepoke == "4":
            exeggutor = Exeggutor(130, 10, 15, socket)
            # while opponentDist["HP"] != 0:
            #     a = exeggutor.skill()
            #     if a == "3":
            #         exeggutor.defend_skill()
            #     else:
            #         exeggutor.attack_skill(a, opponentDist)
        elif thepoke == "5":
            victreebel = Victreebel(130, 15, 15, socket)
            # while opponentDist["HP"] != 0:
            #     a = victreebel.skill()
            #     if a == "3":
            #         victreebel.defend_skill()
            #     else:
            #         victreebel.attack_skill(a, opponentDist)
def checkAccountExist(username,password):
    for i in range(len(database)):
        flag = "false"
        if username == database[i].username:
            flag = "true"
            break
    return flag

# global gameLock
# gameLock = threading.Lock()
global otherPlayerTurn
otherPlayerTurn = threading.Condition()
class playclass:
    playerlist = [None,None]
    # currentPlayer = None# keep track of player with current move
    # PLAYER_0 = 0
    # PLAYER_1 = 1
    # checkTwoPlayer
    # player1socket
    # player2socket
    # n1
    # n2
    # global gameLock
    # gameLock = None
    # otherPlayerTurn = None
    def __init__(self):
        self.PLAYER_0 = 0
        self.PLAYER_1 = 1
        # currentPlayer = self.PLAYER_0
        self.checkTwoPlayer = 1
        self.gameLock = threading.Lock()
        # self.otherPlayerTurn = threading.Condition()
    def execute(self,socket1,socket2,name1,name2):
        print("execute")
        self.playerlist[0] = Player(socket1,0,name1,self.gameLock)
        self.playerlist[0].start()
        self.playerlist[1] = Player(socket2,1,name2,self.gameLock)
        self.playerlist[1].start()
    def checkIftwoPlayer(self,socket,name):
        print("check")
        if self.checkTwoPlayer == 1:
            self.checkTwoPlayer+=1
            self.player1socket=socket
            self.n1 = name
        else:
            self.player2socket = socket
            self.n2 = name
            self.execute(self.player1socket,self.player2socket,self.n1,self.n2)
class Player(threading.Thread,playclass):
    # str name
    # connection
    # playerNumber
    # bool suspended #whether thread is suspend
    def __init__(self,socket,number,name,lock):
        threading.Thread.__init__(self)
        self.connection = socket
        self.playerNumber = number
        self.playername = name 
        self.gameLock = lock
    def otherPlayerAttack(self,atk):
        print("otherAtk")
        # def exeATK(hp,player):
        # # while not current player, must wait for turn
    def run(self):
        print(self.playername +" run")
        if self.playerNumber == 0:
            self.connection.send("Your turn".encode())
            time.sleep(0.05)
            self.connection.send(storeRole[1].encode())#send role
            time.sleep(0.05)
            self.connection.send(str(storeHP[1]).encode())
            time.sleep(0.05)
            self.connection.send(str(storeATK[1]).encode())
            time.sleep(0.05)
            self.connection.send(str(storeEPS[1]).encode())            
        else:
            self.connection.send("Opponent turn,please wait".encode())
            time.sleep(0.05)
            self.connection.send(storeRole[0].encode())#send role   
            time.sleep(0.05)
            self.connection.send(str(storeHP[0]).encode())
            time.sleep(0.05)
            self.connection.send(str(storeATK[0]).encode())
            time.sleep(0.05)
            self.connection.send(str(storeEPS[0]).encode())
        # currentPlayer = (currentPlayer + 1) % 2;// change player
        while True:
            if storeHP[0]==0:
                break
            if storeHP[1]==0:
                break
            getPlayer = self.connection.recv(bufferSize).decode()#get player
            print(getPlayer)
            while getPlayer != str(currentPlayer):
                self.gameLock.acquire()
                # otherPlayerTurn.acquire()
                # otherPlayerTurn.notify()
                # otherPlayerTurn.release()
                self.gameLock.release()
            print("current: " + str(currentPlayer))
            # currentPlayer = (currentPlayer + 1) % 2
            getAttack = self.connection.recv(bufferSize).decode()#string
            print("attack: " + getAttack)
            # storeFD[0].send(getAttack.encode())
            # storeFD[1].send(getAttack.encode())
            # attack_skill_test(mainField[0],storeRole[int(getPlayer)],getAttack, int(getPlayer))  # also send the opponent's information
            print(storeHP[0])
            print(storeHP[1])
            print(storeEPS[0])
            print(storeEPS[1])
            if mainField[0] == "1":  # grassland
                if storeRole[int(getPlayer)] == "1":
                    Turtwig.attack_skill(self,getAttack, int(getPlayer))  # also send the opponent's information
                elif storeRole[int(getPlayer)] == "2":
                    Treecko.attack_skill(self,getAttack, int(getPlayer))
            elif mainField[0] == "2":  # polar
                if storeRole[int(getPlayer)] == "1":
                    Spheal.attack_skill(self,getAttack, int(getPlayer))
                elif storeRole[int(getPlayer)] == "2":
                    Piloswine.attack_skill(self,getAttack, int(getPlayer))
            else:
                print("other")
                print("mainField "+mainField[0])
        if storeHP[0]==0:
            storeFD[1].send("win".encode())
            storeFD[0].send("lose".encode())
        if storeHP[1]==0:
            storeFD[1].send("lose".encode())
            storeFD[0].send("win".encode())
# Receive Client Connection
play = playclass()
class ThreadServer(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        print ("client: ")
        print (self.socket)
        while True:
            action = self.socket.recv(bufferSize).decode()
            if action == "sign in":
                username = self.socket.recv(bufferSize).decode()
                password = self.socket.recv(bufferSize).decode()
                print (username)
                print(password)
                check = checkAccountExist(username,password)
                print (check)
                self.socket.send(check.encode())
                if check == "true":
                    break
            elif action == "create":
                break
        select = self.socket.recv(bufferSize).decode()       
        print(select) 
        if select == "select":
            field = self.socket.recv(bufferSize).decode()
            role = self.socket.recv(bufferSize).decode()
            print (field)
            print(role)
            storeRole.append(role)
            mainField.append(field)
            create(field,role,self.socket)

            play.checkIftwoPlayer(self.socket,username)
if __name__ == "__main__":
    while True:
        (clisocket, cliadr) = serverSocket.accept()
        storeFD.append(clisocket)
        ThreadServer(clisocket).start()
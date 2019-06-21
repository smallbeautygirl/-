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
    def attack(self, damage, dict={}):
        if dict["EPS"] > 0:  # can defend
            if dict["EPS"] - damage < 0:  # damage > eps
                damage -= dict["EPS"]  # rest damage
                dict["EPS"] = 0
                if dict["HP"] - damage < 0:
                    dict["HP"] = 0
                else:
                    dict["HP"] -= damage
            else:
                dict["EPS"] -= damage
        else:  # can't defend
            if dict["HP"] - damage < 0:
                dict["HP"] = 0
            else:
                dict["HP"] -= damage

# ##Grassland## #


class Turtwig(Pokemon):
    def __init__(self, hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)

    def skill(self):
        print("1. Razor Leaf\t2. Seed Bomb\t3. Energy Ball")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # razor leaf
            damage = self.atk + random.randint(0, 10)
        elif a == "2": # Seed bomb
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


class Treecko(Pokemon):
    def __init__(self, hp, atk, eps, socket):
        super().__init__(hp, atk, eps, socket)

    def skill(self):
        print("1. Bullet Seed\t2. Pound\t3. Grass Knot")
        action = input("Choose one of your skill >> ")
        return action

    def attack_skill(self, a, dict={}):
        if a == "1":  # Bullet Seed
            damage = self.atk + random.randint(0, 10)
        elif a == "2": # Pound
            damage = self.atk + random.randint(0, 5)

        print("[damage] : ", damage)
        super().attack(damage, dict)
        print(dict)

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
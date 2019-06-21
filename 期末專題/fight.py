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
from rules import showRule

# def field():
#     print("Choose which field you want to go :")
#     print("a : Grassland")
#     print("b : Polar")
#     print("c : Electrical field")
#     fieldname = input(">> ")
#     choosePokemon(fieldname)


# def choosePokemon(thefield="a"):
#     print("Choose one of your pokemon :")
#     if thefield == "b":  # polar
#         print("1. Spheal")
#         print("2. Piloswine")
#         print("3. Articuno")
#         print("4. Lapras")
#         print("5. Snover")
#     elif thefield == "c":  # electrical
#         print("1. Pikachu")
#         print("2. Ampharos")
#         print("3. Electabuzz")
#         print("4. Zapdos")
#         print("5. Jolteon")
#     else:  # grassland
#         print("1. Turtwig")
#         print("2. Treecko")
#         print("3. Bulbasaur")
#         print("4. Exeggutor")
#         print("5. Victreebel")
#     pokemonName = input(">> ")
#     create(thefield, pokemonName)


def create(thefield, thepoke):  # create pokemon constructor
    opponentDist = {"HP" : 100, "ATK" : 15, "EPS" : 10}
    if thefield == "2":  # polar
        if thepoke == "1":
            spheal = Sopheal(level, 100, 15, 10)
            while opponentDist["HP"] != 0:
                a = spheal.skill()
                if a == "3":
                    spheal.defend_skill()
                else:
                    spheal.attack_skill(a, opponentDist)
        elif thepoke == "2":
            piloswine = Piloswine(level, 130, 10, 15)
            while opponentDist["HP"] != 0:
                a = piloswine.skill()
                if a == "3":
                    piloswine.defend_skill()
                else:
                    piloswine.attack_skill(a, opponentDist)
        elif thepoke == "3":
            articuno = Articuno(level, 130, 15, 10)
            while opponentDist["HP"] != 0:
                a = articuno.skill()
                if a == "3":
                    articuno.defend_skill()
                else:
                    articuno.attack_skill(a, opponentDist)
        elif thepoke == "4":
            lapras = Lapras(level, 150, 15, 10)
            while opponentDist["HP"] != 0:
                a = lapras.skill()
                if a == "3":
                    lapras.defend_skill()
                else:
                    lapras.attack_skill(a, opponentDist)
        elif thepoke == "5":
            snover = Snover(level, 110, 10, 15)
            while opponentDist["HP"] != 0:
                a = snover.skill()
                if a == "3":
                    snover.defend_skill()
                else:
                    snover.attack_skill(a, opponentDist)
    elif thefield == "3":  # electrical
        if thepoke == "1":
            pikachu = Pikachu(level, 80, 15, 15)
            while opponentDist["HP"] != 0:
                a = pikachu.skill()
                if a == "3":
                    pikachu.defend_skill()
                else:
                    pikachu.attack_skill(a, opponentDist)
        elif thepoke == "2":
            ampharos = Ampharos(level, 135, 15, 10)
            while opponentDist["HP"] != 0:
                a = ampharos.skill()
                if a == "3":
                    ampharos.defend_skill()
                else:
                    ampharos.attack_skill(a, opponentDist)
        elif thepoke == "3":
            electabuzz = Electabuzz(level, 110, 10, 12)
            while opponentDist["HP"] != 0:
                a = electabuzz.skill()
                if a == "3":
                    electabuzz.defend_skill()
                else:
                    electabuzz.attack_skill(a, opponentDist)
        elif thepoke == "4":
            zapdos = Zapdos(level, 140, 15, 12)
            while opponentDist["HP"] != 0:
                a = zapdos.skill()
                if a == "3":
                    zapdos.defend_skill()
                else:
                    zapdos.attack_skill(a, opponentDist)
        elif thepoke == "5":
            jolteon = Jolteon(level, 110, 10, 10)
            while opponentDist["HP"] != 0:
                a = jolteon.skill()
                if a == "3":
                    jolteon.defend_skill()
                else:
                    jolteon.attack_skill(a, opponentDist)
    else:  # grassland
        if thepoke == "1":
            turtwig = Turtwig(level, 100, 15, 10)  # set value
            while opponentDist["HP"] != 0:
                a = turtwig.skill()
                if a == "3":
                    turtwig.defend_skill()
                else:
                    turtwig.attack_skill(a, opponentDist)
        elif thepoke == "2":
            treecko = Treecko(level, 90, 10, 12)
            while opponentDist["HP"] != 0:
                a = treecko.skill()
                if a == "3":
                    treecko.defend_skill()
                else:
                    treecko.attack_skill(a, opponentDist)
        elif thepoke == "3":
            bulbasaur = Bulbasaur(level, 95, 8, 20)
            while opponentDist["HP"] != 0:
                a = bulbasaur.skill()
                if a == "3":
                    bulbasaur.defend_skill()
                else:
                    bulbasaur.attack_skill(a, opponentDist)
        elif thepoke == "4":
            exeggutor = Exeggutor(level, 130, 10, 15)
            while opponentDist["HP"] != 0:
                a = exeggutor.skill()
                if a == "3":
                    exeggutor.defend_skill()
                else:
                    exeggutor.attack_skill(a, opponentDist)
        elif thepoke == "5":
            victreebel = Victreebel(level, 130, 15, 15)
            while opponentDist["HP"] != 0:
                a = victreebel.skill()
                if a == "3":
                    victreebel.defend_skill()
                else:
                    victreebel.attack_skill(a, opponentDist)

# level = 1
# showRule()
# field()
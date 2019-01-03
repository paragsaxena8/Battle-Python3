from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# print("\n\n")
# print("NAME                        HP                                      MP")
# print("                            _________________________               ___________  ")
# print(bcolors.BOLD + "Parag              460/460 |" + bcolors.OKGREEN + "████████████████" + bcolors.ENDC + "|       65/65 |" + bcolors.OKBLUE + "███████" + bcolors.OKBLUE + "| ")
# print("                            _________________________               ___________  ")
# print(bcolors.BOLD + "Parag              460/460 |" + bcolors.OKGREEN + "████████████████" + bcolors.ENDC + "|       65/65 |" + bcolors.OKBLUE + "███████" + bcolors.OKBLUE + "| ")
# print("                            _________________________               ___________  ")
# print(bcolors.BOLD + "Parag              460/460 |" + bcolors.OKGREEN + "████████████████" + bcolors.ENDC + "|       65/65 |" + bcolors.OKBLUE + "███████" + bcolors.OKBLUE + "| ")
#
# print("\n\n")

# black magic
# name, cost, dmg, type
fire = Spell("Fire", 250, 60, "black")
thunder = Spell("Thunder", 30, 700, "black")
blizzard = Spell("Blizzard", 45, 800, "black")
meteor = Spell("Meteor", 75, 1200, "black")
quake = Spell("Quake", 100, 1400, "black")

# white magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 35, 1500, "white")

# Items
# name, type, description, prop
portion = Item("Portion", 'portion', "Heals 50 HP", 50)
hiportion = Item("HiPortion", 'portion', "Heals 100 HP", 100)
Suportion = Item("SuperPortion", 'portion', "Heals 500 HP", 500)
elixir = Item("Elixir", 'elixir', 'Fully restore HP/MP of one party Member', 999)
Hielixir = Item("HiElixir", 'elixir', "Fully restore party Member's HP/MP", 9999)

grenade = Item("Grenade", 'attack', 'Deals 500 Damage', 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item": portion, "quantity": 15},
                {"item": hiportion, "quantity": 5},
                {"item": Suportion, "quantity": 2},
                {"item": elixir, "quantity": 2},
                {"item": Hielixir, "quantity": 1},
                {"item": grenade, "quantity": 7}]
# hp, mp, atk, df, magic, items
player1 = Person('Parag: ', 3260, 132, 300, 34, player_spells, player_items)
player2 = Person('Mohit: ', 4160, 188, 311, 34, player_spells, player_items)
player3 = Person('Piyush:', 4089, 174, 288, 34, player_spells, player_items)

enemy = Person('Anther', 14000, 1650, 500, 100, [], [])

players = [player1, player2, player3]
running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "Enemy Attacked" + bcolors.ENDC)

while running:
    print("========================")

    print("\n\n")
    print("NAME                             MP                                               HP")
    for player in players:
        player.get_stats()
    print("\n")
    enemy.get_enemy_stats()
    for player in players:

        player.choose_action()
        choice = input("Choose Action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print("You Attack for", dmg, "Points for Damage.")

        elif index == 1:
            player.choose_magic()
            magic_choose = int(input("Choose Magic:")) - 1

            if magic_choose == -1:
                continue

            spell = player.magic[magic_choose]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot Enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg), "points of damage" + bcolors.ENDC)

        elif index == 2:
            player.choose_items()
            item_choice = int(input("Choose Item:")) - 1
            if item_choice == -1:
                continue
            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "None Left!" + bcolors.ENDC)
                continue
            player.items[item_choice]["quantity"] -= 1

            if item.type == "portion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + "HP" + bcolors.ENDC)
            elif item.type == "elixir":

                if item.type == "MegaElixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restored HP/MP " + bcolors.ENDC)
            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals with " + str(item.prop), " HP" + bcolors.ENDC)

        enemy_choose = 1
        target = random.randrange(0, 3)
        enemy_dmg = enemy.generate_damage()
        players[target].take_damage(enemy_dmg)
        print("Enemy Attack for", enemy_dmg)
        print("------------------------------")
        print("Enemy HP: ", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC + "\n")

        if player1.get_hp() == 0:
            print(bcolors.FAIL + bcolors.BOLD + "You Will be DIE!!" + bcolors.ENDC)
            running = False

        elif enemy.get_hp() == 0:
            print(bcolors.OKGREEN + bcolors.BOLD + "You Won!!!" + bcolors.ENDC)
            running = False

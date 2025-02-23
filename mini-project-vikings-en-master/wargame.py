from vikingsClasses import Soldier, Viking, Saxon, War
import random
import pygame

pygame.init()

soldier_names = ["albert", "andres", "archie", "dani", "david", "gerard", "german", "graham", "imanol", "laura"]
great_war = War()


def init_war(num_of_sold):
    global great_war
    great_war = War()  # Reset war instance

    for _ in range(num_of_sold):
        great_war.addViking(Viking("Viking", 100, random.randint(0, 50)))
        great_war.addSaxon(Saxon(100, random.randint(0, 50)))

def process_battle_round():
    if great_war.showStatus() == "Vikings and Saxons are still in the thick of battle.":
        viking_result = great_war.vikingAttack()
        saxon_result = great_war.saxonAttack()
        print(" 🔄 Round is over with: ")
        return {'viking': viking_result, 'saxon': saxon_result}
    return {'viking': "", 'saxon': ""}

# def process_battle_round():
#     round_result = {}
#     # Process one round of attacks
#     round_result['viking'] = great_war.vikingAttack()
#     round_result['saxon'] = great_war.saxonAttack()
#     return round_result

def main(num_of_sold):
    global great_war
    great_war = War()

    # Create N Vikings
    for _ in range(num_of_sold):
        name = random.choice(soldier_names)
        health = 100
        strength = random.randint(0, 50)
        great_war.addViking(Viking(name, health, strength))

    # Create N Saxons
    for _ in range(num_of_sold):
        health = 100
        strength = random.randint(0, 50)
        great_war.addSaxon(Saxon(health, strength))
    
    round_number = 0
    last_round_time = pygame.time.get_ticks()

    # Battle Loop
    while great_war.showStatus() == "Vikings and Saxons are still in the thick of battle.":
        if pygame.time.get_ticks() - last_round_time >= 1000:  # 1-second delay between rounds
            round_number += 1
            print(f"🔄 Round {round_number}")


            viking_result = great_war.vikingAttack()
            print(viking_result)


            saxon_result = great_war.saxonAttack()
            print(saxon_result)


            print(f"Viking Army: {len(great_war.vikingArmy)} warriors, Saxon Army: {len(great_war.saxonArmy)} warriors")
            print(great_war.showStatus())

            last_round_time = pygame.time.get_ticks()


    print("🎉 " + great_war.showStatus())

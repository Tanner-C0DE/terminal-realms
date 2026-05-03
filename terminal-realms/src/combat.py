import random
import time

from src.ui import (MONSTER_ART, ITEM_ART, BOSS_ART, CEO_ART, WIN_LOGO, breaker,
                show_summary, VENDOR_ART, NURSE_ART)
from src.items import items, effects_data, give_item
from src.player import Enemy


def battle(player, room, manual_enemy=None):
    if manual_enemy:
        enemy = manual_enemy
    else:
        is_boss_room = (room.name == "The CEO's Office")
        name = "CEO" if is_boss_room else random.choice(room.monsters)
        enemy = Enemy(name, room.max_level, player, is_boss=is_boss_room)

    name = enemy.name

    # Display Monster Art
    if enemy.is_boss:
        if enemy.name == "CEO":
            print(f"The CEO glares at you... Prepare for the ultimate battle!")
            print(f"\n{CEO_ART}")
            time.sleep(3)
        else:
            print(f"\n[!] The {enemy.name} appears with {enemy.hp} HP and {enemy.armor} armor!")
            print(f"\n{BOSS_ART[enemy.name]}")
    elif name in MONSTER_ART:
        print(MONSTER_ART[name])
        print(f"\n[!] A wild {enemy} appears with {enemy.hp} HP and {enemy.armor} armor!")
        time.sleep(0.8)

    a_stat = (player.equipped_armor.stat if player.equipped_armor else 0) + (1 if "Resiliant" in player.effects else 0)
    revenue = enemy.hp
    w_name = player.equipped_weapon.name if player.equipped_weapon else "Fists"

    while enemy.hp > 0 and player.is_alive():
        # Player Turn
        damage = player.get_modified_attack()
        crit_damage = damage * 2
        crit_chance = random.random()

        if player.crit_chance_bonus > crit_chance:
            enemy.hp -= crit_damage
            print(f"\nYou CRIT with {w_name} for {crit_damage} damage! Armor couldn't stop it! (Enemy HP: {max(0, enemy.hp)})")
        elif enemy.armor > 0:
            enemy.hp -= max(0, damage - enemy.armor)
            print(f"\nYou strike with {w_name} for {damage} damage! Enemy armor blocked {enemy.armor}! (Enemy HP: {max(0, enemy.hp)})")
        else:
            enemy.hp -= damage
            print(f"\nYou strike with {w_name} for {damage} damage! (Enemy HP: {max(0, enemy.hp)})")
        time.sleep(0.8)
        if enemy.hp <= 0: break

        # Enemy Turn
        if not player.check_dodge():
            e_dmg = max(0, random.randint(1, enemy.max_attack) - (player.equipped_armor.stat if player.equipped_armor else 0))
            player.hp -= e_dmg
            print(f"\nThe {enemy.name} hits for {e_dmg}! Armor blocked {a_stat}. (Your HP: {max(0, player.hp)})")
            time.sleep(0.8)
            if player.hp <= 0:
                insurance_item = player.has_insurance
                if insurance_item and player.dept == "Insurance Agent":
                    dept_action_hp = player.max_hp - 50
                    bonus_hp = dept_action_hp * 2
                    player.hp = 75 + bonus_hp
                    player.max_hp = 75 + bonus_hp
                    player.min_attack = 6
                    player.max_attack = 10
                    give_item(player, "Stapler", equip=True)
                    player.inventory.remove(insurance_item)
                    print(f"\n[!] EMERGENCY REVIVE! Your 'Life Insurance' policy kicked in.")
                    time.sleep(0.8)
                    print(f"\n[INSURANCE] You are back in the fight with bonus HP and bonus damage (HP: {player.hp} HP | MIN/MAX ATK: {player.min_attack}/{player.max_attack})")
                    time.sleep(1.5)
                elif insurance_item and not player.dept == "Insurance Agent":
                    player.hp = insurance_item.stat
                    player.inventory.remove(insurance_item)
                    print(f"\n[!] EMERGENCY REVIVE! Your 'Life Insurance' policy kicked in.")
                    print(f"You're back in the fight with {player.hp} HP!")
                    time.sleep(1.5)
                else:
                    break

    if player.is_alive():
        if room.max_level == 5:
            print(f"{breaker}\t\tCongratulations, {player.name}!\n{WIN_LOGO}")
            time.sleep(2)
            show_summary(player, "win")
            victory = input("\nPress any key to exit or (R)estart: ").upper()
            if victory == "R":
                from src.game import game_loop
                game_loop()
            else:
                exit()
        else:
            # Revenue Siphon passive
            if "Revenue Siphon" in player.effects:
                lifesteal_percent = effects_data["Revenue Siphon"][3]
                if player.hp < player.max_hp:
                    heal_amount = min(round(revenue * lifesteal_percent), player.max_hp - player.hp)
                    player.hp += heal_amount
                    print(f"\n[REVENUE SIPHON] You drain {heal_amount} HP from the defeated {enemy.name}!")
                else:
                    reward = round(revenue * lifesteal_percent)
                    player.gold += reward
                    player.max_hp += 5
                    player.hp += 5
                    print(f"\n[REVENUE SIPHON] Already at full health! Converted drain to {reward} gold and +5 Max HP.")
            else:
                reward = room.max_level * 10
                cards = [i for i in player.inventory if i.name == "Company Credit Card"]
                if cards:
                    multiplier = 0.0
                    for card in cards:
                        multiplier += card.stat
                    print("\n[!] Gold Bonus! Your 'Company Credit Card' kicked in.")
                    reward = round(reward * multiplier)
                player.gold += reward
                print(f"\nVictory! You collect {reward} gold.")
        player.tick_effects()


def generic_shop(player, type, sell_only=False):
    print(f"{type[0]}")

    # Selling
    if sell_only:
        while True:
            print(f" Gold: {player.gold}")
            for i, item in enumerate(player.inventory, 1):
                status = "[EQUIPPED]" if item in (player.equipped_weapon, player.equipped_armor) else "[ACTIVE]" if item.itype == 'special' else ""
                print(f"{status} {i}. {item.name} ({item.itype}) - Sell for {item.value} gold.")

            choice = input("\nEnter number to sell ('B' to back out or 'Sell All'): ").upper()
            if choice == 'B':
                break
            if choice == 'SELL ALL':
                to_sell = []
                for item in player.inventory:
                    is_it_tool = (player.dept == "IT Specialist" and item.name == "Screwdriver")
                    if not (item in (player.equipped_weapon, player.equipped_armor) or item.itype in ('special', 'heal', 'key') or is_it_tool):
                        to_sell.append(item)
                if not to_sell:
                    print("\n[!] You don't have any junk to sell!")
                    continue
                player.gold += sum(item.value for item in to_sell)
                player.inventory = [item for item in player.inventory if item not in to_sell]
                print(f"{breaker}\nYou cleared out your pockets and gained {sum(item.value for item in to_sell)} gold!")
                break
            if choice.isdigit() and 0 <= (idx := int(choice) - 1) < len(player.inventory):
                sold_item = player.inventory.pop(idx)
                player.gold += sold_item.value
                print(f"{breaker}Sold {sold_item.name} for {sold_item.value} gold!")
                if not player.inventory: break
            elif not choice.isdigit():
                print('Invalid item.')
        return

    if player.inventory and type[2] == 'Vendor':
        print(f"\n{breaker}Vendor: 'Care to sell some of your junk first?'")
        choice = input("\nDo you want to (S)ell or skip to (B)uying? ").upper()
        if choice == 'S':
            while True:
                print(f"\n Gold: {player.gold}")
                for i, item in enumerate(player.inventory, 1):
                    status = "[EQUIPPED]" if item in (player.equipped_weapon, player.equipped_armor) else "[ACTIVE]" if item.itype == 'special' else ""
                    print(f"{status} {i}. {item.name} ({item.itype}) - Sell for {item.value} gold.")

                choice = input("\nEnter number to sell ('B' to back out or 'Sell All'): ").upper()
                if choice == 'B':
                    break
                if choice == 'SELL ALL':
                    to_sell = []
                    for item in player.inventory:
                        is_it_tool = (player.dept == "IT Specialist" and item.name == "Screwdriver")
                        if not (item in (player.equipped_weapon, player.equipped_armor) or item.itype in ('special', 'heal', 'key') or is_it_tool):
                            to_sell.append(item)
                    if not to_sell:
                        print("\n[!] You don't have any junk to sell!")
                        continue
                    player.gold += sum(item.value for item in to_sell)
                    player.inventory = [item for item in player.inventory if item not in to_sell]
                    print(f"{breaker}\nYou cleared out your pockets and gained {sum(item.value for item in to_sell)} gold!")
                    break
                if choice.isdigit() and 0 <= (idx := int(choice) - 1) < len(player.inventory):
                    sold_item = player.inventory.pop(idx)
                    player.gold += sold_item.value
                    print(f"{breaker}Sold {sold_item.name} for {sold_item.value} gold!")
                    if not player.inventory: break
                elif not choice.isdigit():
                    print('Invalid item.')

    # Buying
    if type[2] == "Nurse":
        healing_items = [k for k, v in items.items() if v[2] == "heal"]
        stock_names = sorted(random.sample(healing_items, 2), key=lambda k: items[k][1])
    else:
        stock_names = [
            random.choice([k for k, v in items.items() if v[2] == 'weapon']),
            random.choice([k for k, v in items.items() if v[2] == 'armor']),
            random.choice([k for k, v in items.items() if v[2] == 'special'])
        ]

    while stock_names and player.gold > 0:
        price_mod = effects_data["Guilt"][3] if "Guilt" in player.effects else 1.0

        if price_mod > 1.0:
            print(f"\n[!] GUILT TAX: The {type[2]} looks at you with disgust. Prices are increased!")

        print(f"{breaker}Gold: {player.gold}\n{type[2]}: 'Here is what I have today: '")
        for i, s_name in enumerate(stock_names, 1):
            current_price = round(items[s_name][1] * price_mod)
            print(f"{i}. {s_name} | {current_price} Gold - {items[s_name][0]}")

        choice = input("\nEnter number to buy (or 'B' to back out): ")
        if choice.upper() == 'B': break
        if choice.isdigit() and 0 < int(choice) <= len(stock_names):
            idx = int(choice) - 1
            s_name = stock_names[idx]
            price = round(items[s_name][1] * price_mod)
            if player.gold >= price:
                player.gold -= price
                give_item(player, s_name)
                print(f"\nYou bought a {s_name}!")
                print(ITEM_ART[s_name])
                stock_names.pop(idx)
                if not stock_names: print("\nI'm sold out!"); break
            else:
                print("Not enough gold!")
        if player.gold <= 0:
            print("\n[!] You've run out of gold!")
            break


def encounter_locked_closet(player):
    from src.ui import ITEM_ART
    print("\nYou stumble upon a heavy oak door labeled 'SUPPLY CLOSET'.")
    time.sleep(0.5)
    if player.has_key:
        choice = input("\nUse your Key to unlock it? (Y/N): ").upper()
        if choice == 'Y':
            print("\n[!] The key turns with a satisfying click!")
            time.sleep(0.8)
            player.consume_item("Key")
            rand = random.randint(1, 2)

            if int(rand) == 1:
                print("You raid the closet!")
                bonus_gold = random.randint(50, 100)
                player.gold += bonus_gold
                print(f"You found a hidden stash of petty cash! (+{bonus_gold} Gold)")
                print(ITEM_ART["Pile of Loose Change"])

            elif int(rand) == 2:
                high_tier = ["Desk Lamp", "Garbage Can Lid", "Company Credit Card", "Red Pen", "PTO Voucher"]
                loot = random.choice(high_tier)
                give_item(player, loot)
                print(f"You found a {loot} tucked away on the top shelf!")
                print(ITEM_ART[loot])
        else:
            print("You decide to save your key for later.")
    else:
        print("You don't have a key to open this. Maybe there's one hidden in the cubicles?")

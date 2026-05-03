import random
import time
import os

from src.ui import (LOGO, ITEM_ART, GAME_OVER, WIN_LOGO, VENDOR_ART, NURSE_ART, breaker,
                show_summary, display_stats)
from src.items import items, effects_data, dept_actions, give_item
from src.player import Player, Room
from src.combat import battle, generic_shop, encounter_locked_closet


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def inventory(player, office_rooms):
    FILTER_TYPES = ["heal", "weapon", "armor", "special", "item", "key"]

    def print_inventory(filter_type=None):
        print("\n--- Your Inventory ---")
        for index, item in enumerate(player.inventory, 1):
            if filter_type and item.itype != filter_type:
                continue
            is_it_tool = (player.dept == "IT Specialist" and item.name == "Screwdriver")
            if is_it_tool:
                status = "[PERMANENT]"
            elif item == player.equipped_weapon or item == player.equipped_armor:
                status = "[EQUIPPED]"
            elif item.itype == 'special':
                status = "[ACTIVE]"
            else:
                status = ""
            print(f"{status} {index}. {item}")

    if not player.inventory:
        print("Your pockets are empty.")
        return

    print_inventory()

    while True:
        choice = input("\nEnter item number, a type to filter (" + "/".join(FILTER_TYPES) + "), or 'B' to go back: ")

        if choice.upper() == 'B':
            return

        if choice.lower() in FILTER_TYPES:
            print_inventory(filter_type=choice.lower())
            continue

        if choice.isdigit():
            idx = int(choice) - 1

            if 0 <= idx < len(player.inventory):
                selected_item = player.inventory[idx]

                if selected_item.name in ITEM_ART:
                    print(f"\n{ITEM_ART[selected_item.name]}")

                print(f"\nYou used the {selected_item.name}!")

                if selected_item.name == "Sticky Note":
                    room_code = office_rooms["The IT Closet"].required_code
                    print(f"\n[!] 'The IT Closet Door Code is {room_code}.'")

                elif selected_item.itype == "heal":
                    if selected_item.stat == 0:
                        heal_amount = max(0, player.max_hp - player.hp)
                    elif "Optimization" in player.effects:
                        bonus = round(selected_item.stat * 0.5)
                        heal_amount = selected_item.stat + bonus
                        print(f"\n[OPTIMIZATION] Your analytical mind squeezed {bonus} extra HP out of that {selected_item.name}!")
                    else:
                        heal_amount = selected_item.stat
                    player.hp += heal_amount
                    print(f"You feel refreshed! +{heal_amount} HP")
                    player.inventory.pop(idx)

                elif selected_item.itype == 'weapon':
                    player.equipped_weapon = selected_item
                    print(f"\nYou equipped the {selected_item.name}")
                elif selected_item.itype == 'armor':
                    player.equipped_armor = selected_item
                    print(f"\nYou equipped the {selected_item.name}")
                else:
                    print(f"\n[!] The {selected_item.name} is not usable right now.")
                    continue
                return
        else:
            print("\n[!] Invalid item number.")


def select_department(name):
    print(f"{breaker}CHOOSE YOUR DEPARTMENT:\n")
    print(" 1. The Intern (Glass Cannon)      |  50 HP | 11 ATK | Starts with Desk Lamp")
    print(" 2. PE Associate (Lifesteal)       |  70 HP | 5 ATK  | Starts with Umbrella and Garbage Can Lid")
    print(" 3. HR Manager (Resiliant)         |  90 HP | 4 ATK  | Starts with Red Pen")
    print(" 4. Sales Exec (Merchant)          |  80 HP | 5 ATK  | Starts with Credit Card & 100 Gold")
    print(" 5. Corporate Lawyer (Crit Hits)   |  90 HP | 3 ATK  | Starts with Two Red Pens")
    print(" 6. Facilities Manager (Scavenger) |  75 HP | 5 ATK  | Starts with Key")
    print(" 7. PR Specialist (Dodge Hits)     |  70 HP | 4 ATK  | Starts with Hat")
    print(" 8. Data Analyst (Optimize Heals)  |  90 HP | 6 ATK  | Starts with Energy Drink & Leftovers")
    print(" 9. Wealth Manager (Greed)         |  65 HP | 0 ATK  | Starts with 75 Gold")
    print("10. Insurance Agent (Revive)       |  50 HP | 6 ATK  | Starts with Life Insurance & Jacket")
    print("11. IT Specialist (Utility)        |  90 HP | 4 ATK  | Starts with Screwdriver & Key")

    choice = input("\nEnter choice (1-11): ")

    if choice == 'random':
        choice = str(random.randint(1, 11))

    if choice == '1':
        p = Player(name, hp=50, max_attack=11, dept="Intern")
        give_item(p, "Desk Lamp", equip=True)
        return p

    elif choice == '2':
        p = Player(name, hp=70, max_attack=5, dept="PE Associate")
        give_item(p, "Umbrella", equip=True)
        give_item(p, "Garbage Can Lid", equip=True)
        p.add_effect("Revenue Siphon", -1)
        return p

    elif choice == '3':
        p = Player(name, hp=90, max_attack=4, dept="HR Manager")
        p.add_effect("Resiliant", -1)
        give_item(p, "Red Pen")
        return p

    elif choice == '4':
        p = Player(name, hp=80, max_attack=5, gold=100, dept="Sales Exec")
        give_item(p, "Company Credit Card")
        return p

    elif choice == '5':
        p = Player(name, hp=90, max_attack=3, gold=0, dept="Corporate Lawyer")
        give_item(p, "Red Pen")
        give_item(p, "Red Pen")
        return p

    elif choice == '6':
        p = Player(name, hp=75, max_attack=5, gold=0, dept="Facilities Manager")
        p.add_effect("Scavenger", -1)
        give_item(p, "Key")
        return p

    elif choice == '7':
        p = Player(name, hp=70, max_attack=4, dept="PR Specialist")
        p.add_effect("Spin Doctor", -1)
        give_item(p, "Hat", equip=True)
        give_item(p, "Coffee Mug")
        return p

    elif choice == '8':
        p = Player(name, hp=90, max_attack=6, dept="Data Analyst")
        p.add_effect("Optimization", -1)
        give_item(p, "Energy Drink")
        give_item(p, "Plate of Leftovers")
        return p

    elif choice == '9':
        p = Player(name, hp=65, min_attack=0, max_attack=0, gold=75, dept="Wealth Manager")
        p.add_effect("Greed", -1)
        return p

    elif choice == '10':
        p = Player(name, hp=50, max_attack=6, dept="Insurance Agent")
        give_item(p, "Life Insurance")
        give_item(p, "Heavy Jacket", equip=True)
        return p

    elif choice == '11':
        p = Player(name, hp=90, min_attack=0, max_attack=4, dept="IT Specialist")
        give_item(p, "Screwdriver")
        p.passive_slot = p.inventory[-1]
        p.passive_slot.stat = 0
        give_item(p, "Key")
        return p

    else:
        print("Invalid choice. Defaulting to 'Standard Employee'...")
        return Player(name)


def game_loop():
    print(LOGO)
    print("\n--- Welcome to the Terminal Realms ---")
    name = input("Enter your hero's name: ")

    player = select_department(name)

    office_rooms = {
        "The Lobby": Room("The Lobby", ["Cubicle Creeper", "HR Hellion", "Voicemail Viper"], ["item", "key"], max_level=1, boss_name="Security Guard"),
        "The Breakroom": Room("The Breakroom", ["Menacing Microwave", "Deadline Demon", "Corporate Vampire"], ["item", "key"], max_level=2, boss_name="Microwave Chef"),
        "The Conference Room": Room("The Conference Room", ["Paper Jam Poltergeist", "Fax Machine Phantom", "Meeting Minotaur"], ["usable", "item", "key"], max_level=2, loot_limit=3, boss_name="Middle Manager"),
        "The IT Closet": Room("The IT Closet", ["Wi-Fi Witherer", "Spreadsheet Spirit"], ["item", "heal", "key"], max_level=3, loot_limit=2, is_locked=True, required_code="1234", boss_name="IT Director"),
        "The CEO's Office": Room("The CEO's Office", ["CEO"], ["item", "key"], max_level=5, is_locked=True, required_item="Key", boss_name="CEO")
    }

    it_code = f"{random.randint(0, 9999):04}"
    office_rooms["The IT Closet"].required_code = it_code

    room_sequence = ["The Lobby", "The Breakroom", "The Conference Room", "The IT Closet", "The CEO's Office"]
    unlocked_rooms = ["The Lobby"]

    current_room = office_rooms["The Lobby"]

    boosted = False
    explore_count = 0
    finds = 0
    vendor_count = 0
    nurse_count = 0

    while player.is_alive():
        stats = f"{max(0, player.hp)} HP | {player.gold} GOLD"
        print(f"\n{player.name} the {player.dept}: {stats}")

        print(f"\nLocation: {current_room.name} | Battle #{explore_count + 1}")
        choice = input(f"{breaker}Do you (E)xplore, (I)nventory, (L)oot, (D)ept Action, (S)tats or (Q)uit? ").upper()

        if choice == 'D':
            if player.deptaction == True:
                print("\n'Deparment Action' has already been used in this room.")
                continue
            if player.dept in dept_actions:
                data = dept_actions[player.dept]
                desc, cost, heal, bonus = data[0], data[1], data[2], data[3]

                if player.gold >= cost:
                    player.gold -= cost
                    player.hp += heal

                    print(f"\n--- {player.dept.upper()} SPECIAL ---")
                    print(f"{desc}")
                    if not player.dept == "PR Specialist":
                        print(f"Spent {cost} Gold. Healed {heal} HP. (HP: {player.hp}/{player.max_hp})")

                    if bonus == "ClearHead":  # Intern
                        to_remove = [e for e in player.effects if e in ["Jitters", "Guilt", "Audit"]]
                        for effect in to_remove:
                            del player.effects[effect]
                        print("All negative effects cleared!")

                    elif bonus == "Profit":  # Data Analyst
                        player.gold += 40
                        rand_item = random.choice([k for k, v in items.items() if v[2] == "heal"])
                        give_item(player, rand_item)
                        print(f"\n{ITEM_ART[rand_item]}")
                        print(f"You optimized your surroundings! (Gained 40 Gold and a {rand_item}).")

                    elif bonus == "Resistance":  # HR Manager
                        player.max_hp += 10
                        player.hp += 10
                        print("You've built up a thick skin. (+10 HP gained!)")

                    elif bonus == "Greed":  # Sales Exec
                        player.add_effect("Greed", 1)
                        print("You're hungry for that commission! (Greed active)")

                    elif bonus == "Litigate":  # Corporate Lawyer
                        player.add_effect("Overclocked", 3)
                        print("You found a loophole! (Damage boost for next 3 rounds)")

                    elif bonus == "Scavenge":  # Facilities Manager
                        print("You found some forgotten supplies!")
                        for _ in range(2):
                            rand_item = random.choice(list(items.keys()))
                            give_item(player, rand_item)
                            print(f"\n{rand_item}:\n{ITEM_ART[rand_item]}")

                    elif bonus == "SpinControl":  # PR Specialist
                        spin = int(input("\nHow much gold would you like to spin into a heal? "))
                        max_allowed_heal = (player.max_hp * 2) - player.hp
                        spin = min(spin, player.gold)
                        if spin > max_allowed_heal:
                            print(f"\n[!] Regulation Alert: You can't rebrand yourself that much! Capping heal at {max_allowed_heal}.")
                            spin = max_allowed_heal
                        if spin > 0:
                            player.gold -= spin
                            player.hp += spin
                            print(f"\nYou spun {spin} gold into a great heal! (+{spin} HP)")
                        else:
                            print("\nNothing happened. You are already at the corporate health limit!")

                    elif bonus == "RemoteSell":  # PE Associate
                        print("\nAccessing the online market...")
                        time.sleep(1)
                        remote_vendor = ["", [], "Vendor"]
                        generic_shop(player, remote_vendor, sell_only=True)
                        print("\n[!] Connection closed.")

                    elif bonus == "Dividends":  # Wealth Manager
                        interest = int(player.gold * 0.08)
                        player.gold += interest
                        print(f"Market gains! You earned {interest} Gold.")

                    elif bonus == "Premium":  # Insurance Agent
                        player.max_hp += 5
                        print("Policy updated! (+5 Max HP)")

                    elif bonus == "HardwareMod":  # IT Specialist
                        player.min_attack += 1
                        player.max_attack += 1
                        print(f"[IT] System optimized! Your base damage is now {player.min_attack}-{player.max_attack}.")

                    player.dept_actions_used += 1
                    player.deptaction = True

                else:
                    print(f"\n[!] Not enough Gold! Development costs {cost}.")
            else:
                print("\n[!] No special action for your department.")

        elif choice == 'E':
            current_room.loot_count = 0
            finds = random.randint(1, current_room.loot_limit)
            event = random.random()
            vendor = VENDOR_ART, ["weapon", "armor", "special"], "Vendor"
            nurse = NURSE_ART, "heal", "Nurse"

            # Sales Exec vendor first
            if current_room.name == "The Lobby" and vendor_count == 0 and player.dept == "Sales Exec":
                print('\nYou run into a vendor!')
                generic_shop(player, vendor)
                vendor_count += 1
                continue

            # Force first battle
            elif current_room.name == "The Lobby" and explore_count == 0:
                print(f"\nBattle #{explore_count + 1}")
                battle(player, current_room)
                player.battles_fought += 1
                explore_count += 1
                continue

            # -- Performance Review --
            if event < 0.05:
                print(f"\nA Senior Manager stops you for a 'Performance Review'.")
                time.sleep(2)
                if boosted:
                    print("'We need to see consistent results before another promotion.'")
                    continue
                if "Guilt" in player.effects:
                    print("Your confidence seems really low. We cannot offer a promotion at this time.")
                    continue
                if player.hp >= 50:
                    print("'Your energy is impressive! You've been promoted to Senior Associate.'")
                    time.sleep(1)
                    player.min_attack += 2
                    player.max_attack += 2
                    print(f"[!] PERMANENT BUFF: Your Attack range is now {player.min_attack}-{player.max_attack}!")
                    player.promotions += 1
                    boosted = True
                else:
                    fine = random.randint(5, 15)
                    player.gold = max(0, player.gold - fine)
                    print(f"'You look exhausted. We're docking your pay for lack of 'synergy'.' (-{fine} Gold)")

            # -- Vending Machine --
            elif event < 0.1:
                print(f"\nYou find a vending machine. An 'Energy Drink' is stuck against the glass!")
                print("1. Shake it (Risk 5 damage for a free heal)")
                print("2. Pay 5 Gold (Guaranteed 'Plate of Leftovers')")
                if any(i.name == "Screwdriver" for i in player.inventory):
                    print("3. Use Screwdriver (Hack the machine for both!)")

                v_choice = input("What do you do? ")
                if v_choice == '1':
                    if random.random() > 0.5:
                        give_item(player, "Energy Drink")
                        print("\n[!] SUCCESS! The drink falls. You pocket it.")
                    else:
                        player.hp -= 5
                        print("\n[!] CRASH! The machine tips and bruises your arm. (-5 HP)")
                elif v_choice == '2' and player.gold >= 5:
                    player.gold -= 5
                    give_item(player, "Plate of Leftovers")
                    print("\n[!] The machine whirs and drops a plate of old food.")
                elif v_choice == '3' and any(i.name == "Screwdriver" for i in player.inventory):
                    print("\n[!] You expertly pop the glass. You take the Drink AND the Leftovers!")
                    give_item(player, "Energy Drink")
                    give_item(player, "Plate of Leftovers")

            # -- Stray Paycheck --
            elif event < 0.14:
                print(f"\nYou find a loose paycheck on the floor.")
                time.sleep(0.5)
                p_choice = input("Do you (P)ocket it, (L)eave it, or (R)eturn it to HR for 'Good Will'? ").upper()
                if p_choice == 'P':
                    paycheck = random.randint(20, 50)
                    player.gold += paycheck
                    print(f"\n[!] Your bank account looks better, but your conscience... not so much.\n(+{paycheck} gold)")
                    player.add_effect("Guilt", 2)
                elif p_choice == 'R':
                    hp_bonus = random.randint(5, 20)
                    player.hp += hp_bonus
                    print(f"\n[!] HR is impressed by your honesty. They give you a 'Health & Wellness' voucher! (+{hp_bonus} HP)")
                else:
                    continue

            # -- Supply Closet --
            elif event < 0.165:
                encounter_locked_closet(player)

            # -- Printer Fix --
            elif event < 0.175:
                print(f"\nYou find a Printer flashing a 'CYAN EMPTY' error.")
                time.sleep(1)
                choice = input("Do you want to try to repair it? (Y/N): ").upper()
                if choice == 'Y':
                    roll = random.randint(1, 20)
                    if roll <= 5:
                        damage = roll
                        player.hp -= damage
                        print(f"Roll: {roll}. CRITICAL FAILURE! The toner exploded in your face. (-{damage} HP)")
                    elif roll < 15:
                        print(f"Roll: {roll}. You cleared the jam but found nothing but old memos.")
                    else:
                        reward = roll
                        player.gold += reward
                        print(f"Roll: {roll}. CRITICAL SUCCESS! You found a stash of 'Petty Cash' inside the paper tray! (+{reward} Gold)")

            # -- Traveling Nurse --
            elif event < 0.25:
                if nurse_count < 2:
                    print('\nYou run into a traveling nurse!')
                    generic_shop(player, nurse)
                    nurse_count += 1
                else:
                    print("\nYou see the traveling nurse in the distance, but they are busy with another 'patient'.")

            # -- Traveling Vendor --
            elif event < 0.35:
                if vendor_count < 2:
                    print('\nYou run into a vendor!')
                    generic_shop(player, vendor)
                    vendor_count += 1
                else:
                    print("\nYou see the vendor in the distance, but they are busy with another 'client'.")

            # -- Coffee Machine --
            elif event < 0.4:
                print("\nYou stumble upon the office's industrial espresso machine.")
                print("It's wheezing, but there's still some left in the tank.\n")
                print("1. Walk away ... safety first")
                print("2. Double Shot (Heal +10 HP, but get 'The Jitters')")
                print("3. Scavenge (Search the drip tray for loose change)")
                if any(i.name == "Screwdriver" for i in player.inventory):
                    print("4. Overclock (Use Screwdriver to bypass the safety limiter)")

                coffee_choice = input("\nWhat will you do? ")

                if coffee_choice == '1':
                    print("\nYou decide you've had enough caffeine for one career.")
                elif coffee_choice == '2':
                    print("\n[!] You feel a buzz... but your hands won't stop shaking.")
                    player.hp += 10
                    player.add_effect("Jitters", 2)
                    print(f"\nCurrent HP: {player.hp} | Attack reduced by 2 until your next battle!")
                elif coffee_choice == '3':
                    found_gold = random.randint(5, 15)
                    player.gold += found_gold
                    print(f"\nYou find gold in the coinslot and drip tray. Gross, but profit! \n(+{found_gold} Gold)")
                elif coffee_choice == '4' and any(i.name == "Screwdriver" for i in player.inventory):
                    if random.random() < 0.5:
                        print("\n[SUCCESS] You bypass the limiter! The caffeine is glowing. You feel INVINCIBLE.")
                        player.add_effect("Overclocked", 2)
                        print("\nMax Attack increased by 5 for your next 2 fights!")
                    else:
                        print("\n[FAILURE] The boiler explodes! Scalding water sprays everywhere!")
                        player.hp -= 15
                        print("(-15 HP)")
                continue

            # -- Battle --
            elif event < 0.9:
                if current_room.name == unlocked_rooms[-1]:
                    explore_count += 1

                if not current_room.boss_defeated and explore_count >= 5:
                    print(f"\n[!] WARNING: {current_room.boss_name} is blocking your path!")
                    from src.player import Enemy
                    boss_enemy = Enemy(current_room.boss_name, current_room.max_level, player, is_boss=True)
                    time.sleep(1)
                    result = battle(player, current_room, manual_enemy=boss_enemy)
                    player.boss_battles_fought += 1

                    if player.is_alive():
                        current_room.boss_defeated = True
                        print(f"\n[!] Success! The {current_room.boss_name} has been defeated.")

                        current_room_index = room_sequence.index(current_room.name)
                        if current_room_index + 1 < len(room_sequence):
                            next_room_name = room_sequence[current_room_index + 1]
                            current_room = office_rooms[next_room_name]
                            unlocked_rooms.append(next_room_name)

                            explore_count = 0
                            vendor_count = 0
                            nurse_count = 0
                            player.deptaction = False
                            boosted = False
                            print(f"\n{breaker}The path is clear. You proceed to {current_room.name}...")
                        else:
                            return result
                else:
                    battle(player, current_room)
                    player.battles_fought += 1

            # -- Find a random item --
            else:
                options = [k for k, v in items.items() if v[2] == 'weapon' or v[2] == 'heal']
                item_name = random.choice(options)
                print(f"\nYou found a {item_name}: {items[item_name][0]} Worth {items[item_name][1]} Gold!")
                if item_name in ITEM_ART:
                    print(ITEM_ART[item_name])
                give_item(player, item_name)

        elif choice == 'L':
            if current_room.loot_count >= finds:
                print('\n [!] There is no more loot here!')
            else:
                print("\n--- Looting the room... ---")
                time.sleep(0.5)

                while current_room.loot_count < finds:
                    if player.dept == "Facilities Manager" and random.random() < (effects_data["Scavenger"][3]):
                        print("\n[PASSIVE] Scavenger: You found a way to loot without clearing the room!")
                    else:
                        current_room.loot_count += 1

                    loot_options = [name for name, data in items.items() if data[2] in current_room.loot_pool]

                    if loot_options:
                        item_name = random.choice(loot_options)
                        print(ITEM_ART[item_name])
                        give_item(player, item_name)
                        print(f"You found a {item_name}: {items[item_name][0]} Worth {items[item_name][1]} Gold!")
                        time.sleep(0.8)
                    else:
                        print("\n[!] No items found in the loot pool.")
                        break

                print("\n--- Room cleared! ---")

        elif choice == 'I':
            inventory(player, office_rooms)

        elif choice == 'S':
            display_stats(player)

        elif choice == 'Q':
            print("\nYou clock out early...")
            show_summary(player, "loss")
            break

    if not player.is_alive():
        print(f"{GAME_OVER}")
        show_summary(player, "loss")

    death = input("\nPress any key to exit or (R)estart: ").upper()
    return death == "R"

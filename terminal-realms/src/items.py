# Item and enemy data definitions

monster_names = [
    "Spreadsheet Spirit", "Paper Jam Poltergeist", "Menacing Microwave",
    "Fax Machine Phantom", "Cubicle Creeper", "HR Hellion", "Wi-Fi Witherer",
    "Deadline Demon", "Meeting Minotaur", "Corporate Vampire", "Voicemail Viper"
]

items = {
    # "Name": ["Description", Price, Type, StatValue]
    "Coffee Mug": ["There is still some left!", 1, 'item', 0],
    "Pile of Loose Change": ["A pile of coins", 10, 'item', 0],
    "Stick of Glue": ["The purple kind that (eventually) turns clear.", 1, 'item', 0],
    "Mystery Tupperware": ["Whatever is inside is now a sentient lifeform.", 1, 'item', 0],
    "Rubber Band": ["Very stretchy, but not very strong.", 1, 'item', 0],
    "Manilla Folder": ["Good for storing papers, not much else.", 1, 'item', 0],
    "Keyboard": ["It looks broken.", 1, 'item', 0],
    "Stress Ball": ["GRRRRR... You feel a little better after squeezing it.", 1, 'item', 0],
    "Sticky Note": ["It has directions to something.", 2, 'item', 0],

    "Key": ["A shiny silver key. It might fit a locked supply closet...", 5, 'key', 0],

    "Red Pen": ["Increases crit chance significantly.", 75, 'special', 15],              # +15% crit chance
    "Life Insurance": ["Prevents death once. Automatically used.", 100, 'special', 25],  # 25 HP on revive
    "Company Credit Card": ["Earn 1.5x gold from battles.", 100, 'special', 1.5],        # 1.5x multiplier

    "Stapler": ["Adds 1 damage.", 10, 'weapon', 1],
    "Umbrella": ["Adds 2 damage.", 15, 'weapon', 2],
    "Screwdriver": ["Adds 3 damage.", 25, 'weapon', 3],
    "Desk Lamp": ["Adds 4 damage.", 50, 'weapon', 4],

    "Old Shoes": ["Prevents 1 damage.", 10, 'armor', 1],
    "Hat": ["Prevents 1 damage.", 15, 'armor', 1],
    "Heavy Jacket": ["Prevents 2 damage.", 30, 'armor', 2],
    "Garbage Can Lid": ["Blocks 3 damage.", 40, 'armor', 3],

    "Plate of Leftovers": ["Restores 5 HP", 5, 'heal', 5],
    "Water Bottle": ["Restores 10 HP", 10, 'heal', 10],
    "Energy Drink": ["Restores 15 HP", 15, 'heal', 15],
    "PTO Voucher": ["A full recovery. Finally", 75, "heal", 0]
}

# "Name": ["Description", Duration, Type, StatValue]
effects_data = {
    # Attack
    "Jitters": ["Your hands are shaking. -2 attack damage.", 2, "atk", -2],
    "Overclocked": ["Caffeine overload! +5 attack damage.", 2, "atk", 5],
    "Greed": ["Your power is tied to your wallet. +1 Damage per 25 Gold held.", -1, "atk", 0],

    # Defense
    "Spin Doctor": ["25% chance to negate incoming damage and gain +5 HP.", -1, "def", 0.25],
    "Audit": ["Accounting is watching. 10% Gold loss per turn.", -1, "def", -0.1],
    "Resiliant": ["You've built up a thick skin. +1 Defense.", -1, "def", 1],

    # Utility
    "Revenue Siphon": ["Extract residual value from defeated competitors to restore your own vitality.", -1, "util", 0.75],
    "Guilt": ["Your reputation precedes you. Shops cost 50% more.", 2, "util", 1.5],
    "Scavenger": ["35% chance to loot without clearing the room.", -1, "util", 0.35],
    "Optimization": ["+50% healing from items.", -1, "util", 0.5]
}

# Boss stats: "Name": [HP, Max_Attack, Armor]
boss_stats = {
    "Security Guard": [25, 8, 0],
    "Microwave Chef": [40, 12, 1],
    "Middle Manager": [50, 15, 2],
    "IT Director": [60, 18, 3],
    "CEO": [75, 20, 4]
}

# Department actions: [Description, Cost, Heal, BonusKey]
dept_actions = {
    "Intern": ["Take a Power Nap to clear negative status effects (Jitters, Guilt, Audit).", 10, 10, "ClearHead"],
    "Data Analyst": ["Optimize your surroundings for a random heal and 40 immediate Gold.", 25, 5, "Profit"],
    "HR Manager": ["Grants +10 HP (Thick Skin).", 30, 5, "Resistance"],
    "Sales Exec": ["Charge a client lunch to the company card. Free heals but applies the 'Greed' effect.", 0, 20, "Greed"],
    "Corporate Lawyer": ["Grants the 'Overclocked' effect (+5 DMG) for 3 battles.", 40, 10, "Litigate"],
    "Facilities Manager": ["Finds 3 random items from the global item pool.", 25, 10, "Scavenge"],
    "PR Specialist": ["Converts your Gold spent into HP.", 0, 0, "SpinControl"],
    "PE Associate": ["Allows you to sell your junk online.", 10, 10, "RemoteSell"],
    "Wealth Manager": ["Generates 8% interest based on your current Gold balance.", 0, 5, "Dividends"],
    "Insurance Agent": ["Permanently increases Maximum HP by 5.", 25, 5, "Premium"],
    "IT Specialist": ["Permanently increases Min Attack by 1 and Max Attack by 1.", 30, 5, "HardwareMod"]
}


def give_item(player, item_name, equip=False):
    from src.player import Item
    # --- STACKING NERF ---
    if item_name == "Company Credit Card" and player.dept == "Wealth Manager":
        if any(i.name == "Company Credit Card" for i in player.inventory):
            print(f"\n[!] Security flagged your duplicate Credit Card! It was confiscated.")
            return

    d = items[item_name]
    new_item = Item(item_name, d[0], d[1], d[2], d[3])
    player.inventory.append(new_item)
    if equip:
        if new_item.itype == 'weapon': player.equipped_weapon = new_item
        if new_item.itype == 'armor': player.equipped_armor = new_item

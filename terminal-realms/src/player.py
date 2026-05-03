import random
from src.items import effects_data, boss_stats


class Item:
    def __init__(self, name, desc, value, itype, stat=0):
        self.name, self.desc, self.value, self.itype, self.stat = name, desc, value, itype, stat

    def __str__(self):
        return f"{self.name} ({self.itype}): {self.desc} | Value: {self.value} gold."


class Player:
    def __init__(self, name, hp=100, min_attack=1, max_attack=6, gold=0, dept="Unassigned"):
        self.name, self.dept = name, dept
        self.hp = self.max_hp = hp
        self.min_attack, self.max_attack, self.gold = min_attack, max_attack, gold
        self.inventory = []
        self.equipped_weapon = self.equipped_armor = None
        self.deptaction = False
        self.passive_slot = 0
        self.effects = {}  # { "Name": duration }

        # Trackers
        self.dept_actions_used = 0
        self.battles_fought = 0
        self.boss_battles_fought = 0
        self.promotions = 0

    def is_alive(self):
        return self.hp > 0

    def add_effect(self, name, duration):
        self.effects[name] = duration
        print(f"\n[STATUS] You gained the effect: {name}!")

    def tick_effects(self):
        # Internal Audit mechanic
        if self.gold >= 500:
            if "Audit" not in self.effects:
                print("\n[!] ALERT: Your high balance has triggered an Internal Audit!")
                self.add_effect("Audit", -1)

        if self.gold < 500 and "Audit" in self.effects:
            print("\n[STATUS] The auditors have lost interest in your accounts.")
            del self.effects["Audit"]

        if "Audit" in self.effects:
            tax = int(self.gold * 0.1)
            self.gold -= tax
            print(f"[AUDIT] The company 'reclaimed' {tax} gold in taxes and fines.")

        expired = [e for e, d in self.effects.items() if d > 0 and self.effects[e] - 1 == 0]
        for e in self.effects:
            if self.effects[e] > 0: self.effects[e] -= 1
        for e in expired:
            del self.effects[e]
            print(f"\n[STATUS] '{e}' has worn off.")

    def get_modified_attack(self):
        if "Greed" in self.effects:
            gold_damage = (2 + self.gold // 30)
            w_bonus = self.equipped_weapon.stat if self.equipped_weapon else 0
            total_dmg = gold_damage + w_bonus
            print(f"\n[GREED] Your wealth grants you {gold_damage} power!")
            return max(1, total_dmg)

        roll = random.randint(self.min_attack, self.max_attack)
        bonus = sum(effects_data[e][3] for e in self.effects if effects_data[e][2] == "atk")
        w_bonus = self.equipped_weapon.stat if self.equipped_weapon else 0
        p_bonus = self.passive_slot.stat if self.passive_slot else 0

        if bonus != 0: print(f"\n[EFFECTS] Modifying damage by {bonus}")
        return max(1, roll + bonus + w_bonus + p_bonus)

    def check_dodge(self):
        for e in self.effects:
            if e == "Spin Doctor" and random.random() < effects_data[e][3]:
                print(f"\n[!] PR Spin: You rebranded the hit! (0 Damage)")
                return True
        return False

    def consume_item(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                self.inventory.remove(item)
                return True
        return False

    @property
    def has_key(self):
        return next((i for i in self.inventory if i.name == "Key"), None)

    @property
    def has_insurance(self):
        return next((i for i in self.inventory if i.name == "Life Insurance"), None)

    @property
    def crit_chance_bonus(self):
        crit_chance = 0.1
        return (crit_chance + sum(i.stat for i in self.inventory if i.name == "Red Pen") / 100)


class Enemy:
    def __init__(self, name, level, player, is_boss=False):
        self.name, self.level = name, level
        self.is_boss = is_boss
        if name in boss_stats:
            stats = boss_stats[name]
            self.hp = stats[0]
            self.max_attack = stats[1]
            self.armor = stats[2]
        else:
            self.hp = random.randint(level * 5, level * 15)
            self.max_attack = level * 5
            self.armor = random.randint(0, level)

    def __str__(self):
        prefix = "BOSS:" if self.is_boss else f"Level {self.level}"
        return f"{prefix} {self.name}"


class Room:
    def __init__(self, name, monsters, loot_pool, max_level=2, loot_limit=4,
                 is_locked=False, required_item=None, required_code=None, boss_name=None):
        self.name, self.monsters, self.loot_pool = name, monsters, loot_pool
        self.max_level, self.loot_limit, self.loot_count = max_level, loot_limit, 0
        self.is_locked, self.required_item, self.required_code = is_locked, required_item, required_code

        self.boss_name = boss_name
        self.boss_defeated = False if boss_name else True

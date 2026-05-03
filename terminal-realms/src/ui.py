import time

# ASCII Art
LOGO = r"""
  _____ ___ ___ __  __ ___ _  _   _   _       ___ ___   _   _    __  __ ___ 
 |_   _| __| _ \  \/  |_ _| \| | /_\ | |     | _ \ __| /_\ | |  |  \/  / __|
   | | | _||   / |\/| || || .` |/ _ \| |__   |   / _| / _ \| |__| |\/| \__ \
   |_| |___|_|_\_|  |_|___|_|\_/_/ \_\_____| |_|_\___/_/ \_\______|  |_|_|_/
"""

MONSTER_ART = {
    "Spreadsheet Spirit": r"""
      _________________
     |  _  |_  |_  |_  |
     | |_| |_| |_| |_| |
     |  _  |_  |_  |_  |
     | |_| |_| |_| |_| |
     |_________________|
       (  O  ) (  O  )
        \           /
         \  VVVVV  /
    """,
    "Paper Jam Poltergeist": r"""
         _______
        /      /|
       /\__/__/ |
      |(x)(x)|  |
      |  JAM | /
      |______|/
     /  /  /  /
    /  /  /  / 
    """,
    "Menacing Microwave": r"""
      _________________
     |      |  |  |    |
     |  (o) |  |  |    |
     |______|__|__|____|
      \  \  \  /  /  /
       \  *BOOM*   /
        \________/
    """,
    "Fax Machine Phantom": r"""
       _________
      |   ---   |
      |_________|
      |   \  /  |
      | [][][][]|
      |_________|
     /  /  /  / 
    |________|  
    """,
    "Cubicle Creeper": r"""
      _________________
     |                 |
     |   (o)     (o)   |
     |        ^        |
     |      \___/      |
     |_________________|
     /                 \
    """,
    "HR Hellion": r"""
       ________
      |  CLIP  |
      | BOARD  |
      |  [ ]   |
      |  [ ]   |
      |________|
          ||
        --()--  
          ||
    """,
    "Wi-Fi Witherer": r"""
          *
         ***
        *****
      ***(!)***
    (NO SIGNAL...)
    """,
    "Deadline Demon": r"""
          
          /\      /\
         .--- \/ ---.   
        /   \    /   \    
       |   (X)  (X)   |  
       |      /\      | 
        \    /  \    /    ___
         \  '----'  /    | |_|
          '--IIII--'     '---'
         _ /IIIIII\ _     /
        /  \IIIIII/  \   /
       /    \____/    \_/ 
      /      /  \      \
     (______/    \______)
    """,
    "Meeting Minotaur": r"""
     /\                /\
     \ \____======____/ /
      \___          ___/
         |  o\  /o  |
         |  [ () ]  |
         \____--____/
       ______|  |______
      /      |\/|      \
     /  /| = ||||   |\  \
    /  / |   ||||   | \  \
    \  \ |   ||||   | /  /
     \  \|   |\/|   |/  /  
    """,
    "Corporate Vampire": r"""
                 ________
               /          \
              /   \   /    \
             /     \ /      \
           /\|              |/\
          | | \ ==\    /== / | |
           \|   <|>    <|>   |/     
    |\      |    -   \  -    |     /|
    \ \     |        |       |    / / 
     \  \   |       \|      |   /  /  
      \   \  |   _______   |  /   /    
       \    \ | / \/ \/ \ | /    /   
        |      \|        |       |
        |        \______/        |
        |         \    /         | 
        |          \  /          |
       /            \|            \
        """,
    "Voicemail Viper": r"""          
         _________
        /   \   / \
        |  O    O |
        | / v---v |  
        | L___________\/  
      / \_________/
     /    / 
    /   /                                            _     _      
    |  |                                            [ L___I ]
    |  |      ____           ________              |   ...   |
    |  |   __/ __ \__       / _____  \__     ______|   :::   |  
    |  |__/ __/  \__ \_____/ /     \___ \___/ _____    '''   |
    \______/        \_______/          \_____/     '========='

    """
}

ITEM_ART = {
    "Key": r"""
     __
    /o \_______
    \__/-="="`-\
    """,
    "Coffee Mug": r"""
     ___________
    [___________] ___
    |           |/   \
    |           |\___/
     \_________/    
    """,
    "Pile of Loose Change": r"""
     _____
    /  $  \
   |-------|____
   |-------| $  \
   |-------|-----|
   |_______|_____|
    """,
    "Sticky Note": r"""
     ___________________
    |       ~~~~        |
    |  ~~~~~     ~~~~~  |
    |  ~~~~~~~~~~~ ~    |
    |                   |
    |      ~~~~~        |
    |___________________|
    """,
    "Stick of Glue": r"""
     _____
    |     |
    |-----|
    |     |
    | GLUE|
    |     |
    |_____|
    """,   
    "Mystery Tupperware": r"""
      _________________
    /___________________\ 
    |___________________|
     \         _oo     /
      \       /       /
       \  \wx/       /
        \___________/
    """,
    "Rubber Band": r"""
        _________________
     .-'  _____________  '-.
    /  .-'             '-.  \
    \  '_________________'  /
     '-._________________.-'
    """,
    "Manilla Folder": r"""
     __________
    |   _______|________________________
    |  |                                |
    |  |                                |
    |  |                                |
    |  |                                |
    |  |                                |
    |__________________________________/
    """,
    "Keyboard": r"""
     _________________________________________
    /_________________________________________\
    | [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ] |
    | [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ] |
    | [  ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][   ] |
    | [   ][ ][ ][ ][ ][ ][ ][ ][ ][ ][     ] |
    | [ ][ ][      Spacebar     ][ ][ ][ ][ ] |
    \____________________________________ ____/
    """,
    "Stress Ball": r"""
          .-----------.
       .-'             '-.
      /      _______      \
     |     /         \     |
     |    |  SQUISH!  |    |
     |     \_________/     |
      \                   /
       '-._____________.-'
    """,
    "Red Pen": r"""
     __
    (__)
    |  |\
    |  ||
    |__||
    |  |
    |  |
    |  |
    |__|
    \||/
     \/
    """,
    "Life Insurance": r"""
                 ______
            _-.-"      "-.-_      |
       +   ( /____________\ )   --+--  
            |              |      |
            |,  .-.  .-.  ,|      |
            | )(__/  \__)( | 
      |     |/     /\     \|
    --+--   (_     ^^     _)
      |      \__|IIIIII|__/  +
      |       | \IIIIII/ |
           +  \          /      +
               `--------`
    """,
    "Company Credit Card": r"""
     ___________________
    |___________________|
    |  ~~~~~     ~~~~~  |
    |  ~~~~~~~~~~~ ~    |
    |                   |
    |      ~~~~~        |
    |___________________|
    """,
    "Stapler": r"""
       ______________________
      /                      \
     /________________________\
    |____________________/  /___
    |___________________________|

    """,
    "Umbrella": r"""
       __________   
      /          \   
     /____________\   
           |        
           |
           |
        \__/
    """,
    "Screwdriver": r"""
        __________
       /====\=\===\============|[]
       \__________/            
    """,
    "Desk Lamp": r"""
          _____
         /     \
        /_______\
           | |    
           | | 
           | |    
           | |
         __|_|__
    """,
    "Old Shoes": r"""
          __________    __________
         /==========\  /==========\
    ____/            \/            \
   /                  \             \
  |____________________|_____________|
  |_|                |_|           |_|
    """,
    "Hat": r"""
       ___________
      |           |
      |           |
      |           |
      |___________|
   ___|___________|___
  |___________________|
    """,
    "Heavy Jacket": r"""
            _______
          /   ___   \
         |   (   )   |
      ___|____\_/____|___
     /   \           /   \
    /  |  \         /  |  \
   /   |   \_______/   |   \
  |    |     |   |     |    |
  |    |     |   |     |    |
  |    |     |   |     |    |
  |    |     |   |     |    |
  |____|_____|___|_____|____|
    """,
    "Garbage Can Lid": r"""
             _____
          .-'     '-.
         /     _     \
        |    _(O)_    |
         \  (_ _ _)  /
          '-._____.-'
    """,
    "Plate of Leftovers": r"""
           _________________
        .-'      _____      '-.
      /   __|_  /     \  .-.   \
     /   /    \ |     | ( o )   \
    |    \____/ \_____/  '-'     |
    |     ____            ___    |
     \   /    \          /   \  /
      \  \____/          \___/ /
       '-._________________.-'
       """,
    "Water Bottle": r"""
          _____
         |_____|
         /     \
        |       |
        |-------|
        |~~~~~~~|
        |~~~~~~~|
        |-------|
        |       |
        |_______|
    """,
    "Energy Drink": r"""
         ___==__
        |       |
        |-------|
        |/\/\/\/|
        |/\/\/\/|
        |-------|
        |       |
        |_______|
    """,
    "PTO Voucher": r"""
     ___________
    |  ~  ~  ~  |
    |   PAID    |
    |    TIME   |
    |   OFF     |
    |___________|
    | x MANAGER |
    |___________|
    """
}

VENDOR_ART = r"""
               ___
           ___/___\___
             _|___|_
      o_____/ o_____\
      | x w x|       |
      |   x  |       |      _______
      |_0___V|_______|      |     |
             /     \        |=====|
           _|       |_      |_____|
    """

NURSE_ART = r"""
               ___
              /_+_\
             _|___|_
      o_____/ o_____\
      | + t +|       |         _
      |   +  |       |      __|_|__
      |_t___+|_______|      |  +  |
              |    |        |=====|
             _|    |_       [|   |]
    """

BOSS_ART = {
    "Security Guard": r"""
          __________
         /  _    _  \ 
         |  o    o  |
         |   ____   |
         \__|_--_|__/
       ______|  |______
      /       .|       \
     /  /| __ .|    |\  \
    /  / | \/ .|    | \  \
    \  \ |    .|    | /  /
     \  \|    .|    |/  /
""",
    "Microwave Chef": r"""
             __________
            /  \    /  \ 
            |  o    o  |
            |  }----{  |
            \__________/
     ___________|__|__________
    |   _____________         |
   _|  |             | [][][] |_
  [_|  |             | [][][] |_]
    |  |_____________| [][][] |
    |_________________________|
""",
    "Middle Manager": r"""
          _........_
         /  _    _  \ 
         |  o    o  |
         |   ____   |
         \____--____/
       ______|  |______
      /      |\/|      \
     /  /| - ||||   |\  \
    /  / |   ||||   | \  \
    \  \ |   ||||   | /  /
     \  \|   |\/|   |/  /
""",
    "IT Director": r"""
          __________
         /  n    _  \ 
         |-[o]==[o]-|
         |     __   |
         \__________/
       _____|    |_____
      /       \/       \
     /  /|    ||    |\  \
    /  / |    ||    | \  \
    \  \ |    ||    | /  /
     \  \|    \/    |/  /
"""
}

CEO_ART = r"""        
              _________
           .-"         "-.
           /   \     /   \
          |   (O)   (O)   |
          |       ^       | 
           \    -----    /
            '-._______.-'
          ______| _ |______
         /      |\_/|      \
        /  /| _ || ||   |\  \
       /  / |   || ||   | \  \
      /  /  |   || ||   |  \  \
     |_/    |   |\_/|   |    \_|
            |___|___|___|
            |   |   |   |
            |   |   |   |
            |___|   |___|
            (   )   (   )
             \ /     \ /
              V       V
    """

WIN_LOGO = r"""
 __     ______  _    _  __          _______ _   _ _ 
 \ \   / / __ \| |  | | \ \        / /_   _| \ | | |
  \ \_/ / |  | | |  | |  \ \  /\  / /  | | |  \| | |
   \   /| |  | | |  | |   \ \/  \/ /   | | | . ` | |
    | | | |__| | |__| |    \  /\  /   _| |_| |\  |_|
    |_|  \____/ \____/      \/  \/   |_____|_| \_(_)

    YOU ESCAPED THE OFFICE. RETIREMENT STARTS NOW.
        """

GAME_OVER = r"""
     ____    _    __  __  _____    ___ __     _______ ____  
    / ___|  / \  |  \/  || ____|  / _ \\ \   / / ____|  _ \ 
   | |  _  / _ \ | |\/| ||  _|   | | | |\ \ / /|  _| | |_) |
   | |_| |/ ___ \| |  | || |___  | |_| | \ V / | |___|  _ < 
    \____/_/   \_\_|  |_||_____|  \___/   \_/  |_____|_| \_\

                    Your story ends here.
        """

breaker = '----------------------------------------------------------------------\n'


def show_summary(player, outcome):
    """Display a styled end-of-game summary screen."""
    from src.items import effects_data
    W = 70

    def box_line(text="", align="center", pad=1):
        inner = W - 2 * pad
        if align == "center":
            s = text.center(inner)
        elif align == "left":
            s = text.ljust(inner)
        else:
            s = text.rjust(inner)
        return f"║{' ' * pad}{s}{' ' * pad}║"

    def divider(char="─"):
        return f"╠{'═' * (W)}╣" if char == "═" else f"╟{'─' * (W)}╢"

    def section(title):
        lines = []
        lines.append(divider("─"))
        lines.append(box_line(f"[ {title} ]"))
        lines.append(divider("─"))
        return lines

    lines = []
    lines.append(f"╔{'═' * W}╗")

    if outcome == "win":
        lines.append(box_line("★  MISSION COMPLETE  ★"))
        lines.append(box_line("You escaped the office. Retirement starts now."))
    else:
        lines.append(box_line("✗  YOU HAVE BEEN TERMINATED  ✗"))
        lines.append(box_line("HR will mail your belongings in a cardboard box."))

    lines.append(f"╠{'═' * W}╣")
    lines.append(box_line())

    lines += section("EMPLOYEE RECORD")
    lines.append(box_line(f"Name       :  {player.name}", align="left"))
    lines.append(box_line(f"Department :  {player.dept}", align="left"))
    lines.append(box_line())

    lines += section("FINAL VITALS")
    hp_display = max(0, player.hp)
    hp_bar_filled = int((hp_display / player.max_hp) * 20) if player.max_hp > 0 else 0
    hp_bar = f"[{'█' * hp_bar_filled}{'░' * (20 - hp_bar_filled)}]"
    lines.append(box_line(f"HP         :  {hp_display} / {player.max_hp}  {hp_bar}", align="left"))
    lines.append(box_line())

    lines += section("COMBAT STATS")
    w_name = player.equipped_weapon.name if player.equipped_weapon else "Bare Hands"
    w_stat = player.equipped_weapon.stat if player.equipped_weapon else 0
    a_name = player.equipped_armor.name  if player.equipped_armor  else "No Armor"
    a_stat = player.equipped_armor.stat  if player.equipped_armor  else 0
    lines.append(box_line(f"ATK Range  :  {player.min_attack} – {player.max_attack}  (base)", align="left"))
    lines.append(box_line(f"Weapon     :  {w_name}  (+{w_stat} ATK)", align="left"))
    lines.append(box_line(f"Armor      :  {a_name}  ({a_stat} DEF)", align="left"))

    crit_pct = round(player.crit_chance_bonus * 100, 1)
    lines.append(box_line(f"Crit Chance:  {crit_pct}%", align="left"))
    lines.append(box_line())

    lines += section("TREASURY")
    gold_bar_filled = min(20, int(player.gold / 25))
    gold_bar = f"[{'$' * gold_bar_filled}{'·' * (20 - gold_bar_filled)}]"
    lines.append(box_line(f"Gold       :  {player.gold}  {gold_bar}", align="left"))
    lines.append(box_line())

    lines += section("CAREER MILESTONES")
    lines.append(box_line(f"Total Battles      :  {player.battles_fought}", align="left"))
    lines.append(box_line(f"Bosses Defeated    :  {player.boss_battles_fought}", align="left"))
    lines.append(box_line(f"Dept Actions Used  :  {player.dept_actions_used}", align="left"))
    lines.append(box_line(f"Promotions Received:  {player.promotions}", align="left"))
    lines.append(box_line())

    lines += section("INVENTORY")
    if player.inventory:
        for item in player.inventory:
            tag = ""
            if item == player.equipped_weapon or item == player.equipped_armor: tag = " [EQUIPPED]"
            lines.append(box_line(f"  • {item.name}{tag}", align="left"))
    else:
        lines.append(box_line("  (empty pockets)", align="left"))
    lines.append(box_line())

    if player.effects:
        lines += section("ACTIVE EFFECTS AT TIME OF EXIT")
        for effect, duration in player.effects.items():
            timer = "Permanent" if duration == -1 else f"{duration} battles"
            lines.append(box_line(f"  ! {effect}  ({timer})", align="left"))
        lines.append(box_line())

    lines.append(f"╠{'═' * W}╣")
    if outcome == "win":
        lines.append(box_line("Thanks for playing Terminal Realms!"))
    else:
        lines.append(box_line("Better luck next time. The office never sleeps."))
    lines.append(f"╚{'═' * W}╝")

    time.sleep(0.5)
    print()
    for line in lines:
        print(line)
        time.sleep(0.03)
    print()


def display_stats(player):
    from src.items import dept_actions, effects_data

    w_stat = player.equipped_weapon.stat if player.equipped_weapon else 0
    p_stat = player.passive_slot.stat if player.passive_slot else 0
    a_stat = player.equipped_armor.stat if player.equipped_armor else 0
    w_stat += p_stat

    pens = [i for i in player.inventory if i.name == "Red Pen"]
    crit_boost = sum(p.stat for p in pens)

    cards = [i for i in player.inventory if i.name == "Company Credit Card"]
    multiplier = 0.0
    if cards:    
        for card in cards:
            multiplier += card.stat

    w_label = f"({player.equipped_weapon.name})" if player.equipped_weapon else ""
    a_label = f"({player.equipped_armor.name})" if player.equipped_armor else ""

    print(f"\n  --- CORPORATE PROFILE: {player.name.upper()} ---")
    print(f"Department: {player.dept}\n")

    dept_descriptions = {
        "Intern": "The Intern has high energy (Attack) but is incredibly fragile. They haven't been \n'beaten down' by the corporate world ... yet",
        "IT Specialist": "The IT Specialist knows the 'back-end' of the office. They aren't the strongest, \nbut they start with the tools needed to bypass locks and find secrets.",
        "PE Associate": "Private Equity Associate specializes in acquiring distressed assets and extracting \nmaximum value. Growth comes from the downfall of others.",
        "HR Manager": "The HR Manager is used to conflict and has high 'emotional resilience' (HP). They \nstart with a defensive passive to outlast monsters rather than overpowering them.",
        "Sales Exec": "The Sales Executive is all about the bottom line. They aren't great at fighting, \nbut they start with the capital to buy their way to the top.",
        "Corporate Lawyer": "Legal is all about finding the small mistakes that cause big problems. They have \nvery low base attack but start with the tools to deal massive 'critical' damage.",
        "Facilities Manager": "Instead of just fighting, this class interacts with the office environment itself. \nThey are sturdy and know where the 'good stuff' is hidden.",
        "PR Specialist": "The PR Specialist is all about image. They aren't great at direct combat, but they \nare incredibly lucky and can 'spin' bad situations into good ones.",
        "Data Analyst": "The Data Analyst excels at efficiency. They use their inventory better than anyone \nelse, making their consumables go further.",
        "Wealth Manager": "The Wealth Manager's combat effectiveness is tied directly to their personal wealth.\nThey deal 0 base damage, but gain power by hoarding gold.",
        "Insurance Agent": "The Insurance Agent knows that failure is inevitable, so they've planned for it. \nThey have a Life Insurance policy that brings them back with bonus HP and ATK.",
    }
    if player.dept in dept_descriptions:
        print(dept_descriptions[player.dept])

    print(f"\n  --- DEPARTMENT SPECIAL ABILITY ---")
    print(f"Action:  {dept_actions[player.dept][0]}")
    print(f"Cost:    {dept_actions[player.dept][1]} Gold")
    print(f"Healing: +{dept_actions[player.dept][2]} HP")

    print(f"\nVITALITY: {player.hp}/{player.max_hp} HP")
    print(f"OFFENSE:  {player.min_attack}/{player.max_attack} ATK {w_label} (+{w_stat} DMG)")
    if player.dept == "HR Manager":
        print(f"DEFENSE:  {a_stat + 1} DEF {a_label} (Resiliant passive)")
    else:
        print(f"DEFENSE:  {a_stat} DEF {a_label}")
    print(f"CAPITAL:  {player.gold} Gold")

    is_facilities = (player.dept == "Facilities Manager")
    is_pr = (player.dept == "PR Specialist")
    is_data = (player.dept == "Data Analyst")

    if not(crit_boost == 0 and multiplier == 0.0 and not player.has_insurance and not is_facilities):
        print(f"\n  --- ACTIVE BENEFITS ---")
        if crit_boost > 0:
            print(f"[+] Red Pen: +{crit_boost}% Critical Hit Chance")
        if multiplier > 1.0:
            print(f"[+] Corporate Perks: {multiplier}x Gold Multiplier")
        if player.has_insurance:
            print(f"[+] Safety Net: Life Insurance Policy Active")
        if is_facilities:
            print(f"[+] 35% chance to find extra loot.")
        if is_pr:
            print(f"[+] 20% chance to avoid damage entirely.")
        if is_data:
            print(f"[+] 50% more effective healing items.")

    if player.effects:
        print(f"\n  --- ACTIVE EFFECTS ---")
        for effect, duration in player.effects.items():
            desc = effects_data[effect][0]
            timer = "Permanent" if duration == -1 else f"{duration} battles left"
            print(f"[!] {effect}: {desc} ({timer})")

    input("\nPress Enter to return to work...")

import sys
from cli import Colors

def interactive_inventory(player):
    """交互式背包系统"""
    while True:
        print("\n" + "="*20 + " 背包 " + "="*20)
        if not player.inventory:
            print("空空如也")
            print("="*46)
            print("输入 'q' 退出背包")
            ans = input("> ")
            return

        usable_items = []
        for item, count in player.inventory.items():
            print(f"- {item}: {count}")
            if item in ["矿泉水", "巧克力", "饼干", "绷带", "急救包", "高级矿泉水", "高能量棒", "熟肉"]:
                usable_items.append(item)

        print("="*46)
        print("请输入要使用的物品名称（如 '矿泉水'），或输入 'q' 退出")
        ans = input("> ").strip()

        if ans.lower() == 'q':
            return

        if ans in player.inventory and ans in usable_items:
            player.remove_item(ans, 1)
            print(f"\n你使用了 {ans}。")
            if ans == "矿泉水":
                player.update_stats(hydration=30)
            elif ans == "高级矿泉水":
                player.update_stats(hydration=50)
            elif ans in ["巧克力", "饼干"]:
                player.update_stats(satiety=20)
            elif ans == "高能量棒":
                player.update_stats(satiety=40)
            elif ans == "熟肉":
                player.update_stats(satiety=50, hp=10)
            elif ans == "绷带":
                # 改为持续恢复
                player.healing_buffer += 20
                print(f"{Colors.OKGREEN}绷带已包扎，接下来的一段时间内生命值会缓慢恢复。{Colors.ENDC}")
            elif ans == "急救包":
                player.healing_buffer += 50
                print(f"{Colors.OKGREEN}急救包已使用，接下来的一段时间内生命值会大幅缓慢恢复。{Colors.ENDC}")

            # Print updated stats, rounded to nearest integer
            hp_disp = round(player.hp)
            hyd_disp = round(player.hydration)
            sat_disp = round(player.satiety)
            print(f"当前状态 -> 生命:{hp_disp} | 水分:{hyd_disp} | 饱食:{sat_disp}")
        elif ans in player.inventory:
            print(f"\n[{ans}] 无法直接使用。")
        else:
            print("\n背包里没有这个物品，或者输入有误。")

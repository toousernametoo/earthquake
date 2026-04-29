from cli import prompt_with_timeout, display_hud, clear_screen, Colors
import time
import random

class GameEngine:
    def __init__(self, player, time_system):
        self.player = player
        self.time = time_system
        self.running = True
        self.city_map = None

    def process_idle(self, context="normal"):
        if self.time.phase == "quake":
            print(f"\n{Colors.WARNING}你被地动山摇吓傻了，呆立在原地！{Colors.ENDC}")
            self.time.add_seconds(15, self.player)
            damage = random.randint(10, 20)
            print(f"{Colors.FAIL}摇晃导致重物坠落砸中了你！(HP -{damage}){Colors.ENDC}")
            self.player.update_stats(hp=-damage)
            self.pause_and_continue()
            return

        if context == "hazard":
            print(f"\n{Colors.WARNING}你被眼前的灾难吓呆了，没能及时做出反应！{Colors.ENDC}")
            self.time.add_minutes(5, self.player)
            damage = random.randint(15, 30)
            print(f"{Colors.FAIL}周围的乱石/碎片击中了你！(HP -{damage}){Colors.ENDC}")
            self.player.update_stats(hp=-damage)
        elif context == "combat":
            print(f"\n{Colors.WARNING}你在对峙中犹豫了，对方抓住了破绽！{Colors.ENDC}")
            self.time.add_minutes(2, self.player)
            damage = random.randint(10, 20)
            print(f"{Colors.FAIL}你遭到了猛烈的攻击！(HP -{damage}){Colors.ENDC}")
            self.player.update_stats(hp=-damage)
        elif context == "decision":
            print("\n因为恐惧和犹豫，你呆立在原地，浪费了宝贵的时间...")
            self.time.add_minutes(15, self.player)
            self.player.update_stats(hydration=-2, satiety=-2)
        else:
            print("\n你无所事事地发呆了一会儿...")
            self.time.add_minutes(10, self.player)

        self.pause_and_continue()

    def trigger_event(self, event_func):
        clear_screen()
        display_hud(self.player, self.time)
        return event_func(self)

    def game_over(self, reason):
        print("\n" + "=" * 50)
        print(f"{Colors.FAIL}【游戏结束】{Colors.ENDC}")
        print(f"死因: {reason}")
        print("=" * 50)
        self.running = False

    def victory(self, message):
        print("\n" + "=" * 50)
        print(f"{Colors.OKGREEN}【逃出生天】{Colors.ENDC}")
        print(message)
        print("=" * 50)
        self.running = False

    def check_status(self):
        p = self.player

        # 处理持续恢复 (HoT)
        if p.healing_buffer > 0 and p.hp < 100:
            heal_amount = random.randint(1, 3)
            # 如果加上恢复量超过了剩余缓冲，或者超过了满血
            heal_amount = min(heal_amount, p.healing_buffer, 100 - p.hp)
            if heal_amount > 0:
                p.update_stats(hp=heal_amount)
                p.healing_buffer -= heal_amount
                print(f"\n{Colors.OKGREEN}[系统] 医药用品生效，生命值恢复了 {heal_amount} 点。{Colors.ENDC}")
                if p.healing_buffer <= 0 or p.hp >= 100:
                    p.healing_buffer = 0
                    print(f"{Colors.OKGREEN}[系统] 伤口已经处理完毕，停止持续恢复。{Colors.ENDC}")

        if p.hydration <= 0:
            p.debuffs.add("脱水")
            p.update_stats(hp=-10)
            print(f"\n{Colors.FAIL}【警告】你极度脱水，生命值正在流失！{Colors.ENDC}")
        else:
            if "脱水" in p.debuffs: p.debuffs.remove("脱水")

        if p.satiety <= 0:
            p.debuffs.add("饥饿")
            p.update_stats(hp=-5)
            print(f"\n{Colors.FAIL}【警告】你极度饥饿，身体变得虚弱，生命值开始下降！{Colors.ENDC}")
        else:
            if "饥饿" in p.debuffs: p.debuffs.remove("饥饿")

        if p.hp <= 0:
            self.game_over("伤重不治或身体机能耗尽...")
            return False

        # Low Status Warning
        if p.hp < 30 or p.hydration < 30 or p.satiety < 30:
            print(f"\n{Colors.WARNING}{Colors.BOLD}[系统建议] 你的状态非常差，请立刻输入 'inv' 打开背包使用物资补充状态！{Colors.ENDC}")

        return True

    def pause_and_continue(self):
        print("\n(按回车键继续...)")
        try:
            input()
        except EOFError:
            pass

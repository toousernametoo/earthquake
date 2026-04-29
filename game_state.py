from cli import Colors

ITEM_WEIGHTS = {
    "消防斧": 4.0,
    "矿泉水": 0.5,
    "高级矿泉水": 0.5,
    "巧克力": 0.1,
    "饼干": 0.1,
    "高能量棒": 0.1,
    "熟肉": 0.3,
    "绷带": 0.1,
    "急救包": 1.0,
    "手电筒": 0.3,
    "打火机": 0.1,
}

class Player:
    def __init__(self, name="林锐", difficulty="easy"):
        self.name = name
        self.hp = 100.0
        self.hydration = 70.0
        self.satiety = 60.0
        self.inventory = {}
        self.floor = 25
        self.debuffs = set()
        self.companion = None
        self.difficulty = difficulty
        self.healing_buffer = 0

    def get_weight(self):
        w = 0.0
        for item, count in self.inventory.items():
            w += ITEM_WEIGHTS.get(item, 0.5) * count
        return w

    def update_stats(self, hp=0, hydration=0, satiety=0):
        # 困难模式下，正向恢复效果降低 30%
        if self.difficulty == "hard":
            if hp > 0: hp = hp * 0.7
            if hydration > 0: hydration = hydration * 0.7
            if satiety > 0: satiety = satiety * 0.7

        self.hp = max(0.0, min(100.0, self.hp + hp))
        self.hydration = max(0.0, min(100.0, self.hydration + hydration))
        self.satiety = max(0.0, min(100.0, self.satiety + satiety))

    def add_item(self, item, count=1):
        # 困难模式下，如果获得多个物品，数量减1（最低给1个）
        if self.difficulty == "hard" and count > 1:
            count -= 1

        if item in self.inventory:
            self.inventory[item] += count
        else:
            self.inventory[item] = count

    def remove_item(self, item, count=1):
        if item in self.inventory:
            if self.inventory[item] >= count:
                self.inventory[item] -= count
                if self.inventory[item] == 0:
                    del self.inventory[item]
                return True
        return False

    def is_dead(self):
        return self.hp <= 0

    def print_status(self):
        hp_disp = round(self.hp)
        hyd_disp = round(self.hydration)
        sat_disp = round(self.satiety)

        print(f"\n--- 玩家状态 ---")
        print(f"姓名: {self.name} | 当前楼层: {self.floor}层")
        print(f"生命: {hp_disp}/100 | 水分: {hyd_disp}/100 | 饱食度: {sat_disp}/100")
        print(f"负重: {self.get_weight():.1f} kg")
        if self.debuffs:
            print(f"{Colors.FAIL}状态异常: {', '.join(self.debuffs)}{Colors.ENDC}")
        if self.companion:
            print(f"{Colors.OKGREEN}同行同伴: {self.companion} (分担体力消耗){Colors.ENDC}")
        if self.healing_buffer > 0:
            print(f"{Colors.OKGREEN}正在缓慢恢复生命值... (剩余恢复量: {self.healing_buffer} HP){Colors.ENDC}")
        print("-" * 16)

class TimeSystem:
    def __init__(self):
        self.day = 1
        self.hour = 21
        self.minute = 30
        self.second = 0
        self.phase = "quake"

    def add_seconds(self, seconds, player):
        self.second += seconds
        while self.second >= 60:
            self.second -= 60
            self.add_minutes(1, player, is_quake=True)

    def add_minutes(self, minutes, player, is_quake=False):
        self.minute += minutes
        while self.minute >= 60:
            self.minute -= 60
            self.hour += 1
        while self.hour >= 24:
            self.hour -= 24
            self.day += 1

        if not is_quake:
            # 基础下降
            base_hyd = (20.0 / 60.0) * minutes
            base_sat = (15.0 / 60.0) * minutes

            # 负重惩罚：每1kg增加10%的消耗速度
            weight = player.get_weight()
            multiplier = 1.0 + (weight * 0.1)

            player.update_stats(hydration=-(base_hyd * multiplier), satiety=-(base_sat * multiplier))

    def get_time_string(self):
        if self.phase == "quake":
            return f"Day {self.day} - {self.hour:02d}:{self.minute:02d}:{self.second:02d} (主震中)"
        else:
            return f"Day {self.day} - {self.hour:02d}:{self.minute:02d} (生存中)"

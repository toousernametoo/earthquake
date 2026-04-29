from game_state import Player, TimeSystem
from engine import GameEngine
from cli import prompt_with_timeout, clear_screen, Colors
from map_backend import CityMapBackend
from main_quake_events import play_main_quake
import events_pool
import random

def start_chapter1(difficulty="easy"):
    print("正在生成苍海市地图并演算地震影响，请稍候...")
    city_backend = CityMapBackend()

    player = Player(difficulty=difficulty)
    time_sys = TimeSystem()
    engine = GameEngine(player, time_sys)
    engine.city_map = city_backend

    clear_screen()
    print("\n" + "="*50)
    print("【第一章：陨落的巴别塔】")
    print("星寰中心")
    if difficulty == "hard":
        print(f"{Colors.WARNING}[困难模式已开启：物资获取减少，状态回复降低]{Colors.ENDC}")
    print("="*50)
    print("\n这本该是一个再普通不过的周五夜晚...")
    engine.pause_and_continue()

    # 1. 主震阶段
    play_main_quake(engine)

    # 初始化楼梯保底计数器
    engine.stairs_attempts = 0
    engine.current_floor_tracker = player.floor

    # 2. 生存逃生阶段
    while engine.running:
        if not engine.check_status():
            break

        if player.floor <= 1:
            collapsed_count = sum(1 for b in engine.city_map.buildings if b.get('collapsed'))
            total_buildings = len(engine.city_map.buildings)

            msg = f"你冲出了摇摇欲坠的大楼，呼吸到了外面的空气。\n然而，眼前是一座彻底瘫痪的废墟之城...\n"
            msg += f"(放眼望去，城市中 {total_buildings} 栋主要建筑中，有 {collapsed_count} 栋已经化为废墟。)"

            engine.victory(msg)
            break

        # 如果下楼了，重置楼梯保底
        if player.floor != engine.current_floor_tracker:
            engine.stairs_attempts = 0
            engine.current_floor_tracker = player.floor

        engine.trigger_event(floor_decision_node)

def floor_decision_node(engine):
    p = engine.player

    # 35% probability of a random event triggering immediately when trying to make a choice
    if random.random() < 0.35:
        event_func = events_pool.get_random_event(engine)
        event_func(engine)
        return

    desc = f"\n你当前在 {p.floor} 层。\n周围一片漆黑。远处不时传来微弱的结构断裂声。"
    choices = "1. 在这一层仔细探索 (耗时，触发随机事件)\n2. 寻找楼梯往下走"

    ans = prompt_with_timeout(choices, p, description_text=desc)

    if ans == "1":
        event_func = events_pool.get_random_event(engine)
        event_func(engine)
    elif ans == "2":
        search_for_stairs_wrapper(engine)
    elif ans is None:
        engine.process_idle(context="decision")
    else:
        print(f"\n{Colors.WARNING}无效的选择。{Colors.ENDC}")
        engine.pause_and_continue()

def search_for_stairs_wrapper(engine):
    p = engine.player
    t = engine.time

    print("\n你摸索着寻找紧急楼梯...")
    t.add_minutes(5, p)

    # 寻找楼梯过程中，概率触发事件 (最多3次后找到)
    if random.random() < 0.4:
        print(f"\n{Colors.WARNING}通往楼梯间的路上遇到了状况...{Colors.ENDC}")
        engine.pause_and_continue()
        event_func = events_pool.get_random_event(engine)
        event_func(engine)
        return

    find_stairs_node(engine)

def find_stairs_node(engine):
    p = engine.player
    t = engine.time

    engine.stairs_attempts += 1

    # 保底机制：同楼层第3次找到楼梯时必定能走
    if engine.stairs_attempts >= 3:
        stair_state = 0.0
        print(f"\n{Colors.OKGREEN}(你花了很长时间，终于找到了一个确信可以通过的楼梯间！){Colors.ENDC}")
    else:
        stair_state = random.random()

    if stair_state < 0.4:
        print("你找到了一个相对完好的楼梯间！")
        choices = "1. 开始下楼\n2. 放弃，回去探索本层"
        ans = prompt_with_timeout(choices, p)
        if ans == "1":
            descend_safe_stairs(engine)
        else:
            engine.pause_and_continue()

    elif stair_state < 0.7:
        print("你找到的这个楼梯间被巨大的天花板落石彻底封死了！根本无法通行。")
        choices = "1. 返回本层探索"
        ans = prompt_with_timeout(choices, p)
        # 无论选什么，只能返回探索
        engine.pause_and_continue()

    else:
        print("楼梯从中间完全断裂，下面漆黑一片。")
        choices = "1. 返回本层探索\n2. 寻找结实的长绳进行绳降 (危险)\n3. 寻找木板搭设简易桥板 (耗时)"
        ans = prompt_with_timeout(choices, p)

        if ans == "2":
            descend_rope(engine)
        elif ans == "3":
            descend_board(engine)
        else:
            # 包括选择 1 或超时
            engine.pause_and_continue()

def descend_safe_stairs(engine):
    p = engine.player
    t = engine.time

    floors_down = random.randint(1, 3)
    floors_down = min(floors_down, p.floor - 1) # Ensure we don't drop below floor 1

    t.add_minutes(floors_down * 5, p)
    print(f"\n{Colors.OKGREEN}你顺利地往下走了 {floors_down} 层。{Colors.ENDC}")
    p.floor -= floors_down
    if p.floor < 1: p.floor = 1
    print(f"你现在位于 {p.floor} 层。")
    engine.pause_and_continue()

def descend_rope(engine):
    p = engine.player
    t = engine.time
    print("\n你在废墟里翻找，花了些时间找到一捆结实的网线充当绳索...")
    t.add_minutes(15, p)
    p.update_stats(satiety=-10, hydration=-10)

    if random.random() < 0.3:
        print(f"\n{Colors.FAIL}绳索中途断裂！你狠狠摔到了下方楼层。{Colors.ENDC}")
        p.update_stats(hp=-20)
        drop = min(2, p.floor - 1)
        p.floor -= drop
    else:
        floors_down = random.randint(2, 4)
        floors_down = min(floors_down, p.floor - 1)
        print(f"\n{Colors.OKGREEN}你手心磨破了皮，但成功滑降了 {floors_down} 层！{Colors.ENDC}")
        p.update_stats(hp=-5)
        p.floor -= floors_down

    if p.floor < 1: p.floor = 1
    print(f"你现在位于 {p.floor} 层。")
    engine.pause_and_continue()

def descend_board(engine):
    p = engine.player
    t = engine.time
    print("\n你到处收集破碎的门板和桌板，耗费大量体力搭建了一座简易木桥...")
    t.add_minutes(25, p)
    p.update_stats(satiety=-20, hydration=-15)

    if random.random() < 0.15:
        print(f"\n{Colors.FAIL}咔嚓！木板根本承受不住你的重量，你直接坠落到了下一层！{Colors.ENDC}")
        p.update_stats(hp=-15)
        drop = min(2, p.floor - 1)
        p.floor -= drop
    else:
        print(f"\n{Colors.OKGREEN}木板虽然吱呀作响，但你安全地跨越了断崖，下到了一层。{Colors.ENDC}")
        drop = min(1, p.floor - 1)
        p.floor -= drop

    if p.floor < 1: p.floor = 1
    print(f"你现在位于 {p.floor} 层。")
    engine.pause_and_continue()

import random
from cli import prompt_with_timeout, Colors

def run_event(engine, title_desc, choices_dict, require_pause=True, event_type="normal"):
    choices_str = "\n".join([f"{k}. {v[0]}" for k, v in choices_dict.items()])
    while True:
        ans = prompt_with_timeout(choices_str, engine.player, description_text=title_desc)
        if ans is None:
            engine.process_idle(context=event_type)
            return
        if ans in choices_dict:
            choices_dict[ans][1](engine)
            break
        else:
            print("\n无效的选择，请重新输入。")
            import time
            time.sleep(1)
    if require_pause and engine.running:
        engine.pause_and_continue()

def ev_exploration_0(engine):
    desc = "【Exploration】自动贩卖机\n一台被承重墙卡住的贩卖机，里面有水和零食。"
    def opt1(e):
        print(f'\n你选择了: 暴力砸开')
        if random.random() < 0.3:
            print(f'{Colors.FAIL}突发状况：受伤(-10HP){Colors.ENDC}')
            e.player.update_stats(hp=-10)
        print(f'{Colors.OKGREEN}结果: 消耗体力(-10饱食),  获得水x2 巧克力x2{Colors.ENDC}')
        final_sat = -10
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
        e.player.add_item('矿泉水', 2)
        e.player.add_item('巧克力', 2)
    def opt2(e):
        print(f'\n你选择了: 用消防斧劈开')
        e.time.add_minutes(5, e.player)
        print(f'{Colors.OKGREEN}结果: 需要消防斧, 耗时5分, 获得水x3 巧克力x2 饼干x1{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('矿泉水', 3)
        e.player.add_item('巧克力', 2)
        e.player.add_item('饼干', 1)
        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:
            print(f'{Colors.WARNING}你没有消防斧，无法执行此操作！{Colors.ENDC}')
            return
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('暴力砸开', opt1),
        '2': ('用消防斧劈开', opt2),
        '3': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_1(engine):
    desc = "【Exploration】同事的遗物\n残破办公桌下的血迹背包。"
    def opt1(e):
        print(f'\n你选择了: 翻找背包')
        e.time.add_minutes(5, e.player)
        print(f'{Colors.OKGREEN}结果: 获得矿泉水x2 饼干x2, 耗时5分{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('矿泉水', 2)
        e.player.add_item('饼干', 2)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('翻找背包', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_2(engine):
    desc = "【Exploration】被锁的杂物间\n门被变形卡死。"
    def opt1(e):
        print(f'\n你选择了: 用力撞开')
        if random.random() < 0.7:
            print(f'{Colors.FAIL}突发状况：获得消防斧{Colors.ENDC}')
            e.player.update_stats(hp=0)
            e.player.add_item('消防斧', 1)
        print(f'{Colors.FAIL}结果: 消耗饱食(-15){Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=-5, satiety=final_sat, hydration=0)
    def opt2(e):
        print(f'\n你选择了: 用消防斧破门')
        e.time.add_minutes(5, e.player)
        print(f'{Colors.OKGREEN}结果: 需要消防斧, 耗时5分, 获得手电筒x1 绷带x2{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('绷带', 2)
        e.player.add_item('手电筒', 1)
        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:
            print(f'{Colors.WARNING}你没有消防斧，无法执行此操作！{Colors.ENDC}')
            return
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('用力撞开', opt1),
        '2': ('用消防斧破门', opt2),
        '3': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_3(engine):
    desc = "【Exploration】废弃的茶水间\n水管破裂滴水。"
    def opt1(e):
        print(f'\n你选择了: 接水喝')
        if random.random() < 0.4:
            print(f'{Colors.FAIL}突发状况：胃痉挛(-10HP){Colors.ENDC}')
            e.player.update_stats(hp=-10)
        print(f'结果: 水分+25')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=25)
    def opt2(e):
        print(f'\n你选择了: 仔细过滤')
        e.time.add_minutes(5, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时15分, 水分+20, 获得矿泉水x1{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=20)
        e.player.add_item('矿泉水', 1)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('接水喝', opt1),
        '2': ('仔细过滤', opt2),
        '3': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_4(engine):
    desc = "【Exploration】破碎的药箱\n墙角紧急医疗箱。"
    def opt1(e):
        print(f'\n你选择了: 翻找')
        e.time.add_minutes(5, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时5分, 获得绷带x2 急救包x1{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('绷带', 2)
        e.player.add_item('急救包', 1)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('翻找', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_5(engine):
    desc = "【Exploration】幸存者营地\n废纸火堆余温未散。"
    def opt1(e):
        print(f'\n你选择了: 搜刮遗留物资')
        e.time.add_minutes(10, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时10分, 获得熟肉x1 矿泉水x1{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('矿泉水', 1)
        e.player.add_item('熟肉', 1)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('搜刮遗留物资', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_6(engine):
    desc = "【Exploration】遗落的急救包\n走廊中间掉落的完好急救包。"
    def opt1(e):
        print(f'\n你选择了: 跑去捡起')
        if random.random() < 0.5:
            print(f'{Colors.FAIL}突发状况：遭遇天花板掉落(-15HP){Colors.ENDC}')
            e.player.update_stats(hp=-15)
        print(f'{Colors.OKGREEN}结果: 获得医疗箱x2 绷带x1{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('绷带', 1)
        e.player.add_item('急救包', 2)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('跑去捡起', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_7(engine):
    desc = "【Exploration】半开的保险柜\n墙壁破裂露出的保险柜。"
    def opt1(e):
        print(f'\n你选择了: 尝试徒手拉开')
        e.time.add_minutes(5, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时15分, 获得手电筒x1 巧克力x1, 饱食-5{Colors.ENDC}')
        final_sat = -5
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
        e.player.add_item('巧克力', 1)
        e.player.add_item('手电筒', 1)
    def opt2(e):
        print(f'\n你选择了: 用消防斧撬开')
        e.time.add_minutes(5, e.player)
        print(f'{Colors.OKGREEN}结果: 需要消防斧, 耗时5分, 获得高级矿泉水x2 高能量棒x2{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('矿泉水', 2)
        e.player.add_item('高级矿泉水', 2)
        e.player.add_item('高能量棒', 2)
        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:
            print(f'{Colors.WARNING}你没有消防斧，无法执行此操作！{Colors.ENDC}')
            return
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('尝试徒手拉开', opt1),
        '2': ('用消防斧撬开', opt2),
        '3': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_8(engine):
    desc = "【Exploration】员工休息区\n沙发被压扁，可能有吃的。"
    def opt1(e):
        print(f'\n你选择了: 翻找')
        e.time.add_minutes(5, e.player)
        if random.random() < 0.8:
            print(f'{Colors.FAIL}突发状况：获得高能量棒x2 饼干x1{Colors.ENDC}')
            e.player.update_stats(hp=0)
            e.player.add_item('高能量棒', 2)
        print(f'结果: 耗时15分,  饱食-5')
        final_sat = -5
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('翻找', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_9(engine):
    desc = "【Exploration】破碎的饮水机\n还有半桶水没流完。"
    def opt1(e):
        print(f'\n你选择了: 收集水')
        e.time.add_minutes(10, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时10分, 获得矿泉水x2{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('矿泉水', 2)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('收集水', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_10(engine):
    desc = "【Exploration】遗弃的手提箱\n走廊上一个高档手提箱。"
    def opt1(e):
        print(f'\n你选择了: 打开')
        e.time.add_minutes(5, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时5分, 获得高级矿泉水x1 巧克力x1{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('矿泉水', 1)
        e.player.add_item('巧克力', 1)
        e.player.add_item('高级矿泉水', 1)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('打开', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_11(engine):
    desc = "【Exploration】震碎的展示柜\n原本放公司纪念品的柜子，可能藏有应急物资。"
    def opt1(e):
        print(f'\n你选择了: 翻找')
        if random.random() < 0.2:
            print(f'{Colors.FAIL}突发状况：划伤(-5HP){Colors.ENDC}')
            e.player.update_stats(hp=-5)
        print(f'{Colors.OKGREEN}结果: 获得巧克力x2 水x1{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('巧克力', 2)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('翻找', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_12(engine):
    desc = "【Exploration】破损的通风管\n管内似乎有东西闪光。"
    def opt1(e):
        print(f'\n你选择了: 伸手摸')
        if random.random() < 0.1:
            print(f'{Colors.FAIL}突发状况：被老鼠咬(-5HP){Colors.ENDC}')
            e.player.update_stats(hp=-5)
        print(f'{Colors.OKGREEN}结果: 获得打火机x1 饼干x1{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('饼干', 1)
        e.player.add_item('打火机', 1)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('伸手摸', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_13(engine):
    desc = "【Exploration】高管办公室\n门半掩着。"
    def opt1(e):
        print(f'\n你选择了: 进去搜')
        e.time.add_minutes(20, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时20分, 获得高级矿泉水x2 熟肉x1, 饱食-5{Colors.ENDC}')
        final_sat = -5
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
        e.player.add_item('矿泉水', 2)
        e.player.add_item('高级矿泉水', 2)
        e.player.add_item('熟肉', 1)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('进去搜', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_14(engine):
    desc = "【Exploration】散落的外卖\n地上一份还没拆的震前外卖。"
    def opt1(e):
        print(f'\n你选择了: 吃掉')
        if random.random() < 0.4:
            print(f'{Colors.FAIL}突发状况：拉肚子(-10HP{Colors.ENDC}')
            e.player.update_stats(hp=-10)
        print(f'结果: 饱食+30,  状态下降)')
        final_sat = 30
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('吃掉', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_exploration_15(engine):
    desc = "【Exploration】震碎的库房\n库房大门敞开，里面似乎有很多包裹。"
    def opt1(e):
        print(f'\n你选择了: 仔细搜刮')
        e.time.add_minutes(30, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时30分, 饱食-10, 获得高级矿泉水x1 医疗箱x1 高能量棒x1{Colors.ENDC}')
        final_sat = -10
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
        e.player.add_item('矿泉水', 1)
        e.player.add_item('急救包', 1)
        e.player.add_item('高级矿泉水', 1)
        e.player.add_item('高能量棒', 1)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('仔细搜刮', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='normal')

def ev_hazards_0(engine):
    desc = "【Hazards】强烈余震\n大楼剧烈摇晃。"
    def opt1(e):
        print(f'\n你选择了: 躲承重墙角')
        e.time.add_minutes(5, e.player)
        print(f'{Colors.OKGREEN}结果: 安全, 耗时5分{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    def opt2(e):
        print(f'\n你选择了: 走廊中间')
        print(f'{Colors.FAIL}结果: 被砸中(-30HP){Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=-30, satiety=final_sat, hydration=0)
    run_event(engine, desc, {
        '1': ('躲承重墙角', opt1),
        '2': ('走廊中间', opt2),
    }, event_type='hazard')

def ev_hazards_1(engine):
    desc = "【Hazards】浓烟走廊\n前方起火黑烟弥漫。"
    def opt1(e):
        print(f'\n你选择了: 强行穿过')
        e.time.add_minutes(5, e.player)
        print(f'{Colors.FAIL}结果: 耗时5分, HP-15, 水分-20{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=-15, satiety=final_sat, hydration=-20)
    def opt2(e):
        print(f'\n你选择了: 花时间绕路')
        e.time.add_minutes(30, e.player)
        print(f'结果: 耗时30分, 饱食-10, 水分-10')
        final_sat = -10
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=-10)
    run_event(engine, desc, {
        '1': ('强行穿过', opt1),
        '2': ('花时间绕路', opt2),
    }, event_type='hazard')

def ev_hazards_2(engine):
    desc = "【Hazards】深渊陷阱\n走廊大面积塌陷。"
    def opt1(e):
        print(f'\n你选择了: 贴墙挪')
        e.time.add_minutes(5, e.player)
        if random.random() < 0.2:
            print(f'{Colors.FAIL}突发状况：跌落(-15HP){Colors.ENDC}')
            e.player.update_stats(hp=-15)
        print(f'结果: 耗时15分, 饱食-10')
        final_sat = -10
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
    def opt2(e):
        print(f'\n你选择了: 退回去绕路')
        e.time.add_minutes(5, e.player)
        print(f'结果: 耗时45分, 状态-15')
        final_sat = -15
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=-15)
    run_event(engine, desc, {
        '1': ('贴墙挪', opt1),
        '2': ('退回去绕路', opt2),
    }, event_type='hazard')

def ev_hazards_3(engine):
    desc = "【Hazards】天花板崩塌\n头顶钢筋崩裂声。"
    def opt1(e):
        print(f'\n你选择了: 往前扑')
        print(f'{Colors.OKGREEN}结果: 饱食-5, 安全躲过{Colors.ENDC}')
        final_sat = -5
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
    def opt2(e):
        print(f'\n你选择了: 抱头蹲下')
        print(f'{Colors.FAIL}结果: 被砸中肩部(-25HP){Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=-25, satiety=final_sat, hydration=0)
    run_event(engine, desc, {
        '1': ('往前扑', opt1),
        '2': ('抱头蹲下', opt2),
    }, event_type='hazard')

def ev_hazards_4(engine):
    desc = "【Hazards】毒气泄漏\n刺鼻气味弥漫。"
    def opt1(e):
        print(f'\n你选择了: 弯腰狂奔')
        print(f'{Colors.OKGREEN}结果: 水分-15, 安全{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=-15)
    def opt2(e):
        print(f'\n你选择了: 寻找来源')
        print(f'{Colors.FAIL}结果: 吸入毒气(-25HP){Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=-25, satiety=final_sat, hydration=0)
    run_event(engine, desc, {
        '1': ('弯腰狂奔', opt1),
        '2': ('寻找来源', opt2),
    }, event_type='hazard')

def ev_hazards_5(engine):
    desc = "【Hazards】绝对黑暗\n楼梯间毫无光线。"
    def opt1(e):
        print(f'\n你选择了: 使用手电筒')
        print(f'{Colors.OKGREEN}结果: 需要手电筒, 安全通过{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        if '手电筒' not in e.player.inventory or e.player.inventory['手电筒'] <= 0:
            print(f'{Colors.WARNING}你没有手电筒，无法执行此操作！{Colors.ENDC}')
            return
    def opt2(e):
        print(f'\n你选择了: 盲人摸象')
        e.time.add_minutes(5, e.player)
        if random.random() < 0.4:
            print(f'{Colors.FAIL}突发状况：踩空(-20HP){Colors.ENDC}')
            e.player.update_stats(hp=-20)
        print(f'结果: 耗时15分')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    run_event(engine, desc, {
        '1': ('使用手电筒', opt1),
        '2': ('盲人摸象', opt2),
    }, event_type='hazard')

def ev_hazards_6(engine):
    desc = "【Hazards】高空强风\n外墙碎裂，狂风卷玻璃。"
    def opt1(e):
        print(f'\n你选择了: 匍匐前进')
        print(f'{Colors.OKGREEN}结果: 饱食-5, 安全{Colors.ENDC}')
        final_sat = -5
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
    run_event(engine, desc, {
        '1': ('匍匐前进', opt1),
    }, event_type='hazard')

def ev_hazards_7(engine):
    desc = "【Hazards】漏电水洼\n地上的积水里有断裂电线闪火花。"
    def opt1(e):
        print(f'\n你选择了: 跳过去')
        if random.random() < 0.3:
            print(f'{Colors.FAIL}突发状况：踩水触电(-20HP){Colors.ENDC}')
            e.player.update_stats(hp=-20)
        print(f'结果: 消耗饱食-5')
        final_sat = -5
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
    def opt2(e):
        print(f'\n你选择了: 搬杂物垫脚')
        e.time.add_minutes(5, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时15分, 饱食-10, 安全{Colors.ENDC}')
        final_sat = -10
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
    run_event(engine, desc, {
        '1': ('跳过去', opt1),
        '2': ('搬杂物垫脚', opt2),
    }, event_type='hazard')

def ev_hazards_8(engine):
    desc = "【Hazards】倾斜楼板\n楼板倾斜近30度。"
    def opt1(e):
        print(f'\n你选择了: 顺势滑下')
        if random.random() < 0.2:
            print(f'{Colors.FAIL}突发状况：撞墙(-15HP){Colors.ENDC}')
            e.player.update_stats(hp=-15)
        print(f'结果: 快速通过')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    def opt2(e):
        print(f'\n你选择了: 往上爬回去')
        e.time.add_minutes(20, e.player)
        print(f'结果: 饱食-15, 耗时20分')
        final_sat = -15
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
    run_event(engine, desc, {
        '1': ('顺势滑下', opt1),
        '2': ('往上爬回去', opt2),
    }, event_type='hazard')

def ev_hazards_9(engine):
    desc = "【Hazards】悬挂的空调箱\n头顶巨大的中央空调摇摇欲坠。"
    def opt1(e):
        print(f'\n你选择了: 快速跑过')
        if random.random() < 0.1:
            print(f'{Colors.FAIL}突发状况：刚好砸下(-40HP){Colors.ENDC}')
            e.player.update_stats(hp=-40)
        print(f'结果: 水分-5')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=-5)
    def opt2(e):
        print(f'\n你选择了: 等它掉落')
        e.time.add_minutes(30, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时30分, 绝对安全{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    run_event(engine, desc, {
        '1': ('快速跑过', opt1),
        '2': ('等它掉落', opt2),
    }, event_type='hazard')

def ev_hazards_10(engine):
    desc = "【Hazards】粉尘暴\n气流引起大量石膏粉末席卷。"
    def opt1(e):
        print(f'\n你选择了: 硬扛')
        print(f'{Colors.FAIL}结果: 水分-15, HP-5{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=-5, satiety=final_sat, hydration=-15)
    def opt2(e):
        print(f'\n你选择了: 用衣服包头')
        e.time.add_minutes(5, e.player)
        if random.random() < 0.3:
            print(f'{Colors.FAIL}突发状况：跌倒(-5HP){Colors.ENDC}')
            e.player.update_stats(hp=-5)
        print(f'结果: 耗时5分')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    run_event(engine, desc, {
        '1': ('硬扛', opt1),
        '2': ('用衣服包头', opt2),
    }, event_type='hazard')

def ev_hazards_11(engine):
    desc = "【Hazards】突发火情\n旁边的易燃物突然自燃。"
    def opt1(e):
        print(f'\n你选择了: 脱衣扑灭')
        e.time.add_minutes(10, e.player)
        if random.random() < 0.2:
            print(f'{Colors.FAIL}突发状况：烧伤(-10HP){Colors.ENDC}')
            e.player.update_stats(hp=-10)
        print(f'结果: 耗时10分')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    def opt2(e):
        print(f'\n你选择了: 迅速逃离')
        print(f'{Colors.OKGREEN}结果: 安全, 后续增加难度{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    run_event(engine, desc, {
        '1': ('脱衣扑灭', opt1),
        '2': ('迅速逃离', opt2),
    }, event_type='hazard')

def ev_hazards_12(engine):
    desc = "【Hazards】断裂的玻璃地板\n观景区的玻璃布满蜘蛛网裂纹。"
    def opt1(e):
        print(f'\n你选择了: 脱鞋轻走')
        e.time.add_minutes(20, e.player)
        if random.random() < 0.1:
            print(f'{Colors.FAIL}突发状况：扎伤(-5HP){Colors.ENDC}')
            e.player.update_stats(hp=-5)
        print(f'结果: 耗时20分')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    def opt2(e):
        print(f'\n你选择了: 靠边墙壁')
        e.time.add_minutes(10, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时10分, 安全{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    run_event(engine, desc, {
        '1': ('脱鞋轻走', opt1),
        '2': ('靠边墙壁', opt2),
    }, event_type='hazard')

def ev_hazards_13(engine):
    desc = "【Hazards】沉降陷阱\n感觉脚下一软。"
    def opt1(e):
        print(f'\n你选择了: 立刻后退')
        print(f'{Colors.OKGREEN}结果: 水分-5, 安全{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=-5)
    def opt2(e):
        print(f'\n你选择了: 继续走')
        print(f'{Colors.FAIL}结果: 踩破天花板掉落一层(-25HP){Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=-25, satiety=final_sat, hydration=0)
    run_event(engine, desc, {
        '1': ('立刻后退', opt1),
        '2': ('继续走', opt2),
    }, event_type='hazard')

def ev_hazards_14(engine):
    desc = "【Hazards】悬空废墟\n上方水泥板只靠几根钢筋悬挂在半空，随时会砸下。"
    def opt1(e):
        print(f'\n你选择了: 贴墙站屏住呼吸')
        if random.random() < 0.1:
            print(f'{Colors.FAIL}突发状况：被擦伤(-10HP){Colors.ENDC}')
            e.player.update_stats(hp=-10)
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    def opt2(e):
        print(f'\n你选择了: 退回原处绕路')
        e.time.add_minutes(20, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时20分, 安全{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    run_event(engine, desc, {
        '1': ('贴墙站屏住呼吸', opt1),
        '2': ('退回原处绕路', opt2),
    }, event_type='hazard')

def ev_actions_0(engine):
    desc = "【Actions】倒塌文件柜\n通道被堵死。"
    def opt1(e):
        print(f'\n你选择了: 徒手搬开')
        e.time.add_minutes(5, e.player)
        print(f'结果: 耗时25分, 饱食-20, 水分-20')
        final_sat = -20
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=-20)
    def opt2(e):
        print(f'\n你选择了: 用消防斧劈开')
        e.time.add_minutes(5, e.player)
        print(f'结果: 需要消防斧, 耗时5分, 饱食-2')
        final_sat = -2
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:
            print(f'{Colors.WARNING}你没有消防斧，无法执行此操作！{Colors.ENDC}')
            return
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('徒手搬开', opt1),
        '2': ('用消防斧劈开', opt2),
        '3': ('小心绕开/放弃', opt_leave),
    }, event_type='decision')

def ev_actions_1(engine):
    desc = "【Actions】电梯井滑降\n门半开深不见底。"
    def opt1(e):
        print(f'\n你选择了: 顺缆绳滑')
        e.time.add_minutes(5, e.player)
        if random.random() < 0.2:
            print(f'{Colors.FAIL}突发状况：脱手(-35HP){Colors.ENDC}')
            e.player.update_stats(hp=-35)
        print(f'结果: 下3-8层, 耗时15分')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        drop = random.randint(3, 8)
        drop = min(drop, e.player.floor - 1)
        e.player.floor = max(1, e.player.floor - drop)
        if drop > 0: print(f'你向下滑降了 {drop} 层！')
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('顺缆绳滑', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='decision')

def ev_actions_2(engine):
    desc = "【Actions】内线电话\n电话闪红灯。"
    def opt1(e):
        print(f'\n你选择了: 接听')
        if random.random() < 0.5:
            print(f'{Colors.FAIL}突发状况：惨叫(水分-5){Colors.ENDC}')
            e.player.update_stats(hp=0)
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=-5)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('接听', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='decision')

def ev_actions_3(engine):
    desc = "【Actions】极度疲劳\n双腿灌铅眼前发黑。"
    def opt1(e):
        print(f'\n你选择了: 休息半小时')
        e.time.add_minutes(30, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时30分, HP+5{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=5, satiety=final_sat, hydration=0)
    run_event(engine, desc, {
        '1': ('休息半小时', opt1),
    }, event_type='decision')

def ev_actions_4(engine):
    desc = "【Actions】外墙攀爬\n无路可走只能翻窗。"
    def opt1(e):
        print(f'\n你选择了: 爬出')
        e.time.add_minutes(20, e.player)
        if random.random() < 0.2:
            print(f'{Colors.FAIL}突发状况：划伤(-20HP){Colors.ENDC}')
            e.player.update_stats(hp=-20)
        print(f'结果: 耗时20分,  下1层')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        drop = min(1, e.player.floor - 1)
        e.player.floor = max(1, e.player.floor - drop)
    def opt2(e):
        print(f'\n你选择了: 刨开废墟找路')
        e.time.add_minutes(60, e.player)
        print(f'结果: 耗时60分, 状态-20')
        final_sat = -20
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=-20)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('爬出', opt1),
        '2': ('刨开废墟找路', opt2),
        '3': ('小心绕开/放弃', opt_leave),
    }, event_type='decision')

def ev_actions_5(engine):
    desc = "【Actions】锁死的逃生门\n安全门变形锁死。"
    def opt1(e):
        print(f'\n你选择了: 用消防斧劈')
        e.time.add_minutes(5, e.player)
        print(f'结果: 需要消防斧, 耗时5分')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:
            print(f'{Colors.WARNING}你没有消防斧，无法执行此操作！{Colors.ENDC}')
            return
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('用消防斧劈', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='decision')

def ev_actions_6(engine):
    desc = "【Actions】堵漏行动\n消防水管狂喷阻碍视线。"
    def opt1(e):
        print(f'\n你选择了: 去关阀门')
        e.time.add_minutes(10, e.player)
        if random.random() < 0.3:
            print(f'{Colors.FAIL}突发状况：被水压打伤(-5HP){Colors.ENDC}')
            e.player.update_stats(hp=-5)
        print(f'结果: 耗时10分')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('去关阀门', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='decision')

def ev_actions_7(engine):
    desc = "【Actions】深槽跳跃\n两块楼板间有一米五的鸿沟。"
    def opt1(e):
        print(f'\n你选择了: 冲刺跳跃')
        if random.random() < 0.1:
            print(f'{Colors.FAIL}突发状况：没站稳掉落(-20HP){Colors.ENDC}')
            e.player.update_stats(hp=-20)
        print(f'结果: 消耗饱食-5')
        final_sat = -5
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
    def opt2(e):
        print(f'\n你选择了: 找长板搭桥')
        e.time.add_minutes(20, e.player)
        print(f'{Colors.OKGREEN}结果: 耗时20分, 安全{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    run_event(engine, desc, {
        '1': ('冲刺跳跃', opt1),
        '2': ('找长板搭桥', opt2),
    }, event_type='decision')

def ev_actions_8(engine):
    desc = "【Actions】自制火把\n太黑了，看到木棍和破布。"
    def opt1(e):
        print(f'\n你选择了: 制作')
        print(f'{Colors.OKGREEN}结果: 获得打火机x1 获得照明能力{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('打火机', 1)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('制作', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='decision')

def ev_actions_9(engine):
    desc = "【Actions】通风管道\n一条看起来能通往下一层的狭小管道。"
    def opt1(e):
        print(f'\n你选择了: 钻进去')
        e.time.add_minutes(30, e.player)
        print(f'结果: 耗时30分, 幽闭恐惧(水分-15)')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=-15)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('钻进去', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='decision')

def ev_actions_10(engine):
    desc = "【Actions】寻找备用电源\n发现配电箱。"
    def opt1(e):
        print(f'\n你选择了: 尝试恢复照明')
        e.time.add_minutes(20, e.player)
        if random.random() < 0.2:
            print(f'{Colors.FAIL}突发状况：触电(-10HP){Colors.ENDC}')
            e.player.update_stats(hp=-10)
        print(f'结果: 耗时20分')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    def opt2(e):
        print(f'\n你选择了: 不冒险')
        print(f'结果: 无消耗')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    run_event(engine, desc, {
        '1': ('尝试恢复照明', opt1),
        '2': ('不冒险', opt2),
    }, event_type='decision')

def ev_actions_11(engine):
    desc = "【Actions】破窗通风\n室内粉尘太浓。"
    def opt1(e):
        print(f'\n你选择了: 砸碎厚玻璃')
        print(f'结果: 消耗饱食-10, 呼吸顺畅')
        final_sat = -10
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
    def opt2(e):
        print(f'\n你选择了: 用消防斧砸玻璃')
        print(f'结果: 需要消防斧, 无消耗, 呼吸顺畅')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:
            print(f'{Colors.WARNING}你没有消防斧，无法执行此操作！{Colors.ENDC}')
            return
    run_event(engine, desc, {
        '1': ('砸碎厚玻璃', opt1),
        '2': ('用消防斧砸玻璃', opt2),
    }, event_type='decision')

def ev_actions_12(engine):
    desc = "【Actions】滑索下楼\n找到一根长网线和坚固固定点。"
    def opt1(e):
        print(f'\n你选择了: 制作滑索')
        if random.random() < 0.3:
            print(f'{Colors.FAIL}突发状况：网线断裂(-15HP){Colors.ENDC}')
            e.player.update_stats(hp=-15)
        print(f'结果: 下2层')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        drop = min(2, e.player.floor - 1)
        e.player.floor = max(1, e.player.floor - drop)
    def opt2(e):
        print(f'\n你选择了: 太危险放弃')
        print(f'结果: 无消耗')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    run_event(engine, desc, {
        '1': ('制作滑索', opt1),
        '2': ('太危险放弃', opt2),
    }, event_type='decision')

def ev_actions_13(engine):
    desc = "【Actions】安抚自己\n恐惧感压垮了你。"
    def opt1(e):
        print(f'\n你选择了: 吃巧克力')
        print(f'{Colors.OKGREEN}结果: 消耗巧克力x1, HP+10{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=10, satiety=final_sat, hydration=0)
        e.player.add_item('巧克力', 1)
        e.player.remove_item('巧克力', 1)
    def opt2(e):
        print(f'\n你选择了: 深呼吸')
        e.time.add_minutes(10, e.player)
        print(f'结果: 耗时10分, 回复理智')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    run_event(engine, desc, {
        '1': ('吃巧克力', opt1),
        '2': ('深呼吸', opt2),
    }, event_type='decision')

def ev_actions_14(engine):
    desc = "【Actions】搜寻员工名册\n可能对后续找人有帮助。"
    def opt1(e):
        print(f'\n你选择了: 寻找')
        e.time.add_minutes(5, e.player)
        print(f'结果: 耗时15分, 无直接收益')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    def opt2(e):
        print(f'\n你选择了: 没用')
        print(f'结果: 无消耗')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    run_event(engine, desc, {
        '1': ('寻找', opt1),
        '2': ('没用', opt2),
    }, event_type='decision')

def ev_npcs_0(engine):
    desc = "【NPCs】被压住的人\n男人被石板压住双腿。"
    def opt1(e):
        print(f'\n你选择了: 帮忙抬起')
        e.time.add_minutes(20, e.player)
        if random.random() < 0.6:
            print(f'{Colors.FAIL}突发状况：得矿泉水x2{Colors.ENDC}')
            e.player.update_stats(hp=0)
            e.player.add_item('矿泉水', 2)
        print(f'{Colors.FAIL}结果: 耗时20分, 饱食-15{Colors.ENDC}')
        final_sat = -15
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=-10, satiety=final_sat, hydration=0)
    def opt2(e):
        print(f'\n你选择了: 用消防斧作为撬棍')
        e.time.add_minutes(10, e.player)
        print(f'{Colors.OKGREEN}结果: 需要消防斧, 耗时10分, 饱食-5, 安全救出得高级矿泉水x1 绷带x1{Colors.ENDC}')
        final_sat = -5
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
        e.player.add_item('矿泉水', 1)
        e.player.add_item('绷带', 1)
        e.player.add_item('高级矿泉水', 1)
        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:
            print(f'{Colors.WARNING}你没有消防斧，无法执行此操作！{Colors.ENDC}')
            return
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('帮忙抬起', opt1),
        '2': ('用消防斧作为撬棍', opt2),
        '3': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_1(engine):
    desc = "【NPCs】发狂幸存者\n挥舞订书机抢水。"
    def opt1(e):
        print(f'\n你选择了: 安抚')
        e.time.add_minutes(10, e.player)
        if random.random() < 0.5:
            print(f'{Colors.FAIL}突发状况：被砸(-15HP){Colors.ENDC}')
            e.player.update_stats(hp=-15)
        print(f'结果: 耗时10分')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    def opt2(e):
        print(f'\n你选择了: 挥舞消防斧吓走他')
        print(f'{Colors.OKGREEN}结果: 需要消防斧, 他尖叫着跑了, 安全{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:
            print(f'{Colors.WARNING}你没有消防斧，无法执行此操作！{Colors.ENDC}')
            return
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('安抚', opt1),
        '2': ('挥舞消防斧吓走他', opt2),
        '3': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_2(engine):
    desc = "【NPCs】躲藏母女\n瑟瑟发抖的母女。"
    def opt1(e):
        print(f'\n你选择了: 给水和饼干')
        print(f'{Colors.OKGREEN}结果: 失去矿泉水x1, 失去饼干x1, 心灵慰藉(HP+15){Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=15, satiety=final_sat, hydration=0)
        e.player.add_item('矿泉水', 1)
        e.player.add_item('饼干', 1)
        e.player.remove_item('矿泉水', 1)
        e.player.remove_item('饼干', 1)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('给水和饼干', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_3(engine):
    desc = "【NPCs】趁火打劫者\n拿刀的搜刮者。"
    def opt1(e):
        print(f'\n你选择了: 搏斗')
        e.time.add_minutes(5, e.player)
        print(f'{Colors.FAIL}结果: 耗时5分, HP-15, 饱食-10, 得巧克力x2 水x1{Colors.ENDC}')
        final_sat = -10
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=-15, satiety=final_sat, hydration=0)
        e.player.add_item('巧克力', 2)
    def opt2(e):
        print(f'\n你选择了: 亮出消防斧')
        print(f'{Colors.OKGREEN}结果: 需要消防斧, 他立刻丢下物资逃跑, 获得高能量棒x1 矿泉水x1{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('矿泉水', 1)
        e.player.add_item('高能量棒', 1)
        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:
            print(f'{Colors.WARNING}你没有消防斧，无法执行此操作！{Colors.ENDC}')
            return
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('搏斗', opt1),
        '2': ('亮出消防斧', opt2),
        '3': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_4(engine):
    desc = "【NPCs】濒死领导\n作威作福的经理求救。"
    def opt1(e):
        print(f'\n你选择了: 带上他')
        e.time.add_minutes(5, e.player)
        print(f'结果: 耗时15分, 饱食-15')
        final_sat = -15
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('带上他', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_5(engine):
    desc = "【NPCs】保洁阿姨\n讨要绷带。"
    def opt1(e):
        print(f'\n你选择了: 给绷带')
        print(f'结果: 失去绷带x1, 走捷径下2层')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('绷带', 1)
        e.player.remove_item('绷带', 1)
        drop = min(2, e.player.floor - 1)
        e.player.floor = max(1, e.player.floor - drop)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('给绷带', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_6(engine):
    desc = "【NPCs】敲击墙壁\n废墟后传来的求救。"
    def opt1(e):
        print(f'\n你选择了: 徒手挖掘')
        e.time.add_minutes(40, e.player)
        if random.random() < 0.7:
            print(f'{Colors.FAIL}突发状况：得绷带x2 急救包x1{Colors.ENDC}')
            e.player.update_stats(hp=0)
            e.player.add_item('绷带', 2)
            e.player.add_item('急救包', 1)
        print(f'结果: 耗时40分, 饱食-20')
        final_sat = -20
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
    def opt2(e):
        print(f'\n你选择了: 用消防斧破墙')
        e.time.add_minutes(5, e.player)
        if random.random() < 0.8:
            print(f'{Colors.FAIL}突发状况：得高级矿泉水x1 急救包x1{Colors.ENDC}')
            e.player.update_stats(hp=0)
            e.player.add_item('矿泉水', 1)
            e.player.add_item('急救包', 1)
        print(f'结果: 需要消防斧, 耗时15分, 饱食-5')
        final_sat = -5
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:
            print(f'{Colors.WARNING}你没有消防斧，无法执行此操作！{Colors.ENDC}')
            return
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('徒手挖掘', opt1),
        '2': ('用消防斧破墙', opt2),
        '3': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_7(engine):
    desc = "【NPCs】被困电梯的同事\n听到电梯里有人拍门。"
    def opt1(e):
        print(f'\n你选择了: 试图撬门')
        e.time.add_minutes(20, e.player)
        print(f'{Colors.OKGREEN}结果: 饱食-15, 耗时20分, 获得手电筒x1 矿泉水x1{Colors.ENDC}')
        final_sat = -15
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
        e.player.add_item('矿泉水', 1)
        e.player.add_item('手电筒', 1)
    def opt2(e):
        print(f'\n你选择了: 用消防斧撬门')
        e.time.add_minutes(5, e.player)
        print(f'{Colors.OKGREEN}结果: 需要消防斧, 耗时5分, 饱食-2, 获得手电筒x1 饼干x2{Colors.ENDC}')
        final_sat = -2
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
        e.player.add_item('饼干', 2)
        e.player.add_item('手电筒', 1)
        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:
            print(f'{Colors.WARNING}你没有消防斧，无法执行此操作！{Colors.ENDC}')
            return
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('试图撬门', opt1),
        '2': ('用消防斧撬门', opt2),
        '3': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_8(engine):
    desc = "【NPCs】重伤安保\n安保陈硕腹部受伤。"
    def opt1(e):
        print(f'\n你选择了: 给他急救包')
        print(f'结果: 失去急救包x1')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('急救包', 1)
        e.player.remove_item('急救包', 1)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('给他急救包', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_9(engine):
    desc = "【NPCs】惊恐的新人\n一位实习生跟在后面哭着求你带上她。"
    def opt1(e):
        print(f'\n你选择了: 带上她作为同伴')
        print(f'{Colors.OKGREEN}结果: 获得同伴实习生{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.companion = '实习生'
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('带上她作为同伴', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_10(engine):
    desc = "【NPCs】跳楼者\n一个人绝望地站在破窗边缘。"
    def opt1(e):
        print(f'\n你选择了: 劝阻')
        e.time.add_minutes(10, e.player)
        if random.random() < 0.7:
            print(f'{Colors.FAIL}突发状况：跳下(水分-10){Colors.ENDC}')
            e.player.update_stats(hp=0)
        print(f'结果: 耗时10分')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=-10)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('劝阻', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_11(engine):
    desc = "【NPCs】争抢物资的两人\n两人为了一瓶水打架。"
    def opt1(e):
        print(f'\n你选择了: 劝架')
        print(f'{Colors.FAIL}结果: 挨打(-10HP){Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=-10, satiety=final_sat, hydration=0)
    def opt2(e):
        print(f'\n你选择了: 大喝一声亮出消防斧')
        print(f'{Colors.OKGREEN}结果: 需要消防斧, 两人吓跑, 获得矿泉水x2 巧克力x1{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('矿泉水', 2)
        e.player.add_item('巧克力', 1)
        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:
            print(f'{Colors.WARNING}你没有消防斧，无法执行此操作！{Colors.ENDC}')
            return
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('劝架', opt1),
        '2': ('大喝一声亮出消防斧', opt2),
        '3': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_12(engine):
    desc = "【NPCs】绝望的祈祷者\n跪在地上不断磕头。"
    def opt1(e):
        print(f'\n你选择了: 打断他')
        print(f'结果: 无收获')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('打断他', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_13(engine):
    desc = "【NPCs】被锁在冷库的厨师\n餐厅厨房里传出拍打声。"
    def opt1(e):
        print(f'\n你选择了: 砸开门锁')
        e.time.add_minutes(20, e.player)
        print(f'结果: 耗时20分, 饱食-10, 送熟肉x2')
        final_sat = -10
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=0, satiety=final_sat, hydration=0)
        e.player.add_item('熟肉', 2)
    def opt2(e):
        print(f'\n你选择了: 用消防斧劈锁')
        e.time.add_minutes(5, e.player)
        print(f'结果: 需要消防斧, 耗时5分, 送熟肉x2 矿泉水x2')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.add_item('矿泉水', 2)
        e.player.add_item('熟肉', 2)
        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:
            print(f'{Colors.WARNING}你没有消防斧，无法执行此操作！{Colors.ENDC}')
            return
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('砸开门锁', opt1),
        '2': ('用消防斧劈锁', opt2),
        '3': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

def ev_npcs_14(engine):
    desc = "【NPCs】奇怪的幸存者\n一个人躺在地上哀嚎说腿断了，但周围没有任何重物。"
    def opt1(e):
        print(f'\n你选择了: 靠近检查')
        print(f'{Colors.FAIL}结果: 被暗算抢走一样物资, HP-5{Colors.ENDC}')
        final_sat = 0
        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':
            final_sat = int(final_sat * 0.7)
            print(f'{Colors.OKGREEN}(实习生帮你分担了部分体力活！){Colors.ENDC}')
        e.player.update_stats(hp=-5, satiety=final_sat, hydration=0)
    def opt_leave(e):
        print('\n你决定不冒风险，转身离开。')
        e.time.add_minutes(2, e.player)
    run_event(engine, desc, {
        '1': ('靠近检查', opt1),
        '2': ('小心绕开/放弃', opt_leave),
    }, event_type='combat')

ALL_EVENTS = [
    ev_exploration_0,
    ev_exploration_1,
    ev_exploration_2,
    ev_exploration_3,
    ev_exploration_4,
    ev_exploration_5,
    ev_exploration_6,
    ev_exploration_7,
    ev_exploration_8,
    ev_exploration_9,
    ev_exploration_10,
    ev_exploration_11,
    ev_exploration_12,
    ev_exploration_13,
    ev_exploration_14,
    ev_exploration_15,
    ev_hazards_0,
    ev_hazards_1,
    ev_hazards_2,
    ev_hazards_3,
    ev_hazards_4,
    ev_hazards_5,
    ev_hazards_6,
    ev_hazards_7,
    ev_hazards_8,
    ev_hazards_9,
    ev_hazards_10,
    ev_hazards_11,
    ev_hazards_12,
    ev_hazards_13,
    ev_hazards_14,
    ev_actions_0,
    ev_actions_1,
    ev_actions_2,
    ev_actions_3,
    ev_actions_4,
    ev_actions_5,
    ev_actions_6,
    ev_actions_7,
    ev_actions_8,
    ev_actions_9,
    ev_actions_10,
    ev_actions_11,
    ev_actions_12,
    ev_actions_13,
    ev_actions_14,
    ev_npcs_0,
    ev_npcs_1,
    ev_npcs_2,
    ev_npcs_3,
    ev_npcs_4,
    ev_npcs_5,
    ev_npcs_6,
    ev_npcs_7,
    ev_npcs_8,
    ev_npcs_9,
    ev_npcs_10,
    ev_npcs_11,
    ev_npcs_12,
    ev_npcs_13,
    ev_npcs_14
]

def get_random_event(engine=None):
    available_events = list(ALL_EVENTS)
    if engine is not None:
        if not hasattr(engine, 'triggered_npc_events'):
            engine.triggered_npc_events = set()
        available_events = [ev for ev in available_events if ev.__name__ not in engine.triggered_npc_events]
        if not available_events:
            available_events = [ev for ev in ALL_EVENTS if not ev.__name__.startswith('ev_npcs')]

    chosen = random.choice(available_events)
    if engine is not None and chosen.__name__.startswith('ev_npcs'):
        engine.triggered_npc_events.add(chosen.__name__)
    return chosen

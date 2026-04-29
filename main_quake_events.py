from cli import prompt_with_timeout, clear_screen
import time

def run_quake_event(engine, title_desc, choices_dict):
    choices_str = "\n".join([f"{k}. {v[0]}" for k, v in choices_dict.items()])

    while True:
        # 主震阶段极度危险，反应时间极短，覆盖默认文本长度计算
        ans = prompt_with_timeout(choices_str, engine.player, description_text=title_desc, override_timeout=7)
        if ans is None:
            engine.process_idle()
            return
        if ans in choices_dict:
            choices_dict[ans][1](engine)
            break
        else:
            print("\n无效的选择，快点决定！")
            time.sleep(1)

    if engine.running:
        engine.pause_and_continue()


def quake_turn_1(engine):
    desc = "【回合一：突如其来的震颤】\n21:30，星寰中心25层。你还在加班，突然地板传来低沉的轰鸣，桌面咖啡杯瞬间崩裂，大楼开始剧烈摇晃。"
    def opt1(e):
        e.time.add_seconds(15, e.player)
        print("\n你迅速躲进实木办公桌下，完美躲过了第一波掉落的天花板。")
    def opt2(e):
        e.time.add_seconds(20, e.player)
        print("\n你冲向门口抢到了一个应急包！但被砸落的灯管击中背部！")
        e.player.add_item("矿泉水", 1)
        e.player.add_item("手电筒", 1)
        e.player.update_stats(hp=-15)
    def opt3(e):
        e.time.add_seconds(20, e.player)
        print("\n你跑到落地窗前。大楼扭曲导致玻璃瞬间爆裂！你被狂风席卷，受了重伤！")
        e.player.update_stats(hp=-30, hydration=-10)

    run_quake_event(engine, desc, {
        "1": ("立刻钻进实木办公桌下 (避险)", opt1),
        "2": ("冲向门口的应急柜 (贪婪)", opt2),
        "3": ("跑到落地窗前查看情况 (致命)", opt3)
    })

def quake_turn_2(engine):
    desc = "【回合二：黑暗与粉尘】\n大楼供电彻底中断。四周陷入绝对黑暗，伴随着刺耳的钢筋扭曲声，大量石膏粉末充斥空气，令人窒息。"
    def opt1(e):
        e.time.add_seconds(25, e.player)
        print("\n你用衣服捂住口鼻，贴地匍匐前进，安全但缓慢地移动到了走廊。")
        e.player.update_stats(hydration=-5)
    def opt2(e):
        e.time.add_seconds(15, e.player)
        print("\n你在黑暗中看清了路向外狂奔，但被变形的办公桌绊倒，且吸入了大量粉尘！")
        e.player.update_stats(hp=-10, hydration=-15)
    def opt3(e):
        e.time.add_seconds(30, e.player)
        print("\n你摸黑拉住了一名吓呆的实习生带她躲避。作为感谢，她给了你一块巧克力。")
        e.player.add_item("巧克力", 1)
        e.player.update_stats(satiety=-5)

    run_quake_event(engine, desc, {
        "1": ("用衣服捂住口鼻，贴地匍匐前进 (理智)", opt1),
        "2": ("打开手机手电筒盲目狂奔 (慌乱)", opt2),
        "3": ("摸黑寻找身边的同事 (人道)", opt3)
    })

def quake_turn_3(engine):
    desc = "【回合三：坍塌的走廊】\n你来到了电梯间外的主走廊。前方的一段楼板突然发生了局部塌陷，露出通往24层的豁口。"
    def opt1(e):
        e.time.add_seconds(30, e.player)
        print("\n你冒险顺着倾斜的楼板滑下，重重摔在24层的地毯上！")
        e.player.update_stats(hp=-15)
        e.player.floor = 24
    def opt2(e):
        e.time.add_seconds(20, e.player)
        print("\n你眼看着楼板塌陷，自己安全地抱住柱子留在了25层。")
    def opt3(e):
        e.time.add_seconds(30, e.player)
        print("\n你顶着摇晃砸碎消防栓玻璃，手被划伤，但拿到了一把破拆神器！")
        e.player.update_stats(hp=-10)
        e.player.add_item("消防斧", 1)

    run_quake_event(engine, desc, {
        "1": ("顺着倾斜的楼板滑向24层 (冒险)", opt1),
        "2": ("抓住旁边的承重柱死死抱住 (稳妥)", opt2),
        "3": ("砸碎消防栓玻璃拿取消防斧 (准备)", opt3)
    })

def quake_turn_4(engine):
    desc = "【回合四：最后的震荡】\n大楼发出了最后的悲鸣。通往安全通道的防火门因为门框变形卡死了。"
    def opt1(e):
        e.time.add_seconds(45, e.player)
        if "消防斧" in e.player.inventory and e.player.inventory["消防斧"] > 0:
            print("\n你抡起刚刚拿到的消防斧，几下就劈开了变形的门！")
        else:
            print("\n你深呼吸，用尽全身力气一次次撞击，终于撞开了门！这消耗了极大体力。")
            e.player.update_stats(satiety=-15, hp=-5)
    def opt2(e):
        e.time.add_seconds(60, e.player)
        print("\n你在走廊尽头找到了一个备用的维修通道钻了进去。极其狭窄让你满头大汗。")
        e.player.update_stats(hydration=-20)
    def opt3(e):
        e.time.add_seconds(60, e.player)
        print("\n主震终于停止了。你被困在这片区域，且被掉落的杂物轻微砸伤。")
        e.player.update_stats(hp=-10)

    run_quake_event(engine, desc, {
        "1": ("深呼吸，用尽全身力气撞门 (力量)", opt1),
        "2": ("寻找维修通道或其他出口 (探索)", opt2),
        "3": ("原地绝望地等待摇晃停止 (放弃)", opt3)
    })

def play_main_quake(engine):
    engine.time.phase = "quake"
    engine.trigger_event(quake_turn_1)
    if engine.running: engine.trigger_event(quake_turn_2)
    if engine.running: engine.trigger_event(quake_turn_3)
    if engine.running: engine.trigger_event(quake_turn_4)

    if engine.running:
        clear_screen()
        print("="*50)
        from cli import Colors
        print(f"{Colors.BOLD}主震停止了。{Colors.ENDC}")
        print("建筑的哀鸣声取代了隆隆的震颤。空气中满是灰尘的呛鼻味道。")
        print("时间仿佛重新开始了流转。真正的生存考验，现在才开始。")
        print("="*50)
        engine.time.phase = "survival"
        engine.pause_and_continue()

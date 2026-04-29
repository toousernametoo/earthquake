import json
import re

events_data = {
    "Exploration": [
        {"name": "自动贩卖机", "desc": "一台被承重墙卡住的贩卖机，里面有水和零食。", "opts": [
            ("暴力砸开", "消耗体力(-10饱食), {P_30}受伤(-10HP), 获得水x2 巧克力x2"),
            ("用消防斧劈开", "需要消防斧, 耗时5分, 获得水x3 巧克力x2 饼干x1")
        ]},
        {"name": "同事的遗物", "desc": "残破办公桌下的血迹背包。", "opts": [("翻找背包", "获得矿泉水x2 饼干x2, 耗时5分")]},
        {"name": "被锁的杂物间", "desc": "门被变形卡死。", "opts": [
            ("用力撞开", "消耗饱食(-15), {P_70}获得消防斧, {P_30}受伤(-5HP)"),
            ("用消防斧破门", "需要消防斧, 耗时5分, 获得手电筒x1 绷带x2")
        ]},
        {"name": "废弃的茶水间", "desc": "水管破裂滴水。", "opts": [("接水喝", "水分+25, {P_40}胃痉挛(-10HP)"), ("仔细过滤", "耗时15分, 水分+20, 获得矿泉水x1")]},
        {"name": "破碎的药箱", "desc": "墙角紧急医疗箱。", "opts": [("翻找", "耗时5分, 获得绷带x2 急救包x1")]},
        {"name": "幸存者营地", "desc": "废纸火堆余温未散。", "opts": [("搜刮遗留物资", "耗时10分, 获得熟肉x1 矿泉水x1")]},
        {"name": "遗落的急救包", "desc": "走廊中间掉落的完好急救包。", "opts": [("跑去捡起", "{P_50}遭遇天花板掉落(-15HP), 获得医疗箱x2 绷带x1")]},
        {"name": "半开的保险柜", "desc": "墙壁破裂露出的保险柜。", "opts": [
            ("尝试徒手拉开", "耗时15分, 获得手电筒x1 巧克力x1, 饱食-5"),
            ("用消防斧撬开", "需要消防斧, 耗时5分, 获得高级矿泉水x2 高能量棒x2")
        ]},
        {"name": "员工休息区", "desc": "沙发被压扁，可能有吃的。", "opts": [("翻找", "耗时15分, {P_80}获得高能量棒x2 饼干x1, 饱食-5")]},
        {"name": "破碎的饮水机", "desc": "还有半桶水没流完。", "opts": [("收集水", "耗时10分, 获得矿泉水x2")]},
        {"name": "遗弃的手提箱", "desc": "走廊上一个高档手提箱。", "opts": [("打开", "耗时5分, 获得高级矿泉水x1 巧克力x1")]},
        {"name": "震碎的展示柜", "desc": "原本放公司纪念品的柜子，可能藏有应急物资。", "opts": [("翻找", "获得巧克力x2 水x1, {P_20}划伤(-5HP)")]},
        {"name": "破损的通风管", "desc": "管内似乎有东西闪光。", "opts": [("伸手摸", "获得打火机x1 饼干x1, {P_10}被老鼠咬(-5HP)")]},
        {"name": "高管办公室", "desc": "门半掩着。", "opts": [("进去搜", "耗时20分, 获得高级矿泉水x2 熟肉x1, 饱食-5")]},
        {"name": "散落的外卖", "desc": "地上一份还没拆的震前外卖。", "opts": [("吃掉", "饱食+30, {P_40}拉肚子(-10HP, 状态下降)")]},
        {"name": "震碎的库房", "desc": "库房大门敞开，里面似乎有很多包裹。", "opts": [("仔细搜刮", "耗时30分, 饱食-10, 获得高级矿泉水x1 医疗箱x1 高能量棒x1")]}
    ],
    "Hazards": [
        {"name": "强烈余震", "desc": "大楼剧烈摇晃。", "opts": [("躲承重墙角", "安全, 耗时5分"), ("走廊中间", "被砸中(-30HP)")]},
        {"name": "浓烟走廊", "desc": "前方起火黑烟弥漫。", "opts": [("强行穿过", "耗时5分, HP-15, 水分-20"), ("花时间绕路", "耗时30分, 饱食-10, 水分-10")]},
        {"name": "深渊陷阱", "desc": "走廊大面积塌陷。", "opts": [("贴墙挪", "耗时15分, 饱食-10, {P_20}跌落(-15HP)"), ("退回去绕路", "耗时45分, 状态-15")]},
        {"name": "天花板崩塌", "desc": "头顶钢筋崩裂声。", "opts": [("往前扑", "饱食-5, 安全躲过"), ("抱头蹲下", "被砸中肩部(-25HP)")]},
        {"name": "毒气泄漏", "desc": "刺鼻气味弥漫。", "opts": [("弯腰狂奔", "水分-15, 安全"), ("寻找来源", "吸入毒气(-25HP)")]},
        {"name": "绝对黑暗", "desc": "楼梯间毫无光线。", "opts": [("使用手电筒", "需要手电筒, 安全通过"), ("盲人摸象", "耗时15分, {P_40}踩空(-20HP)")]},
        {"name": "高空强风", "desc": "外墙碎裂，狂风卷玻璃。", "opts": [("匍匐前进", "饱食-5, 安全")]},
        {"name": "漏电水洼", "desc": "地上的积水里有断裂电线闪火花。", "opts": [("跳过去", "消耗饱食-5, {P_30}踩水触电(-20HP)"), ("搬杂物垫脚", "耗时15分, 饱食-10, 安全")]},
        {"name": "倾斜楼板", "desc": "楼板倾斜近30度。", "opts": [("顺势滑下", "快速通过, {P_20}撞墙(-15HP)"), ("往上爬回去", "饱食-15, 耗时20分")]},
        {"name": "悬挂的空调箱", "desc": "头顶巨大的中央空调摇摇欲坠。", "opts": [("快速跑过", "水分-5, {P_10}刚好砸下(-40HP)"), ("等它掉落", "耗时30分, 绝对安全")]},
        {"name": "粉尘暴", "desc": "气流引起大量石膏粉末席卷。", "opts": [("硬扛", "水分-15, HP-5"), ("用衣服包头", "耗时5分, {P_30}跌倒(-5HP)")]},
        {"name": "突发火情", "desc": "旁边的易燃物突然自燃。", "opts": [("脱衣扑灭", "耗时10分, {P_20}烧伤(-10HP)"), ("迅速逃离", "安全, 后续增加难度")]},
        {"name": "断裂的玻璃地板", "desc": "观景区的玻璃布满蜘蛛网裂纹。", "opts": [("脱鞋轻走", "耗时20分, {P_10}扎伤(-5HP)"), ("靠边墙壁", "耗时10分, 安全")]},
        {"name": "沉降陷阱", "desc": "感觉脚下一软。", "opts": [("立刻后退", "水分-5, 安全"), ("继续走", "踩破天花板掉落一层(-25HP)")]},
        {"name": "悬空废墟", "desc": "上方水泥板只靠几根钢筋悬挂在半空，随时会砸下。", "opts": [("贴墙站屏住呼吸", "{P_10}被擦伤(-10HP)"), ("退回原处绕路", "耗时20分, 安全")]}
    ],
    "Actions": [
        {"name": "倒塌文件柜", "desc": "通道被堵死。", "opts": [
            ("徒手搬开", "耗时25分, 饱食-20, 水分-20"),
            ("用消防斧劈开", "需要消防斧, 耗时5分, 饱食-2")
        ]},
        {"name": "电梯井滑降", "desc": "门半开深不见底。", "opts": [("顺缆绳滑", "下3-8层, 耗时15分, {P_20}脱手(-35HP)")]},
        {"name": "内线电话", "desc": "电话闪红灯。", "opts": [("接听", "{P_50}惨叫(水分-5)")]},
        {"name": "极度疲劳", "desc": "双腿灌铅眼前发黑。", "opts": [("休息半小时", "耗时30分, HP+5")]},
        {"name": "外墙攀爬", "desc": "无路可走只能翻窗。", "opts": [("爬出", "耗时20分, {P_20}划伤(-20HP), 下1层"), ("刨开废墟找路", "耗时60分, 状态-20")]},
        {"name": "锁死的逃生门", "desc": "安全门变形锁死。", "opts": [("用消防斧劈", "需要消防斧, 耗时5分")]},
        {"name": "堵漏行动", "desc": "消防水管狂喷阻碍视线。", "opts": [("去关阀门", "耗时10分, {P_30}被水压打伤(-5HP)")]},
        {"name": "深槽跳跃", "desc": "两块楼板间有一米五的鸿沟。", "opts": [("冲刺跳跃", "消耗饱食-5, {P_10}没站稳掉落(-20HP)"), ("找长板搭桥", "耗时20分, 安全")]},
        {"name": "自制火把", "desc": "太黑了，看到木棍和破布。", "opts": [("制作", "获得打火机x1 获得照明能力")]},
        {"name": "通风管道", "desc": "一条看起来能通往下一层的狭小管道。", "opts": [("钻进去", "耗时30分, 幽闭恐惧(水分-15)")]},
        {"name": "寻找备用电源", "desc": "发现配电箱。", "opts": [("尝试恢复照明", "耗时20分, {P_20}触电(-10HP)"), ("不冒险", "无消耗")]},
        {"name": "破窗通风", "desc": "室内粉尘太浓。", "opts": [
            ("砸碎厚玻璃", "消耗饱食-10, 呼吸顺畅"),
            ("用消防斧砸玻璃", "需要消防斧, 无消耗, 呼吸顺畅")
        ]},
        {"name": "滑索下楼", "desc": "找到一根长网线和坚固固定点。", "opts": [("制作滑索", "下2层, {P_30}网线断裂(-15HP)"), ("太危险放弃", "无消耗")]},
        {"name": "安抚自己", "desc": "恐惧感压垮了你。", "opts": [("吃巧克力", "消耗巧克力x1, HP+10"), ("深呼吸", "耗时10分, 回复理智")]},
        {"name": "搜寻员工名册", "desc": "可能对后续找人有帮助。", "opts": [("寻找", "耗时15分, 无直接收益"), ("没用", "无消耗")]}
    ],
    "NPCs": [
        {"name": "被压住的人", "desc": "男人被石板压住双腿。", "opts": [
            ("帮忙抬起", "耗时20分, 饱食-15, {P_60}得矿泉水x2, {P_40}闪腰(-10HP)"),
            ("用消防斧作为撬棍", "需要消防斧, 耗时10分, 饱食-5, 安全救出得高级矿泉水x1 绷带x1")
        ]},
        {"name": "发狂幸存者", "desc": "挥舞订书机抢水。", "opts": [
            ("安抚", "耗时10分, {P_50}被砸(-15HP)"),
            ("挥舞消防斧吓走他", "需要消防斧, 他尖叫着跑了, 安全")
        ]},
        {"name": "躲藏母女", "desc": "瑟瑟发抖的母女。", "opts": [("给水和饼干", "失去矿泉水x1, 失去饼干x1, 心灵慰藉(HP+15)")]},
        {"name": "趁火打劫者", "desc": "拿刀的搜刮者。", "opts": [
            ("搏斗", "耗时5分, HP-15, 饱食-10, 得巧克力x2 水x1"),
            ("亮出消防斧", "需要消防斧, 他立刻丢下物资逃跑, 获得高能量棒x1 矿泉水x1")
        ]},
        {"name": "濒死领导", "desc": "作威作福的经理求救。", "opts": [("带上他", "耗时15分, 饱食-15")]},
        {"name": "保洁阿姨", "desc": "讨要绷带。", "opts": [("给绷带", "失去绷带x1, 走捷径下2层")]},
        {"name": "敲击墙壁", "desc": "废墟后传来的求救。", "opts": [
            ("徒手挖掘", "耗时40分, 饱食-20, {P_70}得绷带x2 急救包x1"),
            ("用消防斧破墙", "需要消防斧, 耗时15分, 饱食-5, {P_80}得高级矿泉水x1 急救包x1")
        ]},
        {"name": "被困电梯的同事", "desc": "听到电梯里有人拍门。", "opts": [
            ("试图撬门", "饱食-15, 耗时20分, 获得手电筒x1 矿泉水x1"),
            ("用消防斧撬门", "需要消防斧, 耗时5分, 饱食-2, 获得手电筒x1 饼干x2")
        ]},
        {"name": "重伤安保", "desc": "安保陈硕腹部受伤。", "opts": [("给他急救包", "失去急救包x1")]},
        {"name": "惊恐的新人", "desc": "一位实习生跟在后面哭着求你带上她。", "opts": [("带上她作为同伴", "获得同伴实习生")]},
        {"name": "跳楼者", "desc": "一个人绝望地站在破窗边缘。", "opts": [("劝阻", "耗时10分, {P_70}跳下(水分-10)")]},
        {"name": "争抢物资的两人", "desc": "两人为了一瓶水打架。", "opts": [
            ("劝架", "挨打(-10HP)"),
            ("大喝一声亮出消防斧", "需要消防斧, 两人吓跑, 获得矿泉水x2 巧克力x1")
        ]},
        {"name": "绝望的祈祷者", "desc": "跪在地上不断磕头。", "opts": [("打断他", "无收获")]},
        {"name": "被锁在冷库的厨师", "desc": "餐厅厨房里传出拍打声。", "opts": [
            ("砸开门锁", "耗时20分, 饱食-10, 送熟肉x2"),
            ("用消防斧劈锁", "需要消防斧, 耗时5分, 送熟肉x2 矿泉水x2")
        ]},
        {"name": "奇怪的幸存者", "desc": "一个人躺在地上哀嚎说腿断了，但周围没有任何重物。", "opts": [("靠近检查", "被暗算抢走一样物资, HP-5")]}
    ]
}

def extract_mod(text, prefix):
    match = re.search(prefix + r'([-+]\d+)', text)
    if match: return int(match.group(1))
    match2 = re.search(r'([-+]\d+)' + prefix, text)
    if match2: return int(match2.group(1))
    return 0

md_content = "# 第一章：星寰中心逃生 事件设计规划 (共 60 个事件)\n\n"
for cat, events in events_data.items():
    md_content += f"## {cat}\n"
    for i, ev in enumerate(events):
        md_content += f"{i+1}. **{ev['name']}**：{ev['desc']}\n"
        for opt in ev['opts']:
            md_content += f"   - 选择：{opt[0]} -> 结果：{opt[1]}\n"
    md_content += "\n"

with open("events_design.md", "w") as f:
    f.write(md_content)

py_content = "import random\nfrom cli import prompt_with_timeout, Colors\n\n"
py_content += """def run_event(engine, title_desc, choices_dict, require_pause=True, event_type="normal"):
    choices_str = "\\n".join([f"{k}. {v[0]}" for k, v in choices_dict.items()])
    while True:
        ans = prompt_with_timeout(choices_str, engine.player, description_text=title_desc)
        if ans is None:
            engine.process_idle(context=event_type)
            return
        if ans in choices_dict:
            choices_dict[ans][1](engine)
            break
        else:
            print("\\n无效的选择，请重新输入。")
            import time
            time.sleep(1)
    if require_pause and engine.running:
        engine.pause_and_continue()
"""

all_event_funcs = []
for cat, events in events_data.items():
    for i, ev in enumerate(events):
        func_name = f"ev_{cat.lower()}_{i}"
        all_event_funcs.append(func_name)

        py_content += f"\ndef {func_name}(engine):\n"
        py_content += f"    desc = \"【{cat}】{ev['name']}\\n{ev['desc']}\"\n"

        opts_dict = {}
        has_leave_opt = False

        for idx, opt in enumerate(ev['opts']):
            opt_num = str(idx + 1)
            opt_title = opt[0]
            opt_res_raw = opt[1]

            if "无消耗" in opt_res_raw or "无收益" in opt_res_raw:
                has_leave_opt = True

            py_content += f"    def opt{opt_num}(e):\n"
            py_content += f"        print(f'\\n你选择了: {opt_title}')\n"

            time_val = extract_mod(opt_res_raw, "耗时")
            if time_val == 0:
                for mm in [5,10,15,20,25,30,40,45,60]:
                    if f"{mm}分" in opt_res_raw: time_val = mm; break
            if time_val > 0:
                py_content += f"        e.time.add_minutes({time_val}, e.player)\n"

            sat_mod = extract_mod(opt_res_raw, "饱食")
            hyd_mod = extract_mod(opt_res_raw, "水分")
            hp_mod = extract_mod(opt_res_raw, "HP")
            state_mod = extract_mod(opt_res_raw, "状态")
            if state_mod < 0:
                sat_mod += state_mod
                hyd_mod += state_mod

            prob_match = re.search(r'\{P_(\d+)\}(.+?)(?:,|\Z)', opt_res_raw)
            prob_hp = 0
            if prob_match:
                prob_val = int(prob_match.group(1)) / 100.0
                prob_outcome = prob_match.group(2)

                prob_hp = extract_mod(prob_outcome, "HP")
                if prob_hp < 0: hp_mod -= prob_hp

                clean_res = re.sub(r'\{P_(\d+)\}.+?(?:,|\Z)', '', opt_res_raw)
                clean_res = clean_res.strip(" ,")

                py_content += f"        if random.random() < {prob_val}:\n"
                py_content += f"            print(f'{{Colors.FAIL}}突发状况：{prob_outcome}{{Colors.ENDC}}')\n"
                py_content += f"            e.player.update_stats(hp={prob_hp})\n"

                if "得水x1" in prob_outcome or "矿泉水x1" in prob_outcome: py_content += f"            e.player.add_item('矿泉水', 1)\n"
                elif "得水x2" in prob_outcome or "矿泉水x2" in prob_outcome: py_content += f"            e.player.add_item('矿泉水', 2)\n"
                elif "得水x3" in prob_outcome or "矿泉水x3" in prob_outcome: py_content += f"            e.player.add_item('矿泉水', 3)\n"
                if "消防斧" in prob_outcome: py_content += f"            e.player.add_item('消防斧', 1)\n"
                if "绷带x1" in prob_outcome: py_content += f"            e.player.add_item('绷带', 1)\n"
                if "绷带x2" in prob_outcome: py_content += f"            e.player.add_item('绷带', 2)\n"
                if "高能量棒x1" in prob_outcome: py_content += f"            e.player.add_item('高能量棒', 1)\n"
                if "高能量棒x2" in prob_outcome: py_content += f"            e.player.add_item('高能量棒', 2)\n"
                if "急救包x1" in prob_outcome or "医疗箱x1" in prob_outcome: py_content += f"            e.player.add_item('急救包', 1)\n"
                if "急救包x2" in prob_outcome or "医疗箱x2" in prob_outcome: py_content += f"            e.player.add_item('急救包', 2)\n"

            else:
                clean_res = opt_res_raw

            if clean_res:
                if hp_mod < 0:
                    py_content += f"        print(f'{{Colors.FAIL}}结果: {clean_res}{{Colors.ENDC}}')\n"
                elif hp_mod > 0 or "获得" in clean_res or "安全" in clean_res:
                    py_content += f"        print(f'{{Colors.OKGREEN}}结果: {clean_res}{{Colors.ENDC}}')\n"
                else:
                    py_content += f"        print(f'结果: {clean_res}')\n"

            py_content += f"        final_sat = {sat_mod}\n"
            py_content += f"        if final_sat < 0 and hasattr(e.player, 'companion') and e.player.companion == '实习生':\n"
            py_content += f"            final_sat = int(final_sat * 0.7)\n"
            py_content += f"            print(f'{{Colors.OKGREEN}}(实习生帮你分担了部分体力活！){{Colors.ENDC}}')\n"

            if hp_mod != 0 or sat_mod != 0 or hyd_mod != 0:
                py_content += f"        e.player.update_stats(hp={hp_mod}, satiety=final_sat, hydration={hyd_mod})\n"

            if "实习生" in clean_res and "同伴" in clean_res: py_content += f"        e.player.companion = '实习生'\n"

            if "获得水x1" in clean_res or "矿泉水x1" in clean_res: py_content += f"        e.player.add_item('矿泉水', 1)\n"
            elif "获得水x2" in clean_res or "矿泉水x2" in clean_res: py_content += f"        e.player.add_item('矿泉水', 2)\n"
            elif "获得水x3" in clean_res or "矿泉水x3" in clean_res: py_content += f"        e.player.add_item('矿泉水', 3)\n"

            if "巧克力x1" in clean_res: py_content += f"        e.player.add_item('巧克力', 1)\n"
            elif "巧克力x2" in clean_res: py_content += f"        e.player.add_item('巧克力', 2)\n"

            if "饼干x1" in clean_res: py_content += f"        e.player.add_item('饼干', 1)\n"
            elif "饼干x2" in clean_res: py_content += f"        e.player.add_item('饼干', 2)\n"

            if "绷带x1" in clean_res: py_content += f"        e.player.add_item('绷带', 1)\n"
            elif "绷带x2" in clean_res: py_content += f"        e.player.add_item('绷带', 2)\n"

            if "急救包x1" in clean_res or "医疗箱x1" in clean_res: py_content += f"        e.player.add_item('急救包', 1)\n"
            elif "急救包x2" in clean_res or "医疗箱x2" in clean_res: py_content += f"        e.player.add_item('急救包', 2)\n"

            if "高级矿泉水x1" in clean_res: py_content += f"        e.player.add_item('高级矿泉水', 1)\n"
            elif "高级矿泉水x2" in clean_res: py_content += f"        e.player.add_item('高级矿泉水', 2)\n"

            if "高能量棒x1" in clean_res: py_content += f"        e.player.add_item('高能量棒', 1)\n"
            elif "高能量棒x2" in clean_res: py_content += f"        e.player.add_item('高能量棒', 2)\n"

            if "熟肉x1" in clean_res: py_content += f"        e.player.add_item('熟肉', 1)\n"
            elif "熟肉x2" in clean_res: py_content += f"        e.player.add_item('熟肉', 2)\n"

            if "打火机x1" in clean_res: py_content += f"        e.player.add_item('打火机', 1)\n"
            if "手电筒x1" in clean_res: py_content += f"        e.player.add_item('手电筒', 1)\n"

            if "失去绷带" in clean_res: py_content += f"        e.player.remove_item('绷带', 1)\n"
            if "失去急救包" in clean_res: py_content += f"        e.player.remove_item('急救包', 1)\n"
            if "失去矿泉水" in clean_res: py_content += f"        e.player.remove_item('矿泉水', 1)\n"
            if "失去饼干" in clean_res: py_content += f"        e.player.remove_item('饼干', 1)\n"
            if "消耗巧克力" in clean_res: py_content += f"        e.player.remove_item('巧克力', 1)\n"

            if "需要消防斧" in clean_res:
                py_content += f"        if '消防斧' not in e.player.inventory or e.player.inventory['消防斧'] <= 0:\n"
                py_content += f"            print(f'{{Colors.WARNING}}你没有消防斧，无法执行此操作！{{Colors.ENDC}}')\n"
                py_content += f"            return\n"
            if "需要手电筒" in clean_res:
                py_content += f"        if '手电筒' not in e.player.inventory or e.player.inventory['手电筒'] <= 0:\n"
                py_content += f"            print(f'{{Colors.WARNING}}你没有手电筒，无法执行此操作！{{Colors.ENDC}}')\n"
                py_content += f"            return\n"

            if "下1层" in clean_res:
                py_content += f"        drop = min(1, e.player.floor - 1)\n"
                py_content += f"        e.player.floor = max(1, e.player.floor - drop)\n"
            if "下2层" in clean_res:
                py_content += f"        drop = min(2, e.player.floor - 1)\n"
                py_content += f"        e.player.floor = max(1, e.player.floor - drop)\n"
            if "下3-8层" in clean_res:
                py_content += f"        drop = random.randint(3, 8)\n"
                py_content += f"        drop = min(drop, e.player.floor - 1)\n"
                py_content += f"        e.player.floor = max(1, e.player.floor - drop)\n"
                py_content += f"        if drop > 0: print(f'你向下滑降了 {{drop}} 层！')\n"

            opts_dict[opt_num] = (opt_title, f"opt{opt_num}")

        if cat != "Hazards" and not has_leave_opt and ev['name'] not in ["极度疲劳", "搜寻员工名册", "深槽跳跃", "安抚自己"]:
            leave_num = str(len(opts_dict) + 1)
            py_content += f"    def opt_leave(e):\n"
            py_content += f"        print('\\n你决定不冒风险，转身离开。')\n"
            py_content += f"        e.time.add_minutes(2, e.player)\n"
            opts_dict[leave_num] = ("小心绕开/放弃", "opt_leave")

        py_content += "    run_event(engine, desc, {\n"
        for k, v in opts_dict.items():
            py_content += f"        '{k}': ('{v[0]}', {v[1]}),\n"

        event_type = "normal"
        if cat == "Hazards": event_type = "hazard"
        elif cat == "Actions": event_type = "decision"
        elif cat == "NPCs": event_type = "combat"

        py_content += f"    }}, event_type='{event_type}')\n"

py_content += "\nALL_EVENTS = [\n    "
py_content += ",\n    ".join(all_event_funcs)
py_content += "\n]\n"
py_content += """
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
"""

with open("events_pool.py", "w") as f:
    f.write(py_content)

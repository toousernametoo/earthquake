import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource

# ==========================================
# 系统字体配置
# ==========================================
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 建筑参数与灾难设定配置表
# ==========================================
BUILDING_SPECS = {
    'StarRing': {'name': '中央星寰写字楼', 'N': (150, 150), 'R': 6, 'mu': 0.1, 'color': '#d62728'},
    'Landmark': {'name': '超高层商业地标', 'N': (60, 120), 'R': 5, 'mu': 0.9, 'color': '#ff7f0e'},
    'Office': {'name': '甲级写字楼', 'N': (25, 50), 'R': 4, 'mu': 0.3, 'color': '#1f77b4'},
    'Residential': {'name': '高密度住宅区', 'N': (15, 35), 'R': 3, 'mu': 0.8, 'color': '#2ca02c'},
    'OldRes': {'name': '老旧多层板楼', 'N': (5, 8), 'R': 1, 'mu': 0.2, 'color': '#bcbd22'},
    'Mall': {'name': '商业综合体', 'N': (4, 8), 'R': 3, 'mu': 0.4, 'color': '#9467bd'},
    'Hospital': {'name': '三甲综合医院', 'N': (8, 15), 'R': 5, 'mu': 0.05, 'color': '#17becf'},
    'School': {'name': '教育园区', 'N': (3, 6), 'R': 4, 'mu': 0.1, 'color': '#aec7e8'},
    'Parking': {'name': '立体停车库', 'N': (5, 10), 'R': 2, 'mu': 0.15, 'color': '#7f7f7f'},
    'Factory': {'name': '工业大跨度厂房', 'N': (3, 4), 'R': 2, 'mu': 0.5, 'color': '#8c564b'},
    'Historical': {'name': '历史保护建筑', 'N': (2, 4), 'R': 1, 'mu': 0.9, 'color': '#e377c2'},
    'Plaza': {'name': '城市绿地广场', 'N': (0, 0), 'R': 10, 'mu': 0.0, 'color': '#8fbc8f'},
}

GRID_SIZE = 80
CENTER = GRID_SIZE // 2


class CityDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("苍海市 1.0 - 灾难推演控制台 (平行地震波引擎版)")
        self.root.geometry("1400x850")

        self.buildings = []
        self.debris_rects = []
        self.anim_events = []

        # --- 平行地震波属性初始化 ---
        self.wave_theta = np.random.uniform(0, 2 * np.pi)  # 随机入侵角度
        self.wave_vx = np.cos(self.wave_theta)  # 传播方向向量 X
        self.wave_vy = np.sin(self.wave_theta)  # 传播方向向量 Y

        # 计算城市网格在波传播方向上的投影极值，用于确定波的起点和终点
        corners = [(0, 0), (GRID_SIZE, 0), (0, GRID_SIZE), (GRID_SIZE, GRID_SIZE)]
        projections = [x * self.wave_vx + y * self.wave_vy for x, y in corners]
        self.wave_pmin = min(projections)
        self.wave_pmax = max(projections)

        self.anim_id = None
        self.display_state = 'before'
        self.city_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

        self._run_simulation_backend()
        self._setup_ui()
        self.show_2d_map(state='before')

    def _generate_organic_roads(self, x1, y1, x2, y2, depth):
        if depth <= 0 or (x2 - x1) < 8 or (y2 - y1) < 8: return
        split_horiz = False if x2 - x1 > (y2 - y1) * 1.5 else (
            True if y2 - y1 > (x2 - x1) * 1.5 else np.random.choice([True, False]))

        if not split_horiz and (x2 - x1) >= 8:
            split_x = np.random.randint(x1 + 3, x2 - 3)
            w = np.random.choice([1, 2])
            self.city_grid[split_x:split_x + w, y1:y2] = -1
            self._generate_organic_roads(x1, y1, split_x, y2, depth - 1)
            self._generate_organic_roads(split_x + w, y1, x2, y2, depth - 1)
        elif split_horiz and (y2 - y1) >= 8:
            split_y = np.random.randint(y1 + 3, y2 - 3)
            w = np.random.choice([1, 2])
            self.city_grid[x1:x2, split_y:split_y + w] = -1
            self._generate_organic_roads(x1, y1, x2, split_y, depth - 1)
            self._generate_organic_roads(x1, split_y + w, x2, y2, depth - 1)

    def _run_simulation_backend(self):
        print(">>> [核心线程] 开始演算有机路网与建筑拓扑...")
        self._generate_organic_roads(0, 0, GRID_SIZE, GRID_SIZE, depth=7)

        plaza_radius = 6
        pz_min, pz_max = CENTER - plaza_radius, CENTER + plaza_radius

        for i in range(pz_min, pz_max + 1):
            for j in range(pz_min, pz_max + 1):
                if (i - CENTER) ** 2 + (j - CENTER) ** 2 <= plaza_radius ** 2:
                    self.city_grid[i, j] = -2

        star_w, star_h = 4, 4
        sx, sy = CENTER - star_w // 2, CENTER - star_h // 2
        self.city_grid[sx: sx + star_w, sy: sy + star_h] = 1
        self._add_building(sx, sy, star_w, star_h, 'StarRing')

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if self.city_grid[x, y] in [0, -2]:
                    dist_to_center = np.sqrt((x - CENTER) ** 2 + (y - CENTER) ** 2)
                    max_w, max_h = 1, 1
                    while x + max_w < GRID_SIZE and self.city_grid[x + max_w, y] in [0, -2] and max_w < 5: max_w += 1
                    while y + max_h < GRID_SIZE and self.city_grid[x, y + max_h] in [0, -2] and max_h < 5: max_h += 1

                    target_w = np.random.randint(1, max_w + 1) if max_w > 1 else 1
                    target_h = np.random.randint(1, max_h + 1) if max_h > 1 else 1

                    area_valid = True
                    for i in range(x, x + target_w):
                        for j in range(y, y + target_h):
                            if self.city_grid[i, j] not in [0, -2]:
                                area_valid = False;
                                break

                    if area_valid:
                        if self.city_grid[x, y] == -2:
                            b_type = 'Plaza';
                            target_w, target_h = 1, 1
                        elif dist_to_center < 18:
                            b_type = np.random.choice(['Landmark', 'Office', 'Mall', 'Plaza'],
                                                      p=[0.15, 0.55, 0.20, 0.10])
                            if b_type == 'Mall': target_w, target_h = max(2, target_w), max(2, target_h)
                        elif dist_to_center < 35:
                            b_type = np.random.choice(
                                ['Office', 'Residential', 'Hospital', 'Parking', 'School', 'Plaza'],
                                p=[0.15, 0.35, 0.10, 0.10, 0.15, 0.15])
                        else:
                            b_type = np.random.choice(['Residential', 'OldRes', 'Factory', 'Historical', 'Plaza'],
                                                      p=[0.20, 0.30, 0.15, 0.15, 0.20])

                        if b_type in ['OldRes', 'Historical', 'Parking', 'Plaza']: target_w, target_h = min(2,
                                                                                                            target_w), min(
                            2, target_h)
                        self.city_grid[x: x + target_w, y: y + target_h] = 1
                        self._add_building(x, y, target_w, target_h, b_type)

        print(">>> [核心线程] 建筑规划完成，开始平行地震波广域破坏推演...")

        active_collapses = []
        for b in self.buildings:
            if b['type'] not in ['StarRing', 'Plaza']:
                # 【平行波距离计算】：建筑中心点在波传播方向上的投影减去起点投影
                cx, cy = b['x'] + b['w'] / 2, b['y'] + b['h'] / 2
                p_b = cx * self.wave_vx + cy * self.wave_vy
                wave_dist = p_b - self.wave_pmin
                b['dist_to_epi'] = wave_dist  # 在这里，dist代表距离地震波接触城市的首个切面的距离

                # 【全局烈度平衡】：衰减系数大幅降至 0.05，确保最远端烈度也能维持在 4 级以上
                intensity = max(4.0, 10.0 - wave_dist * 0.05)
                # 【破坏倍率提升】：基础倍率 2.2，确保全域均有真实倒塌分布
                prob = (intensity / 10.0) * (1.0 / b['spec']['R']) * 2.2

                if np.random.rand() < prob:
                    b['collapsed'] = True
                    b['z_final'] = max(0.5, b['z_init'] * (1 - b['spec']['mu']))
                    b['color_final'] = '#4a4a4a'
                    b['cause'] = "首轮平行地震波震垮"
                    active_collapses.append(b)
            else:
                cx, cy = b['x'] + b['w'] / 2, b['y'] + b['h'] / 2
                b['dist_to_epi'] = (cx * self.wave_vx + cy * self.wave_vy) - self.wave_pmin

        cascade_round = 1
        while active_collapses:
            new_collapses = []
            for b in active_collapses:
                source_h = b['z_init']
                source_mu = b['spec']['mu']
                impact_radius = (source_h / 5.0) * source_mu

                # 使用 np.round 真实还原比例，无低频保底
                coef = 0.40 if source_mu >= 0.8 else (0.35 if source_mu <= 0.3 else 0.20)
                fall_len = int(np.round((source_h / 4.0) * coef))

                if fall_len >= 1:
                    direction = np.random.choice(['N', 'S', 'E', 'W'])
                    bx, by, bw, bh = b['x'], b['y'], b['w'], b['h']
                    fx, fy, fw, fh = bx, by, bw, bh
                    if direction == 'N':
                        fy = by + bh; fh = fall_len
                    elif direction == 'S':
                        fy = by - fall_len; fh = fall_len
                    elif direction == 'E':
                        fx = bx + bw; fw = fall_len
                    elif direction == 'W':
                        fx = bx - fall_len; fw = fall_len

                    if fx < 0: fw += fx; fx = 0
                    if fy < 0: fh += fy; fy = 0
                    if fx + fw > GRID_SIZE: fw = GRID_SIZE - fx
                    if fy + fh > GRID_SIZE: fh = GRID_SIZE - fy

                    if fw > 0 and fh > 0:
                        if not (fx + fw < pz_min or fx > pz_max or fy + fh < pz_min or fy > pz_max):
                            pass
                        else:
                            self.debris_rects.append({
                                'x': fx, 'y': fy, 'w': fw, 'h': fh,
                                'dist_to_epi': b['dist_to_epi'] + 2,
                                'patch': None
                            })

                for other in self.buildings:
                    if not other['collapsed'] and other['type'] not in ['StarRing', 'Plaza']:
                        dx = (b['x'] + b['w'] / 2) - (other['x'] + other['w'] / 2)
                        dy = (b['y'] + b['h'] / 2) - (other['y'] + other['h'] / 2)
                        dist = max(1.0, np.sqrt(dx ** 2 + dy ** 2))

                        if dist <= impact_radius:
                            target_r = other['spec']['R']
                            # 【级联调整】：坚决执行 1.4 次方距离惩罚
                            p_cascade = (source_h / 25.0) * (1.0 / (dist ** 1.4)) * (1.0 / target_r) * source_mu * 0.25

                            if np.random.rand() < p_cascade:
                                other['collapsed'] = True
                                other['z_final'] = max(0.5, other['z_init'] * (1 - other['spec']['mu']))
                                other['color_final'] = '#4a4a4a'
                                other['cause'] = f"波及: 被[{b['spec']['name']}]势能震塌"
                                # 动画时序延后：确保在波阵面推过之后再发生级联反应
                                other['dist_to_epi'] = b['dist_to_epi'] + (dist * 0.3) + cascade_round
                                new_collapses.append(other)

            active_collapses = new_collapses
            cascade_round += 1

        for b in self.buildings:
            if b['collapsed']:
                self.anim_events.append({'dist': b['dist_to_epi'], 'type': 'b', 'obj': b})
        for d in self.debris_rects:
            self.anim_events.append({'dist': d['dist_to_epi'], 'type': 'd', 'obj': d})

        self.anim_events.sort(key=lambda x: x['dist'])

        print(f">>> [核心线程] 演算完毕。已生成 {len(self.anim_events)} 帧动画序列。")

    def _add_building(self, x, y, w, h, b_type):
        spec = BUILDING_SPECS[b_type]
        h_min, h_max = spec['N']
        height = np.random.randint(h_min, h_max + 1) if h_max > h_min else h_min

        self.buildings.append({
            'x': x, 'y': y, 'w': w, 'h': h,
            'type': b_type, 'spec': spec,
            'z_init': height, 'z_final': height,
            'color_init': spec['color'], 'color_final': spec['color'],
            'collapsed': False, 'cause': '正常',
            'patch': None, 'text_patch': None
        })

    def _setup_ui(self):
        left_frame = tk.Frame(self.root, width=320, bg='#f0f0f0', padx=15, pady=15)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(left_frame, text="视图控制台", font=("Microsoft YaHei", 14, "bold"), bg='#f0f0f0').pack(pady=(0, 15))

        btn_2d_before = tk.Button(left_frame, text="1. 震前俯视图 (2D/支持点击)",
                                  command=lambda: self.show_2d_map('before'), height=2, bg='#e1f5fe')
        btn_2d_before.pack(fill=tk.X, pady=5)

        btn_2d_after = tk.Button(left_frame, text="2. 震后俯视图 (2D/展示全域毁损)",
                                 command=lambda: self.show_2d_map('after'), height=2, bg='#e1f5fe')
        btn_2d_after.pack(fill=tk.X, pady=5)

        btn_animate = tk.Button(left_frame, text="▶ 播放平行地震波破坏动画", command=self.play_2d_animation, height=2,
                                bg='#ffcdd2', font=("Microsoft YaHei", 9, "bold"))
        btn_animate.pack(fill=tk.X, pady=5)

        ttk.Separator(left_frame, orient='horizontal').pack(fill=tk.X, pady=10)

        btn_3d_before = tk.Button(left_frame, text="3. 震前全景渲染 (3D/耗时)",
                                  command=lambda: self.show_3d_map('before'), height=2, bg='#f3e5f5')
        btn_3d_before.pack(fill=tk.X, pady=5)

        btn_3d_after = tk.Button(left_frame, text="4. 震后废墟渲染 (3D/耗时)",
                                 command=lambda: self.show_3d_map('after'), height=2, bg='#fff3e0')
        btn_3d_after.pack(fill=tk.X, pady=5)

        info_frame = tk.LabelFrame(left_frame, text="物理状态侦测面板 (鼠标点击)", font=("Microsoft YaHei", 10, "bold"),
                                   bg='#f0f0f0', padx=10, pady=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        self.info_labels = {}
        fields = [("目标类型", "type"), ("抗震/坍塌参数", "params"),
                  ("受灾动因", "cause"), ("当前状态", "status")]

        for name, key in fields:
            row = tk.Frame(info_frame, bg='#f0f0f0')
            row.pack(fill=tk.X, pady=4)
            tk.Label(row, text=f"{name}:", width=10, anchor='w', bg='#f0f0f0').pack(side=tk.LEFT)
            val_label = tk.Label(row, text="--", font=("Microsoft YaHei", 9, "bold"), fg="#333", bg='#f0f0f0',
                                 wraplength=170, justify="left")
            val_label.pack(side=tk.LEFT)
            self.info_labels[key] = val_label

        self.right_frame = tk.Frame(self.root, bg='white')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig = plt.Figure(figsize=(10, 8), dpi=100, facecolor='#1e1e2f')
        self.fig.subplots_adjust(right=0.85)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect('button_press_event', self.on_click_2d)

    def _cancel_animation(self):
        if self.anim_id:
            self.root.after_cancel(self.anim_id)
            self.anim_id = None

    def _add_legend(self, ax):
        handles = []
        for key, spec in BUILDING_SPECS.items():
            handles.append(mpatches.Patch(color=spec['color'], label=spec['name']))
        handles.append(mpatches.Patch(color='#4a4a4a', label='建筑主体废墟'))
        handles.append(mpatches.Patch(color='#3a3a40', label='倾覆波及带/掩埋道路'))

        ax.legend(handles=handles, loc='center left', bbox_to_anchor=(1.05, 0.5),
                  title="地图图例", facecolor='#2a2a35', edgecolor='none', labelcolor='white', title_fontsize=12,
                  fontsize=10)

    def show_2d_map(self, state='before'):
        self._cancel_animation()
        self.fig.clear()
        self.display_state = state

        self.ax_2d = self.fig.add_subplot(111)
        self.ax_2d.set_facecolor('#2a2a35')

        for b in self.buildings:
            color = b['color_init'] if state == 'before' else b['color_final']
            rect = Rectangle((b['x'], b['y']), b['w'], b['h'], facecolor=color, edgecolor='black', linewidth=0.5)
            self.ax_2d.add_patch(rect)
            b['patch'] = rect

            is_visible = (state == 'after' and b['collapsed'])
            b['text_patch'] = self.ax_2d.text(b['x'] + b['w'] / 2, b['y'] + b['h'] / 2, '×',
                                              color='red', ha='center', va='center', fontsize=8, visible=is_visible)

        for d in self.debris_rects:
            d_rect = Rectangle((d['x'], d['y']), d['w'], d['h'], facecolor='#3a3a40', edgecolor='none', alpha=0.8)
            d_rect.set_visible(state == 'after')
            self.ax_2d.add_patch(d_rect)
            d['patch'] = d_rect

        # 绘制平行地震波入侵方向的指示箭头 (在波源点外侧 10 格指向城市)
        source_x = -self.wave_vx * 15
        source_y = -self.wave_vy * 15
        # 寻找距离波源最近的城市角落作为箭头终点基准
        corners = [(0, 0), (GRID_SIZE, 0), (0, GRID_SIZE), (GRID_SIZE, GRID_SIZE)]
        closest_corner = min(corners, key=lambda c: c[0] * self.wave_vx + c[1] * self.wave_vy)

        arr_start_x = closest_corner[0] - self.wave_vx * 20
        arr_start_y = closest_corner[1] - self.wave_vy * 20
        arr_end_x = closest_corner[0] - self.wave_vx * 4
        arr_end_y = closest_corner[1] - self.wave_vy * 4

        self.ax_2d.annotate('平行波\n入侵方向', xy=(arr_end_x, arr_end_y), xytext=(arr_start_x, arr_start_y),
                            arrowprops=dict(facecolor='red', edgecolor='red', width=3, headwidth=10),
                            color='red', fontsize=10, weight='bold', ha='center', va='center')

        # 预加载平行波阵面实体线段 (Line2D)
        self.wave_line, = self.ax_2d.plot([], [], color='red', linewidth=3, alpha=0.6, solid_capstyle='round')
        self.wave_line.set_visible(False)

        self.ax_2d.set_xlim(-15, GRID_SIZE + 15)
        self.ax_2d.set_ylim(-15, GRID_SIZE + 15)
        self.ax_2d.set_aspect('equal')
        title_txt = "苍海市 - 震前俯视图 (优化绿地分布)" if state == 'before' else "苍海市 - 震后俯视图 (全局平行震波破坏与 1.4次衰减)"
        self.ax_2d.set_title(title_txt + "\n(在2D模式下点击任意色块，可查看被波及原因或废墟阻挡状态)", color='white',
                             pad=15, fontsize=14)
        self.ax_2d.set_axis_off()
        self._add_legend(self.ax_2d)
        self.canvas.draw()

    def play_2d_animation(self):
        self.show_2d_map(state='before')
        self.display_state = 'anim'
        self.ax_2d.set_title("⚠️ 正在进行平行地震波扫荡演算...", color='#ffcdd2', pad=15, fontsize=14, weight='bold')

        self.wave_dist = 0  # 波阵面推进距离
        self.anim_event_idx = 0
        self.wave_line.set_visible(True)

        self._animate_step()

    def _animate_step(self):
        self.wave_dist += 2.0

        # 计算当前波阵面的核心位置 (p_min 加上已推进的距离)
        current_p = self.wave_pmin + self.wave_dist

        # 波形直线方程的几何绘制：垂直于波传播方向的线段
        cx = current_p * self.wave_vx
        cy = current_p * self.wave_vy
        tangent_x = -self.wave_vy  # 垂直切线向量
        tangent_y = self.wave_vx

        # 画一条足够宽的线段贯穿整个城市
        lx = [cx - 120 * tangent_x, cx + 120 * tangent_x]
        ly = [cy - 120 * tangent_y, cy + 120 * tangent_y]
        self.wave_line.set_data(lx, ly)

        while self.anim_event_idx < len(self.anim_events) and self.anim_events[self.anim_event_idx][
            'dist'] <= self.wave_dist:
            ev = self.anim_events[self.anim_event_idx]
            if ev['type'] == 'b':
                obj = ev['obj']
                obj['patch'].set_facecolor('#4a4a4a')
                obj['text_patch'].set_visible(True)
            elif ev['type'] == 'd':
                obj = ev['obj']
                obj['patch'].set_visible(True)
            self.anim_event_idx += 1

        self.canvas.draw_idle()

        # 推进距离：直到完全覆盖城市的最远投影点
        if self.wave_pmin + self.wave_dist < self.wave_pmax + 10:
            self.anim_id = self.root.after(30, self._animate_step)
        else:
            self.ax_2d.set_title("苍海市 - 平行地震波演算播放完毕", color='white', pad=15, fontsize=14)
            self.wave_line.set_visible(False)
            self.canvas.draw_idle()
            self.display_state = 'after'
            self.anim_id = None

    def show_3d_map(self, state='before'):
        self._cancel_animation()
        self.fig.clear()
        self.display_state = '3d'
        ax = self.fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#1e1e2f')

        _x, _y, _z, _dx, _dy, _dz, _c = [], [], [], [], [], [], []

        for b in self.buildings:
            _x.append(b['x']);
            _y.append(b['y']);
            _z.append(0)
            _dx.append(b['w'] * 0.85);
            _dy.append(b['h'] * 0.85)
            _dz.append(b['z_init'] if state == 'before' else b['z_final'])
            _c.append(b['color_init'] if state == 'before' else b['color_final'])

        if state == 'after':
            for d in self.debris_rects:
                _x.append(d['x']);
                _y.append(d['y']);
                _z.append(0)
                _dx.append(d['w']);
                _dy.append(d['h'])
                _dz.append(1.5)
                _c.append('#3a3a40')

        ax.bar3d(0, 0, -1, GRID_SIZE, GRID_SIZE, 1, color='#2a2a35', shade=False)
        ls = LightSource(azdeg=315, altdeg=45)
        ax.bar3d(_x, _y, _z, _dx, _dy, _dz, color=_c, shade=True, lightsource=ls)

        ax.view_init(elev=50, azim=-55)
        ax.set_zlim(0, 160)
        ax.set_axis_off()
        title = "苍海市 - 震前 3D 全景" if state == 'before' else "苍海市 - 震后 3D 废墟 (全局全境波及)"
        ax.set_title(title, color='white', pad=15, fontsize=14)

        self._add_legend(ax)
        self.fig.tight_layout()
        self.canvas.draw()

    def on_click_2d(self, event):
        if self.display_state not in ['before', 'after'] or event.xdata is None or event.ydata is None:
            return

        cx, cy = event.xdata, event.ydata

        if self.display_state == 'after':
            for d in self.debris_rects:
                if d['x'] <= cx <= d['x'] + d['w'] and d['y'] <= cy <= d['y'] + d['h']:
                    self._update_debris_panel()
                    return

        for b in self.buildings:
            if b['x'] <= cx <= b['x'] + b['w'] and b['y'] <= cy <= b['y'] + b['h']:
                self._update_info_panel(b)
                return

    def _update_info_panel(self, b):
        self.info_labels["type"].config(text=f"[{b['spec']['name']}] (H:{b['z_init']})", fg="#333")
        self.info_labels["params"].config(text=f"抗震R={b['spec']['R']} | 倾覆系数={b['spec']['mu']}")
        self.info_labels["cause"].config(text=b['cause'] if b['collapsed'] else "未受到致命破坏")

        if b['collapsed']:
            if "波及" in b['cause']:
                self.info_labels["status"].config(text="连带坍塌 (被周围倒塌波及)", fg="#ff7f0e")
            else:
                self.info_labels["status"].config(text="初次坍塌 (自身结构震毁)", fg="red")
        else:
            self.info_labels["status"].config(text="结构完整 / 允许通行", fg="green")

    def _update_debris_panel(self):
        self.info_labels["type"].config(text="[散落瓦砾/掩埋道路]", fg="#4a4a4a")
        self.info_labels["params"].config(text="不适用 (N/A)")
        self.info_labels["cause"].config(text="由周围建筑倾覆飞溅砸落形成")
        self.info_labels["status"].config(text="道路堵塞 / 难以通行", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = CityDashboard(root)
    root.mainloop()

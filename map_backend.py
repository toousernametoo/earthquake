import numpy as np

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

class CityMapBackend:
    def __init__(self):
        self.buildings = []
        self.debris_rects = []
        self.anim_events = []
        self.city_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

        self.wave_theta = np.random.uniform(0, 2 * np.pi)
        self.wave_vx = np.cos(self.wave_theta)
        self.wave_vy = np.sin(self.wave_theta)

        corners = [(0, 0), (GRID_SIZE, 0), (0, GRID_SIZE), (GRID_SIZE, GRID_SIZE)]
        projections = [x * self.wave_vx + y * self.wave_vy for x, y in corners]
        self.wave_pmin = min(projections)
        self.wave_pmax = max(projections)

        self._run_simulation()

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

    def _run_simulation(self):
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
                                area_valid = False
                                break

                    if area_valid:
                        if self.city_grid[x, y] == -2:
                            b_type = 'Plaza'
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

                        if b_type in ['OldRes', 'Historical', 'Parking', 'Plaza']:
                            target_w, target_h = min(2, target_w), min(2, target_h)
                        self.city_grid[x: x + target_w, y: y + target_h] = 1
                        self._add_building(x, y, target_w, target_h, b_type)

        active_collapses = []
        for b in self.buildings:
            if b['type'] not in ['StarRing', 'Plaza']:
                cx, cy = b['x'] + b['w'] / 2, b['y'] + b['h'] / 2
                p_b = cx * self.wave_vx + cy * self.wave_vy
                wave_dist = p_b - self.wave_pmin
                b['dist_to_epi'] = wave_dist

                intensity = max(4.0, 10.0 - wave_dist * 0.05)
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
                        if fx + fw < pz_min or fx > pz_max or fy + fh < pz_min or fy > pz_max:
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
                            p_cascade = (source_h / 25.0) * (1.0 / (dist ** 1.4)) * (1.0 / target_r) * source_mu * 0.25

                            if np.random.rand() < p_cascade:
                                other['collapsed'] = True
                                other['z_final'] = max(0.5, other['z_init'] * (1 - other['spec']['mu']))
                                other['color_final'] = '#4a4a4a'
                                other['cause'] = f"波及: 被[{b['spec']['name']}]势能震塌"
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

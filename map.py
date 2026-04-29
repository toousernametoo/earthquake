import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource
from map_backend import CityMapBackend, BUILDING_SPECS, GRID_SIZE

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class CityDashboard:
    def __init__(self, root, backend):
        self.root = root
        self.backend = backend
        self.root.title("苍海市 1.0 - 灾难推演控制台 (分离渲染版)")
        self.root.geometry("1400x850")

        self.anim_id = None
        self.display_state = 'before'

        self._setup_ui()
        self.show_2d_map(state='before')

    # ... GUI methods ...
    def _setup_ui(self):
        left_frame = tk.Frame(self.root, width=320, bg='#f0f0f0', padx=15, pady=15)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(left_frame, text="视图控制台", font=("Microsoft YaHei", 14, "bold"), bg='#f0f0f0').pack(pady=(0, 15))

        tk.Button(left_frame, text="1. 震前俯视图", command=lambda: self.show_2d_map('before'), height=2).pack(fill=tk.X, pady=5)
        tk.Button(left_frame, text="2. 震后俯视图", command=lambda: self.show_2d_map('after'), height=2).pack(fill=tk.X, pady=5)

        self.right_frame = tk.Frame(self.root, bg='white')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig = plt.Figure(figsize=(10, 8), dpi=100, facecolor='#1e1e2f')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_2d_map(self, state='before'):
        self.fig.clear()
        self.ax_2d = self.fig.add_subplot(111)
        self.ax_2d.set_facecolor('#2a2a35')

        for b in self.backend.buildings:
            color = b['color_init'] if state == 'before' else b['color_final']
            rect = Rectangle((b['x'], b['y']), b['w'], b['h'], facecolor=color, edgecolor='black', linewidth=0.5)
            self.ax_2d.add_patch(rect)
            b['patch'] = rect

        for d in self.backend.debris_rects:
            d_rect = Rectangle((d['x'], d['y']), d['w'], d['h'], facecolor='#3a3a40', edgecolor='none', alpha=0.8)
            d_rect.set_visible(state == 'after')
            self.ax_2d.add_patch(d_rect)
            d['patch'] = d_rect

        self.ax_2d.set_xlim(-15, GRID_SIZE + 15)
        self.ax_2d.set_ylim(-15, GRID_SIZE + 15)
        self.ax_2d.set_aspect('equal')
        self.ax_2d.set_axis_off()
        self.canvas.draw()

if __name__ == "__main__":
    backend = CityMapBackend()
    root = tk.Tk()
    app = CityDashboard(root, backend)
    root.mainloop()

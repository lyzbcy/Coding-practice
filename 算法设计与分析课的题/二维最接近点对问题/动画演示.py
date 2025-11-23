"""
二维最接近点对问题 - 动画演示
使用 matplotlib 手动控制分治算法的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class ClosestPairAnimation:
    def __init__(self, points):
        self.points = points.copy()
        self.n = len(points)
        self.steps = []
        self.current_step = 0
        
        # 按x坐标排序
        self.points.sort(key=lambda p: (p[0], p[1]))
        
        self.code_lines = [
            "double closestUtil(Point points[], int n) {",
            "    if (n <= 3) return bruteForce(points, n);",
            "    int mid = n / 2;",
            "    double dl = closestUtil(points, mid);",
            "    double dr = closestUtil(points+mid, n-mid);",
            "    double d = min(dl, dr);",
            "    // 构建条带",
            "    double stripMin = stripClosest(strip, d);",
            "    return min(d, stripMin);",
            "}",
        ]
        
        self._simulate_algorithm(0, self.n, 0)
        
        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        self.fig.canvas.manager.set_window_title('二维最接近点对问题 - 动画演示（手动控制）')
        
        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
    
    def _distance(self, p1, p2):
        """计算两点间距离"""
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.sqrt(dx * dx + dy * dy)
    
    def _brute_force(self, points, left, right):
        """暴力法计算最短距离"""
        min_dist = float('inf')
        for i in range(left, right):
            for j in range(i + 1, right):
                dist = self._distance(self.points[i], self.points[j])
                if dist < min_dist:
                    min_dist = dist
        return min_dist
    
    def _simulate_algorithm(self, left, right, depth):
        """模拟分治算法，记录每一步"""
        n = right - left
        
        # 记录当前状态
        self.steps.append({
            'type': 'enter',
            'left': left,
            'right': right,
            'depth': depth,
            'action': f'进入递归：处理区间 [{left}, {right})，共 {n} 个点',
            'code_highlight': [0],
            'explanations': [
                f'当前处理区间包含 {n} 个点（索引 {left} 到 {right-1}）',
                f'递归深度：{depth}'
            ]
        })
        
        # 递归终止条件
        if n <= 3:
            min_dist = self._brute_force(self.points, left, right)
            self.steps.append({
                'type': 'brute',
                'left': left,
                'right': right,
                'depth': depth,
                'min_dist': min_dist,
                'action': f'点数 ≤ 3，使用暴力法，最短距离 = {min_dist:.2f}',
                'code_highlight': [1],
                'explanations': [
                    f'在区间 [{left}, {right}) 中暴力枚举所有点对',
                    f'找到最短距离：{min_dist:.2f}'
                ]
            })
            return min_dist
        
        # 分割
        mid = left + n // 2
        mid_x = self.points[mid][0]
        
        self.steps.append({
            'type': 'split',
            'left': left,
            'right': right,
            'mid': mid,
            'mid_x': mid_x,
            'depth': depth,
            'action': f'分割：中点索引 {mid}，x坐标 = {mid_x}',
            'code_highlight': [2],
            'explanations': [
                f'将区间分为两部分：左 [{left}, {mid})，右 [{mid}, {right})',
                f'分割线 x = {mid_x}'
            ]
        })
        
        # 递归左半部分
        dl = self._simulate_algorithm(left, mid, depth + 1)
        
        self.steps.append({
            'type': 'left_result',
            'left': left,
            'right': right,
            'mid': mid,
            'depth': depth,
            'dl': dl,
            'action': f'左半部分结果：最短距离 = {dl:.2f}',
            'code_highlight': [3],
            'explanations': [
                f'左区间 [{left}, {mid}) 的最短距离：{dl:.2f}'
            ]
        })
        
        # 递归右半部分
        dr = self._simulate_algorithm(mid, right, depth + 1)
        
        self.steps.append({
            'type': 'right_result',
            'left': left,
            'right': right,
            'mid': mid,
            'depth': depth,
            'dr': dr,
            'action': f'右半部分结果：最短距离 = {dr:.2f}',
            'code_highlight': [4],
            'explanations': [
                f'右区间 [{mid}, {right}) 的最短距离：{dr:.2f}'
            ]
        })
        
        # 合并
        d = min(dl, dr)
        
        self.steps.append({
            'type': 'merge_start',
            'left': left,
            'right': right,
            'mid': mid,
            'mid_x': mid_x,
            'depth': depth,
            'd': d,
            'action': f'合并：取左右最小值 d = {d:.2f}，构建条带区域',
            'code_highlight': [5, 6],
            'explanations': [
                f'左右两部分的最短距离：{d:.2f}',
                f'构建条带：距离中线 x={mid_x} 在 d 范围内的点'
            ]
        })
        
        # 构建条带
        strip = []
        for i in range(left, right):
            if abs(self.points[i][0] - mid_x) < d:
                strip.append(i)
        
        # 按y坐标排序条带中的点
        strip_sorted = sorted(strip, key=lambda i: (self.points[i][1], self.points[i][0]))
        
        self.steps.append({
            'type': 'strip',
            'left': left,
            'right': right,
            'mid': mid,
            'mid_x': mid_x,
            'depth': depth,
            'd': d,
            'strip': strip_sorted,
            'action': f'条带区域：包含 {len(strip_sorted)} 个点，检查跨中线点对',
            'code_highlight': [7],
            'explanations': [
                f'条带内共有 {len(strip_sorted)} 个点',
                '按 y 坐标排序后，每个点最多检查其后 6 个点'
            ]
        })
        
        # 计算条带内的最短距离
        strip_min = d
        for i in range(len(strip_sorted)):
            for j in range(i + 1, len(strip_sorted)):
                idx1, idx2 = strip_sorted[i], strip_sorted[j]
                if self.points[idx2][1] - self.points[idx1][1] >= d:
                    break
                dist = self._distance(self.points[idx1], self.points[idx2])
                if dist < strip_min:
                    strip_min = dist
                    self.steps.append({
                        'type': 'strip_check',
                        'left': left,
                        'right': right,
                        'mid': mid,
                        'mid_x': mid_x,
                        'depth': depth,
                        'd': d,
                        'strip': strip_sorted,
                        'check_i': i,
                        'check_j': j,
                        'dist': dist,
                        'action': f'检查点对 ({idx1}, {idx2})，距离 = {dist:.2f}',
                        'code_highlight': [7],
                        'explanations': [
                            f'点 {idx1} 和点 {idx2} 的距离：{dist:.2f}',
                            f'更新条带内最短距离'
                        ]
                    })
        
        result = min(d, strip_min)
        
        self.steps.append({
            'type': 'merge_end',
            'left': left,
            'right': right,
            'mid': mid,
            'depth': depth,
            'd': d,
            'strip_min': strip_min,
            'result': result,
            'action': f'合并完成：最终最短距离 = {result:.2f}',
            'code_highlight': [8],
            'explanations': [
                f'条带内最短距离：{strip_min:.2f}',
                f'全局最短距离：{result:.2f}'
            ]
        })
        
        return result
    
    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step
        
        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index
        
        self.ax.clear()
        step_data = self.steps[step_index]
        
        # 设置坐标轴
        if self.points:
            xs = [p[0] for p in self.points]
            ys = [p[1] for p in self.points]
            x_min, x_max = min(xs), max(xs)
            y_min, y_max = min(ys), max(ys)
            x_range = x_max - x_min
            y_range = y_max - y_min
            margin = max(x_range, y_range) * 0.1
        else:
            x_min = y_min = 0
            x_max = y_max = 10
            margin = 1
        
        self.ax.set_xlim(x_min - margin, x_max + margin)
        self.ax.set_ylim(y_min - margin, y_max + margin)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('X 坐标', fontsize=12)
        self.ax.set_ylabel('Y 坐标', fontsize=12)
        
        # 标题
        self.ax.set_title(
            f'步骤 {step_index + 1}/{len(self.steps)}: {step_data["action"]}',
            fontsize=14, fontweight='bold', pad=20
        )
        
        # 绘制所有点
        for i, point in enumerate(self.points):
            color = 'blue'
            size = 100
            alpha = 0.6
            
            # 根据步骤类型高亮不同的点
            if step_data['type'] in ['split', 'merge_start', 'strip', 'strip_check', 'merge_end']:
                left = step_data.get('left', 0)
                right = step_data.get('right', self.n)
                mid = step_data.get('mid', 0)
                mid_x = step_data.get('mid_x', 0)
                d = step_data.get('d', 0)
                
                if left <= i < right:
                    if i < mid:
                        color = 'lightblue'
                    elif i >= mid:
                        color = 'lightcoral'
                    else:
                        color = 'blue'
                    
                    # 条带内的点
                    if step_data['type'] in ['strip', 'strip_check']:
                        strip = step_data.get('strip', [])
                        if i in strip:
                            color = 'yellow'
                            size = 150
                            alpha = 0.8
                    
                    # 正在检查的点对
                    if step_data['type'] == 'strip_check':
                        check_i = step_data.get('check_i', -1)
                        check_j = step_data.get('check_j', -1)
                        strip = step_data.get('strip', [])
                        if check_i >= 0 and check_j >= 0 and i in [strip[check_i], strip[check_j]]:
                            color = 'red'
                            size = 200
                            alpha = 1.0
            
            self.ax.scatter(point[0], point[1], c=color, s=size, alpha=alpha, 
                          edgecolors='black', linewidths=1.5, zorder=5)
            self.ax.text(point[0], point[1] + margin * 0.05, f'P{i}', 
                        fontsize=9, ha='center', zorder=6)
        
        # 绘制分割线
        if step_data['type'] in ['split', 'merge_start', 'strip', 'strip_check', 'merge_end']:
            mid_x = step_data.get('mid_x', None)
            if mid_x is not None:
                self.ax.axvline(x=mid_x, color='green', linestyle='--', 
                              linewidth=2, alpha=0.7, label='分割线', zorder=1)
                
                # 绘制条带区域
                d = step_data.get('d', 0)
                if d > 0:
                    rect = patches.Rectangle(
                        (mid_x - d, y_min - margin), 2 * d, y_max - y_min + 2 * margin,
                        linewidth=2, edgecolor='orange', facecolor='yellow', 
                        alpha=0.2, zorder=0, label='条带区域'
                    )
                    self.ax.add_patch(rect)
        
        # 绘制正在检查的点对连线
        if step_data['type'] == 'strip_check':
            check_i = step_data.get('check_i', -1)
            check_j = step_data.get('check_j', -1)
            strip = step_data.get('strip', [])
            if check_i >= 0 and check_j >= 0:
                idx1, idx2 = strip[check_i], strip[check_j]
                p1, p2 = self.points[idx1], self.points[idx2]
                self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 
                           'r-', linewidth=2, alpha=0.7, zorder=4)
                dist = step_data.get('dist', 0)
                mid_x = (p1[0] + p2[0]) / 2
                mid_y = (p1[1] + p2[1]) / 2
                self.ax.text(mid_x, mid_y, f'{dist:.2f}', 
                           fontsize=10, ha='center', va='center',
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                           zorder=7)
        
        # 说明文字
        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'• {line}' for line in explanations)
            self.ax.text(0.02, 0.98, explain_text, transform=self.ax.transAxes,
                        fontsize=10, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # 代码面板
        self._draw_code_panel(step_data)
        
        # 操作提示
        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(0.5, 0.02, controls_text, transform=self.ax.transAxes,
                    ha='center', fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6))
        
        self.fig.canvas.draw()
    
    def _draw_code_panel(self, step_data):
        """绘制代码面板"""
        highlight = set(step_data.get('code_highlight', []))
        
        code_text = 'C 代码同步显示\n'
        for idx, line in enumerate(self.code_lines):
            if idx in highlight:
                code_text += f'▶ {line}\n'
            else:
                code_text += f'  {line}\n'
        
        self.ax.text(0.98, 0.5, code_text, transform=self.ax.transAxes,
                    fontsize=9, family='monospace', verticalalignment='center',
                    horizontalalignment='right',
                    bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.8))
    
    def _on_key_press(self, event):
        if event.key in ('right', ' ', 'enter'):
            if self.current_step < len(self.steps) - 1:
                self.current_step += 1
                self._draw_step()
        elif event.key == 'left':
            if self.current_step > 0:
                self.current_step -= 1
                self._draw_step()
        elif event.key == 'home':
            self.current_step = 0
            self._draw_step()
        elif event.key == 'end':
            self.current_step = len(self.steps) - 1
            self._draw_step()
        elif event.key in ('q', 'escape'):
            plt.close(self.fig)
    
    def show(self):
        self._draw_step(0)
        plt.tight_layout()
        plt.show()


def main():
    print("=" * 60)
    print("二维最接近点对问题 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: 4个点 (0,0), (0,1), (1,0), (1,1)")
    print("2. 示例 2: 3个点 (0,0), (1,1), (2,2)")
    print("3. 示例 3: 6个点（随机分布）")
    print("4. 自定义输入")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    if choice == '1':
        points = [(0, 0), (0, 1), (1, 0), (1, 1)]
    elif choice == '2':
        points = [(0, 0), (1, 1), (2, 2)]
    elif choice == '3':
        import random
        random.seed(42)
        points = [(random.randint(0, 10), random.randint(0, 10)) for _ in range(6)]
    elif choice == '4':
        n = int(input("请输入点的个数: "))
        points = []
        for i in range(n):
            x, y = map(int, input(f"点 {i+1} 的坐标 (x y): ").split())
            points.append((x, y))
    else:
        print("无效选择，使用示例 1")
        points = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    print("\n开始演示...")
    print(f"点数: {len(points)}")
    print("操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")
    
    anim = ClosestPairAnimation(points)
    anim.show()


if __name__ == '__main__':
    main()


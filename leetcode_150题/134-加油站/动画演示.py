"""
LeetCode 134. 加油站 - 动画演示
使用 matplotlib 手动观察 total、tank、start 的变化
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches


# 设置中文字体，避免出现乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class GasStationAnimation:
    def __init__(self, gas, cost):
        self.gas = gas
        self.cost = cost
        self.n = len(gas)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.n, 6)
        self.x_limit = self.visual_width + 18

        self.code_lines = [
            "int canCompleteCircuit(int* gas, int gasSize, int* cost, int costSize) {",
            "    if (gasSize != costSize) {",
            "        return -1;",
            "    }",
            "    int total = 0;",
            "    int tank = 0;",
            "    int start = 0;",
            "    for (int i = 0; i < gasSize; i++) {",
            "        int gain = gas[i] - cost[i];",
            "        total += gain;",
            "        tank += gain;",
            "        if (tank < 0) {",
            "            start = i + 1;",
            "            tank = 0;",
            "        }",
            "    }",
            "    return total >= 0 ? start % gasSize : -1;",
            "}",
        ]

        self._simulate()

        self.fig, self.ax = plt.subplots(figsize=(15, 9))
        self.fig.canvas.manager.set_window_title('加油站 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-4, 9)
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate(self):
        total = 0
        tank = 0
        start = 0

        self.steps.append({
            'index': None,
            'start': start,
            'tank': tank,
            'tank_display': tank,
            'total': total,
            'gain': None,
            'pending_reset': False,
            'action': '初始化：total=0，tank=0，start=0，准备从 0 号站出发',
            'explanations': [
                'total 用来判断整圈是否有解。',
                'tank 表示当前起点能否继续前进，start 记录候选起点。'
            ],
            'code_highlight': [0, 1, 4, 5, 6]
        })

        for i in range(self.n):
            gain = self.gas[i] - self.cost[i]
            total += gain
            tank += gain

            action = (f'站点 {i}：加 {self.gas[i]} 升，耗 {self.cost[i]} 升，'
                      f'净变化 gain={gain}，tank -> {tank}')
            explanations = [
                f'累计 total = {total}，用于最终判断是否存在解。',
                f'tank 更新为 {tank}，若为负则说明当前起点无法到达下一站。'
            ]
            code_lines = [7, 8, 9, 10]
            pending_reset = False
            reset_to = start
            tank_display = tank

            if tank < 0:
                pending_reset = True
                reset_to = (i + 1) % self.n
                tank_display = tank
                explanations.append(
                    f'tank < 0，说明从 start={start} 出发无法经过站点 {i}，'
                    f'将起点重置为 {reset_to} 并清空油箱。'
                )
                action += f' → tank<0，重置 start={reset_to}，下一轮 tank=0'
                code_lines.extend([11, 12, 13])
                start = reset_to
                tank = 0

            self.steps.append({
                'index': i,
                'start': start,
                'tank_display': tank_display,
                'total': total,
                'gain': gain,
                'pending_reset': pending_reset,
                'reset_to': reset_to,
                'action': action,
                'explanations': explanations,
                'code_highlight': code_lines
            })

        result = start if total >= 0 else -1
        action = (f'遍历完成：total={total}，'
                  f'{">=0，返回起点 " + str(result) if total >= 0 else "<0，返回 -1"}')
        self.steps.append({
            'index': None,
            'start': start,
            'tank': 0,
            'tank_display': 0,
            'total': total,
            'gain': None,
            'pending_reset': False,
            'reset_to': None,
            'action': action,
            'explanations': [
                'total >= 0 说明全程油量不亏，返回记录下来的 start。',
                'total < 0 则代表总油量不足，无论从哪出发都无法跑完一圈。'
            ],
            'code_highlight': [15, 16]
        })

    def _draw_array(self, step_data):
        for idx in range(self.n):
            base_color = 'lavender'
            if idx == step_data.get('start', -1):
                base_color = 'lightblue'
            rect = patches.Rectangle(
                (idx - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor=base_color
            )
            self.ax.add_patch(rect)
            self.ax.text(idx, 1.3, f'站 {idx}', ha='center', fontsize=11, color='dimgray')
            self.ax.text(
                idx, 1,
                f'加 {self.gas[idx]}',
                ha='center', va='center', fontsize=12, color='black'
            )
            self.ax.text(
                idx, 0.6,
                f'耗 {self.cost[idx]}',
                ha='center', va='center', fontsize=11, color='firebrick'
            )

        current = step_data.get('index')
        if current is not None and 0 <= current < self.n:
            rect = patches.Rectangle(
                (current - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=3, edgecolor='orange', facecolor='none'
            )
            self.ax.add_patch(rect)
            self.ax.annotate(
                '当前站点',
                xy=(current, 1.5), xytext=(current, 2.4),
                arrowprops=dict(arrowstyle='->', color='orange', lw=2),
                ha='center', color='orange'
            )

        start_idx = step_data.get('start')
        if start_idx is not None and start_idx < self.n:
            self.ax.annotate(
                f'start={start_idx}',
                xy=(start_idx, -0.2), xytext=(start_idx, -1.3),
                arrowprops=dict(arrowstyle='->', color='steelblue', lw=2),
                ha='center', color='steelblue'
            )
        else:
            self.ax.text(
                self.n - 0.5, -1.2,
                f'start={start_idx}',
                fontsize=12, color='steelblue',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7)
            )

    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step

        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index

        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-4, 9)

        step_data = self.steps[step_index]

        self.ax.text(
            max(self.n / 2, 3), 8.3,
            f'步骤 {step_index + 1}/{len(self.steps)}',
            ha='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.85)
        )
        self.ax.text(
            max(self.n / 2, 3), 7.3,
            step_data['action'],
            ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )

        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(
                max(self.n / 2, 3), 6.2,
                explain_text,
                ha='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )

        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            max(self.n / 2, 3), 5.1,
            controls_text,
            ha='center', fontsize=10.5,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.7)
        )

        info_text = (f'total = {step_data.get("total", 0)}   |   '
                     f'tank = {step_data.get("tank_display", step_data.get("tank", 0))}   |   '
                     f'start = {step_data.get("start", 0)}')
        self.ax.text(
            -0.5, 4.6,
            info_text,
            fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.9)
        )

        if step_data.get('pending_reset'):
            self.ax.text(
                -0.5, 3.9,
                f'tank < 0，下一轮将从站 {step_data["reset_to"]} 重启，油箱清零',
                fontsize=11,
                bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.9)
            )

        self.ax.text(-0.5, 1, '站点信息：', ha='right', va='center',
                     fontsize=13, fontweight='bold')
        self._draw_array(step_data)
        self._draw_code_panel(step_data)
        self._draw_legend()

        self.fig.canvas.draw()

    def _draw_code_panel(self, step_data):
        start_x = self.visual_width + 1.2
        start_y = 4.8
        line_height = 0.6
        highlight = set(step_data.get('code_highlight', []))

        self.ax.text(
            start_x, start_y + 2.4,
            'C 代码同步显示', fontsize=13, fontweight='bold', ha='left',
            bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.6)
        )

        for idx, line in enumerate(self.code_lines):
            y = start_y - idx * line_height
            facecolor = 'peachpuff' if idx in highlight else 'white'
            self.ax.text(
                start_x, y, f'{idx + 1:02d} {line}',
                ha='left', va='center', fontsize=10, family='monospace',
                bbox=dict(boxstyle='round', facecolor=facecolor, alpha=0.95, pad=0.3)
            )

    def _draw_legend(self):
        legend_items = [
            ('lightblue', '当前候选起点 start'),
            ('lavender', '普通站点'),
            ('橙色描边', '正在访问的站点'),
        ]
        for i, (color, text) in enumerate(legend_items):
            if color == '橙色描边':
                self.ax.add_patch(patches.Rectangle(
                    (i * 2, -2.3), 0.7, 0.7,
                    facecolor='white', edgecolor='orange', linewidth=3
                ))
            else:
                self.ax.add_patch(patches.Rectangle(
                    (i * 2, -2.3), 0.7, 0.7,
                    facecolor=color, edgecolor='black'
                ))
            self.ax.text(i * 2 + 0.9, -1.95, text, fontsize=10, va='center')

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


def _parse_custom_input():
    try:
        gas = list(map(int, input("请输入 gas 数组（空格分隔）：").strip().split()))
        cost = list(map(int, input("请输入 cost 数组（空格分隔）：").strip().split()))
        if len(gas) != len(cost):
            print("⚠️ gas 与 cost 长度必须一致，已放弃自定义输入。")
            return [1, 2, 3, 4, 5], [3, 4, 5, 1, 2]
        return gas, cost
    except ValueError:
        print("⚠️ 输入格式不正确，已使用默认示例。")
        return [1, 2, 3, 4, 5], [3, 4, 5, 1, 2]


def main():
    print("=" * 62)
    print("LeetCode 134. 加油站 - 动画演示")
    print("=" * 62)
    print("\n选择示例：")
    print("1. 官方示例：gas=[1,2,3,4,5], cost=[3,4,5,1,2]")
    print("2. 无解示例：gas=[2,3,4], cost=[3,4,3]")
    print("3. 单一站点：gas=[5], cost=[4]")
    print("4. 自定义输入")

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        gas = [1, 2, 3, 4, 5]
        cost = [3, 4, 5, 1, 2]
    elif choice == '2':
        gas = [2, 3, 4]
        cost = [3, 4, 3]
    elif choice == '3':
        gas = [5]
        cost = [4]
    elif choice == '4':
        gas, cost = _parse_custom_input()
    else:
        print("无效选择，默认使用示例 1。")
        gas = [1, 2, 3, 4, 5]
        cost = [3, 4, 5, 1, 2]

    print("\n开始演示...")
    print(f"gas  = {gas}")
    print(f"cost = {cost}")
    print("\n操作提示：")
    print("  空格 / →：下一步")
    print("  ←       ：上一步")
    print("  Home/End：跳转到起点 / 终点")
    print("  Q / Esc ：退出动画")
    print("⚠️ 先点击弹出的窗口以获得焦点，再使用键盘控制。\n")

    anim = GasStationAnimation(gas, cost)
    anim.show()


if __name__ == '__main__':
    main()



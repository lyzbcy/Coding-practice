"""
LeetCode 141. 环形链表 - 动画演示
使用 matplotlib 手动控制快慢指针的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class HasCycleAnimation:
    def __init__(self, values, pos):
        """
        初始化动画
        values: 链表节点的值列表，如 [3, 2, 0, -4]
        pos: 环的入口位置，-1 表示无环
        """
        self.values = values
        self.pos = pos
        self.length = len(values)
        self.has_cycle = pos != -1
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length * 2, 10)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "bool hasCycle(ListNode *head) {",
            "    if (head == NULL || head->next == NULL)",
            "        return false;",
            "    ListNode *slow = head;",
            "    ListNode *fast = head->next;",
            "    while (fast != NULL && fast->next != NULL) {",
            "        if (slow == fast)",
            "            return true;",
            "        slow = slow->next;",
            "        fast = fast->next->next;",
            "    }",
            "    return false;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        self.fig.canvas.manager.set_window_title('环形链表 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 10)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        if self.length == 0:
            self.steps.append({
                'slow': -1,
                'fast': -1,
                'action': '空链表，返回 false',
                'code_highlight': [0, 1, 2],
                'explanations': ['链表为空，不存在环。'],
                'meet': False,
                'finished': True
            })
            return

        if self.length == 1:
            self.steps.append({
                'slow': 0,
                'fast': -1,
                'action': '单节点链表，返回 false',
                'code_highlight': [0, 1, 2],
                'explanations': ['单节点链表，不存在环。'],
                'meet': False,
                'finished': True
            })
            return

        # 模拟链表结构
        slow = 0  # 慢指针位置
        fast = 1  # 快指针位置
        step_count = 0
        max_steps = self.length * 3  # 防止无限循环

        self.steps.append({
            'slow': slow,
            'fast': fast,
            'action': '初始化：slow=head，fast=head->next，开始检测',
            'code_highlight': [0, 3, 4],
            'explanations': [
                'slow 指针指向头节点，fast 指针指向第二个节点。',
                '我们将使用快慢指针检测是否存在环。'
            ],
            'meet': False,
            'finished': False
        })

        while step_count < max_steps:
            step_count += 1

            # 检查 fast 是否到达末尾
            if fast >= self.length or (fast + 1 >= self.length and not self.has_cycle):
                self.steps.append({
                    'slow': slow,
                    'fast': fast,
                    'action': f'fast 指针到达链表末尾（fast={fast}），无环，返回 false',
                    'code_highlight': [5, 11],
                    'explanations': [
                        'fast 指针已经到达链表末尾（NULL）。',
                        '如果存在环，fast 指针永远不会到达 NULL。',
                        '返回 false：链表中不存在环。'
                    ],
                    'meet': False,
                    'finished': True
                })
                break

            # 检查是否相遇
            if slow == fast:
                self.steps.append({
                    'slow': slow,
                    'fast': fast,
                    'action': f'✅ 快慢指针相遇（slow={slow}, fast={fast}），存在环，返回 true',
                    'code_highlight': [6, 7],
                    'explanations': [
                        f'slow 和 fast 指针在位置 {slow} 相遇。',
                        '如果链表没有环，快慢指针永远不会相遇。',
                        '返回 true：链表中存在环。'
                    ],
                    'meet': True,
                    'finished': True
                })
                break

            # 记录移动过程
            self.steps.append({
                'slow': slow,
                'fast': fast,
                'action': f'slow={slow}, fast={fast}，未相遇，继续移动',
                'code_highlight': [8, 9],
                'explanations': [
                    f'slow 指针在位置 {slow}，fast 指针在位置 {fast}。',
                    'slow 移动一步，fast 移动两步。'
                ],
                'meet': False,
                'finished': False
            })

            # 移动指针
            slow = (slow + 1) % self.length if self.has_cycle else slow + 1
            if self.has_cycle:
                fast = (fast + 2) % self.length
            else:
                fast = fast + 2

        # 如果超过最大步数（理论上不应该发生）
        if step_count >= max_steps:
            self.steps.append({
                'slow': slow,
                'fast': fast,
                'action': '超过最大步数，检测结束',
                'code_highlight': [],
                'explanations': ['检测过程超过预期步数。'],
                'meet': False,
                'finished': True
            })

    def _draw_linked_list(self, step_data):
        """绘制链表"""
        slow = step_data['slow']
        fast = step_data['fast']
        meet = step_data.get('meet', False)

        # 计算节点位置（圆形布局，如果有环）
        node_positions = []
        center_x = self.visual_width / 2
        center_y = 4
        radius = min(self.length * 0.8, 4)

        if self.has_cycle and self.length > 0:
            # 圆形布局
            for i in range(self.length):
                angle = 2 * np.pi * i / self.length - np.pi / 2
                x = center_x + radius * np.cos(angle)
                y = center_y + radius * np.sin(angle)
                node_positions.append((x, y))
        else:
            # 线性布局
            spacing = 1.5
            start_x = 1
            for i in range(self.length):
                x = start_x + i * spacing
                y = center_y
                node_positions.append((x, y))

        # 绘制节点
        for i, (x, y) in enumerate(node_positions):
            # 确定节点颜色
            if i == slow and i == fast:
                color = 'red'  # 相遇点
            elif i == slow:
                color = 'lightgreen'  # slow 指针
            elif i == fast:
                color = 'lightblue'  # fast 指针
            elif i < max(slow, fast) if slow >= 0 and fast >= 0 else False:
                color = 'lightgray'  # 已访问
            else:
                color = 'wheat'  # 未访问

            # 绘制节点（圆形）
            circle = plt.Circle((x, y), 0.4, color=color, ec='black', lw=2, zorder=3)
            self.ax.add_patch(circle)

            # 显示节点值
            self.ax.text(x, y, str(self.values[i]), ha='center', va='center',
                        fontsize=12, fontweight='bold', zorder=4)

            # 显示节点索引
            self.ax.text(x, y - 0.7, f'[{i}]', ha='center', va='center',
                        fontsize=9, color='gray', zorder=4)

        # 绘制箭头（连接）
        for i in range(self.length):
            if i < self.length - 1:
                x1, y1 = node_positions[i]
                x2, y2 = node_positions[i + 1]
            elif self.has_cycle:
                # 最后一个节点指向环的入口
                x1, y1 = node_positions[i]
                x2, y2 = node_positions[self.pos]
            else:
                continue

            # 绘制箭头
            arrow = FancyArrowPatch((x1 + 0.3, y1), (x2 - 0.3, y2),
                                   arrowstyle='->', mutation_scale=20,
                                   color='black', lw=1.5, zorder=2)
            self.ax.add_patch(arrow)

        # 如果是环，绘制从最后一个节点到环入口的箭头
        if self.has_cycle and self.length > 0:
            x1, y1 = node_positions[-1]
            x2, y2 = node_positions[self.pos]
            # 使用曲线箭头
            arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                   arrowstyle='->', mutation_scale=20,
                                   color='red', lw=2, linestyle='--', zorder=1)
            self.ax.add_patch(arrow)

        # 绘制指针标签
        if slow >= 0:
            x, y = node_positions[slow]
            self.ax.annotate('slow', xy=(x, y + 0.6), xytext=(x, y + 1.2),
                            arrowprops=dict(arrowstyle='->', color='green', lw=2),
                            fontsize=12, color='green', ha='center', fontweight='bold', zorder=5)

        if fast >= 0 and fast < self.length:
            x, y = node_positions[fast]
            self.ax.annotate('fast', xy=(x, y + 0.6), xytext=(x, y + 1.5),
                            arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                            fontsize=12, color='blue', ha='center', fontweight='bold', zorder=5)

    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step

        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index

        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 10)

        step_data = self.steps[step_index]

        # 标题与说明
        self.ax.text(
            self.visual_width / 2, 9.5,
            f'步骤 {step_index + 1}/{len(self.steps)}',
            ha='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )

        self.ax.text(
            self.visual_width / 2, 8.6,
            step_data['action'],
            ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )

        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(
                self.visual_width / 2, 7.6,
                explain_text,
                ha='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )

        # 显示结果
        if step_data.get('finished'):
            if step_data.get('meet'):
                result_text = '✅ 存在环'
                result_color = 'lightgreen'
            else:
                result_text = '❌ 不存在环'
                result_color = 'lightcoral'
            self.ax.text(
                self.visual_width / 2, 6.8,
                result_text,
                ha='center', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor=result_color, alpha=0.8)
            )

        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            self.visual_width / 2, 6.2,
            controls_text,
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

        # 绘制链表
        if self.length > 0:
            self._draw_linked_list(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightgreen', 'slow 指针位置'),
            ('lightblue', 'fast 指针位置'),
            ('red', '快慢指针相遇点'),
            ('lightgray', '已访问节点'),
            ('wheat', '未访问节点')
        ]
        for i, (color, text) in enumerate(legend_items):
            y_pos = 1.8 - i * 0.3
            circle = plt.Circle((i % 3 * 3, y_pos), 0.2, color=color, ec='black')
            self.ax.add_patch(circle)
            self.ax.text(i % 3 * 3 + 0.4, y_pos, text, fontsize=9, va='center')

        self.fig.canvas.draw()

    def _draw_code_panel(self, step_data):
        start_x = self.visual_width + 1.5
        start_y = 4.5
        line_height = 0.5
        highlight = set(step_data.get('code_highlight', []))

        self.ax.text(start_x, start_y + 2.5, 'C 代码同步显示', fontsize=13,
                     fontweight='bold', ha='left',
                     bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.6))

        for idx, line in enumerate(self.code_lines):
            y = start_y - idx * line_height
            facecolor = 'peachpuff' if idx in highlight else 'white'
            self.ax.text(
                start_x, y, f'{idx + 1:02d} {line}',
                ha='left', va='center', fontsize=9, family='monospace',
                bbox=dict(boxstyle='round', facecolor=facecolor, alpha=0.9, pad=0.3)
            )

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
    print("LeetCode 141. 环形链表 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print('1. 示例 1: [3,2,0,-4], pos=1（有环）')
    print('2. 示例 2: [1,2], pos=0（有环）')
    print('3. 示例 3: [1], pos=-1（无环）')
    print('4. 简单示例: [1,2,3,4,5], pos=2（有环）')
    print('5. 自定义输入')

    choice = input("\n请输入选择 (1-5): ").strip()

    if choice == '1':
        values, pos = [3, 2, 0, -4], 1
    elif choice == '2':
        values, pos = [1, 2], 0
    elif choice == '3':
        values, pos = [1], -1
    elif choice == '4':
        values, pos = [1, 2, 3, 4, 5], 2
    elif choice == '5':
        values_str = input("请输入节点值（用逗号分隔，如：3,2,0,-4）: ").strip()
        values = [int(x.strip()) for x in values_str.split(',')]
        pos_str = input("请输入环的入口位置（-1 表示无环）: ").strip()
        pos = int(pos_str)
    else:
        print("无效选择，使用示例 1")
        values, pos = [3, 2, 0, -4], 1

    print("\n开始演示...")
    print(f'节点值: {values}')
    print(f'环入口位置: {pos}' + ('（有环）' if pos != -1 else '（无环）'))
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = HasCycleAnimation(values, pos)
    anim.show()


if __name__ == '__main__':
    main()


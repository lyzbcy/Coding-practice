"""
LeetCode 2. 两数相加 - 动画演示
使用 matplotlib 手动控制链表相加的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class ListNode:
    """链表节点类"""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class AddTwoNumbersAnimation:
    def __init__(self, l1_vals, l2_vals):
        """
        初始化动画
        l1_vals: 第一个链表的节点值列表
        l2_vals: 第二个链表的节点值列表
        """
        self.l1_vals = l1_vals
        self.l2_vals = l2_vals
        self.l1 = self._create_list(l1_vals)
        self.l2 = self._create_list(l2_vals)
        self.steps = []
        self.current_step = 0
        self.max_len = max(len(l1_vals), len(l2_vals)) + 2  # 预留进位空间
        self.visual_width = max(self.max_len * 3, 12)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "struct ListNode* addTwoNumbers(...) {",
            "    ListNode* dummy = new ListNode(0);",
            "    ListNode* current = dummy;",
            "    int carry = 0;",
            "    while (l1 || l2 || carry) {",
            "        int sum = carry;",
            "        if (l1) { sum += l1->val; l1 = l1->next; }",
            "        if (l2) { sum += l2->val; l2 = l2->next; }",
            "        carry = sum / 10;",
            "        int digit = sum % 10;",
            "        current->next = new ListNode(digit);",
            "        current = current->next;",
            "    }",
            "    return dummy->next;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(18, 12))
        self.fig.canvas.manager.set_window_title('两数相加 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-2, self.x_limit)
        self.ax.set_ylim(-4, 12)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _create_list(self, vals):
        """根据值列表创建链表"""
        if not vals:
            return None
        head = ListNode(vals[0])
        current = head
        for val in vals[1:]:
            current.next = ListNode(val)
            current = current.next
        return head

    def _list_to_array(self, head):
        """将链表转换为数组（用于显示）"""
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        l1 = self._create_list(self.l1_vals)
        l2 = self._create_list(self.l2_vals)
        
        # 创建虚拟头节点
        dummy = ListNode(0)
        current = dummy
        carry = 0
        result_vals = []

        # 初始化步骤
        self.steps.append({
            'l1_vals': self._list_to_array(l1),
            'l2_vals': self._list_to_array(l2),
            'l1_pos': 0,
            'l2_pos': 0,
            'result_vals': [],
            'carry': 0,
            'sum': 0,
            'digit': 0,
            'action': '初始化：创建虚拟头节点 dummy，carry=0',
            'code_highlight': [0, 1, 2, 3],
            'explanations': [
                '创建虚拟头节点 dummy，简化边界处理。',
                '初始化 current 指向 dummy，用于构建结果链表。',
                '初始化进位 carry = 0。'
            ],
            'finished': False
        })

        step_count = 0
        while l1 or l2 or carry != 0:
            step_count += 1
            sum_val = carry
            l1_val = l1.val if l1 else None
            l2_val = l2.val if l2 else None
            l1_pos = len(self._list_to_array(self.l1)) - len(self._list_to_array(l1)) if l1 else len(self.l1_vals)
            l2_pos = len(self._list_to_array(self.l2)) - len(self._list_to_array(l2)) if l2 else len(self.l2_vals)

            # 加上 l1 的当前位
            if l1:
                sum_val += l1.val
                l1 = l1.next
            else:
                l1_pos = -1

            # 加上 l2 的当前位
            if l2:
                sum_val += l2.val
                l2 = l2.next
            else:
                l2_pos = -1

            # 计算进位和当前位
            new_carry = sum_val // 10
            digit = sum_val % 10
            result_vals.append(digit)

            # 构建动作描述
            parts = []
            if l1_val is not None or l2_val is not None or carry != 0:
                parts.append(f'第 {step_count} 次相加：')
            if l1_val is not None:
                parts.append(f'l1={l1_val}')
            if l2_val is not None:
                parts.append(f'l2={l2_val}')
            if carry != 0:
                parts.append(f'carry={carry}')
            parts.append(f'→ sum={sum_val}')
            parts.append(f'→ digit={digit}, carry={new_carry}')

            action = ' '.join(parts)

            explanations = []
            if l1_val is not None:
                explanations.append(f'加上 l1 的当前位：{l1_val}')
            if l2_val is not None:
                explanations.append(f'加上 l2 的当前位：{l2_val}')
            if carry != 0:
                explanations.append(f'加上进位：{carry}')
            explanations.append(f'总和：sum = {sum_val}')
            explanations.append(f'当前位：digit = {sum_val} % 10 = {digit}')
            explanations.append(f'新进位：carry = {sum_val} // 10 = {new_carry}')

            self.steps.append({
                'l1_vals': self._list_to_array(l1) if l1 else [],
                'l2_vals': self._list_to_array(l2) if l2 else [],
                'l1_pos': l1_pos if l1_pos >= 0 else None,
                'l2_pos': l2_pos if l2_pos >= 0 else None,
                'result_vals': result_vals.copy(),
                'carry': new_carry,
                'sum': sum_val,
                'digit': digit,
                'action': action,
                'code_highlight': [4, 5, 6, 7, 8, 9, 10, 11],
                'explanations': explanations,
                'finished': False
            })

            carry = new_carry

        # 完成步骤
        self.steps.append({
            'l1_vals': [],
            'l2_vals': [],
            'l1_pos': None,
            'l2_pos': None,
            'result_vals': result_vals,
            'carry': 0,
            'sum': 0,
            'digit': 0,
            'action': f'✅ 处理完成，返回结果链表：{result_vals}',
            'code_highlight': [13],
            'explanations': [
                '两个链表都已遍历完，且没有进位。',
                f'结果链表：{result_vals}',
                '返回 dummy->next（跳过虚拟头节点）。'
            ],
            'finished': True
        })

    def _draw_list(self, vals, start_x, start_y, label, highlight_pos=None, color='lightblue'):
        """绘制链表"""
        if not vals:
            self.ax.text(start_x, start_y, f'{label}: (空)', fontsize=12, 
                        bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))
            return

        self.ax.text(start_x - 1, start_y, f'{label}:', fontsize=12, fontweight='bold', ha='right')
        
        for i, val in enumerate(vals):
            x = start_x + i * 2.5
            is_highlight = (highlight_pos is not None and i == highlight_pos)
            
            # 节点框
            facecolor = 'yellow' if is_highlight else color
            rect = FancyBboxPatch(
                (x - 0.4, start_y - 0.4), 0.8, 0.8,
                boxstyle='round,pad=0.1', linewidth=2,
                edgecolor='black', facecolor=facecolor
            )
            self.ax.add_patch(rect)
            
            # 节点值
            self.ax.text(x, start_y, str(val), ha='center', va='center',
                        fontsize=14, fontweight='bold')
            
            # 索引
            self.ax.text(x, start_y - 0.8, f'[{i}]', ha='center', va='center',
                        fontsize=9, color='gray')
            
            # 箭头（除了最后一个节点）
            if i < len(vals) - 1:
                arrow = FancyArrowPatch(
                    (x + 0.4, start_y), (x + 2.1, start_y),
                    arrowstyle='->', mutation_scale=20, lw=1.5, color='black'
                )
                self.ax.add_patch(arrow)

    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step

        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index

        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-2, self.x_limit)
        self.ax.set_ylim(-4, 12)

        step_data = self.steps[step_index]

        # 标题与说明
        self.ax.text(
            self.visual_width / 2, 11.5,
            f'步骤 {step_index + 1}/{len(self.steps)}',
            ha='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )

        self.ax.text(
            self.visual_width / 2, 10.5,
            step_data['action'],
            ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )

        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(
                self.visual_width / 2, 9.2,
                explain_text,
                ha='center', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )

        # 显示状态信息
        status_text = f"carry = {step_data['carry']}"
        if step_data.get('sum', 0) > 0:
            status_text += f"  |  sum = {step_data['sum']}"
        if step_data.get('digit', 0) >= 0:
            status_text += f"  |  digit = {step_data['digit']}"
        
        self.ax.text(
            self.visual_width / 2, 8.2,
            status_text,
            ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8)
        )

        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            self.visual_width / 2, 7.4,
            controls_text,
            ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

        # 绘制链表
        self._draw_list(
            self.l1_vals, 0, 6, 'l1',
            highlight_pos=step_data.get('l1_pos'),
            color='lightblue'
        )
        self._draw_list(
            self.l2_vals, 0, 4, 'l2',
            highlight_pos=step_data.get('l2_pos'),
            color='lightgreen'
        )
        self._draw_list(
            step_data['result_vals'], 0, 2, '结果',
            highlight_pos=len(step_data['result_vals']) - 1 if step_data['result_vals'] else None,
            color='mistyrose'
        )

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightblue', 'l1 链表'),
            ('lightgreen', 'l2 链表'),
            ('mistyrose', '结果链表'),
            ('yellow', '当前处理位置')
        ]
        for i, (color, text) in enumerate(legend_items):
            y_pos = 0.5 - i * 0.4
            rect = patches.Rectangle((i % 2 * 4, y_pos), 0.4, 0.4,
                                     facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(i % 2 * 4 + 0.5, y_pos + 0.2, text, fontsize=9, va='center')

        self.fig.canvas.draw()

    def _draw_code_panel(self, step_data):
        start_x = self.visual_width + 1.5
        start_y = 6
        line_height = 0.5
        highlight = set(step_data.get('code_highlight', []))

        self.ax.text(start_x, start_y + 2, 'C++ 代码同步显示', fontsize=13,
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
    print("LeetCode 2. 两数相加 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print('1. 示例 1: l1=[2,4,3], l2=[5,6,4] → [7,0,8]')
    print('2. 示例 2: l1=[0], l2=[0] → [0]')
    print('3. 示例 3: l1=[9,9,9,9,9,9,9], l2=[9,9,9,9] → [8,9,9,9,0,0,0,1]')
    print('4. 自定义输入')

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        l1_vals = [2, 4, 3]
        l2_vals = [5, 6, 4]
    elif choice == '2':
        l1_vals = [0]
        l2_vals = [0]
    elif choice == '3':
        l1_vals = [9, 9, 9, 9, 9, 9, 9]
        l2_vals = [9, 9, 9, 9]
    elif choice == '4':
        l1_str = input("请输入 l1（空格分隔，逆序）: ").strip()
        l2_str = input("请输入 l2（空格分隔，逆序）: ").strip()
        l1_vals = list(map(int, l1_str.split())) if l1_str else [0]
        l2_vals = list(map(int, l2_str.split())) if l2_str else [0]
    else:
        print("无效选择，使用示例 1")
        l1_vals = [2, 4, 3]
        l2_vals = [5, 6, 4]

    print("\n开始演示...")
    print(f'l1 = {l1_vals} (表示数字 {int("".join(map(str, reversed(l1_vals))))})')
    print(f'l2 = {l2_vals} (表示数字 {int("".join(map(str, reversed(l2_vals))))})')
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = AddTwoNumbersAnimation(l1_vals, l2_vals)
    anim.show()


if __name__ == '__main__':
    main()


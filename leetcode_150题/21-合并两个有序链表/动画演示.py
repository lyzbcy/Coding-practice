"""
LeetCode 21. 合并两个有序链表 - 动画演示
使用 matplotlib 手动控制链表合并的执行过程
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


class MergeTwoListsAnimation:
    def __init__(self, list1_vals, list2_vals):
        """
        初始化动画
        list1_vals: 第一个链表的节点值列表
        list2_vals: 第二个链表的节点值列表
        """
        self.list1_vals = list1_vals
        self.list2_vals = list2_vals
        self.list1 = self._create_list(list1_vals)
        self.list2 = self._create_list(list2_vals)
        self.steps = []
        self.current_step = 0
        self.max_len = max(len(list1_vals), len(list2_vals)) + len(list1_vals) + len(list2_vals)
        self.visual_width = max(self.max_len * 2.5, 12)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "struct ListNode* mergeTwoLists(...) {",
            "    ListNode* dummy = new ListNode(0);",
            "    ListNode* current = dummy;",
            "    while (list1 && list2) {",
            "        if (list1->val <= list2->val) {",
            "            current->next = list1;",
            "            list1 = list1->next;",
            "        } else {",
            "            current->next = list2;",
            "            list2 = list2->next;",
            "        }",
            "        current = current->next;",
            "    }",
            "    current->next = list1 ? list1 : list2;",
            "    return dummy->next;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(18, 12))
        self.fig.canvas.manager.set_window_title('合并两个有序链表 - 动画演示（手动控制）')
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
        list1 = self._create_list(self.list1_vals)
        list2 = self._create_list(self.list2_vals)
        
        # 创建虚拟头节点
        dummy = ListNode(0)
        current = dummy
        result_vals = []

        # 初始化步骤
        self.steps.append({
            'list1_vals': self._list_to_array(list1) if list1 else [],
            'list2_vals': self._list_to_array(list2) if list2 else [],
            'list1_pos': 0 if list1 else None,
            'list2_pos': 0 if list2 else None,
            'result_vals': [],
            'action': '初始化：创建虚拟头节点 dummy，current 指向 dummy',
            'code_highlight': [0, 1, 2],
            'explanations': [
                '创建虚拟头节点 dummy，简化边界处理。',
                '初始化 current 指向 dummy，用于构建结果链表。',
                '准备同时遍历两个链表。'
            ],
            'finished': False
        })

        step_count = 0
        while list1 and list2:
            step_count += 1
            # 保存比较前的值（用于显示）
            list1_val = list1.val
            list2_val = list2.val
            list1_pos = len(self._list_to_array(self.list1)) - len(self._list_to_array(list1)) if list1 else None
            list2_pos = len(self._list_to_array(self.list2)) - len(self._list_to_array(list2)) if list2 else None
            
            # 选择较小的节点
            if list1.val <= list2.val:
                chosen_val = list1.val
                chosen_list = 'list1'
                result_vals.append(list1.val)
                list1 = list1.next
            else:
                chosen_val = list2.val
                chosen_list = 'list2'
                result_vals.append(list2.val)
                list2 = list2.next

            action = f'第 {step_count} 次合并：比较 list1={list1_val} 和 list2={list2_val}，选择 {chosen_list} 的 {chosen_val}'

            explanations = []
            if list1_val <= list2_val:
                explanations.append(f'比较：list1->val={list1_val} <= list2->val={list2_val}')
                explanations.append(f'选择 list1 的节点 {list1_val}，连接到结果链表')
            else:
                explanations.append(f'比较：list1->val={list1_val} > list2->val={list2_val}')
                explanations.append(f'选择 list2 的节点 {list2_val}，连接到结果链表')

            self.steps.append({
                'list1_vals': self._list_to_array(list1) if list1 else [],
                'list2_vals': self._list_to_array(list2) if list2 else [],
                'list1_pos': list1_pos if list1_pos is not None else None,
                'list2_pos': list2_pos if list2_pos is not None else None,
                'result_vals': result_vals.copy(),
                'action': action,
                'code_highlight': [3, 4, 5, 6, 7, 8, 9, 10, 11],
                'explanations': explanations,
                'finished': False
            })

        # 处理剩余节点
        if list1 or list2:
            remaining = self._list_to_array(list1) if list1 else self._list_to_array(list2)
            result_vals.extend(remaining)
            self.steps.append({
                'list1_vals': [],
                'list2_vals': [],
                'list1_pos': None,
                'list2_pos': None,
                'result_vals': result_vals,
                'action': f'处理剩余节点：将 {"list1" if list1 else "list2"} 的剩余部分连接到结果链表',
                'code_highlight': [13],
                'explanations': [
                    f'{"list1" if list1 else "list2"} 已遍历完，将 {"list2" if list1 else "list1"} 的剩余部分直接连接。',
                    f'剩余节点：{remaining}'
                ],
                'finished': False
            })

        # 完成步骤
        self.steps.append({
            'list1_vals': [],
            'list2_vals': [],
            'list1_pos': None,
            'list2_pos': None,
            'result_vals': result_vals,
            'action': f'✅ 合并完成，返回结果链表：{result_vals}',
            'code_highlight': [14],
            'explanations': [
                '两个链表都已遍历完。',
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

        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            self.visual_width / 2, 8.2,
            controls_text,
            ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

        # 绘制链表
        self._draw_list(
            self.list1_vals, 0, 6, 'list1',
            highlight_pos=step_data.get('list1_pos'),
            color='lightblue'
        )
        self._draw_list(
            self.list2_vals, 0, 4, 'list2',
            highlight_pos=step_data.get('list2_pos'),
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
            ('lightblue', 'list1 链表'),
            ('lightgreen', 'list2 链表'),
            ('mistyrose', '结果链表'),
            ('yellow', '当前比较位置')
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
    print("LeetCode 21. 合并两个有序链表 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print('1. 示例 1: list1=[1,2,4], list2=[1,3,4] → [1,1,2,3,4,4]')
    print('2. 示例 2: list1=[], list2=[] → []')
    print('3. 示例 3: list1=[], list2=[0] → [0]')
    print('4. 自定义输入')

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        list1_vals = [1, 2, 4]
        list2_vals = [1, 3, 4]
    elif choice == '2':
        list1_vals = []
        list2_vals = []
    elif choice == '3':
        list1_vals = []
        list2_vals = [0]
    elif choice == '4':
        list1_str = input("请输入 list1（空格分隔，升序）: ").strip()
        list2_str = input("请输入 list2（空格分隔，升序）: ").strip()
        list1_vals = list(map(int, list1_str.split())) if list1_str else []
        list2_vals = list(map(int, list2_str.split())) if list2_str else []
    else:
        print("无效选择，使用示例 1")
        list1_vals = [1, 2, 4]
        list2_vals = [1, 3, 4]

    print("\n开始演示...")
    print(f'list1 = {list1_vals}')
    print(f'list2 = {list2_vals}')
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = MergeTwoListsAnimation(list1_vals, list2_vals)
    anim.show()


if __name__ == '__main__':
    main()


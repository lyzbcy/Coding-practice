"""
LeetCode 27. 移除元素 - 动画演示
使用 matplotlib 手动控制快慢指针的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class RemoveElementAnimation:
    def __init__(self, nums, val):
        self.val = val
        self.nums = nums.copy()
        self.length = len(nums)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "int removeElement(int* nums, int numsSize, int val) {",
            "    int slow = 0;",
            "    for (int fast = 0; fast < numsSize; fast++) {",
            "        if (nums[fast] != val) {",
            "            nums[slow] = nums[fast];",
            "            slow++;",
            "        }",
            "    }",
            "    return slow;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.canvas.manager.set_window_title('移除元素 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 8)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        slow = 0
        self.steps.append({
            'nums': self.nums.copy(),
            'slow': slow,
            'fast': None,
            'write_index': None,
            'kept': False,
            'value': None,
            'action': '初始化：slow=0，fast=0，开始扫描数组',
            'code_highlight': [0, 1],
            'explanations': [
                'slow 指向写入区起点，用于记录下一个可写位置。',
                'fast 将在 for 循环中遍历每个元素。'
            ]
        })

        for fast in range(self.length):
            current = self.nums[fast]
            write_index = slow

            if current == self.val:
                action = f'nums[{fast}]={current} 等于目标值 {self.val}，跳过'
                kept = False
                code_lines = [2, 3]
                explanations = [
                    f'检查 nums[{fast}] = {current}，与 val 相等，需要丢弃。',
                    'fast 前进到下一个元素，slow 保持不动。'
                ]
            else:
                self.nums[write_index] = current
                kept = True
                if write_index == fast:
                    action = f'nums[{fast}]={current} 不等于 {self.val}，位置无需调整，slow 前进'
                else:
                    action = (f'nums[{fast}]={current} 不等于 {self.val}，'
                              f'覆盖 nums[{write_index}]，slow 前进')
                slow += 1
                code_lines = [2, 3, 4, 5]
                explanations = [
                    f'nums[{fast}] = {current} 保留，并写入 slow={write_index} 的位置。',
                    'slow 向右移动，表示有效区长度加一。'
                ]

            self.steps.append({
                'nums': self.nums.copy(),
                'slow': slow,
                'fast': fast,
                'write_index': write_index if kept else None,
                'kept': kept,
                'value': current,
                'action': action,
                'code_highlight': code_lines,
                'explanations': explanations
            })

        self.steps.append({
            'nums': self.nums.copy(),
            'slow': slow,
            'fast': None,
            'write_index': None,
            'kept': False,
            'value': None,
            'action': f'✅ 处理完成，返回 k = {slow}',
            'code_highlight': [8],
            'explanations': [
                f'遍历结束，slow = {slow} 即为有效元素数量。',
                '返回 k 供调用者根据需要截断数组。'
            ]
        })

    def _draw_array(self, step_data):
        nums = step_data['nums']
        max_len = max(self.length, 1)

        for idx in range(max_len):
            val = nums[idx] if idx < len(nums) else ''
            if idx < step_data['slow']:
                color = 'lightblue'
            else:
                color = 'lightgray'

            rect = patches.Rectangle(
                (idx - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)
            self.ax.text(idx, 1, str(val), ha='center', va='center',
                         fontsize=14, fontweight='bold')
            self.ax.text(idx, 0.1, f'[{idx}]', ha='center', va='center',
                         fontsize=10, color='gray')

        # 高亮 fast 和写入位置
        highlights = []
        if step_data['fast'] is not None:
            highlights.append(('fast', step_data['fast'], 'yellow'))
        if step_data['write_index'] is not None:
            highlights.append(('write', step_data['write_index'], 'khaki'))

        for label, idx, color in highlights:
            if 0 <= idx < max_len:
                rect = patches.Rectangle(
                    (idx - 0.45, 1 - 0.45), 0.9, 0.9,
                    linewidth=3, edgecolor='red', facecolor='none'
                )
                self.ax.add_patch(rect)

    def _draw_pointers(self, step_data):
        slow = step_data['slow']
        fast = step_data['fast']
        max_len = max(self.length, 1)

        # slow 指针（指向下一个写入位置）
        if slow < max_len:
            self.ax.annotate('slow', xy=(slow, 1.8), xytext=(slow, 2.8),
                             arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                             fontsize=12, color='blue', ha='center')
        else:
            self.ax.text(max_len - 0.5, 2.5, f'slow=k={slow}',
                         color='blue', fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

        # fast 指针（扫描位置）
        if fast is not None and fast < max_len:
            self.ax.annotate('fast', xy=(fast, 0.2), xytext=(fast, -0.8),
                             arrowprops=dict(arrowstyle='->', color='green', lw=2),
                             fontsize=12, color='green', ha='center')

    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step

        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index

        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 8)

        step_data = self.steps[step_index]

        # 标题与说明
        self.ax.text(
            max(self.length / 2, 3), 7.5,
            f'步骤 {step_index + 1}/{len(self.steps)}',
            ha='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )

        self.ax.text(
            max(self.length / 2, 3), 6.6,
            step_data['action'],
            ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )

        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(
                max(self.length / 2, 3), 5.6,
                explain_text,
                ha='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )

        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            max(self.length / 2, 3), 4.6,
            controls_text,
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

        # 目标值信息
        self.ax.text(-0.5, 4.8, f'目标值 val = {self.val}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))
        self.ax.text(-0.5, 4.1, f'当前 k = slow = {step_data["slow"]}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

        # 绘制数组
        self.ax.text(-0.5, 1, 'nums:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_array(step_data)

        # 绘制指针
        self._draw_pointers(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightblue', '已保留的元素'),
            ('lightgray', '待处理区域'),
            ('yellow', 'fast 当前比较位置'),
            ('khaki', '写入 slow 位置')
        ]
        for i, (color, text) in enumerate(legend_items):
            rect = patches.Rectangle((i * 2, 3.3), 0.5, 0.5,
                                     facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(i * 2 + 0.6, 3.55, text, fontsize=10, va='center')
    def _draw_code_panel(self, step_data):
        start_x = self.visual_width + 1.5
        start_y = 3.5
        line_height = 0.6
        highlight = set(step_data.get('code_highlight', []))

        self.ax.text(start_x, start_y + 2.2, 'C 代码同步显示', fontsize=13,
                     fontweight='bold', ha='left',
                     bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.6))

        for idx, line in enumerate(self.code_lines):
            y = start_y - idx * line_height
            facecolor = 'peachpuff' if idx in highlight else 'white'
            self.ax.text(
                start_x, y, f'{idx + 1:02d} {line}',
                ha='left', va='center', fontsize=10, family='monospace',
                bbox=dict(boxstyle='round', facecolor=facecolor, alpha=0.9, pad=0.3)
            )

        self.fig.canvas.draw()

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
    print("LeetCode 27. 移除元素 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: nums=[3,2,2,3], val=3")
    print("2. 示例 2: nums=[0,1,2,2,3,0,4,2], val=2")
    print("3. 所有元素都被移除: nums=[1,1,1], val=1")
    print("4. 自定义输入")

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        nums = [3, 2, 2, 3]
        val = 3
    elif choice == '2':
        nums = [0, 1, 2, 2, 3, 0, 4, 2]
        val = 2
    elif choice == '3':
        nums = [1, 1, 1]
        val = 1
    elif choice == '4':
        nums = list(map(int, input("请输入 nums（空格分隔）: ").split()))
        val = int(input("请输入 val: "))
    else:
        print("无效选择，使用示例 1")
        nums = [3, 2, 2, 3]
        val = 3

    print("\n开始演示...")
    print(f"nums = {nums}")
    print(f"val = {val}")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = RemoveElementAnimation(nums, val)
    anim.show()


if __name__ == '__main__':
    main()




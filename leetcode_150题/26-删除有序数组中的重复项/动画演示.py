"""
LeetCode 26. 删除有序数组中的重复项 - 动画演示
使用 matplotlib 手动控制快慢指针的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class RemoveDuplicatesAnimation:
    def __init__(self, nums):
        self.original_nums = nums
        self.nums = nums.copy()
        self.length = len(nums)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "int removeDuplicates(int* nums, int numsSize) {",
            "    if (numsSize == 0) return 0;",
            "    int slow = 0;",
            "    for (int fast = 1; fast < numsSize; fast++) {",
            "        if (nums[fast] != nums[slow]) {",
            "            slow++;",
            "            nums[slow] = nums[fast];",
            "        }",
            "    }",
            "    return slow + 1;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.canvas.manager.set_window_title('删除有序数组中的重复项 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 8)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        if self.length == 0:
            self.steps.append({
                'nums': [],
                'slow': 0,
                'fast': None,
                'write_index': None,
                'value': None,
                'action': '数组为空，直接返回 0',
                'code_highlight': [0, 1, 9],
                'explanations': ['题目默认长度>=1，但动画仍兼容空数组情况。']
            })
            return

        slow = 0
        self.steps.append({
            'nums': self.nums.copy(),
            'slow': slow,
            'fast': None,
            'write_index': None,
            'value': self.nums[slow],
            'action': f'初始化：slow=0 指向首个唯一值 {self.nums[slow]}，fast=1 开始扫描',
            'code_highlight': [0, 1, 2, 3],
            'explanations': [
                'nums[0] 作为第一个唯一元素已经就位。',
                'fast 将从索引 1 开始检查是否遇到新值。'
            ]
        })

        for fast in range(1, self.length):
            current = self.nums[fast]
            if self.nums[slow] == current:
                action = (f'fast={fast}，nums[{fast}]={current} 与 nums[{slow}] 相同，'
                          '为重复值，fast 前进')
                code_lines = [3, 4]
                explanations = [
                    f'当前值 {current} 重复，写指针 slow 保持在 {slow}。',
                    '只移动 fast，继续寻找下一个不同的数。'
                ]
                write_index = None
            else:
                slow += 1
                self.nums[slow] = current
                write_index = slow
                action = (f'fast={fast}，发现新值 {current}，写入 slow={slow} 的位置，'
                          'slow 与 fast 同步前进')
                code_lines = [3, 4, 5, 6, 7]
                explanations = [
                    f'nums[{fast}]={current} 与 nums[{slow-1}] 不同，属于唯一元素。',
                    f'覆盖写入 nums[{slow}]，保证前 {slow+1} 个位置无重复。'
                ]

            self.steps.append({
                'nums': self.nums.copy(),
                'slow': slow,
                'fast': fast,
                'write_index': write_index,
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
            'value': None,
            'action': f'✅ 全部扫描完成，返回 k = slow + 1 = {slow + 1}',
            'code_highlight': [8, 9],
            'explanations': [
                f'数组前 {slow + 1} 个位置已全部填充唯一元素。',
                '后续元素可以忽略，不影响判题。'
            ]
        })

    def _draw_array(self, step_data):
        nums = step_data['nums']
        max_len = max(self.length, 1)

        for idx in range(max_len):
            val = nums[idx] if idx < len(nums) else ''
            if idx <= step_data['slow']:
                color = 'lightblue'
            else:
                color = 'lightgray'

            rect = patches.Rectangle(
                (idx - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)
            if idx < len(nums):
                self.ax.text(idx, 1, str(val), ha='center', va='center',
                             fontsize=14, fontweight='bold')
            self.ax.text(idx, 0.1, f'[{idx}]', ha='center', va='center',
                         fontsize=10, color='gray')

        highlights = []
        if step_data['fast'] is not None:
            highlights.append(('fast', step_data['fast'], 'yellow'))
        if step_data['write_index'] is not None:
            highlights.append(('write', step_data['write_index'], 'khaki'))

        for _, idx, _ in highlights:
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

        if slow < max_len:
            self.ax.annotate('slow', xy=(slow, 1.8), xytext=(slow, 2.8),
                             arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                             fontsize=12, color='blue', ha='center')
        else:
            self.ax.text(max_len - 0.5, 2.5, f'slow=k-1={slow}',
                         color='blue', fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

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

        self.ax.text(-0.5, 4.8, f'当前唯一元素数量（slow+1）= {step_data["slow"] + 1 if self.length else 0}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        self.ax.text(-0.5, 4.1, f'原始数组：{self.original_nums}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))

        self.ax.text(-0.5, 1, 'nums:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_array(step_data)
        self._draw_pointers(step_data)
        self._draw_code_panel(step_data)

        legend_items = [
            ('lightblue', '已确认唯一元素'),
            ('lightgray', '待处理区域'),
            ('yellow', 'fast 当前比较'),
            ('khaki', '写入 slow 的位置')
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
    print("LeetCode 26. 删除有序数组中的重复项 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1：nums = [1, 1, 2]")
    print("2. 示例 2：nums = [0,0,1,1,1,2,2,3,3,4]")
    print("3. 全是相同元素：nums = [5,5,5,5]")
    print("4. 已全唯一：nums = [1,2,3,4,5]")
    print("5. 自定义输入")

    choice = input("\n请输入选择 (1-5): ").strip()

    if choice == '1':
        nums = [1, 1, 2]
    elif choice == '2':
        nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    elif choice == '3':
        nums = [5, 5, 5, 5]
    elif choice == '4':
        nums = [1, 2, 3, 4, 5]
    elif choice == '5':
        raw = input("请输入 nums（空格分隔，需非递减排序）: ").strip()
        if raw:
            nums = list(map(int, raw.split()))
        else:
            nums = []
    else:
        print("无效选择，默认使用示例 1")
        nums = [1, 1, 2]

    print("\n开始演示...")
    print(f"nums = {nums}")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = RemoveDuplicatesAnimation(nums)
    anim.show()


if __name__ == '__main__':
    main()


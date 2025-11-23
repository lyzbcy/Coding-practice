"""
LeetCode 189. 轮转数组 - 动画演示
使用 matplotlib 手动控制三次反转法的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class RotateArrayAnimation:
    def __init__(self, nums, k):
        self.k = k
        self.nums = nums.copy()
        self.length = len(nums)
        self.k = k % self.length  # 处理 k >= length 的情况
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "void rotate(int* nums, int numsSize, int k) {",
            "    k = k % numsSize;",
            "    reverse(nums, 0, numsSize - 1);",
            "    reverse(nums, 0, k - 1);",
            "    reverse(nums, k, numsSize - 1);",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.canvas.manager.set_window_title('轮转数组 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 8)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _reverse(self, start, end):
        """反转数组的指定区间"""
        while start < end:
            self.nums[start], self.nums[end] = self.nums[end], self.nums[start]
            start += 1
            end -= 1

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        # 初始化步骤
        self.steps.append({
            'nums': self.nums.copy(),
            'phase': 'init',
            'start': None,
            'end': None,
            'left': None,
            'right': None,
            'action': f'初始化：数组长度 n={self.length}，轮转 k={self.k} 个位置',
            'code_highlight': [0, 1],
            'explanations': [
                f'原数组：{self.nums}',
                f'需要向右轮转 {self.k} 个位置',
                f'使用三次反转法实现轮转'
            ]
        })

        # 第一次反转：反转整个数组
        self.steps.append({
            'nums': self.nums.copy(),
            'phase': 'reverse_all',
            'start': 0,
            'end': self.length - 1,
            'left': 0,
            'right': self.length - 1,
            'action': '步骤 1：反转整个数组 [0, n-1]',
            'code_highlight': [2],
            'explanations': [
                '调用 reverse(nums, 0, n-1)',
                '将整个数组反转'
            ]
        })

        left, right = 0, self.length - 1
        while left < right:
            self.nums[left], self.nums[right] = self.nums[right], self.nums[left]
            self.steps.append({
                'nums': self.nums.copy(),
                'phase': 'reverse_all',
                'start': 0,
                'end': self.length - 1,
                'left': left,
                'right': right,
                'action': f'交换 nums[{left}] 和 nums[{right}]',
                'code_highlight': [2],
                'explanations': [
                    f'交换位置 {left} 和 {right} 的元素',
                    f'当前数组：{self.nums}'
                ]
            })
            left += 1
            right -= 1

        # 第二次反转：反转前 k 个元素
        self.steps.append({
            'nums': self.nums.copy(),
            'phase': 'reverse_first_k',
            'start': 0,
            'end': self.k - 1,
            'left': 0,
            'right': self.k - 1,
            'action': f'步骤 2：反转前 k 个元素 [0, {self.k - 1}]',
            'code_highlight': [3],
            'explanations': [
                f'调用 reverse(nums, 0, {self.k - 1})',
                f'反转前 {self.k} 个元素'
            ]
        })

        left, right = 0, self.k - 1
        while left < right:
            self.nums[left], self.nums[right] = self.nums[right], self.nums[left]
            self.steps.append({
                'nums': self.nums.copy(),
                'phase': 'reverse_first_k',
                'start': 0,
                'end': self.k - 1,
                'left': left,
                'right': right,
                'action': f'交换 nums[{left}] 和 nums[{right}]',
                'code_highlight': [3],
                'explanations': [
                    f'交换位置 {left} 和 {right} 的元素',
                    f'当前数组：{self.nums}'
                ]
            })
            left += 1
            right -= 1

        # 第三次反转：反转后 n-k 个元素
        self.steps.append({
            'nums': self.nums.copy(),
            'phase': 'reverse_last_nk',
            'start': self.k,
            'end': self.length - 1,
            'left': self.k,
            'right': self.length - 1,
            'action': f'步骤 3：反转后 n-k 个元素 [{self.k}, {self.length - 1}]',
            'code_highlight': [4],
            'explanations': [
                f'调用 reverse(nums, {self.k}, {self.length - 1})',
                f'反转后 {self.length - self.k} 个元素'
            ]
        })

        left, right = self.k, self.length - 1
        while left < right:
            self.nums[left], self.nums[right] = self.nums[right], self.nums[left]
            self.steps.append({
                'nums': self.nums.copy(),
                'phase': 'reverse_last_nk',
                'start': self.k,
                'end': self.length - 1,
                'left': left,
                'right': right,
                'action': f'交换 nums[{left}] 和 nums[{right}]',
                'code_highlight': [4],
                'explanations': [
                    f'交换位置 {left} 和 {right} 的元素',
                    f'当前数组：{self.nums}'
                ]
            })
            left += 1
            right -= 1

        # 完成步骤
        self.steps.append({
            'nums': self.nums.copy(),
            'phase': 'done',
            'start': None,
            'end': None,
            'left': None,
            'right': None,
            'action': f'✅ 轮转完成！数组已向右轮转 {self.k} 个位置',
            'code_highlight': [5],
            'explanations': [
                f'最终结果：{self.nums}',
                '三次反转法成功完成轮转'
            ]
        })

    def _draw_array(self, step_data):
        nums = step_data['nums']
        phase = step_data['phase']
        start = step_data['start']
        end = step_data['end']
        left = step_data['left']
        right = step_data['right']

        for idx in range(self.length):
            val = nums[idx]
            
            # 根据阶段设置颜色
            if phase == 'init':
                color = 'lightgray'
            elif phase == 'reverse_all':
                if start is not None and end is not None and start <= idx <= end:
                    color = 'lightcoral'
                else:
                    color = 'lightgray'
            elif phase == 'reverse_first_k':
                if idx < self.k:
                    if start is not None and end is not None and start <= idx <= end:
                        color = 'lightblue'
                    else:
                        color = 'lightcyan'
                else:
                    color = 'lightgray'
            elif phase == 'reverse_last_nk':
                if idx < self.k:
                    color = 'lightcyan'
                else:
                    if start is not None and end is not None and start <= idx <= end:
                        color = 'lightgreen'
                    else:
                        color = 'lightgray'
            elif phase == 'done':
                if idx < self.k:
                    color = 'lightcyan'
                else:
                    color = 'lightgreen'
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

        # 高亮正在交换的位置
        if left is not None and right is not None:
            for idx in [left, right]:
                if 0 <= idx < self.length:
                    rect = patches.Rectangle(
                        (idx - 0.45, 1 - 0.45), 0.9, 0.9,
                        linewidth=3, edgecolor='red', facecolor='none'
                    )
                    self.ax.add_patch(rect)

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

        # 参数信息
        self.ax.text(-0.5, 4.8, f'k = {self.k}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))
        self.ax.text(-0.5, 4.1, f'n = {self.length}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

        # 绘制数组
        self.ax.text(-0.5, 1, 'nums:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_array(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightcyan', '前 k 个元素'),
            ('lightgreen', '后 n-k 个元素'),
            ('lightcoral', '正在反转的区域'),
            ('red', '正在交换的位置')
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
    print("LeetCode 189. 轮转数组 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: nums=[1,2,3,4,5,6,7], k=3")
    print("2. 示例 2: nums=[-1,-100,3,99], k=2")
    print("3. 边界情况: nums=[1,2], k=3 (k > n)")
    print("4. 自定义输入")

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        nums = [1, 2, 3, 4, 5, 6, 7]
        k = 3
    elif choice == '2':
        nums = [-1, -100, 3, 99]
        k = 2
    elif choice == '3':
        nums = [1, 2]
        k = 3
    elif choice == '4':
        nums = list(map(int, input("请输入 nums（空格分隔）: ").split()))
        k = int(input("请输入 k: "))
    else:
        print("无效选择，使用示例 1")
        nums = [1, 2, 3, 4, 5, 6, 7]
        k = 3

    print("\n开始演示...")
    print(f"nums = {nums}")
    print(f"k = {k}")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = RotateArrayAnimation(nums, k)
    anim.show()


if __name__ == '__main__':
    main()



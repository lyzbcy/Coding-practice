"""
LeetCode 9. 回文数 - 动画演示
使用 matplotlib 手动控制数字反转和比较的过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class PalindromeNumberAnimation:
    def __init__(self, x):
        """
        初始化动画
        x: 要判断的整数
        """
        self.original_x = x
        self.x = x
        self.digits = self._get_digits(x)  # 获取每一位数字
        self.length = len(self.digits)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length * 2, 10)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "bool isPalindrome(int x) {",
            "    if (x < 0) return false;",
            "    if (x == 0) return true;",
            "    if (x % 10 == 0) return false;",
            "    int reversed = 0;",
            "    while (x > reversed) {",
            "        reversed = reversed * 10 + x % 10;",
            "        x /= 10;",
            "    }",
            "    return x == reversed || x == reversed / 10;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        self.fig.canvas.manager.set_window_title('回文数 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 10)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _get_digits(self, num):
        """获取数字的每一位"""
        if num == 0:
            return [0]
        if num < 0:
            num = -num
        digits = []
        while num > 0:
            digits.append(num % 10)
            num //= 10
        digits.reverse()
        return digits

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        x = self.original_x
        reversed_num = 0

        # 边界情况处理
        if x < 0:
            self.steps.append({
                'x': x,
                'reversed': 0,
                'action': '负数不是回文数，返回 false',
                'code_highlight': [1],
                'explanations': [
                    '负数反转后符号位置会改变（如 -121 变成 121-）。',
                    '因此负数不是回文数，直接返回 false。'
                ],
                'finished': True,
                'result': False
            })
            return

        if x == 0:
            self.steps.append({
                'x': 0,
                'reversed': 0,
                'action': '0 是回文数，返回 true',
                'code_highlight': [2],
                'explanations': [
                    '0 正序和倒序都是 0。',
                    '因此 0 是回文数，返回 true。'
                ],
                'finished': True,
                'result': True
            })
            return

        if x != 0 and x % 10 == 0:
            self.steps.append({
                'x': x,
                'reversed': 0,
                'action': f'{x} 以 0 结尾且不为 0，不是回文数，返回 false',
                'code_highlight': [3],
                'explanations': [
                    f'{x} 以 0 结尾，反转后第一位是 0（如 10 变成 01）。',
                    '因此不是回文数，返回 false。'
                ],
                'finished': True,
                'result': False
            })
            return

        # 初始化
        self.steps.append({
            'x': x,
            'reversed': 0,
            'action': f'初始化：x={x}，reversed=0，开始反转后一半数字',
            'code_highlight': [4, 5],
            'explanations': [
                f'原始数字：{x}',
                '我们将反转数字的后一半，然后与前一半比较。'
            ],
            'finished': False,
            'result': None
        })

        # 反转过程
        step_count = 0
        while x > reversed_num:
            step_count += 1
            digit = x % 10
            reversed_num = reversed_num * 10 + digit
            x //= 10

            self.steps.append({
                'x': x,
                'reversed': reversed_num,
                'action': f'第 {step_count} 次反转：提取 {digit}，reversed={reversed_num}，x={x}',
                'code_highlight': [6, 7],
                'explanations': [
                    f'从 x 中提取最后一位：{digit}',
                    f'reversed = reversed * 10 + digit = {reversed_num // 10} * 10 + {digit} = {reversed_num}',
                    f'x = x / 10 = {x * 10 + digit} / 10 = {x}'
                ],
                'finished': False,
                'result': None
            })

        # 判断结果
        is_even = (self.length % 2 == 0)
        if is_even:
            # 偶数位数
            if x == reversed_num:
                result = True
                action = f'✅ 偶数位数：x={x} == reversed={reversed_num}，是回文数，返回 true'
                explanations = [
                    f'数字有 {self.length} 位（偶数位）。',
                    f'前一半：x = {x}',
                    f'反转的后一半：reversed = {reversed_num}',
                    f'x == reversed，因此是回文数。'
                ]
            else:
                result = False
                action = f'❌ 偶数位数：x={x} != reversed={reversed_num}，不是回文数，返回 false'
                explanations = [
                    f'数字有 {self.length} 位（偶数位）。',
                    f'前一半：x = {x}',
                    f'反转的后一半：reversed = {reversed_num}',
                    f'x != reversed，因此不是回文数。'
                ]
        else:
            # 奇数位数
            if x == reversed_num // 10:
                result = True
                action = f'✅ 奇数位数：x={x} == reversed/10={reversed_num//10}，是回文数，返回 true'
                explanations = [
                    f'数字有 {self.length} 位（奇数位）。',
                    f'前一半（去掉中间位）：x = {x}',
                    f'反转的后一半（去掉中间位）：reversed/10 = {reversed_num}//10 = {reversed_num//10}',
                    f'x == reversed/10，因此是回文数。'
                ]
            else:
                result = False
                action = f'❌ 奇数位数：x={x} != reversed/10={reversed_num//10}，不是回文数，返回 false'
                explanations = [
                    f'数字有 {self.length} 位（奇数位）。',
                    f'前一半（去掉中间位）：x = {x}',
                    f'反转的后一半（去掉中间位）：reversed/10 = {reversed_num}//10 = {reversed_num//10}',
                    f'x != reversed/10，因此不是回文数。'
                ]

        self.steps.append({
            'x': x,
            'reversed': reversed_num,
            'action': action,
            'code_highlight': [9],
            'explanations': explanations,
            'finished': True,
            'result': result
        })

    def _draw_digits(self, step_data):
        """绘制数字的每一位"""
        x = step_data['x']
        reversed_num = step_data['reversed']
        finished = step_data.get('finished', False)

        # 获取当前 x 的每一位
        current_digits = self._get_digits(x) if x > 0 else [0] if x == 0 else []
        reversed_digits = self._get_digits(reversed_num) if reversed_num > 0 else []

        # 绘制原始数字
        self.ax.text(-0.5, 4, '原始数字 x:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        for i, digit in enumerate(self.digits):
            x_pos = i * 1.2
            color = 'lightgreen' if i < len(current_digits) else 'lightgray'
            rect = patches.Rectangle(
                (x_pos - 0.4, 3.5), 0.8, 0.8,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)
            self.ax.text(x_pos, 3.9, str(digit), ha='center', va='center',
                        fontsize=14, fontweight='bold')
            self.ax.text(x_pos, 3.2, f'[{i}]', ha='center', va='center',
                        fontsize=9, color='gray')

        # 绘制当前 x（前一半）
        if x >= 0:
            self.ax.text(-0.5, 2.5, '当前 x (前一半):', ha='right', va='center',
                         fontsize=14, fontweight='bold')
            for i, digit in enumerate(current_digits):
                x_pos = i * 1.2
                rect = patches.Rectangle(
                    (x_pos - 0.4, 2), 0.8, 0.8,
                    linewidth=2, edgecolor='blue', facecolor='lightblue'
                )
                self.ax.add_patch(rect)
                self.ax.text(x_pos, 2.4, str(digit), ha='center', va='center',
                            fontsize=14, fontweight='bold')

        # 绘制反转后的数字（后一半）
        if reversed_num > 0:
            self.ax.text(-0.5, 1, 'reversed (反转的后一半):', ha='right', va='center',
                         fontsize=14, fontweight='bold')
            for i, digit in enumerate(reversed_digits):
                x_pos = i * 1.2
                rect = patches.Rectangle(
                    (x_pos - 0.4, 0.5), 0.8, 0.8,
                    linewidth=2, edgecolor='red', facecolor='mistyrose'
                )
                self.ax.add_patch(rect)
                self.ax.text(x_pos, 0.9, str(digit), ha='center', va='center',
                            fontsize=14, fontweight='bold')

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
            result = step_data.get('result')
            if result is not None:
                result_text = '✅ 是回文数' if result else '❌ 不是回文数'
                result_color = 'lightgreen' if result else 'lightcoral'
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

        # 绘制数字
        self._draw_digits(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightgreen', '已处理的前一半数字'),
            ('lightgray', '已移除的后一半数字'),
            ('lightblue', '当前 x（前一半）'),
            ('mistyrose', 'reversed（反转的后一半）')
        ]
        for i, (color, text) in enumerate(legend_items):
            y_pos = -1.5 - i * 0.3
            rect = patches.Rectangle((i % 3 * 3, y_pos), 0.4, 0.4,
                                     facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(i % 3 * 3 + 0.5, y_pos + 0.2, text, fontsize=9, va='center')

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
    print("LeetCode 9. 回文数 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print('1. 示例 1: 121（是回文数）')
    print('2. 示例 2: -121（不是回文数）')
    print('3. 示例 3: 10（不是回文数）')
    print('4. 示例 4: 1221（偶数位回文数）')
    print('5. 自定义输入')

    choice = input("\n请输入选择 (1-5): ").strip()

    if choice == '1':
        x = 121
    elif choice == '2':
        x = -121
    elif choice == '3':
        x = 10
    elif choice == '4':
        x = 1221
    elif choice == '5':
        x_str = input("请输入整数: ").strip()
        x = int(x_str)
    else:
        print("无效选择，使用示例 1")
        x = 121

    print("\n开始演示...")
    print(f'输入数字: {x}')
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = PalindromeNumberAnimation(x)
    anim.show()


if __name__ == '__main__':
    main()


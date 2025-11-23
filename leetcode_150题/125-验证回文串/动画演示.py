"""
LeetCode 125. 验证回文串 - 动画演示
使用 matplotlib 手动控制双指针的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class ValidPalindromeAnimation:
    def __init__(self, s):
        self.original_s = s
        self.s = list(s)  # 转为列表便于修改显示
        self.length = len(s)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 10)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "bool isPalindrome(char* s) {",
            "    int left = 0;",
            "    int right = strlen(s) - 1;",
            "    while (left < right) {",
            "        while (left < right && !isalnum(s[left]))",
            "            left++;",
            "        while (left < right && !isalnum(s[right]))",
            "            right--;",
            "        if (tolower(s[left]) != tolower(s[right]))",
            "            return false;",
            "        left++;",
            "        right--;",
            "    }",
            "    return true;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        self.fig.canvas.manager.set_window_title('验证回文串 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 9)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _is_alnum(self, c):
        """判断是否为字母数字字符"""
        return c.isalnum()

    def _to_lower(self, c):
        """转为小写"""
        return c.lower()

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        left = 0
        right = self.length - 1

        self.steps.append({
            'left': left,
            'right': right,
            'action': '初始化：left=0，right=len(s)-1，开始双指针比较',
            'code_highlight': [0, 1, 2],
            'explanations': [
                'left 从左侧开始，right 从右侧开始。',
                '我们将从两端向中间比较字符。'
            ],
            'skip_left': False,
            'skip_right': False,
            'compare_result': None
        })

        while left < right:
            # 跳过左侧非字母数字字符
            skip_left = False
            while left < right and not self._is_alnum(self.original_s[left]):
                skip_left = True
                self.steps.append({
                    'left': left,
                    'right': right,
                    'action': f's[left] = "{self.original_s[left]}" 不是字母数字，跳过',
                    'code_highlight': [4, 5],
                    'explanations': [
                        f'位置 {left} 的字符 "{self.original_s[left]}" 不是字母数字，',
                        'left 指针向右移动，跳过该字符。'
                    ],
                    'skip_left': True,
                    'skip_right': False,
                    'compare_result': None
                })
                left += 1

            # 跳过右侧非字母数字字符
            skip_right = False
            while left < right and not self._is_alnum(self.original_s[right]):
                skip_right = True
                self.steps.append({
                    'left': left,
                    'right': right,
                    'action': f's[right] = "{self.original_s[right]}" 不是字母数字，跳过',
                    'code_highlight': [6, 7],
                    'explanations': [
                        f'位置 {right} 的字符 "{self.original_s[right]}" 不是字母数字，',
                        'right 指针向左移动，跳过该字符。'
                    ],
                    'skip_left': False,
                    'skip_right': True,
                    'compare_result': None
                })
                right -= 1

            # 如果 left >= right，说明已经比较完
            if left >= right:
                break

            # 比较字符
            left_char = self._to_lower(self.original_s[left])
            right_char = self._to_lower(self.original_s[right])
            is_match = left_char == right_char

            self.steps.append({
                'left': left,
                'right': right,
                'action': f'比较 s[{left}]="{self.original_s[left]}" 和 s[{right}]="{self.original_s[right]}"（转小写后："{left_char}" vs "{right_char}"）',
                'code_highlight': [8, 9],
                'explanations': [
                    f'比较位置 {left} 和位置 {right} 的字符。',
                    f'转小写后："{left_char}" {"==" if is_match else "!="} "{right_char}"'
                ],
                'skip_left': False,
                'skip_right': False,
                'compare_result': is_match
            })

            if not is_match:
                self.steps.append({
                    'left': left,
                    'right': right,
                    'action': f'❌ 字符不匹配，返回 false',
                    'code_highlight': [9],
                    'explanations': [
                        f'"{left_char}" != "{right_char}"，不是回文串。',
                        '函数返回 false。'
                    ],
                    'skip_left': False,
                    'skip_right': False,
                    'compare_result': False
                })
                return

            # 匹配成功，继续
            left += 1
            right -= 1

        # 所有字符都匹配
        self.steps.append({
            'left': left,
            'right': right,
            'action': '✅ 所有字符都匹配，返回 true',
            'code_highlight': [13],
            'explanations': [
                'left >= right，所有对应字符都已比较完毕。',
                '字符串是回文串，返回 true。'
            ],
            'skip_left': False,
            'skip_right': False,
            'compare_result': True
        })

    def _draw_string(self, step_data):
        """绘制字符串数组"""
        left = step_data['left']
        right = step_data['right']

        for idx in range(self.length):
            char = self.original_s[idx]
            is_alnum = self._is_alnum(char)

            # 确定颜色
            if idx == left:
                color = 'lightgreen' if is_alnum else 'lightcoral'
            elif idx == right:
                color = 'lightblue' if is_alnum else 'lightcoral'
            elif idx < left or idx > right:
                color = 'lightgray'  # 已处理区域
            elif is_alnum:
                color = 'wheat'  # 待处理的字母数字
            else:
                color = 'lightyellow'  # 待处理的非字母数字

            # 绘制字符框
            rect = patches.Rectangle(
                (idx - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)

            # 显示字符
            display_char = char if char != ' ' else '␣'
            self.ax.text(idx, 1, display_char, ha='center', va='center',
                         fontsize=12, fontweight='bold')

            # 显示索引
            self.ax.text(idx, 0.1, f'[{idx}]', ha='center', va='center',
                         fontsize=9, color='gray')

        # 高亮当前比较位置
        if left < self.length:
            rect = patches.Rectangle(
                (left - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=3, edgecolor='red', facecolor='none'
            )
            self.ax.add_patch(rect)

        if right >= 0 and right != left:
            rect = patches.Rectangle(
                (right - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=3, edgecolor='blue', facecolor='none'
            )
            self.ax.add_patch(rect)

    def _draw_pointers(self, step_data):
        """绘制指针"""
        left = step_data['left']
        right = step_data['right']

        # left 指针
        if left < self.length:
            self.ax.annotate('left', xy=(left, 1.8), xytext=(left, 2.8),
                             arrowprops=dict(arrowstyle='->', color='green', lw=2),
                             fontsize=12, color='green', ha='center')

        # right 指针
        if right >= 0:
            self.ax.annotate('right', xy=(right, 1.8), xytext=(right, 3.5),
                             arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                             fontsize=12, color='blue', ha='center')

    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step

        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index

        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 9)

        step_data = self.steps[step_index]

        # 标题与说明
        self.ax.text(
            max(self.length / 2, 5), 8.5,
            f'步骤 {step_index + 1}/{len(self.steps)}',
            ha='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )

        self.ax.text(
            max(self.length / 2, 5), 7.6,
            step_data['action'],
            ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )

        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(
                max(self.length / 2, 5), 6.6,
                explain_text,
                ha='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )

        # 显示比较结果
        if step_data.get('compare_result') is not None:
            result_text = '✅ 匹配' if step_data['compare_result'] else '❌ 不匹配'
            result_color = 'lightgreen' if step_data['compare_result'] else 'lightcoral'
            self.ax.text(
                max(self.length / 2, 5), 5.8,
                result_text,
                ha='center', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor=result_color, alpha=0.8)
            )

        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            max(self.length / 2, 5), 5.2,
            controls_text,
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

        # 绘制字符串
        self.ax.text(-0.5, 1, 's:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_string(step_data)

        # 绘制指针
        self._draw_pointers(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightgreen', 'left 当前位置（字母数字）'),
            ('lightblue', 'right 当前位置（字母数字）'),
            ('lightcoral', '当前跳过位置（非字母数字）'),
            ('lightgray', '已处理区域'),
            ('wheat', '待处理字母数字'),
            ('lightyellow', '待处理非字母数字')
        ]
        for i, (color, text) in enumerate(legend_items):
            if i < 3:
                y_pos = 4.2 - i * 0.3
            else:
                y_pos = 3.2 - (i - 3) * 0.3
            rect = patches.Rectangle((i % 3 * 3, y_pos), 0.4, 0.4,
                                     facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(i % 3 * 3 + 0.5, y_pos + 0.2, text, fontsize=9, va='center')

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
    print("LeetCode 125. 验证回文串 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print('1. 示例 1: s = "A man, a plan, a canal: Panama"')
    print('2. 示例 2: s = "race a car"')
    print('3. 示例 3: s = " "')
    print('4. 简单回文: s = "Madam"')
    print('5. 自定义输入')

    choice = input("\n请输入选择 (1-5): ").strip()

    if choice == '1':
        s = "A man, a plan, a canal: Panama"
    elif choice == '2':
        s = "race a car"
    elif choice == '3':
        s = " "
    elif choice == '4':
        s = "Madam"
    elif choice == '5':
        s = input("请输入字符串 s: ").strip()
    else:
        print("无效选择，使用示例 1")
        s = "A man, a plan, a canal: Panama"

    print("\n开始演示...")
    print(f's = "{s}"')
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = ValidPalindromeAnimation(s)
    anim.show()


if __name__ == '__main__':
    main()


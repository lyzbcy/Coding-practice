"""
LeetCode 58. 最后一个单词的长度 - 动画演示
使用 matplotlib 手动控制从后往前遍历字符串的过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class LengthOfLastWordAnimation:
    def __init__(self, s):
        self.s = s
        self.length = len(s)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "int lengthOfLastWord(char* s) {",
            "    int i = strlen(s) - 1;",
            "    while (i >= 0 && s[i] == ' ') {",
            "        i--;",
            "    }",
            "    int length = 0;",
            "    while (i >= 0 && s[i] != ' ') {",
            "        length++;",
            "        i--;",
            "    }",
            "    return length;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.canvas.manager.set_window_title('最后一个单词的长度 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 8)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        i = self.length - 1
        length = 0
        phase = 'skip_spaces'  # 'skip_spaces' 或 'count_word'
        
        # 初始状态
        self.steps.append({
            'i': i,
            'length': length,
            'phase': phase,
            'action': f'初始化：i = {i}（从字符串末尾开始）',
            'code_highlight': [0, 1],
            'explanations': [
                '从字符串末尾开始遍历，准备跳过末尾空格。',
                f'当前字符串长度：{self.length}'
            ]
        })

        # 阶段1：跳过末尾空格
        while i >= 0 and self.s[i] == ' ':
            i -= 1
            self.steps.append({
                'i': i,
                'length': length,
                'phase': 'skip_spaces',
                'action': f's[{i+1}] 是空格，跳过，i = {i}',
                'code_highlight': [2, 3, 4],
                'explanations': [
                    f'当前位置 s[{i+1}] 是空格，需要跳过。',
                    '继续向前移动指针，直到找到非空格字符。'
                ]
            })

        # 阶段2：计数最后一个单词
        if i >= 0:
            self.steps.append({
                'i': i,
                'length': length,
                'phase': 'count_word',
                'action': f'开始计数：s[{i}] = \'{self.s[i]}\'（第一个非空格字符）',
                'code_highlight': [5, 6],
                'explanations': [
                    '找到最后一个单词的起始位置。',
                    '开始从后往前计数单词长度。'
                ]
            })

        while i >= 0 and self.s[i] != ' ':
            length += 1
            i -= 1
            self.steps.append({
                'i': i,
                'length': length,
                'phase': 'count_word',
                'action': f's[{i+1}] = \'{self.s[i+1]}\'，计数 length = {length}，i = {i}',
                'code_highlight': [6, 7, 8],
                'explanations': [
                    f'当前字符 s[{i+1}] = \'{self.s[i+1]}\' 是单词的一部分。',
                    f'长度加一，当前 length = {length}。'
                ]
            })

        # 结束状态
        self.steps.append({
            'i': i,
            'length': length,
            'phase': 'done',
            'action': f'✅ 处理完成，返回 length = {length}',
            'code_highlight': [10],
            'explanations': [
                f'遍历结束，最后一个单词的长度为 {length}。',
                '返回结果。'
            ]
        })

    def _draw_string(self, step_data):
        """绘制字符串"""
        i = step_data['i']
        phase = step_data['phase']
        length = step_data['length']

        for idx in range(self.length):
            char = self.s[idx]
            # 根据位置和阶段设置颜色
            if phase == 'skip_spaces' and idx > i:
                color = 'lightcoral'  # 已跳过的空格
            elif phase == 'count_word' and idx > i and idx <= i + length:
                color = 'lightgreen'  # 正在计数的单词
            elif phase == 'done' and idx > i and idx <= i + length:
                color = 'lightblue'  # 最后一个单词
            else:
                color = 'lightgray'  # 其他区域

            # 绘制字符框
            rect = patches.Rectangle(
                (idx - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)
            
            # 显示字符（空格显示为特殊符号）
            display_char = char if char != ' ' else '␣'
            self.ax.text(idx, 1, display_char, ha='center', va='center',
                         fontsize=14, fontweight='bold')
            self.ax.text(idx, 0.1, f'[{idx}]', ha='center', va='center',
                         fontsize=10, color='gray')

        # 高亮当前指针位置
        if i >= 0 and i < self.length:
            rect = patches.Rectangle(
                (i - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=3, edgecolor='red', facecolor='none'
            )
            self.ax.add_patch(rect)

    def _draw_pointer(self, step_data):
        """绘制指针"""
        i = step_data['i']
        phase = step_data['phase']
        
        if i >= 0 and i < self.length:
            # 绘制指针箭头
            self.ax.annotate('i', xy=(i, 0.2), xytext=(i, -0.8),
                             arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                             fontsize=12, color='blue', ha='center')
        elif i < 0:
            # 指针已超出范围
            self.ax.text(-0.5, 0.2, 'i = -1', color='blue', fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

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

        # 状态信息
        phase_text = {
            'skip_spaces': '阶段：跳过末尾空格',
            'count_word': '阶段：计数最后一个单词',
            'done': '阶段：完成'
        }
        self.ax.text(-0.5, 4.8, phase_text.get(step_data['phase'], ''), fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))
        self.ax.text(-0.5, 4.1, f'当前 length = {step_data["length"]}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        self.ax.text(-0.5, 3.4, f'当前 i = {step_data["i"]}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

        # 绘制字符串
        self.ax.text(-0.5, 1, 's:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_string(step_data)

        # 绘制指针
        self._draw_pointer(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightcoral', '已跳过的空格'),
            ('lightgreen', '正在计数的单词'),
            ('lightblue', '最后一个单词'),
            ('lightgray', '其他区域')
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
    print("LeetCode 58. 最后一个单词的长度 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: s=\"Hello World\"")
    print("2. 示例 2: s=\"   fly me   to   the moon  \"")
    print("3. 示例 3: s=\"luffy is still joyboy\"")
    print("4. 自定义输入")

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        s = "Hello World"
    elif choice == '2':
        s = "   fly me   to   the moon  "
    elif choice == '3':
        s = "luffy is still joyboy"
    elif choice == '4':
        s = input("请输入字符串 s: ").strip('"').strip("'")
    else:
        print("无效选择，使用示例 1")
        s = "Hello World"

    print("\n开始演示...")
    print(f's = "{s}"')
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = LengthOfLastWordAnimation(s)
    anim.show()


if __name__ == '__main__':
    main()


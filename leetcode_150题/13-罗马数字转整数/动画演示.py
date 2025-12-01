"""
LeetCode 13. 罗马数字转整数 - 动画演示
使用 matplotlib 手动控制罗马数字转换的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class RomanToIntAnimation:
    def __init__(self, s):
        self.s = s
        self.length = len(s)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 14
        
        # 字符到数值的映射
        self.char_to_value = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }
        
        self.code_lines = [
            "int romanToInt(char* s) {",
            "    int result = 0;",
            "    int len = strlen(s);",
            "    for (int i = 0; i < len; i++) {",
            "        int current = getValue(s[i]);",
            "        if (i+1 < len && current < getValue(s[i+1])) {",
            "            result += getValue(s[i+1]) - current;",
            "            i++;",
            "        } else {",
            "            result += current;",
            "        }",
            "    }",
            "    return result;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.canvas.manager.set_window_title('罗马数字转整数 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 9)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _get_value(self, c):
        """获取字符对应的数值"""
        return self.char_to_value.get(c, 0)

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        result = 0
        i = 0
        
        self.steps.append({
            's': list(self.s),
            'i': None,
            'result': result,
            'current_char': None,
            'next_char': None,
            'current_value': None,
            'next_value': None,
            'is_special': False,
            'action': '初始化：result=0，开始从左到右扫描字符串',
            'code_highlight': [0, 1, 2, 3],
            'explanations': [
                '初始化结果变量 result = 0。',
                '准备从左到右遍历字符串，逐个处理每个字符。'
            ]
        })

        while i < self.length:
            current_char = self.s[i]
            current_value = self._get_value(current_char)
            
            # 检查是否有下一个字符
            has_next = i + 1 < self.length
            next_char = self.s[i + 1] if has_next else None
            next_value = self._get_value(next_char) if has_next else 0
            
            # 判断是否是特殊情况
            is_special = has_next and current_value < next_value
            
            if is_special:
                # 特殊情况：相减
                diff = next_value - current_value
                result += diff
                action = (f's[{i}]={current_char}({current_value}) < '
                         f's[{i+1}]={next_char}({next_value})，特殊情况：'
                         f'result += {next_value} - {current_value} = {diff}')
                code_lines = [4, 5, 6, 7]
                explanations = [
                    f'当前字符 {current_char} 的值为 {current_value}，',
                    f'下一个字符 {next_char} 的值为 {next_value}。',
                    f'因为 {current_value} < {next_value}，这是特殊情况，',
                    f'需要相减：{next_value} - {current_value} = {diff}。',
                    f'将 {diff} 加到结果中，然后跳过下一个字符。'
                ]
                i += 2
            else:
                # 正常情况：相加
                result += current_value
                if has_next:
                    action = (f's[{i}]={current_char}({current_value}) >= '
                             f's[{i+1}]={next_char}({next_value})，正常情况：'
                             f'result += {current_value}')
                else:
                    action = (f's[{i}]={current_char}({current_value}) 是最后一个字符，'
                             f'正常情况：result += {current_value}')
                code_lines = [4, 5, 9, 10]
                explanations = [
                    f'当前字符 {current_char} 的值为 {current_value}。',
                    f'{"下一个字符的值小于等于当前字符" if has_next else "这是最后一个字符"}，',
                    '属于正常情况，直接加上当前字符的值。'
                ]
                i += 1

            self.steps.append({
                's': list(self.s),
                'i': i - (2 if is_special else 1),
                'result': result,
                'current_char': current_char,
                'next_char': next_char if is_special else None,
                'current_value': current_value,
                'next_value': next_value if is_special else None,
                'is_special': is_special,
                'action': action,
                'code_highlight': code_lines,
                'explanations': explanations
            })

        self.steps.append({
            's': list(self.s),
            'i': None,
            'result': result,
            'current_char': None,
            'next_char': None,
            'current_value': None,
            'next_value': None,
            'is_special': False,
            'action': f'✅ 处理完成，返回 result = {result}',
            'code_highlight': [12, 13],
            'explanations': [
                f'遍历结束，所有字符都已处理完毕。',
                f'最终结果：{self.s} = {result}'
            ]
        })

    def _draw_string(self, step_data):
        """绘制字符串数组"""
        s = step_data['s']
        max_len = max(self.length, 1)
        current_i = step_data['i']

        for idx in range(max_len):
            if idx < len(s):
                char = s[idx]
                value = self._get_value(char)
                
                # 根据状态选择颜色
                if current_i is not None:
                    if idx == current_i:
                        color = 'yellow'  # 当前字符
                    elif step_data['is_special'] and idx == current_i + 1:
                        color = 'orange'  # 特殊情况的下一个字符
                    elif idx < current_i:
                        color = 'lightgreen'  # 已处理
                    else:
                        color = 'lightgray'  # 未处理
                else:
                    color = 'lightgreen'  # 全部处理完成
            else:
                char = ''
                value = ''
                color = 'white'

            # 绘制字符框
            rect = patches.Rectangle(
                (idx - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)
            
            # 显示字符
            self.ax.text(idx, 1.3, char, ha='center', va='center',
                         fontsize=16, fontweight='bold')
            
            # 显示数值
            if idx < len(s):
                self.ax.text(idx, 0.7, str(value), ha='center', va='center',
                             fontsize=12, color='blue')
            
            # 显示索引
            self.ax.text(idx, 0.1, f'[{idx}]', ha='center', va='center',
                         fontsize=10, color='gray')

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
            max(self.length / 2, 3), 8.5,
            f'步骤 {step_index + 1}/{len(self.steps)}',
            ha='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )

        self.ax.text(
            max(self.length / 2, 3), 7.6,
            step_data['action'],
            ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )

        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(
                max(self.length / 2, 3), 6.2,
                explain_text,
                ha='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )

        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            max(self.length / 2, 3), 5.2,
            controls_text,
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

        # 结果显示
        self.ax.text(-0.5, 4.8, f'当前结果 result = {step_data["result"]}', 
                     fontsize=14, fontweight='bold',
                     bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
        if step_data['current_char']:
            self.ax.text(-0.5, 4.1, 
                        f'当前字符: {step_data["current_char"]} = {step_data["current_value"]}',
                        fontsize=12,
                        bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))

        # 绘制字符串
        self.ax.text(-0.5, 1, '字符串 s:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_string(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightgreen', '已处理的字符'),
            ('lightgray', '未处理的字符'),
            ('yellow', '当前正在处理的字符'),
            ('orange', '特殊情况的下一个字符')
        ]
        for i, (color, text) in enumerate(legend_items):
            rect = patches.Rectangle((i * 2.5, 3.3), 0.5, 0.5,
                                     facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(i * 2.5 + 0.6, 3.55, text, fontsize=10, va='center')

        self.fig.canvas.draw()

    def _draw_code_panel(self, step_data):
        start_x = self.visual_width + 1.5
        start_y = 4.5
        line_height = 0.5
        highlight = set(step_data.get('code_highlight', []))

        self.ax.text(start_x, start_y + 2.2, 'C 代码同步显示', fontsize=13,
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
    print("LeetCode 13. 罗马数字转整数 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: s=\"III\" (输出: 3)")
    print("2. 示例 2: s=\"IV\" (输出: 4)")
    print("3. 示例 3: s=\"IX\" (输出: 9)")
    print("4. 示例 4: s=\"LVIII\" (输出: 58)")
    print("5. 示例 5: s=\"MCMXCIV\" (输出: 1994)")
    print("6. 自定义输入")

    choice = input("\n请输入选择 (1-6): ").strip()

    if choice == '1':
        s = "III"
    elif choice == '2':
        s = "IV"
    elif choice == '3':
        s = "IX"
    elif choice == '4':
        s = "LVIII"
    elif choice == '5':
        s = "MCMXCIV"
    elif choice == '6':
        s = input("请输入罗马数字字符串: ").strip().upper()
    else:
        print("无效选择，使用示例 1")
        s = "III"

    print("\n开始演示...")
    print(f"输入: s = \"{s}\"")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = RomanToIntAnimation(s)
    anim.show()


if __name__ == '__main__':
    main()


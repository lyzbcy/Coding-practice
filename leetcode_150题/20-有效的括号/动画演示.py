"""
LeetCode 20. 有效的括号 - 动画演示
使用 matplotlib 手动控制栈的匹配过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class ValidParenthesesAnimation:
    def __init__(self, s):
        self.s = s
        self.length = len(s)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 14
        
        # 匹配映射
        self.pairs = {')': '(', ']': '[', '}': '{'}
        
        self.code_lines = [
            "bool isValid(string s) {",
            "    stack<char> stk;",
            "    for (char c : s) {",
            "        if (pairs.count(c)) {",
            "            if (stk.empty() || stk.top() != pairs[c]) {",
            "                return false;",
            "            }",
            "            stk.pop();",
            "        } else {",
            "            stk.push(c);",
            "        }",
            "    }",
            "    return stk.empty();",
            "}",
        ]
        
        self._simulate_algorithm()
        
        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.fig.canvas.manager.set_window_title('有效的括号 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-4, 9)
        
        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
    
    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        stack = []
        result = True
        
        # 初始化步骤
        self.steps.append({
            's': self.s,
            'stack': stack.copy(),
            'current_idx': None,
            'current_char': None,
            'action': '初始化：创建空栈，开始遍历字符串',
            'code_highlight': [0, 1],
            'explanations': [
                '创建一个栈用于存储左括号。',
                '准备从左到右遍历字符串中的每个字符。'
            ],
            'is_valid': None,
            'match_result': None
        })
        
        for i, char in enumerate(self.s):
            # 判断是左括号还是右括号
            is_right = char in self.pairs
            
            if is_right:
                # 右括号：检查匹配
                if not stack:
                    # 栈为空，不匹配
                    result = False
                    self.steps.append({
                        's': self.s,
                        'stack': stack.copy(),
                        'current_idx': i,
                        'current_char': char,
                        'action': f'遇到右括号 "{char}"，但栈为空，匹配失败',
                        'code_highlight': [2, 3, 4, 5],
                        'explanations': [
                            f'当前字符是右括号 "{char}"，需要检查是否有对应的左括号。',
                            '栈为空，说明没有未匹配的左括号，字符串无效。'
                        ],
                        'is_valid': False,
                        'match_result': '栈为空'
                    })
                    break
                else:
                    top = stack[-1]
                    expected = self.pairs[char]
                    if top == expected:
                        # 匹配成功
                        stack.pop()
                        self.steps.append({
                            's': self.s,
                            'stack': stack.copy(),
                            'current_idx': i,
                            'current_char': char,
                            'action': f'遇到右括号 "{char}"，与栈顶 "{top}" 匹配，出栈',
                            'code_highlight': [2, 3, 4, 7],
                            'explanations': [
                                f'当前字符是右括号 "{char}"，检查栈顶元素。',
                                f'栈顶是 "{top}"，与 "{char}" 匹配，弹出栈顶。'
                            ],
                            'is_valid': None,
                            'match_result': '匹配成功'
                        })
                    else:
                        # 类型不匹配
                        result = False
                        self.steps.append({
                            's': self.s,
                            'stack': stack.copy(),
                            'current_idx': i,
                            'current_char': char,
                            'action': f'遇到右括号 "{char}"，但栈顶是 "{top}"，类型不匹配',
                            'code_highlight': [2, 3, 4, 5],
                            'explanations': [
                                f'当前字符是右括号 "{char}"，期望匹配 "{expected}"。',
                                f'但栈顶是 "{top}"，类型不匹配，字符串无效。'
                            ],
                            'is_valid': False,
                            'match_result': '类型不匹配'
                        })
                        break
            else:
                # 左括号：入栈
                stack.append(char)
                self.steps.append({
                    's': self.s,
                    'stack': stack.copy(),
                    'current_idx': i,
                    'current_char': char,
                    'action': f'遇到左括号 "{char}"，入栈',
                    'code_highlight': [2, 8, 9],
                    'explanations': [
                        f'当前字符是左括号 "{char}"，将其压入栈中。',
                        '等待后续的右括号来匹配。'
                    ],
                    'is_valid': None,
                    'match_result': None
                })
        
        # 最终检查
        if result and len(stack) == 0:
            self.steps.append({
                's': self.s,
                'stack': stack.copy(),
                'current_idx': None,
                'current_char': None,
                'action': '✅ 遍历完成，栈为空，字符串有效',
                'code_highlight': [12],
                'explanations': [
                    '所有字符处理完毕，栈为空。',
                    '说明所有括号都正确匹配，返回 true。'
                ],
                'is_valid': True,
                'match_result': None
            })
        elif result and len(stack) > 0:
            self.steps.append({
                's': self.s,
                'stack': stack.copy(),
                'current_idx': None,
                'current_char': None,
                'action': f'❌ 遍历完成，但栈中还有 {len(stack)} 个未匹配的左括号',
                'code_highlight': [12],
                'explanations': [
                    '所有字符处理完毕，但栈不为空。',
                    f'栈中还有未匹配的左括号：{stack}，返回 false。'
                ],
                'is_valid': False,
                'match_result': None
            })
    
    def _draw_string(self, step_data):
        """绘制字符串"""
        s = step_data['s']
        current_idx = step_data['current_idx']
        
        for i, char in enumerate(s):
            # 当前字符高亮
            if i == current_idx:
                color = 'yellow'
                edgecolor = 'red'
                linewidth = 3
            else:
                color = 'lightblue' if char in '([{' else 'lightgreen'
                edgecolor = 'black'
                linewidth = 2
            
            rect = FancyBboxPatch(
                (i - 0.4, 1 - 0.4), 0.8, 0.8,
                boxstyle="round,pad=0.1",
                linewidth=linewidth, edgecolor=edgecolor, facecolor=color
            )
            self.ax.add_patch(rect)
            self.ax.text(i, 1, char, ha='center', va='center',
                         fontsize=16, fontweight='bold')
            self.ax.text(i, 0.1, f'[{i}]', ha='center', va='center',
                         fontsize=10, color='gray')
    
    def _draw_stack(self, step_data):
        """绘制栈"""
        stack = step_data['stack']
        stack_x = self.visual_width + 1
        
        # 栈的标题
        self.ax.text(stack_x, 7.5, '栈 (Stack)', ha='center', va='center',
                     fontsize=14, fontweight='bold',
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))
        
        # 栈的容器
        stack_height = max(len(stack), 1) * 0.8 + 0.4
        stack_rect = FancyBboxPatch(
            (stack_x - 0.5, 6.5 - stack_height), 1.0, stack_height,
            boxstyle="round,pad=0.1",
            linewidth=2, edgecolor='black', facecolor='white', alpha=0.5
        )
        self.ax.add_patch(stack_rect)
        
        # 绘制栈中的元素（从下往上）
        for i, char in enumerate(stack):
            y_pos = 6.5 - (len(stack) - 1 - i) * 0.8 - 0.4
            rect = FancyBboxPatch(
                (stack_x - 0.4, y_pos - 0.3), 0.8, 0.6,
                boxstyle="round,pad=0.05",
                linewidth=2, edgecolor='blue', facecolor='lightblue'
            )
            self.ax.add_patch(rect)
            self.ax.text(stack_x, y_pos, char, ha='center', va='center',
                         fontsize=14, fontweight='bold')
        
        # 栈为空时的提示
        if len(stack) == 0:
            self.ax.text(stack_x, 6.2, '(空)', ha='center', va='center',
                         fontsize=12, color='gray', style='italic')
        
        # 栈顶标记
        if len(stack) > 0:
            top_y = 6.5 - 0.4
            self.ax.annotate('栈顶', xy=(stack_x, top_y), xytext=(stack_x + 1.5, top_y),
                             arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                             fontsize=11, color='blue')
    
    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step
        
        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index
        
        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-4, 9)
        
        step_data = self.steps[step_index]
        
        # 标题与说明
        self.ax.text(
            max(self.length / 2, 3), 8.5,
            f'步骤 {step_index + 1}/{len(self.steps)}',
            ha='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )
        
        # 操作说明
        action_text = step_data['action']
        action_color = 'green' if step_data.get('is_valid') is True else \
                      'red' if step_data.get('is_valid') is False else 'black'
        self.ax.text(
            max(self.length / 2, 3), 7.8,
            action_text,
            ha='center', fontsize=12, color=action_color,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )
        
        # 详细解释
        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(
                max(self.length / 2, 3), 6.8,
                explain_text,
                ha='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )
        
        # 控制提示
        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            max(self.length / 2, 3), 5.8,
            controls_text,
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )
        
        # 当前字符信息
        if step_data['current_char']:
            char_info = f'当前字符: "{step_data["current_char"]}" (索引 {step_data["current_idx"]})'
            self.ax.text(-0.5, 4.5, char_info, fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
        # 匹配结果
        if step_data.get('match_result'):
            match_info = f'匹配结果: {step_data["match_result"]}'
            self.ax.text(-0.5, 3.8, match_info, fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.8))
        
        # 最终结果
        if step_data.get('is_valid') is not None:
            result_text = f'结果: {"✅ 有效" if step_data["is_valid"] else "❌ 无效"}'
            result_color = 'green' if step_data['is_valid'] else 'red'
            self.ax.text(-0.5, 3.1, result_text, fontsize=14, fontweight='bold', color=result_color,
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
        
        # 绘制字符串
        self.ax.text(-0.5, 1, '字符串 s:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_string(step_data)
        
        # 绘制栈
        self._draw_stack(step_data)
        
        # 绘制代码面板
        self._draw_code_panel(step_data)
        
        # 图例
        legend_items = [
            ('lightblue', '左括号'),
            ('lightgreen', '右括号'),
            ('yellow', '当前字符'),
            ('lightblue', '栈中元素')
        ]
        for i, (color, text) in enumerate(legend_items):
            rect = patches.Rectangle((i * 2, 0.5), 0.5, 0.5,
                                     facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(i * 2 + 0.6, 0.75, text, fontsize=10, va='center')
        
        self.fig.canvas.draw()
    
    def _draw_code_panel(self, step_data):
        start_x = self.visual_width + 1.5
        start_y = 5.5
        line_height = 0.5
        highlight = set(step_data.get('code_highlight', []))
        
        self.ax.text(start_x, start_y + 1.5, 'C++ 代码同步显示', fontsize=13,
                     fontweight='bold', ha='left',
                     bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.6))
        
        for idx, line in enumerate(self.code_lines):
            y = start_y - idx * line_height
            facecolor = 'peachpuff' if idx in highlight else 'white'
            self.ax.text(
                start_x, y, f'{idx + 1:02d} {line}',
                ha='left', va='center', fontsize=9, family='monospace',
                bbox=dict(boxstyle='round', facecolor=facecolor, alpha=0.9, pad=0.2)
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
    print("LeetCode 20. 有效的括号 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: s = \"()\"")
    print("2. 示例 2: s = \"()[]{}\"")
    print("3. 示例 3: s = \"(]\"")
    print("4. 示例 4: s = \"([])\"")
    print("5. 示例 5: s = \"([)]\"")
    print("6. 自定义输入")
    
    choice = input("\n请输入选择 (1-6): ").strip()
    
    if choice == '1':
        s = "()"
    elif choice == '2':
        s = "()[]{}"
    elif choice == '3':
        s = "(]"
    elif choice == '4':
        s = "([])"
    elif choice == '5':
        s = "([)]"
    elif choice == '6':
        s = input("请输入字符串 s: ").strip()
    else:
        print("无效选择，使用示例 1")
        s = "()"
    
    print("\n开始演示...")
    print(f"s = \"{s}\"")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")
    
    anim = ValidParenthesesAnimation(s)
    anim.show()


if __name__ == '__main__':
    main()


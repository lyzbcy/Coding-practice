"""
LeetCode 392. 判断子序列 - 动画演示
使用 matplotlib 手动控制双指针的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class IsSubsequenceAnimation:
    def __init__(self, s, t):
        self.s = list(s)  # 转为列表便于修改显示
        self.t = list(t)
        self.len_s = len(s)
        self.len_t = len(t)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.len_s, self.len_t, 10)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "bool isSubsequence(char* s, char* t) {",
            "    int i = 0;  // s 的指针",
            "    int j = 0;  // t 的指针",
            "    while (i < len_s && j < len_t) {",
            "        if (s[i] == t[j]) {",
            "            i++;  // 匹配成功",
            "        }",
            "        j++;  // 继续遍历 t",
            "    }",
            "    return i == len_s;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        self.fig.canvas.manager.set_window_title('判断子序列 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 10)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        i = 0  # s 的指针
        j = 0  # t 的指针

        self.steps.append({
            'i': i,
            'j': j,
            'action': '初始化：i=0（指向s），j=0（指向t），开始匹配',
            'code_highlight': [0, 1, 2],
            'explanations': [
                'i 指向 s 的第一个字符，j 指向 t 的第一个字符。',
                '我们将尝试在 t 中按顺序找到 s 的所有字符。'
            ],
            'match_result': None,
            'matched_chars': []
        })

        while i < self.len_s and j < self.len_t:
            # 比较字符
            is_match = self.s[i] == self.t[j]
            matched_chars = list(range(i))  # 已匹配的字符索引

            if is_match:
                self.steps.append({
                    'i': i,
                    'j': j,
                    'action': f's[{i}]="{self.s[i]}" == t[{j}]="{self.t[j]}"，匹配成功！',
                    'code_highlight': [4, 5],
                    'explanations': [
                        f's 的第 {i+1} 个字符 "{self.s[i]}" 在 t 的位置 {j} 找到了。',
                        'i 和 j 都向前移动。'
                    ],
                    'match_result': True,
                    'matched_chars': matched_chars
                })
                i += 1
                j += 1
            else:
                self.steps.append({
                    'i': i,
                    'j': j,
                    'action': f's[{i}]="{self.s[i]}" != t[{j}]="{self.t[j]}"，不匹配',
                    'code_highlight': [4, 7],
                    'explanations': [
                        f't 的位置 {j} 的字符 "{self.t[j]}" 不是我们需要的。',
                        '只移动 j，继续在 t 中寻找。'
                    ],
                    'match_result': False,
                    'matched_chars': matched_chars
                })
                j += 1

        # 判断结果
        if i == self.len_s:
            self.steps.append({
                'i': i,
                'j': j,
                'action': f'✅ 成功！i={i} == len(s)={self.len_s}，s 的所有字符都在 t 中找到了',
                'code_highlight': [9],
                'explanations': [
                    f's 的所有 {self.len_s} 个字符都在 t 中按顺序找到了。',
                    '返回 true：s 是 t 的子序列。'
                ],
                'match_result': True,
                'matched_chars': list(range(self.len_s))
            })
        else:
            self.steps.append({
                'i': i,
                'j': j,
                'action': f'❌ 失败！j={j} == len(t)={self.len_t}，但 i={i} < len(s)={self.len_s}',
                'code_highlight': [9],
                'explanations': [
                    f't 已经遍历完了，但 s 的第 {i+1} 个字符 "{self.s[i]}" 还没找到。',
                    '返回 false：s 不是 t 的子序列。'
                ],
                'match_result': False,
                'matched_chars': list(range(i))
            })

    def _draw_strings(self, step_data):
        """绘制两个字符串"""
        i = step_data['i']
        j = step_data['j']
        matched_chars = set(step_data.get('matched_chars', []))

        # 绘制字符串 s
        self.ax.text(-0.5, 6, 's:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        for idx in range(self.len_s):
            char = self.s[idx]
            # 确定颜色
            if idx == i and i < self.len_s:
                color = 'lightgreen'  # 当前要匹配的位置
            elif idx in matched_chars:
                color = 'lightblue'  # 已匹配的字符
            elif idx < i:
                color = 'lightgray'  # 已处理区域
            else:
                color = 'wheat'  # 待处理区域

            # 绘制字符框
            rect = patches.Rectangle(
                (idx - 0.45, 6 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)

            # 显示字符
            self.ax.text(idx, 6, char, ha='center', va='center',
                         fontsize=12, fontweight='bold')

            # 显示索引
            self.ax.text(idx, 5.1, f'[{idx}]', ha='center', va='center',
                         fontsize=9, color='gray')

        # 高亮当前 i 位置
        if i < self.len_s:
            rect = patches.Rectangle(
                (i - 0.45, 6 - 0.45), 0.9, 0.9,
                linewidth=3, edgecolor='red', facecolor='none'
            )
            self.ax.add_patch(rect)

        # 绘制字符串 t
        self.ax.text(-0.5, 3, 't:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        for idx in range(self.len_t):
            char = self.t[idx]
            # 确定颜色
            if idx == j and j < self.len_t:
                color = 'lightcoral'  # 当前检查的位置
            elif idx < j:
                color = 'lightgray'  # 已检查区域
            else:
                color = 'wheat'  # 待检查区域

            # 绘制字符框
            rect = patches.Rectangle(
                (idx - 0.45, 3 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)

            # 显示字符
            self.ax.text(idx, 3, char, ha='center', va='center',
                         fontsize=12, fontweight='bold')

            # 显示索引
            self.ax.text(idx, 2.1, f'[{idx}]', ha='center', va='center',
                         fontsize=9, color='gray')

        # 高亮当前 j 位置
        if j < self.len_t:
            rect = patches.Rectangle(
                (j - 0.45, 3 - 0.45), 0.9, 0.9,
                linewidth=3, edgecolor='blue', facecolor='none'
            )
            self.ax.add_patch(rect)

        # 如果匹配，画连接线
        if step_data.get('match_result') is True and i > 0:
            matched = step_data.get('matched_chars', [])
            if matched:
                # 找到对应的 t 中的位置（简化处理，实际需要记录）
                # 这里我们简化显示，只显示当前匹配
                if i <= len(matched):
                    # 可以添加连接线显示匹配关系
                    pass

    def _draw_pointers(self, step_data):
        """绘制指针"""
        i = step_data['i']
        j = step_data['j']

        # i 指针（指向 s）
        if i < self.len_s:
            self.ax.annotate('i', xy=(i, 6.8), xytext=(i, 7.8),
                             arrowprops=dict(arrowstyle='->', color='green', lw=2),
                             fontsize=12, color='green', ha='center', fontweight='bold')

        # j 指针（指向 t）
        if j < self.len_t:
            self.ax.annotate('j', xy=(j, 3.8), xytext=(j, 4.8),
                             arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                             fontsize=12, color='blue', ha='center', fontweight='bold')

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
            max(self.visual_width / 2, 5), 9.5,
            f'步骤 {step_index + 1}/{len(self.steps)}',
            ha='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )

        self.ax.text(
            max(self.visual_width / 2, 5), 8.6,
            step_data['action'],
            ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )

        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(
                max(self.visual_width / 2, 5), 7.6,
                explain_text,
                ha='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )

        # 显示匹配结果
        if step_data.get('match_result') is not None:
            result_text = '✅ 匹配' if step_data['match_result'] else '❌ 不匹配'
            result_color = 'lightgreen' if step_data['match_result'] else 'lightcoral'
            self.ax.text(
                max(self.visual_width / 2, 5), 6.8,
                result_text,
                ha='center', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor=result_color, alpha=0.8)
            )

        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            max(self.visual_width / 2, 5), 6.2,
            controls_text,
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

        # 绘制字符串
        self._draw_strings(step_data)

        # 绘制指针
        self._draw_pointers(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightgreen', 'i 当前位置（s中待匹配）'),
            ('lightblue', 's 中已匹配的字符'),
            ('lightcoral', 'j 当前位置（t中检查）'),
            ('lightgray', '已处理区域'),
            ('wheat', '待处理区域')
        ]
        for i, (color, text) in enumerate(legend_items):
            y_pos = 1.8 - i * 0.3
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
    print("LeetCode 392. 判断子序列 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print('1. 示例 1: s = "abc", t = "ahbgdc"')
    print('2. 示例 2: s = "axc", t = "ahbgdc"')
    print('3. 示例 3: s = "", t = "ahbgdc"')
    print('4. 简单示例: s = "ace", t = "abcde"')
    print('5. 自定义输入')

    choice = input("\n请输入选择 (1-5): ").strip()

    if choice == '1':
        s, t = "abc", "ahbgdc"
    elif choice == '2':
        s, t = "axc", "ahbgdc"
    elif choice == '3':
        s, t = "", "ahbgdc"
    elif choice == '4':
        s, t = "ace", "abcde"
    elif choice == '5':
        s = input("请输入字符串 s: ").strip()
        t = input("请输入字符串 t: ").strip()
    else:
        print("无效选择，使用示例 1")
        s, t = "abc", "ahbgdc"

    print("\n开始演示...")
    print(f's = "{s}"')
    print(f't = "{t}"')
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = IsSubsequenceAnimation(s, t)
    anim.show()


if __name__ == '__main__':
    main()


"""
LeetCode 14. 最长公共前缀 - 动画演示
使用 matplotlib 手动控制纵向扫描字符串数组的过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class LongestCommonPrefixAnimation:
    def __init__(self, strs):
        self.strs = strs
        self.strsSize = len(strs)
        self.steps = []
        self.current_step = 0
        self.max_len = max([len(s) for s in strs] + [6])
        self.x_limit = self.max_len + 14
        self.y_limit = self.strsSize + 8
        self.code_lines = [
            "char* longestCommonPrefix(char** strs, int strsSize) {",
            "    if (strsSize == 0) return \"\";",
            "    for (int i = 0; i < strlen(strs[0]); i++) {",
            "        char c = strs[0][i];",
            "        for (int j = 1; j < strsSize; j++) {",
            "            if (i >= strlen(strs[j]) || strs[j][i] != c) {",
            "                return prefix[0:i];",
            "            }",
            "        }",
            "    }",
            "    return strs[0];",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.fig.canvas.manager.set_window_title('最长公共前缀 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-1, self.y_limit)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        if self.strsSize == 0:
            self.steps.append({
                'i': None,
                'j': None,
                'prefix_len': 0,
                'action': '数组为空，返回空字符串',
                'code_highlight': [1],
                'explanations': ['输入数组为空，直接返回空字符串。']
            })
            return

        prefix_len = 0
        first_str_len = len(self.strs[0])

        # 初始状态
        self.steps.append({
            'i': None,
            'j': None,
            'prefix_len': 0,
            'action': f'初始化：以第一个字符串 "{self.strs[0]}" 为基准',
            'code_highlight': [2],
            'explanations': [
                '以第一个字符串为基准，开始纵向扫描。',
                f'共有 {self.strsSize} 个字符串需要比较。'
            ]
        })

        # 纵向扫描
        for i in range(first_str_len):
            char = self.strs[0][i]
            
            # 开始比较位置 i
            self.steps.append({
                'i': i,
                'j': None,
                'prefix_len': prefix_len,
                'action': f'检查位置 {i}：基准字符为 \'{char}\'',
                'code_highlight': [2, 3],
                'explanations': [
                    f'开始检查所有字符串的第 {i} 个字符。',
                    f'基准字符：strs[0][{i}] = \'{char}\''
                ]
            })

            # 检查所有其他字符串
            for j in range(1, self.strsSize):
                # 检查字符串 j 的位置 i
                if i >= len(self.strs[j]):
                    # 字符串长度不足
                    self.steps.append({
                        'i': i,
                        'j': j,
                        'prefix_len': prefix_len,
                        'action': f'strs[{j}] 长度不足，位置 {i} 不存在',
                        'code_highlight': [4, 5, 6],
                        'explanations': [
                            f'strs[{j}] = "{self.strs[j]}" 的长度为 {len(self.strs[j])}，',
                            f'位置 {i} 不存在，公共前缀结束。'
                        ]
                    })
                    return
                
                if self.strs[j][i] != char:
                    # 字符不匹配
                    self.steps.append({
                        'i': i,
                        'j': j,
                        'prefix_len': prefix_len,
                        'action': f'strs[{j}][{i}] = \'{self.strs[j][i]}\' 与基准字符 \'{char}\' 不匹配',
                        'code_highlight': [4, 5, 6],
                        'explanations': [
                            f'strs[{j}] = "{self.strs[j]}" 的第 {i} 个字符为 \'{self.strs[j][i]}\'，',
                            f'与基准字符 \'{char}\' 不匹配，公共前缀结束。'
                        ]
                    })
                    return
                
                # 字符匹配
                self.steps.append({
                    'i': i,
                    'j': j,
                    'prefix_len': prefix_len,
                    'action': f'strs[{j}][{i}] = \'{self.strs[j][i]}\' 匹配 ✓',
                    'code_highlight': [4, 5],
                    'explanations': [
                        f'strs[{j}] = "{self.strs[j]}" 的第 {i} 个字符匹配。',
                        '继续检查下一个字符串。'
                    ]
                })

            # 所有字符串的位置 i 都匹配
            prefix_len = i + 1
            self.steps.append({
                'i': i,
                'j': None,
                'prefix_len': prefix_len,
                'action': f'位置 {i} 所有字符串都匹配，当前公共前缀长度 = {prefix_len}',
                'code_highlight': [2, 3],
                'explanations': [
                    f'所有字符串的第 {i} 个字符都匹配。',
                    f'当前公共前缀："{self.strs[0][:prefix_len]}"'
                ]
            })

        # 所有字符都匹配
        self.steps.append({
            'i': None,
            'j': None,
            'prefix_len': prefix_len,
            'action': f'✅ 所有字符都匹配，返回完整公共前缀 "{self.strs[0]}"',
            'code_highlight': [10],
            'explanations': [
                f'第一个字符串的所有字符都与其他字符串匹配。',
                f'返回完整公共前缀："{self.strs[0]}"'
            ]
        })

    def _draw_strings(self, step_data):
        """绘制字符串数组"""
        i = step_data['i']
        j = step_data['j']
        prefix_len = step_data['prefix_len']

        # 绘制每个字符串
        for str_idx in range(self.strsSize):
            y_pos = self.strsSize - str_idx - 1
            
            # 字符串标签
            self.ax.text(-1.5, y_pos, f'strs[{str_idx}]:', ha='right', va='center',
                         fontsize=12, fontweight='bold')
            
            # 绘制字符
            for char_idx in range(self.max_len):
                if char_idx < len(self.strs[str_idx]):
                    char = self.strs[str_idx][char_idx]
                else:
                    char = ''
                
                # 确定颜色
                if char_idx < prefix_len:
                    color = 'lightgreen'  # 已确认的公共前缀
                elif i is not None and char_idx == i:
                    if j is not None and str_idx == j:
                        color = 'lightcoral'  # 不匹配的位置
                    else:
                        color = 'lightyellow'  # 正在比较的位置
                else:
                    color = 'lightgray'  # 其他区域
                
                # 绘制字符框
                rect = patches.Rectangle(
                    (char_idx - 0.45, y_pos - 0.45), 0.9, 0.9,
                    linewidth=2, edgecolor='black', facecolor=color
                )
                self.ax.add_patch(rect)
                
                if char:
                    self.ax.text(char_idx, y_pos, char, ha='center', va='center',
                                 fontsize=14, fontweight='bold')
                    self.ax.text(char_idx, y_pos - 0.6, f'[{char_idx}]', ha='center', va='center',
                                 fontsize=9, color='gray')

    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step

        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index

        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-1, self.y_limit)

        step_data = self.steps[step_index]

        # 标题与说明
        self.ax.text(
            max(self.max_len / 2, 3), self.y_limit - 1,
            f'步骤 {step_index + 1}/{len(self.steps)}',
            ha='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )

        self.ax.text(
            max(self.max_len / 2, 3), self.y_limit - 2,
            step_data['action'],
            ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )

        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(
                max(self.max_len / 2, 3), self.y_limit - 3.5,
                explain_text,
                ha='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )

        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            max(self.max_len / 2, 3), self.y_limit - 4.5,
            controls_text,
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

        # 状态信息
        prefix_text = f'当前公共前缀长度 = {step_data["prefix_len"]}'
        if step_data['prefix_len'] > 0:
            prefix_str = self.strs[0][:step_data['prefix_len']]
            prefix_text += f' ("{prefix_str}")'
        self.ax.text(-1, self.y_limit - 1, prefix_text, fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))

        # 绘制字符串数组
        self._draw_strings(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightgreen', '已确认的公共前缀'),
            ('lightyellow', '正在比较的位置'),
            ('lightcoral', '不匹配的位置'),
            ('lightgray', '其他区域')
        ]
        for idx, (color, text) in enumerate(legend_items):
            rect = patches.Rectangle((idx * 2, self.y_limit - 6), 0.5, 0.5,
                                     facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(idx * 2 + 0.6, self.y_limit - 5.75, text, fontsize=10, va='center')

    def _draw_code_panel(self, step_data):
        start_x = self.max_len + 1.5
        start_y = self.strsSize - 1
        line_height = 0.5
        highlight = set(step_data.get('code_highlight', []))

        self.ax.text(start_x, start_y + 1.5, 'C 代码同步显示', fontsize=13,
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
    print("LeetCode 14. 最长公共前缀 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: strs=[\"flower\",\"flow\",\"flight\"]")
    print("2. 示例 2: strs=[\"dog\",\"racecar\",\"car\"]")
    print("3. 示例 3: strs=[\"ab\", \"a\"]")
    print("4. 自定义输入")

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        strs = ["flower", "flow", "flight"]
    elif choice == '2':
        strs = ["dog", "racecar", "car"]
    elif choice == '3':
        strs = ["ab", "a"]
    elif choice == '4':
        input_str = input("请输入字符串数组（用逗号分隔）: ").strip()
        strs = [s.strip().strip('"').strip("'") for s in input_str.split(',')]
    else:
        print("无效选择，使用示例 1")
        strs = ["flower", "flow", "flight"]

    print("\n开始演示...")
    print(f'strs = {strs}')
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = LongestCommonPrefixAnimation(strs)
    anim.show()


if __name__ == '__main__':
    main()



"""
LeetCode 383. 赎金信 - 动画演示
使用 matplotlib 手动控制“统计 magazine → 消耗 ransomNote”的过程
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class RansomNoteAnimation:
    def __init__(self, ransom, magazine):
        self.ransom = ransom
        self.magazine = magazine
        self.steps = []
        self.current_step = 0
        self.code_lines = [
            "bool canConstruct(char* ransomNote, char* magazine) {",
            "    int count[26] = {0};",
            "    for (int i = 0; magazine[i] != '\\0'; i++) {",
            "        count[magazine[i] - 'a']++;",
            "    }",
            "    for (int i = 0; ransomNote[i] != '\\0'; i++) {",
            "        int idx = ransomNote[i] - 'a';",
            "        count[idx]--;",
            "        if (count[idx] < 0) return false;",
            "    }",
            "    return true;",
            "}",
        ]

        self.letters = sorted(set(ransom + magazine)) or ['a']
        self._simulate()

        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.canvas.manager.set_window_title('赎金信 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, len(self.letters) + 12)
        self.ax.set_ylim(-3, 10)
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate(self):
        counts = {ch: 0 for ch in self.letters}

        self.steps.append({
            'phase': 'init',
            'mag_idx': None,
            'ran_idx': None,
            'counts': counts.copy(),
            'action': '初始化：count[26] = 0，准备统计 magazine',
            'notes': ['所有字母库存置零。'],
            'code_highlight': [0, 1]
        })

        # 统计 magazine
        for idx, ch in enumerate(self.magazine):
            counts[ch] += 1
            self.steps.append({
                'phase': 'mag',
                'mag_idx': idx,
                'ran_idx': None,
                'counts': counts.copy(),
                'action': f'统计 magazine[{idx}] = \\'{ch}\\'，库存 {ch} -> {counts[ch]}',
                'notes': [
                    f'将字母 {ch} 计入库存。',
                    '后续赎金信可用该库存。'
                ],
                'code_highlight': [2, 3, 4],
                'focus_letter': ch
            })

        self.steps.append({
            'phase': 'transition',
            'mag_idx': None,
            'ran_idx': None,
            'counts': counts.copy(),
            'action': 'magazine 统计完成，开始消耗 ransomNote',
            'notes': ['逐个字符扣减库存，一旦出现负数即失败。'],
            'code_highlight': [5]
        })

        # 消耗 ransomNote
        for idx, ch in enumerate(self.ransom):
            counts[ch] -= 1
            if counts[ch] < 0:
                self.steps.append({
                    'phase': 'fail',
                    'mag_idx': None,
                    'ran_idx': idx,
                    'counts': counts.copy(),
                    'action': (f'扣减 ransomNote[{idx}] = \\'{ch}\\' 后库存变为 {counts[ch]}，'
                               '出现负数 => 无法构成'),
                    'notes': [
                        f'字母 {ch} 需求超出 magazine 提供数量。',
                        '立即返回 false。'
                    ],
                    'code_highlight': [5, 6, 7, 8],
                    'focus_letter': ch
                })
                break

            self.steps.append({
                'phase': 'ransom',
                'mag_idx': None,
                'ran_idx': idx,
                'counts': counts.copy(),
                'action': f'扣减 ransomNote[{idx}] = \\'{ch}\\'，剩余 {ch} = {counts[ch]}',
                'notes': [
                    f'库存充足，继续处理下一位。',
                ],
                'code_highlight': [5, 6, 7],
                'focus_letter': ch
            })
        else:
            self.steps.append({
                'phase': 'success',
                'mag_idx': None,
                'ran_idx': len(self.ransom) - 1 if self.ransom else None,
                'counts': counts.copy(),
                'action': '✅ 所有字符扣减完毕，返回 true',
                'notes': ['杂志提供的字符足够，成功构造赎金信。'],
                'code_highlight': [9, 10]
            })

    def _draw_counts(self, step):
        letters = self.letters
        counts = [step['counts'][ch] for ch in letters]
        x = np.arange(len(letters))
        colors = []
        focus = step.get('focus_letter')
        for ch in letters:
            if step['counts'][ch] < 0:
                colors.append('#f28b82')  # red
            elif ch == focus:
                colors.append('#ffe082')  # yellow
            else:
                colors.append('#90caf9')  # blue

        bars = self.ax.bar(x, counts, color=colors, edgecolor='black')
        for rect, val in zip(bars, counts):
            self.ax.text(rect.get_x() + rect.get_width() / 2,
                         rect.get_height() + 0.05,
                         str(val),
                         ha='center',
                         fontsize=11)

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(letters, fontsize=12)
        self.ax.set_ylim(min(-1, min(counts) - 1), max(3, max(counts) + 2))
        self.ax.set_ylabel('库存数量')

    def _draw_strings(self, step):
        self.ax.text(-0.5, 7.5, f'magazine: "{self.magazine}"', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.6))
        self.ax.text(-0.5, 6.5, f'rensomNote: "{self.ransom}"', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.6))

        if step['mag_idx'] is not None:
            idx = step['mag_idx']
            self.ax.annotate('mag idx', xy=(idx, 6.2), xytext=(idx, 5.6),
                             arrowprops=dict(arrowstyle='->', color='purple', lw=2),
                             ha='center', color='purple')

        if step['ran_idx'] is not None and self.ransom:
            idx = step['ran_idx']
            self.ax.annotate('ransom idx', xy=(idx, 4.8), xytext=(idx, 4.0),
                             arrowprops=dict(arrowstyle='->', color='green', lw=2),
                             ha='center', color='green')

    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step
        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index

        step = self.steps[step_index]
        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-1, len(self.letters) + 12)
        self.ax.set_ylim(-3, 10)

        self.ax.text(len(self.letters) / 2, 9.2,
                     f'步骤 {step_index + 1}/{len(self.steps)}',
                     fontsize=16, fontweight='bold',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        self.ax.text(len(self.letters) / 2, 8.2,
                     step['action'],
                     fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True)
        if step.get('notes'):
            notes = '\n'.join(f'· {line}' for line in step['notes'])
            self.ax.text(len(self.letters) / 2, 7.2,
                         notes,
                         fontsize=11,
                         bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True)

        controls = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(len(self.letters) / 2, -2.2,
                     controls,
                     fontsize=10,
                     bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6))

        self._draw_strings(step)
        self._draw_counts(step)
        self._draw_code_panel(step)

    def _draw_code_panel(self, step):
        start_x = len(self.letters) + 1
        start_y = 6.5
        line_height = 0.6
        highlight = set(step.get('code_highlight', []))

        self.ax.text(start_x, start_y + 1.8, 'C 代码同步显示', fontsize=13,
                     fontweight='bold',
                     bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.6))

        for idx, line in enumerate(self.code_lines):
            y = start_y - idx * line_height
            facecolor = 'peachpuff' if idx in highlight else 'white'
            self.ax.text(start_x, y,
                         f'{idx + 1:02d} {line}',
                         fontsize=9,
                         family='monospace',
                         bbox=dict(boxstyle='round', facecolor=facecolor, alpha=0.9, pad=0.2))

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
    print("LeetCode 383. 赎金信 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: ransomNote=\"a\", magazine=\"b\"")
    print("2. 示例 2: ransomNote=\"aa\", magazine=\"ab\"")
    print("3. 示例 3: ransomNote=\"aa\", magazine=\"aab\"")
    print("4. 自定义输入")

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        ransom, magazine = "a", "b"
    elif choice == '2':
        ransom, magazine = "aa", "ab"
    elif choice == '3':
        ransom, magazine = "aa", "aab"
    elif choice == '4':
        ransom = input("请输入 ransomNote: ").strip()
        magazine = input("请输入 magazine: ").strip()
    else:
        print("无效选择，默认使用示例 3")
        ransom, magazine = "aa", "aab"

    print("\n开始演示...")
    print(f"ransomNote = \"{ransom}\"")
    print(f"magazine   = \"{magazine}\"")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = RansomNoteAnimation(ransom, magazine)
    anim.show()


if __name__ == '__main__':
    main()



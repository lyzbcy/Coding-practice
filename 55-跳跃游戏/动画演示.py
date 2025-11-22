"""
LeetCode 55. 跳跃游戏 - 动画演示
使用 matplotlib 手动控制贪心算法的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class JumpGameAnimation:
    def __init__(self, nums):
        self.nums = nums.copy()
        self.length = len(nums)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "bool canJump(int* nums, int numsSize) {",
            "    int maxReach = 0;",
            "    for(int i = 0; i < numsSize; i++) {",
            "        if(i > maxReach) {",
            "            return false;",
            "        }",
            "        maxReach = max(maxReach, i + nums[i]);",
            "        if(maxReach >= numsSize - 1) {",
            "            return true;",
            "        }",
            "    }",
            "    return true;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.canvas.manager.set_window_title('跳跃游戏 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 8)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        maxReach = 0
        self.steps.append({
            'nums': self.nums.copy(),
            'i': None,
            'maxReach': maxReach,
            'canReach': True,
            'action': '初始化：maxReach=0，开始遍历数组',
            'code_highlight': [0, 1],
            'explanations': [
                'maxReach 表示当前能到达的最远位置，初始为 0。',
                '从位置 0 开始遍历数组。'
            ]
        })

        for i in range(self.length):
            # 检查可达性
            canReach = i <= maxReach
            if not canReach:
                action = f'位置 {i} 无法到达（i={i} > maxReach={maxReach}），返回 false'
                code_lines = [2, 3, 4, 5]
                explanations = [
                    f'当前位置 i = {i}，但 maxReach = {maxReach}。',
                    f'因为 i > maxReach，说明无法到达位置 {i}，返回 false。'
                ]
                self.steps.append({
                    'nums': self.nums.copy(),
                    'i': i,
                    'maxReach': maxReach,
                    'canReach': False,
                    'action': action,
                    'code_highlight': code_lines,
                    'explanations': explanations
                })
                break

            # 更新 maxReach
            oldMaxReach = maxReach
            maxReach = max(maxReach, i + self.nums[i])
            reachable = i + self.nums[i]

            if maxReach >= self.length - 1:
                action = f'位置 {i}：maxReach={maxReach} >= {self.length-1}，可以到达终点，返回 true'
                code_lines = [2, 3, 6, 7, 8, 9]
                explanations = [
                    f'从位置 {i} 最多能到达位置 {reachable}。',
                    f'更新 maxReach = max({oldMaxReach}, {reachable}) = {maxReach}。',
                    f'因为 maxReach >= {self.length-1}，可以到达终点，返回 true。'
                ]
            else:
                if maxReach > oldMaxReach:
                    action = f'位置 {i}：更新 maxReach = {maxReach}（从位置 {i} 最多能到位置 {reachable}）'
                else:
                    action = f'位置 {i}：maxReach 保持不变 = {maxReach}（从位置 {i} 最多能到位置 {reachable}）'
                code_lines = [2, 3, 6]
                explanations = [
                    f'当前位置 i = {i}，可以到达（i <= maxReach）。',
                    f'从位置 {i} 最多能到达位置 {reachable}。',
                    f'更新 maxReach = max({oldMaxReach}, {reachable}) = {maxReach}。'
                ]

            self.steps.append({
                'nums': self.nums.copy(),
                'i': i,
                'maxReach': maxReach,
                'canReach': True,
                'action': action,
                'code_highlight': code_lines,
                'explanations': explanations
            })

            if maxReach >= self.length - 1:
                break

        # 如果遍历完成
        if self.steps[-1]['canReach']:
            self.steps.append({
                'nums': self.nums.copy(),
                'i': None,
                'maxReach': maxReach,
                'canReach': True,
                'action': f'✅ 遍历完成，可以到达终点（maxReach={maxReach} >= {self.length-1}）',
                'code_highlight': [11],
                'explanations': [
                    f'遍历完整个数组，maxReach = {maxReach}。',
                    f'因为 maxReach >= {self.length-1}，可以到达终点，返回 true。'
                ]
            })

    def _draw_array(self, step_data):
        nums = step_data['nums']
        max_len = max(self.length, 1)
        i = step_data['i']
        maxReach = step_data['maxReach']

        for idx in range(max_len):
            val = nums[idx] if idx < len(nums) else ''
            
            # 确定颜色
            if idx <= maxReach:
                if i is not None and idx == i:
                    color = 'lightgreen'  # 当前位置
                elif idx <= maxReach:
                    color = 'lightblue'  # 可达区域
                else:
                    color = 'lightgray'
            else:
                color = 'lightgray'  # 不可达区域

            rect = patches.Rectangle(
                (idx - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)
            self.ax.text(idx, 1, str(val), ha='center', va='center',
                         fontsize=14, fontweight='bold')
            self.ax.text(idx, 0.1, f'[{idx}]', ha='center', va='center',
                         fontsize=10, color='gray')

            # 绘制从当前位置能到达的范围
            if i is not None and idx == i:
                reachable = i + nums[i]
                for j in range(i + 1, min(reachable + 1, max_len)):
                    if j < max_len:
                        # 绘制箭头表示可达
                        self.ax.annotate('', xy=(j, 1.3), xytext=(i, 1.3),
                                        arrowprops=dict(arrowstyle='->', 
                                                       color='orange', 
                                                       lw=1.5, alpha=0.6))

        # 高亮当前位置
        if i is not None and 0 <= i < max_len:
            rect = patches.Rectangle(
                (i - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=3, edgecolor='red', facecolor='none'
            )
            self.ax.add_patch(rect)

    def _draw_pointers(self, step_data):
        i = step_data['i']
        maxReach = step_data['maxReach']
        max_len = max(self.length, 1)

        # maxReach 标记
        if maxReach < max_len:
            self.ax.annotate('maxReach', xy=(maxReach, 1.8), xytext=(maxReach, 2.8),
                             arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                             fontsize=12, color='blue', ha='center')
        else:
            self.ax.text(max_len - 0.5, 2.5, f'maxReach={maxReach}',
                         color='blue', fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

        # 当前位置 i
        if i is not None and i < max_len:
            self.ax.annotate('i', xy=(i, 0.2), xytext=(i, -0.8),
                             arrowprops=dict(arrowstyle='->', color='green', lw=2),
                             fontsize=12, color='green', ha='center')

        # 绘制可达区域
        if maxReach >= 0:
            reachable_end = min(maxReach, max_len - 1)
            if reachable_end >= 0:
                rect = patches.Rectangle(
                    (-0.45, 1.5), reachable_end + 0.9, 0.3,
                    linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.3
                )
                self.ax.add_patch(rect)
                self.ax.text(reachable_end / 2, 1.65, '可达区域', 
                            ha='center', fontsize=10, color='blue')

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
        self.ax.text(-0.5, 4.8, f'maxReach = {step_data["maxReach"]}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))
        if step_data['i'] is not None:
            self.ax.text(-0.5, 4.1, f'当前位置 i = {step_data["i"]}', fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
            if step_data['i'] < self.length:
                reachable = step_data['i'] + self.nums[step_data['i']]
                self.ax.text(-0.5, 3.4, f'从位置 {step_data["i"]} 最多能到 {reachable}', 
                             fontsize=11,
                             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

        # 绘制数组
        self.ax.text(-0.5, 1, 'nums:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_array(step_data)

        # 绘制指针和标记
        self._draw_pointers(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightblue', '可达区域'),
            ('lightgreen', '当前位置'),
            ('lightgray', '不可达区域'),
            ('orange', '可达路径')
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
    print("LeetCode 55. 跳跃游戏 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: nums=[2,3,1,1,4] (可以到达)")
    print("2. 示例 2: nums=[3,2,1,0,4] (无法到达)")
    print("3. 示例 3: nums=[0] (已在终点)")
    print("4. 示例 4: nums=[1,0,1,0] (无法到达)")
    print("5. 自定义输入")

    choice = input("\n请输入选择 (1-5): ").strip()

    if choice == '1':
        nums = [2, 3, 1, 1, 4]
    elif choice == '2':
        nums = [3, 2, 1, 0, 4]
    elif choice == '3':
        nums = [0]
    elif choice == '4':
        nums = [1, 0, 1, 0]
    elif choice == '5':
        nums = list(map(int, input("请输入 nums（空格分隔）: ").split()))
    else:
        print("无效选择，使用示例 1")
        nums = [2, 3, 1, 1, 4]

    print("\n开始演示...")
    print(f"nums = {nums}")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = JumpGameAnimation(nums)
    anim.show()


if __name__ == '__main__':
    main()


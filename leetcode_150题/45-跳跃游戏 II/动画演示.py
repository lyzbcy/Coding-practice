"""
LeetCode 45. 跳跃游戏 II - 动画演示
使用 matplotlib 手动控制贪心算法（边界跳跃法）的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class JumpGameIIAnimation:
    def __init__(self, nums):
        self.nums = nums.copy()
        self.length = len(nums)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "int jump(int* nums, int numsSize) {",
            "    int jumps = 0;",
            "    int end = 0;",
            "    int maxReach = 0;",
            "    for(int i = 0; i < numsSize - 1; i++) {",
            "        maxReach = max(maxReach, i + nums[i]);",
            "        if(i == end) {",
            "            jumps++;",
            "            end = maxReach;",
            "        }",
            "    }",
            "    return jumps;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.canvas.manager.set_window_title('跳跃游戏 II - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 8)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        jumps = 0
        end = 0
        maxReach = 0
        
        self.steps.append({
            'nums': self.nums.copy(),
            'i': None,
            'jumps': jumps,
            'end': end,
            'maxReach': maxReach,
            'action': '初始化：jumps=0, end=0, maxReach=0，开始遍历数组',
            'code_highlight': [0, 1, 2, 3],
            'explanations': [
                'jumps 表示跳跃次数，初始为 0。',
                'end 表示上一次跳跃能到达的最远位置（边界），初始为 0。',
                'maxReach 表示当前能到达的最远位置，初始为 0。',
                '从位置 0 开始遍历数组（只遍历到 numsSize - 1）。'
            ]
        })

        for i in range(self.length - 1):  # 只遍历到 length - 1
            oldMaxReach = maxReach
            reachable = i + self.nums[i]
            maxReach = max(maxReach, reachable)
            
            # 检查是否到达边界
            reached_end = (i == end)
            if reached_end:
                oldJumps = jumps
                oldEnd = end
                jumps += 1
                end = maxReach
                action = f'位置 {i}：到达边界 end={oldEnd}，需要再跳一次，jumps={jumps}，更新 end={end}'
                code_lines = [4, 5, 6, 7, 8, 9]
                explanations = [
                    f'当前位置 i = {i}，从位置 {i} 最多能到达位置 {reachable}。',
                    f'更新 maxReach = max({oldMaxReach}, {reachable}) = {maxReach}。',
                    f'因为 i == end（{i} == {oldEnd}），到达了上一次跳跃的边界。',
                    f'需要再跳一次，更新 jumps = {oldJumps} + 1 = {jumps}。',
                    f'更新边界 end = maxReach = {end}。'
                ]
            else:
                if maxReach > oldMaxReach:
                    action = f'位置 {i}：更新 maxReach = {maxReach}（从位置 {i} 最多能到位置 {reachable}）'
                else:
                    action = f'位置 {i}：maxReach 保持不变 = {maxReach}（从位置 {i} 最多能到位置 {reachable}）'
                code_lines = [4, 5]
                explanations = [
                    f'当前位置 i = {i}，从位置 {i} 最多能到达位置 {reachable}。',
                    f'更新 maxReach = max({oldMaxReach}, {reachable}) = {maxReach}。',
                    f'因为 i != end（{i} != {end}），未到达边界，不需要跳跃。'
                ]

            self.steps.append({
                'nums': self.nums.copy(),
                'i': i,
                'jumps': jumps,
                'end': end,
                'maxReach': maxReach,
                'action': action,
                'code_highlight': code_lines,
                'explanations': explanations
            })

        # 结束
        self.steps.append({
            'nums': self.nums.copy(),
            'i': None,
            'jumps': jumps,
            'end': end,
            'maxReach': maxReach,
            'action': f'✅ 遍历完成，最小跳跃次数为 {jumps}',
            'code_highlight': [11],
            'explanations': [
                f'遍历完数组（到位置 {self.length - 2}），返回 jumps = {jumps}。',
                f'这是到达最后一个位置的最小跳跃次数。'
            ]
        })

    def _draw_array(self, step_data):
        nums = step_data['nums']
        max_len = max(self.length, 1)
        i = step_data['i']
        end = step_data['end']
        maxReach = step_data['maxReach']

        for idx in range(max_len):
            val = nums[idx] if idx < len(nums) else ''
            
            # 确定颜色
            if idx <= end:
                if i is not None and idx == i:
                    color = 'lightgreen'  # 当前位置
                else:
                    color = 'lightblue'  # 边界内（可达区域）
            elif idx <= maxReach:
                color = 'lightyellow'  # 边界外但可达
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
        end = step_data['end']
        maxReach = step_data['maxReach']
        max_len = max(self.length, 1)

        # end 边界标记
        if end < max_len:
            self.ax.annotate('end', xy=(end, 1.8), xytext=(end, 2.8),
                             arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                             fontsize=12, color='blue', ha='center')
        else:
            self.ax.text(max_len - 0.5, 2.5, f'end={end}',
                         color='blue', fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

        # maxReach 标记
        if maxReach < max_len:
            self.ax.annotate('maxReach', xy=(maxReach, 1.5), xytext=(maxReach, 2.2),
                             arrowprops=dict(arrowstyle='->', color='purple', lw=2),
                             fontsize=12, color='purple', ha='center')
        else:
            self.ax.text(max_len - 0.5, 2.0, f'maxReach={maxReach}',
                         color='purple', fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.7))

        # 当前位置 i
        if i is not None and i < max_len:
            self.ax.annotate('i', xy=(i, 0.2), xytext=(i, -0.8),
                             arrowprops=dict(arrowstyle='->', color='green', lw=2),
                             fontsize=12, color='green', ha='center')

        # 绘制边界区域
        if end >= 0:
            end_pos = min(end, max_len - 1)
            if end_pos >= 0:
                rect = patches.Rectangle(
                    (-0.45, 1.5), end_pos + 0.9, 0.3,
                    linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.3
                )
                self.ax.add_patch(rect)
                self.ax.text(end_pos / 2, 1.65, '边界内', 
                            ha='center', fontsize=10, color='blue')

        # 绘制 maxReach 区域
        if maxReach > end and maxReach < max_len:
            reach_pos = min(maxReach, max_len - 1)
            if reach_pos > end:
                rect = patches.Rectangle(
                    (end + 0.45, 1.5), reach_pos - end, 0.3,
                    linewidth=2, edgecolor='purple', facecolor='lightyellow', alpha=0.3
                )
                self.ax.add_patch(rect)
                self.ax.text((end + reach_pos) / 2, 1.65, '可达但需跳跃', 
                            ha='center', fontsize=10, color='purple')

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
        self.ax.text(-0.5, 4.8, f'jumps = {step_data["jumps"]}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))
        self.ax.text(-0.5, 4.1, f'end = {step_data["end"]}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        self.ax.text(-0.5, 3.4, f'maxReach = {step_data["maxReach"]}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        if step_data['i'] is not None:
            self.ax.text(-0.5, 2.7, f'当前位置 i = {step_data["i"]}', fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
            if step_data['i'] < self.length:
                reachable = step_data['i'] + self.nums[step_data['i']]
                self.ax.text(-0.5, 2.0, f'从位置 {step_data["i"]} 最多能到 {reachable}', 
                             fontsize=11,
                             bbox=dict(boxstyle='round', facecolor='peachpuff', alpha=0.8))

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
            ('lightblue', '边界内'),
            ('lightyellow', '可达但需跳跃'),
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
    print("LeetCode 45. 跳跃游戏 II - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: nums=[2,3,1,1,4] (最小跳跃次数: 2)")
    print("2. 示例 2: nums=[2,3,0,1,4] (最小跳跃次数: 2)")
    print("3. 示例 3: nums=[1,1,1,1] (最小跳跃次数: 3)")
    print("4. 示例 4: nums=[1] (最小跳跃次数: 0)")
    print("5. 自定义输入")

    choice = input("\n请输入选择 (1-5): ").strip()

    if choice == '1':
        nums = [2, 3, 1, 1, 4]
    elif choice == '2':
        nums = [2, 3, 0, 1, 4]
    elif choice == '3':
        nums = [1, 1, 1, 1]
    elif choice == '4':
        nums = [1]
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

    anim = JumpGameIIAnimation(nums)
    anim.show()


if __name__ == '__main__':
    main()


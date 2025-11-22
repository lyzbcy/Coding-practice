"""
LeetCode 169. 多数元素 - 动画演示
使用 matplotlib 手动控制 Boyer-Moore 投票算法的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class MajorityElementAnimation:
    def __init__(self, nums):
        self.nums = nums.copy()
        self.length = len(nums)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "int majorityElement(int* nums, int numsSize) {",
            "    int candidate = nums[0];",
            "    int count = 1;",
            "    for (int i = 1; i < numsSize; i++) {",
            "        if (count == 0) {",
            "            candidate = nums[i];",
            "            count = 1;",
            "        } else if (nums[i] == candidate) {",
            "            count++;",
            "        } else {",
            "            count--;",
            "        }",
            "    }",
            "    return candidate;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.canvas.manager.set_window_title('多数元素 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 8)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        candidate = self.nums[0]
        count = 1
        
        self.steps.append({
            'nums': self.nums.copy(),
            'candidate': candidate,
            'count': count,
            'i': None,
            'current_value': None,
            'action': '初始化：candidate=nums[0]，count=1，开始遍历',
            'code_highlight': [0, 1, 2],
            'explanations': [
                '将第一个元素设为候选多数元素 candidate。',
                '初始化计数器 count = 1，表示候选元素已出现一次。',
                '从索引 1 开始遍历数组。'
            ]
        })

        for i in range(1, self.length):
            current_value = self.nums[i]
            
            if count == 0:
                candidate = current_value
                count = 1
                action = f'nums[{i}]={current_value}，count=0，更新 candidate={current_value}，count=1'
                code_lines = [3, 4, 5, 6, 7]
                explanations = [
                    f'当前计数器 count = 0，前面的元素已抵消完毕。',
                    f'将 nums[{i}] = {current_value} 设为新的候选元素。',
                    '重置计数器 count = 1。'
                ]
            elif current_value == candidate:
                count += 1
                action = f'nums[{i}]={current_value} 等于 candidate，count++ → {count}'
                code_lines = [3, 7, 8]
                explanations = [
                    f'nums[{i}] = {current_value} 与候选元素 candidate = {candidate} 相同。',
                    f'计数器加 1，count = {count}。'
                ]
            else:
                count -= 1
                action = f'nums[{i}]={current_value} 不等于 candidate，count-- → {count}'
                code_lines = [3, 9, 10]
                explanations = [
                    f'nums[{i}] = {current_value} 与候选元素 candidate = {candidate} 不同。',
                    f'计数器减 1（抵消），count = {count}。'
                ]

            self.steps.append({
                'nums': self.nums.copy(),
                'candidate': candidate,
                'count': count,
                'i': i,
                'current_value': current_value,
                'action': action,
                'code_highlight': code_lines,
                'explanations': explanations
            })

        self.steps.append({
            'nums': self.nums.copy(),
            'candidate': candidate,
            'count': count,
            'i': None,
            'current_value': None,
            'action': f'✅ 遍历完成，返回 candidate = {candidate}',
            'code_highlight': [13],
            'explanations': [
                f'遍历结束，最终候选元素 candidate = {candidate}。',
                '由于题目保证存在多数元素，candidate 就是答案。',
                f'最终计数器 count = {count}（注意：这不是多数元素出现次数）。'
            ]
        })

    def _draw_array(self, step_data):
        nums = step_data['nums']
        candidate = step_data['candidate']
        max_len = max(self.length, 1)

        for idx in range(max_len):
            val = nums[idx] if idx < len(nums) else ''
            # 根据元素是否等于候选元素来着色
            if idx < len(nums):
                if nums[idx] == candidate:
                    color = 'lightgreen'  # 与候选相同
                else:
                    color = 'lightcoral'  # 与候选不同
            else:
                color = 'lightgray'

            rect = patches.Rectangle(
                (idx - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)
            self.ax.text(idx, 1, str(val), ha='center', va='center',
                         fontsize=14, fontweight='bold')
            self.ax.text(idx, 0.1, f'[{idx}]', ha='center', va='center',
                         fontsize=10, color='gray')

        # 高亮当前遍历位置
        if step_data['i'] is not None:
            i = step_data['i']
            if 0 <= i < max_len:
                rect = patches.Rectangle(
                    (i - 0.45, 1 - 0.45), 0.9, 0.9,
                    linewidth=3, edgecolor='red', facecolor='none'
                )
                self.ax.add_patch(rect)

    def _draw_state(self, step_data):
        candidate = step_data['candidate']
        count = step_data['count']
        i = step_data['i']
        
        # 显示候选元素和计数器
        state_text = f'候选元素 candidate = {candidate}\n计数器 count = {count}'
        self.ax.text(
            -0.5, 4.5, state_text,
            fontsize=12, ha='left', va='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8)
        )
        
        if i is not None:
            current_text = f'当前遍历: i = {i}, nums[{i}] = {step_data["current_value"]}'
            self.ax.text(
                -0.5, 3.8, current_text,
                fontsize=11, ha='left', va='top',
                bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8)
            )

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

        # 绘制状态信息
        self._draw_state(step_data)

        # 绘制数组
        self.ax.text(-0.5, 1, 'nums:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_array(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightgreen', '等于 candidate'),
            ('lightcoral', '不等于 candidate'),
            ('red边框', '当前遍历位置')
        ]
        for i, (color, text) in enumerate(legend_items):
            if color == 'red边框':
                rect = patches.Rectangle((i * 2.5, 3.3), 0.5, 0.5,
                                         facecolor='white', edgecolor='red', linewidth=2)
            else:
                rect = patches.Rectangle((i * 2.5, 3.3), 0.5, 0.5,
                                         facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(i * 2.5 + 0.6, 3.55, text, fontsize=10, va='center')

    def _draw_code_panel(self, step_data):
        start_x = self.visual_width + 1.5
        start_y = 3.5
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
    print("LeetCode 169. 多数元素 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: nums=[3,2,3]")
    print("2. 示例 2: nums=[2,2,1,1,1,2,2]")
    print("3. 简单示例: nums=[1,1,2]")
    print("4. 自定义输入")

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        nums = [3, 2, 3]
    elif choice == '2':
        nums = [2, 2, 1, 1, 1, 2, 2]
    elif choice == '3':
        nums = [1, 1, 2]
    elif choice == '4':
        nums = list(map(int, input("请输入 nums（空格分隔）: ").split()))
    else:
        print("无效选择，使用示例 1")
        nums = [3, 2, 3]

    print("\n开始演示...")
    print(f"nums = {nums}")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = MajorityElementAnimation(nums)
    anim.show()


if __name__ == '__main__':
    main()


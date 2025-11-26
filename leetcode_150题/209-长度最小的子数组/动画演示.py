"""
LeetCode 209. 长度最小的子数组 - 动画演示
使用 matplotlib 手动控制滑动窗口的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class MinSubArrayLenAnimation:
    def __init__(self, nums, target):
        """
        初始化动画
        nums: 输入数组
        target: 目标值
        """
        self.nums = nums
        self.target = target
        self.length = len(nums)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "int minSubArrayLen(int target, int* nums, int numsSize) {",
            "    int left = 0;",
            "    int sum = 0;",
            "    int minLen = INT_MAX;",
            "    for (int right = 0; right < numsSize; right++) {",
            "        sum += nums[right];  // 扩展窗口",
            "        while (sum >= target) {",
            "            minLen = min(minLen, right - left + 1);",
            "            sum -= nums[left];  // 缩小窗口",
            "            left++;",
            "        }",
            "    }",
            "    return minLen == INT_MAX ? 0 : minLen;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(18, 12))
        self.fig.canvas.manager.set_window_title('长度最小的子数组 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-2, self.x_limit)
        self.ax.set_ylim(-4, 12)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        left = 0
        sum_val = 0
        minLen = float('inf')
        
        # 初始化步骤
        self.steps.append({
            'left': left,
            'right': None,
            'sum': sum_val,
            'minLen': minLen,
            'window': [],
            'action': '初始化：left=0, sum=0, minLen=∞',
            'code_highlight': [0, 1, 2, 3],
            'explanations': [
                '初始化左指针 left = 0。',
                '初始化窗口和 sum = 0。',
                '初始化最小长度 minLen = ∞（表示尚未找到满足条件的子数组）。',
                '准备开始滑动窗口算法。'
            ],
            'finished': False
        })

        for right in range(self.length):
            # 扩展窗口
            sum_val += self.nums[right]
            window = self.nums[left:right+1]
            
            # 检查是否需要更新最小长度
            if sum_val >= self.target:
                currentLen = right - left + 1
                if currentLen < minLen:
                    minLen = currentLen
                    action = f'right={right}：扩展窗口，sum={sum_val} >= target，更新 minLen={minLen}'
                    code_highlight = [4, 5, 6, 7]
                else:
                    action = f'right={right}：扩展窗口，sum={sum_val} >= target，当前长度 {currentLen} 不小于 minLen'
                    code_highlight = [4, 5, 6]
            else:
                action = f'right={right}：扩展窗口，sum={sum_val} < target，继续扩展'
                code_highlight = [4, 5]

            explanations = [
                f'将 nums[{right}] = {self.nums[right]} 加入窗口。',
                f'当前窗口：[{", ".join(map(str, window))}]，和 = {sum_val}。'
            ]
            if sum_val >= self.target:
                explanations.append(f'窗口和 >= target，当前长度 = {right - left + 1}。')
                if minLen != float('inf'):
                    explanations.append(f'更新最小长度：minLen = {minLen}。')

            self.steps.append({
                'left': left,
                'right': right,
                'sum': sum_val,
                'minLen': minLen,
                'window': window.copy(),
                'action': action,
                'code_highlight': code_highlight,
                'explanations': explanations,
                'finished': False
            })

            # 收缩窗口
            while sum_val >= self.target:
                currentLen = right - left + 1
                if currentLen < minLen:
                    minLen = currentLen
                
                # 移除左边界元素
                removed_val = self.nums[left]
                sum_val -= removed_val
                left += 1
                window = self.nums[left:right+1] if left <= right else []

                action = f'收缩窗口：移除 nums[{left-1}]={removed_val}，sum={sum_val}，minLen={minLen}'
                code_highlight = [7, 8, 9, 10]

                explanations = [
                    f'窗口和 >= target，尝试缩小窗口。',
                    f'移除 nums[{left-1}] = {removed_val}，新窗口和 = {sum_val}。',
                    f'左指针 left 移动到 {left}。'
                ]
                if window:
                    explanations.append(f'当前窗口：[{", ".join(map(str, window))}]。')
                if sum_val >= self.target:
                    explanations.append(f'窗口和仍然 >= target，继续缩小。')
                else:
                    explanations.append(f'窗口和 < target，停止缩小。')

                self.steps.append({
                    'left': left,
                    'right': right,
                    'sum': sum_val,
                    'minLen': minLen,
                    'window': window.copy(),
                    'action': action,
                    'code_highlight': code_highlight,
                    'explanations': explanations,
                    'finished': False
                })

        # 完成步骤
        result = int(minLen) if minLen != float('inf') else 0
        self.steps.append({
            'left': left,
            'right': self.length - 1,
            'sum': sum_val,
            'minLen': minLen,
            'window': [],
            'action': f'✅ 处理完成，返回 minLen = {result}',
            'code_highlight': [12],
            'explanations': [
                '遍历结束，所有可能的子数组都已检查。',
                f'最小长度：{result}（{"找到满足条件的子数组" if result > 0 else "未找到满足条件的子数组"}）。',
                '返回结果。'
            ],
            'finished': True
        })

    def _draw_array(self, step_data):
        """绘制数组"""
        for idx in range(self.length):
            val = self.nums[idx]
            x = idx
            
            # 判断是否在窗口内
            left = step_data['left']
            right = step_data.get('right')
            in_window = (right is not None and left <= idx <= right)
            
            # 选择颜色
            if in_window:
                color = 'lightgreen'
                edgecolor = 'green'
                linewidth = 3
            else:
                color = 'lightgray'
                edgecolor = 'black'
                linewidth = 2
            
            # 绘制矩形
            rect = FancyBboxPatch(
                (x - 0.4, 1 - 0.4), 0.8, 0.8,
                boxstyle='round,pad=0.1', linewidth=linewidth,
                edgecolor=edgecolor, facecolor=color
            )
            self.ax.add_patch(rect)
            
            # 数值
            self.ax.text(x, 1, str(val), ha='center', va='center',
                        fontsize=14, fontweight='bold')
            
            # 索引
            self.ax.text(x, 0.1, f'[{idx}]', ha='center', va='center',
                        fontsize=9, color='gray')

    def _draw_pointers(self, step_data):
        """绘制指针"""
        left = step_data['left']
        right = step_data.get('right')
        
        # left 指针
        if left < self.length:
            self.ax.annotate('left', xy=(left, 1.8), xytext=(left, 2.8),
                             arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                             fontsize=12, color='blue', ha='center', fontweight='bold')
        
        # right 指针
        if right is not None and right < self.length:
            self.ax.annotate('right', xy=(right, 0.2), xytext=(right, -0.8),
                             arrowprops=dict(arrowstyle='->', color='red', lw=2),
                             fontsize=12, color='red', ha='center', fontweight='bold')

    def _draw_window_info(self, step_data):
        """绘制窗口信息"""
        left = step_data['left']
        right = step_data.get('right')
        sum_val = step_data['sum']
        minLen = step_data['minLen']
        window = step_data.get('window', [])
        
        # 窗口范围
        if right is not None and left <= right:
            window_text = f'窗口范围：[{left}, {right}]'
            window_vals = f'窗口元素：[{", ".join(map(str, window))}]'
        else:
            window_text = '窗口范围：无'
            window_vals = '窗口元素：[]'
        
        # 窗口和
        sum_text = f'窗口和：{sum_val}'
        if sum_val >= self.target:
            sum_text += ' ✅ (>= target)'
        else:
            sum_text += ' ❌ (< target)'
        
        # 最小长度
        if minLen == float('inf'):
            minLen_text = '最小长度：∞（未找到）'
        else:
            minLen_text = f'最小长度：{int(minLen)}'
        
        # 绘制信息框
        info_y = 4.5
        self.ax.text(-0.5, info_y, window_text, fontsize=11,
                     bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        self.ax.text(-0.5, info_y - 0.6, window_vals, fontsize=10,
                     bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
        self.ax.text(-0.5, info_y - 1.2, sum_text, fontsize=11,
                     bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        self.ax.text(-0.5, info_y - 1.8, minLen_text, fontsize=11,
                     bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.8))
        self.ax.text(-0.5, info_y - 2.4, f'目标值：{self.target}', fontsize=11,
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))

    def _draw_code_panel(self, step_data):
        """绘制代码面板"""
        start_x = self.visual_width + 1.5
        start_y = 6
        line_height = 0.5
        highlight = set(step_data.get('code_highlight', []))

        self.ax.text(start_x, start_y + 2, 'C 代码同步显示', fontsize=13,
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

    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step

        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index

        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-2, self.x_limit)
        self.ax.set_ylim(-4, 12)

        step_data = self.steps[step_index]

        # 标题与说明
        self.ax.text(
            self.visual_width / 2, 11.5,
            f'步骤 {step_index + 1}/{len(self.steps)}',
            ha='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )

        self.ax.text(
            self.visual_width / 2, 10.5,
            step_data['action'],
            ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )

        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(
                self.visual_width / 2, 9.2,
                explain_text,
                ha='center', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )

        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            self.visual_width / 2, 8.2,
            controls_text,
            ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

        # 绘制数组
        self.ax.text(-0.5, 1, 'nums:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_array(step_data)

        # 绘制指针
        self._draw_pointers(step_data)

        # 绘制窗口信息
        self._draw_window_info(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightgreen', '窗口内元素'),
            ('lightgray', '窗口外元素'),
            ('blue', 'left 指针'),
            ('red', 'right 指针')
        ]
        for i, (color, text) in enumerate(legend_items):
            y_pos = 0.5 - i * 0.4
            if i < 2:
                rect = patches.Rectangle((i % 2 * 4, y_pos), 0.4, 0.4,
                                         facecolor=color, edgecolor='black')
                self.ax.add_patch(rect)
            else:
                self.ax.plot([i % 2 * 4, i % 2 * 4 + 0.4], [y_pos + 0.2, y_pos + 0.2],
                            color=color, linewidth=3)
            self.ax.text(i % 2 * 4 + 0.5, y_pos + 0.2, text, fontsize=9, va='center')

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
    print("LeetCode 209. 长度最小的子数组 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print('1. 示例 1: target=7, nums=[2,3,1,2,4,3] → 2')
    print('2. 示例 2: target=4, nums=[1,4,4] → 1')
    print('3. 示例 3: target=11, nums=[1,1,1,1,1,1,1,1] → 0')
    print('4. 自定义输入')

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        target = 7
        nums = [2, 3, 1, 2, 4, 3]
    elif choice == '2':
        target = 4
        nums = [1, 4, 4]
    elif choice == '3':
        target = 11
        nums = [1, 1, 1, 1, 1, 1, 1, 1]
    elif choice == '4':
        target = int(input("请输入 target: ").strip())
        nums_str = input("请输入 nums（空格分隔）: ").strip()
        nums = list(map(int, nums_str.split())) if nums_str else []
    else:
        print("无效选择，使用示例 1")
        target = 7
        nums = [2, 3, 1, 2, 4, 3]

    print("\n开始演示...")
    print(f'target = {target}')
    print(f'nums = {nums}')
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = MinSubArrayLenAnimation(nums, target)
    anim.show()


if __name__ == '__main__':
    main()




"""
LeetCode 42. 接雨水 - 动画演示
使用 matplotlib 手动控制左右指针与水量累积过程
"""

import matplotlib.pyplot as plt

# 设置中文字体，避免渲染乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class TrappingRainWaterAnimation:
    def __init__(self, heights):
        self.heights = heights
        self.n = len(heights)
        self.steps = []
        self.current_step = 0
        self.code_lines = [
            "int trap(int* height, int heightSize) {",
            "    if (height == NULL || heightSize <= 2) {",
            "        return 0;",
            "    }",
            "    int left = 0, right = heightSize - 1;",
            "    int leftMax = 0, rightMax = 0;",
            "    int water = 0;",
            "    while (left < right) {",
            "        if (height[left] < height[right]) {",
            "            leftMax = max(leftMax, height[left]);",
            "            water += leftMax - height[left];",
            "            left++;",
            "        } else {",
            "            rightMax = max(rightMax, height[right]);",
            "            water += rightMax - height[right];",
            "            right--;",
            "        }",
            "    }",
            "    return water;",
            "}",
        ]

        self._simulate()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.canvas.manager.set_window_title('接雨水 - 动画演示（手动控制）')
        self.ax.axis('off')

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate(self):
        """记录算法执行过程"""
        left = 0
        right = self.n - 1
        left_max = 0
        right_max = 0
        total_water = 0
        water_layers = [0] * self.n

        self.steps.append({
            'left': left,
            'right': right,
            'left_max': left_max,
            'right_max': right_max,
            'water': total_water,
            'gain': 0,
            'water_layers': water_layers.copy(),
            'action': '初始化：left=0，right=n-1，尚未产生雨水',
            'notes': [
                '左右指针从两端开始夹逼。',
                'leftMax/rightMax 记录到目前为止的最高边界。',
            ],
            'code_highlight': [0, 1, 2, 4, 5, 6]
        })

        while left < right:
            if self.heights[left] < self.heights[right]:
                left_max = max(left_max, self.heights[left])
                gain = left_max - self.heights[left]
                total_water += gain
                water_layers[left] = gain
                notes = [
                    f'height[{left}] = {self.heights[left]}，由左侧最高 {left_max} 决定水位。',
                    f'本轮新增水量 {gain}，总水量 {total_water}。'
                ]
                action = f'左侧较矮，处理索引 {left}，left++'
                self.steps.append({
                    'left': left + 1,
                    'right': right,
                    'left_max': left_max,
                    'right_max': right_max,
                    'water': total_water,
                    'gain': gain,
                    'water_layers': water_layers.copy(),
                    'action': action,
                    'notes': notes,
                    'code_highlight': [7, 8, 9, 10, 11]
                })
                left += 1
            else:
                right_max = max(right_max, self.heights[right])
                gain = right_max - self.heights[right]
                total_water += gain
                water_layers[right] = gain
                notes = [
                    f'height[{right}] = {self.heights[right]}，由右侧最高 {right_max} 决定水位。',
                    f'本轮新增水量 {gain}，总水量 {total_water}。'
                ]
                action = f'右侧较矮或相等，处理索引 {right}，right--'
                self.steps.append({
                    'left': left,
                    'right': right - 1,
                    'left_max': left_max,
                    'right_max': right_max,
                    'water': total_water,
                    'gain': gain,
                    'water_layers': water_layers.copy(),
                    'action': action,
                    'notes': notes,
                    'code_highlight': [7, 12, 13, 14, 15]
                })
                right -= 1

        self.steps.append({
            'left': left,
            'right': right,
            'left_max': left_max,
            'right_max': right_max,
            'water': total_water,
            'gain': 0,
            'water_layers': water_layers.copy(),
            'action': f'✅ 结束：left 与 right 相遇，返回 {total_water}',
            'notes': ['全部位置处理完毕，while 循环退出。'],
            'code_highlight': [17, 18]
        })

    def _draw_bars(self, step):
        x = list(range(self.n))
        bar_width = 0.6
        self.ax.bar(x, self.heights, width=bar_width, color='#4F81BD', edgecolor='black', label='柱子高度')
        self.ax.bar(
            x,
            step['water_layers'],
            width=bar_width,
            bottom=self.heights,
            color='#4FC3F7',
            edgecolor='black',
            alpha=0.8,
            label='积水'
        )

        for idx, h in enumerate(self.heights):
            self.ax.text(idx, h + step['water_layers'][idx] + 0.3, str(h), ha='center', fontsize=10)

    def _draw_pointers(self, step):
        left = step['left']
        right = step['right']
        if left < self.n:
            self.ax.annotate(
                'left',
                xy=(left, -0.3),
                xytext=(left, -1.5),
                ha='center',
                arrowprops=dict(arrowstyle='->', color='darkorange', lw=2),
                color='darkorange',
                fontsize=12
            )
        if right >= 0:
            self.ax.annotate(
                'right',
                xy=(right, -0.3),
                xytext=(right, -1.5),
                ha='center',
                arrowprops=dict(arrowstyle='->', color='green', lw=2),
                color='green',
                fontsize=12
            )

    def _draw_info_panel(self, step, idx):
        info_y = self.ax.get_ylim()[1] + 1
        self.ax.text(
            self.n / 2 - 0.5,
            info_y,
            f'步骤 {idx + 1}/{len(self.steps)}',
            ha='center',
            fontsize=16,
            fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )

        self.ax.text(
            -0.5,
            info_y - 0.8,
            step['action'],
            fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9),
            wrap=True
        )

        notes = '\n'.join(f'· {n}' for n in step.get('notes', []))
        if notes:
            self.ax.text(
                -0.5,
                info_y - 2.1,
                notes,
                fontsize=11,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9),
                wrap=True
            )

        status_text = (
            f'left={step["left"]}, right={step["right"]}\n'
            f'leftMax={step["left_max"]}, rightMax={step["right_max"]}\n'
            f'本轮新增水量={step["gain"]}, 累计={step["water"]}'
        )
        self.ax.text(
            self.n + 0.5,
            info_y - 0.8,
            status_text,
            fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.9)
        )

        controls = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            self.n / 2 - 0.5,
            -2.2,
            controls,
            ha='center',
            fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

    def _draw_code_panel(self, step):
        start_x = self.n + 2
        start_y = self.ax.get_ylim()[1] - 0.5
        line_height = 0.6
        highlight = set(step.get('code_highlight', []))

        self.ax.text(
            start_x,
            start_y + 0.8,
            'C 代码同步显示',
            fontsize=13,
            fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.7)
        )

        for idx, line in enumerate(self.code_lines):
            y = start_y - idx * line_height
            facecolor = 'peachpuff' if idx in highlight else 'white'
            self.ax.text(
                start_x,
                y,
                f'{idx + 1:02d} {line}',
                fontsize=9,
                family='monospace',
                ha='left',
                va='center',
                bbox=dict(boxstyle='round', facecolor=facecolor, alpha=0.9, pad=0.2)
            )

    def _draw_step(self, idx=None):
        if idx is None:
            idx = self.current_step
        idx = max(0, min(idx, len(self.steps) - 1))
        self.current_step = idx

        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.n + 8)
        max_height = max(max(self.heights), max(self.steps[idx]['water_layers'], default=0))
        self.ax.set_ylim(-3, max_height + 6)

        step = self.steps[idx]

        self._draw_bars(step)
        self._draw_pointers(step)
        self._draw_info_panel(step, idx)
        self._draw_code_panel(step)

        legend_y = max_height + 0.5
        self.ax.text(0, legend_y, '图例：', fontsize=11, fontweight='bold')
        self.ax.text(1.2, legend_y, '■ 柱子高度', color='#4F81BD', fontsize=10)
        self.ax.text(3.5, legend_y, '■ 积水', color='#4FC3F7', fontsize=10)

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


def _parse_custom_input():
    raw = input("请输入高度数组（逗号或空格分隔）: ").strip()
    if not raw:
        raise ValueError("输入为空")
    separators = [',', ' ']
    for sep in separators:
        raw = raw.replace(sep, ' ')
    nums = [int(x) for x in raw.split() if x]
    if len(nums) < 3:
        raise ValueError("至少需要 3 根柱子才能蓄水")
    return nums


def main():
    print("=" * 60)
    print("LeetCode 42. 接雨水 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 官方示例 1")
    print("2. 官方示例 2")
    print("3. 山峰-谷地交替的数组")
    print("4. 自定义输入")

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        nums = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    elif choice == '2':
        nums = [4, 2, 0, 3, 2, 5]
    elif choice == '3':
        nums = [2, 0, 2, 0, 3, 0, 1, 0, 4]
    elif choice == '4':
        try:
            nums = _parse_custom_input()
        except ValueError as exc:
            print(f"输入无效：{exc}，使用示例 1")
            nums = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    else:
        print("无效选择，默认使用示例 1")
        nums = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]

    print("\n开始演示...")
    print(f"height = {nums}")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳到起点 / 终点")
    print("  Q / Esc      ：退出动画")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = TrappingRainWaterAnimation(nums)
    anim.show()


if __name__ == '__main__':
    main()




"""
LeetCode 80. 删除有序数组中的重复项 II - 错误代码演示
展示学生提交代码的问题所在
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class WrongCodeAnimation:
    def __init__(self, nums):
        self.original_nums = nums.copy()
        self.nums = nums.copy()
        self.length = len(nums)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "int removeDuplicates(int* nums, int numsSize) {",
            "    int slow=0;",
            "    int fast=1;",
            "    int n=0;",
            "    for(;fast<numsSize;fast++){",
            "        if(nums[slow]!=nums[fast]){",
            "            nums[++slow]=nums[fast];",
            "            n=0;",
            "        }else{",
            "            n++;",
            "            if(n>1){",
            "                continue;",
            "            }else{",
            "                slow++;  // ❌ 问题：只移动了指针，没有赋值！",
            "            }",
            "        }",
            "    }",
            "    return slow+1;",
            "}",
        ]

        self._simulate_wrong_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.canvas.manager.set_window_title('错误代码演示 - 删除有序数组中的重复项 II')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 8)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_wrong_algorithm(self):
        """模拟错误代码的执行过程"""
        if self.length == 0:
            return

        slow = 0
        n = 0
        
        # 初始状态
        self.steps.append({
            'nums': self.nums.copy(),
            'slow': slow,
            'fast': None,
            'n': n,
            'write_index': None,
            'value': self.nums[slow] if slow < self.length else None,
            'action': f'初始化：slow=0, fast=1, n=0',
            'code_highlight': [1, 2, 3],
            'explanations': [
                '初始状态：slow=0 指向第一个元素，fast=1 开始扫描',
                'n=0 用于计数连续相同元素的个数'
            ],
            'error': None
        })

        for fast in range(1, self.length):
            current = self.nums[fast]
            prev_value = self.nums[slow] if slow < self.length else None
            
            if prev_value != current:
                # 不同元素
                slow += 1
                self.nums[slow] = current
                n = 0
                action = f'fast={fast}，nums[{fast}]={current} != nums[{slow-1}]={prev_value}，写入 nums[{slow}]'
                code_lines = [5, 6, 7, 8]
                explanations = [
                    f'遇到不同元素，slow++ 后写入 nums[{slow}]={current}',
                    'n 重置为 0'
                ]
                write_index = slow
                error = None
            else:
                # 相同元素
                n += 1
                if n > 1:
                    # 已经有两个相同元素，跳过
                    action = f'fast={fast}，nums[{fast}]={current}，n={n} > 1，跳过（已出现两次）'
                    code_lines = [9, 10, 11, 12]
                    explanations = [
                        f'当前值 {current} 已经出现 {n} 次（超过2次），跳过'
                    ]
                    write_index = None
                    error = None
                else:
                    # ⚠️ 关键错误：只移动了指针，没有赋值！
                    slow += 1
                    # 注意：这里没有执行 nums[slow] = nums[fast]
                    action = f'fast={fast}，nums[{fast}]={current}，n={n} <= 1，slow++ 但❌没有赋值！'
                    code_lines = [9, 10, 13, 14]
                    explanations = [
                        f'⚠️ 错误：slow 移动到 {slow}，但 nums[{slow}] 没有被赋值！',
                        f'此时 nums[{slow}] 的值是：{self.nums[slow] if slow < self.length else "越界"}',
                        '这会导致数组内容不正确！'
                    ]
                    write_index = None
                    error = slow

            self.steps.append({
                'nums': self.nums.copy(),
                'slow': slow,
                'fast': fast,
                'n': n,
                'write_index': write_index,
                'value': current,
                'action': action,
                'code_highlight': code_lines,
                'explanations': explanations,
                'error': error
            })

        # 最终状态
        self.steps.append({
            'nums': self.nums.copy(),
            'slow': slow,
            'fast': None,
            'n': n,
            'write_index': None,
            'value': None,
            'action': f'❌ 执行完成，返回 {slow + 1}，但数组内容可能不正确！',
            'code_highlight': [17, 18],
            'explanations': [
                f'返回值为 {slow + 1}，但数组中前 {slow + 1} 个元素可能包含错误的值',
                '因为有些位置只移动了指针但没有赋值'
            ],
            'error': None
        })

    def _draw_array(self, step_data):
        nums = step_data['nums']
        max_len = max(self.length, 1)

        for idx in range(max_len):
            val = nums[idx] if idx < len(nums) else ''
            if idx <= step_data['slow']:
                color = 'lightblue'
            else:
                color = 'lightgray'

            # 标记错误位置
            if step_data.get('error') == idx:
                edge_color = 'red'
                edge_width = 3
            else:
                edge_color = 'black'
                edge_width = 2

            rect = patches.Rectangle(
                (idx - 0.45, 1 - 0.45), 0.9, 0.9,
                linewidth=edge_width, edgecolor=edge_color, facecolor=color
            )
            self.ax.add_patch(rect)
            if idx < len(nums):
                self.ax.text(idx, 1, str(val), ha='center', va='center',
                             fontsize=14, fontweight='bold')
            self.ax.text(idx, 0.1, f'[{idx}]', ha='center', va='center',
                         fontsize=10, color='gray')

        # 高亮 fast 和写入位置
        if step_data['fast'] is not None:
            idx = step_data['fast']
            if 0 <= idx < max_len:
                rect = patches.Rectangle(
                    (idx - 0.45, 1 - 0.45), 0.9, 0.9,
                    linewidth=3, edgecolor='yellow', facecolor='none'
                )
                self.ax.add_patch(rect)

        if step_data['write_index'] is not None:
            idx = step_data['write_index']
            if 0 <= idx < max_len:
                rect = patches.Rectangle(
                    (idx - 0.45, 1 - 0.45), 0.9, 0.9,
                    linewidth=3, edgecolor='green', facecolor='none'
                )
                self.ax.add_patch(rect)

    def _draw_pointers(self, step_data):
        slow = step_data['slow']
        fast = step_data['fast']
        n = step_data.get('n', 0)
        max_len = max(self.length, 1)

        if slow < max_len:
            self.ax.annotate('slow', xy=(slow, 1.8), xytext=(slow, 2.8),
                             arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                             fontsize=12, color='blue', ha='center')
        else:
            self.ax.text(max_len - 0.5, 2.5, f'slow={slow}',
                         color='blue', fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

        if fast is not None and fast < max_len:
            self.ax.annotate('fast', xy=(fast, 0.2), xytext=(fast, -0.8),
                             arrowprops=dict(arrowstyle='->', color='green', lw=2),
                             fontsize=12, color='green', ha='center')

        # 显示 n 的值
        self.ax.text(max_len + 0.5, 2.5, f'n = {n}',
                     color='purple', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.7))

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

        # 标题
        self.ax.text(
            max(self.length / 2, 3), 7.5,
            f'错误代码演示 - 步骤 {step_index + 1}/{len(self.steps)}',
            ha='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8)
        )

        # 操作说明
        self.ax.text(
            max(self.length / 2, 3), 6.6,
            step_data['action'],
            ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )

        # 详细说明
        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            color = 'mistyrose' if step_data.get('error') is not None else 'honeydew'
            self.ax.text(
                max(self.length / 2, 3), 5.2,
                explain_text,
                ha='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor=color, alpha=0.9), wrap=True
            )

        # 控制提示
        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            max(self.length / 2, 3), 4.4,
            controls_text,
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

        # 左侧信息
        self.ax.text(-0.5, 4.8, f'当前 slow+1 = {step_data["slow"] + 1}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        self.ax.text(-0.5, 4.1, f'原始数组：{self.original_nums}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))

        self.ax.text(-0.5, 1, 'nums:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_array(step_data)
        self._draw_pointers(step_data)
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightblue', '已确认有效元素'),
            ('lightgray', '待处理区域'),
            ('yellow', 'fast 当前比较'),
            ('green', '写入位置'),
            ('red', '❌ 错误位置（未赋值）')
        ]
        for i, (color, text) in enumerate(legend_items):
            rect = patches.Rectangle((i * 2, 3.3), 0.5, 0.5,
                                     facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(i * 2 + 0.6, 3.55, text, fontsize=9, va='center')

    def _draw_code_panel(self, step_data):
        start_x = self.visual_width + 1.5
        start_y = 3.5
        line_height = 0.6
        highlight = set(step_data.get('code_highlight', []))

        self.ax.text(start_x, start_y + 2.2, '错误代码显示', fontsize=13,
                     fontweight='bold', ha='left',
                     bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.6))

        for idx, line in enumerate(self.code_lines):
            y = start_y - idx * line_height
            if idx in highlight:
                facecolor = 'peachpuff'
            else:
                facecolor = 'white'
            
            # 标记错误行
            if '❌' in line or idx == 13:
                edgecolor = 'red'
                edgewidth = 2
            else:
                edgecolor = 'black'
                edgewidth = 1
                
            self.ax.text(
                start_x, y, f'{idx + 1:02d} {line}',
                ha='left', va='center', fontsize=9, family='monospace',
                bbox=dict(boxstyle='round', facecolor=facecolor, alpha=0.9, 
                         pad=0.3, edgecolor=edgecolor, linewidth=edgewidth)
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
    print("LeetCode 80. 删除有序数组中的重复项 II - 错误代码演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1：nums = [1,1,1,2,2,3]")
    print("2. 示例 2：nums = [0,0,1,1,1,1,2,3,3]")
    print("3. 全是相同元素：nums = [5,5,5,5,5]")
    print("4. 自定义输入")

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        nums = [1, 1, 1, 2, 2, 3]
    elif choice == '2':
        nums = [0, 0, 1, 1, 1, 1, 2, 3, 3]
    elif choice == '3':
        nums = [5, 5, 5, 5, 5]
    elif choice == '4':
        raw = input("请输入 nums（空格分隔，需非递减排序）: ").strip()
        if raw:
            nums = list(map(int, raw.split()))
        else:
            nums = [1, 1, 1, 2, 2, 3]
    else:
        print("无效选择，默认使用示例 1")
        nums = [1, 1, 1, 2, 2, 3]

    print("\n开始演示错误代码的执行过程...")
    print(f"nums = {nums}")
    print("\n⚠️  注意观察：当遇到相同元素且 n<=1 时，slow++ 但没有赋值！")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = WrongCodeAnimation(nums)
    anim.show()


if __name__ == '__main__':
    main()


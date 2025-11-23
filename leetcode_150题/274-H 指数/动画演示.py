"""
LeetCode 274. H 指数 - 动画演示（计数排序法）
使用 matplotlib 手动控制计数排序法计算 H 指数的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class HIndexAnimation:
    def __init__(self, citations):
        self.citations = citations.copy()
        self.original = citations.copy()
        self.length = len(citations)
        self.steps = []
        self.current_step = 0
        self.max_count_size = max(self.length + 1, 10)  # 计数数组大小
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 18
        self.h_index = 0
        self.code_lines = [
            "int hIndex(int* citations, int citationsSize) {",
            "    // 计数数组：统计每个引用次数的论文数量",
            "    int count[1001] = {0};",
            "    ",
            "    // 统计频次（超过 n 的按 n 计算）",
            "    for (int i = 0; i < citationsSize; i++) {",
            "        if (citations[i] > citationsSize) {",
            "            count[citationsSize]++;",
            "        } else {",
            "            count[citations[i]]++;",
            "        }",
            "    }",
            "    ",
            "    // 从高到低累加，找到最大的 h",
            "    int sum = 0;",
            "    for (int h = citationsSize; h >= 0; h--) {",
            "        sum += count[h];",
            "        if (sum >= h) {",
            "            return h;",
            "        }",
            "    }",
            "    return 0;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        self.fig.canvas.manager.set_window_title('H 指数 - 计数排序法动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-4, 9)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        count = [0] * (self.length + 1)
        
        # 步骤 1: 显示原始数组
        self.steps.append({
            'phase': 'init',
            'citations': self.citations.copy(),
            'count': count.copy(),
            'i': None,
            'h': None,
            'sum': None,
            'action': '初始状态：原始数组',
            'code_highlight': [0],
            'explanations': [
                f'原始数组：{self.citations}',
                '需要计算 H 指数：至少有 h 篇论文的引用次数 ≥ h',
                '使用计数排序法：统计每个引用次数的论文数量'
            ]
        })

        # 步骤 2: 统计频次阶段
        for i, citation in enumerate(self.citations):
            if citation > self.length:
                count[self.length] += 1
                action = f'citations[{i}]={citation} > {self.length}，count[{self.length}]++'
                explanation = f'引用次数 {citation} 超过数组长度 {self.length}，按 {self.length} 计算'
            else:
                count[citation] += 1
                action = f'citations[{i}]={citation}，count[{citation}]++'
                explanation = f'引用次数为 {citation} 的论文数量 +1'
            
            self.steps.append({
                'phase': 'counting',
                'citations': self.citations.copy(),
                'count': count.copy(),
                'i': i,
                'h': None,
                'sum': None,
                'action': f'统计频次：{action}',
                'code_highlight': [5, 6, 7, 8, 9, 10],
                'explanations': [
                    explanation,
                    f'当前计数数组：{count[:self.length+1]}'
                ]
            })

        # 步骤 3: 显示统计完成
        self.steps.append({
            'phase': 'count_done',
            'citations': self.citations.copy(),
            'count': count.copy(),
            'i': None,
            'h': None,
            'sum': None,
            'action': '统计完成：计数数组已构建',
            'code_highlight': [11],
            'explanations': [
                f'计数数组：count[0..{self.length}] = {count[:self.length+1]}',
                '接下来从高到低累加，找到最大的 h'
            ]
        })

        # 步骤 4: 从高到低累加查找
        sum_val = 0
        found = False
        for h in range(self.length, -1, -1):
            sum_val += count[h]
            
            if sum_val >= h:
                # 找到 h 指数
                self.h_index = h
                found = True
                self.steps.append({
                    'phase': 'found',
                    'citations': self.citations.copy(),
                    'count': count.copy(),
                    'i': None,
                    'h': h,
                    'sum': sum_val,
                    'action': f'✅ 找到 H 指数：h={h}，sum={sum_val} >= {h}',
                    'code_highlight': [15, 16, 17, 18],
                    'explanations': [
                        f'检查 h={h}：累计论文数 sum={sum_val}',
                        f'因为 sum={sum_val} >= h={h}，满足条件',
                        f'因此 H 指数为 {h}'
                    ]
                })
                break
            else:
                # 继续检查
                self.steps.append({
                    'phase': 'checking',
                    'citations': self.citations.copy(),
                    'count': count.copy(),
                    'i': None,
                    'h': h,
                    'sum': sum_val,
                    'action': f'检查 h={h}：sum={sum_val} < {h}，继续',
                    'code_highlight': [15, 16, 17],
                    'explanations': [
                        f'检查 h={h}：累计论文数 sum={sum_val}',
                        f'因为 sum={sum_val} < h={h}，不满足条件',
                        f'继续检查更小的 h 值...'
                    ]
                })
        
        if not found:
            # 所有 h 都不满足（理论上不会发生，但保留）
            self.h_index = 0
            self.steps.append({
                'phase': 'not_found',
                'citations': self.citations.copy(),
                'count': count.copy(),
                'i': None,
                'h': 0,
                'sum': sum_val,
                'action': '未找到满足条件的 h，返回 0',
                'code_highlight': [15, 21],
                'explanations': [
                    '所有 h 值都不满足条件',
                    '返回 0'
                ]
            })

    def _draw_citations_array(self, step_data):
        """绘制原始数组"""
        citations = step_data['citations']
        i = step_data.get('i')
        
        self.ax.text(-0.5, 2.5, 'citations:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        
        for idx in range(self.length):
            val = citations[idx]
            
            # 根据是否正在处理着色
            if i is not None and idx == i:
                color = 'lightyellow'  # 当前处理的元素
            else:
                color = 'lightgray'  # 其他元素
            
            rect = patches.Rectangle(
                (idx - 0.45, 2 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)
            self.ax.text(idx, 2, str(val), ha='center', va='center',
                         fontsize=14, fontweight='bold')
            self.ax.text(idx, 1.3, f'[{idx}]', ha='center', va='center',
                         fontsize=10, color='gray')
            
            # 高亮当前处理位置
            if i is not None and idx == i:
                rect = patches.Rectangle(
                    (idx - 0.45, 2 - 0.45), 0.9, 0.9,
                    linewidth=3, edgecolor='red', facecolor='none'
                )
                self.ax.add_patch(rect)

    def _draw_count_array(self, step_data):
        """绘制计数数组"""
        count = step_data['count']
        h = step_data.get('h')
        sum_val = step_data.get('sum')
        
        self.ax.text(-0.5, 0.5, 'count:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        
        # 只显示有意义的计数数组部分（0 到 length）
        display_size = min(self.length + 1, self.max_count_size)
        
        for idx in range(display_size):
            val = count[idx] if idx < len(count) else 0
            
            # 根据是否正在检查着色
            if h is not None:
                if idx == h:
                    color = 'lightyellow'  # 当前检查的 h
                elif idx > h:
                    color = 'lightgreen'  # 已检查过的 h
                else:
                    color = 'lightgray'  # 未检查的 h
            else:
                color = 'lightblue' if val > 0 else 'lightgray'
            
            rect = patches.Rectangle(
                (idx - 0.45, 0 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)
            self.ax.text(idx, 0, str(val), ha='center', va='center',
                         fontsize=12, fontweight='bold')
            self.ax.text(idx, -0.7, f'[{idx}]', ha='center', va='center',
                         fontsize=9, color='gray')
            
            # 高亮当前检查的 h
            if h is not None and idx == h:
                rect = patches.Rectangle(
                    (idx - 0.45, 0 - 0.45), 0.9, 0.9,
                    linewidth=3, edgecolor='red', facecolor='none'
                )
                self.ax.add_patch(rect)
        
        # 显示 sum 值
        if sum_val is not None:
            self.ax.text(display_size + 1, 0, f'sum={sum_val}', ha='left', va='center',
                         fontsize=14, fontweight='bold',
                         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

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

        self.ax.text(
            max(self.length / 2, 3), 7.6,
            step_data['action'],
            ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )

        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(
                max(self.length / 2, 3), 6.4,
                explain_text,
                ha='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )

        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            max(self.length / 2, 3), 5.4,
            controls_text,
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

        # 信息面板
        self.ax.text(-0.5, 4.8, f'原始数组: {self.original}', fontsize=11,
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))
        h_val = step_data.get('h', '?')
        if h_val == '?':
            h_val = self.h_index if step_data.get('phase') == 'found' else '?'
        self.ax.text(-0.5, 4.1, f'当前 H 指数: {h_val}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        if step_data.get('i') is not None:
            self.ax.text(-0.5, 3.4, f'当前处理: citations[{step_data["i"]}]', fontsize=11,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        if step_data.get('h') is not None:
            self.ax.text(-0.5, 3.4, f'当前检查: h={step_data["h"]}', fontsize=11,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

        # 绘制数组
        self._draw_citations_array(step_data)
        self._draw_count_array(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightgreen', '已检查/已统计'),
            ('lightyellow', '当前处理'),
            ('lightblue', '有值的计数'),
            ('lightgray', '未处理/零值')
        ]
        for i, (color, text) in enumerate(legend_items):
            rect = patches.Rectangle((i * 2.5, -2.5), 0.5, 0.5,
                                     facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(i * 2.5 + 0.6, -2.25, text, fontsize=9, va='center')

        self.fig.canvas.draw()

    def _draw_code_panel(self, step_data):
        start_x = self.visual_width + 2
        start_y = 4
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
    print("LeetCode 274. H 指数 - 计数排序法动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: citations=[3,0,6,1,5] (答案: 3)")
    print("2. 示例 2: citations=[1,3,1] (答案: 1)")
    print("3. 所有论文都满足: citations=[5,4,3,2,1] (答案: 3)")
    print("4. 所有引用为 0: citations=[0,0,0] (答案: 0)")
    print("5. 自定义输入")

    choice = input("\n请输入选择 (1-5): ").strip()

    if choice == '1':
        citations = [3, 0, 6, 1, 5]
    elif choice == '2':
        citations = [1, 3, 1]
    elif choice == '3':
        citations = [5, 4, 3, 2, 1]
    elif choice == '4':
        citations = [0, 0, 0]
    elif choice == '5':
        citations = list(map(int, input("请输入 citations（空格分隔）: ").split()))
    else:
        print("无效选择，使用示例 1")
        citations = [3, 0, 6, 1, 5]

    print("\n开始演示...")
    print(f"citations = {citations}")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = HIndexAnimation(citations)
    anim.show()


if __name__ == '__main__':
    main()

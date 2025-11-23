"""
LeetCode 380. O(1) 时间插入、删除和获取随机元素 - 动画演示
使用 matplotlib 手动控制哈希表+数组的操作过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class RandomizedSetAnimation:
    def __init__(self, operations):
        """
        operations: 操作列表，每个元素为 ('insert', val) 或 ('remove', val) 或 ('getRandom',)
        """
        self.operations = operations
        self.nums = []  # 数组存储元素
        self.valToIndex = {}  # 哈希表：值 -> 索引
        self.steps = []
        self.current_step = 0
        self.visual_width = 8
        self.x_limit = self.visual_width + 14
        
        self.code_lines = {
            'insert': [
                "bool insert(int val) {",
                "    if (valToIndex.find(val) != valToIndex.end()) {",
                "        return false;  // 已存在",
                "    }",
                "    nums.push_back(val);",
                "    valToIndex[val] = nums.size() - 1;",
                "    return true;",
                "}"
            ],
            'remove': [
                "bool remove(int val) {",
                "    if (valToIndex.find(val) == valToIndex.end()) {",
                "        return false;  // 不存在",
                "    }",
                "    int idx = valToIndex[val];",
                "    int lastVal = nums.back();",
                "    nums[idx] = lastVal;  // 交换到末尾",
                "    valToIndex[lastVal] = idx;",
                "    nums.pop_back();",
                "    valToIndex.erase(val);",
                "    return true;",
                "}"
            ],
            'getRandom': [
                "int getRandom() {",
                "    int randomIndex = rand() % nums.size();",
                "    return nums[randomIndex];",
                "}"
            ]
        }
        
        self._simulate_algorithm()
        
        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        self.fig.canvas.manager.set_window_title('O(1) 时间插入、删除和获取随机元素 - 动画演示')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-4, 9)
        
        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
    
    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        # 初始状态
        self.steps.append({
            'nums': [],
            'valToIndex': {},
            'operation': None,
            'val': None,
            'result': None,
            'highlight_idx': None,
            'action': '初始化 RandomizedSet，nums 和 valToIndex 均为空',
            'code_highlight': [],
            'explanations': [
                'nums: 数组，存储所有元素，支持 O(1) 随机访问',
                'valToIndex: 哈希表，存储值到数组索引的映射，支持 O(1) 查找'
            ]
        })
        
        for op_type, *args in self.operations:
            if op_type == 'insert':
                val = args[0]
                if val in self.valToIndex:
                    # 已存在
                    self.steps.append({
                        'nums': self.nums.copy(),
                        'valToIndex': self.valToIndex.copy(),
                        'operation': 'insert',
                        'val': val,
                        'result': False,
                        'highlight_idx': None,
                        'action': f'insert({val}): 元素已存在，返回 false',
                        'code_highlight': [0, 1, 2, 6],
                        'explanations': [
                            f'检查 valToIndex 中是否存在 {val}',
                            '已存在，直接返回 false，不进行任何修改'
                        ]
                    })
                else:
                    # 插入
                    self.nums.append(val)
                    self.valToIndex[val] = len(self.nums) - 1
                    self.steps.append({
                        'nums': self.nums.copy(),
                        'valToIndex': self.valToIndex.copy(),
                        'operation': 'insert',
                        'val': val,
                        'result': True,
                        'highlight_idx': len(self.nums) - 1,
                        'action': f'insert({val}): 插入成功，添加到数组末尾，返回 true',
                        'code_highlight': [0, 1, 4, 5, 6],
                        'explanations': [
                            f'检查 {val} 不存在，可以插入',
                            f'将 {val} 添加到 nums 末尾（索引 {len(self.nums) - 1}）',
                            f'在 valToIndex 中记录映射：{val} -> {len(self.nums) - 1}'
                        ]
                    })
            
            elif op_type == 'remove':
                val = args[0]
                if val not in self.valToIndex:
                    # 不存在
                    self.steps.append({
                        'nums': self.nums.copy(),
                        'valToIndex': self.valToIndex.copy(),
                        'operation': 'remove',
                        'val': val,
                        'result': False,
                        'highlight_idx': None,
                        'action': f'remove({val}): 元素不存在，返回 false',
                        'code_highlight': [0, 1, 2, 11],
                        'explanations': [
                            f'检查 valToIndex 中是否存在 {val}',
                            '不存在，直接返回 false'
                        ]
                    })
                else:
                    # 删除
                    idx = self.valToIndex[val]
                    lastVal = self.nums[-1]
                    
                    # 交换
                    self.nums[idx] = lastVal
                    self.valToIndex[lastVal] = idx
                    self.nums.pop()
                    del self.valToIndex[val]
                    
                    self.steps.append({
                        'nums': self.nums.copy(),
                        'valToIndex': self.valToIndex.copy(),
                        'operation': 'remove',
                        'val': val,
                        'result': True,
                        'highlight_idx': idx if idx < len(self.nums) else None,
                        'last_val': lastVal,
                        'action': f'remove({val}): 删除成功，将末尾元素 {lastVal} 移到位置 {idx}',
                        'code_highlight': [0, 1, 4, 5, 6, 7, 8, 9, 11],
                        'explanations': [
                            f'找到 {val} 在数组中的索引 {idx}',
                            f'获取数组最后一个元素 {lastVal}',
                            f'将 {lastVal} 移动到位置 {idx}（覆盖 {val}）',
                            f'更新 valToIndex：{lastVal} -> {idx}',
                            f'删除数组最后一个元素，删除 valToIndex 中的 {val} 映射'
                        ]
                    })
            
            elif op_type == 'getRandom':
                if len(self.nums) == 0:
                    continue
                random_idx = random.randint(0, len(self.nums) - 1)
                random_val = self.nums[random_idx]
                self.steps.append({
                    'nums': self.nums.copy(),
                    'valToIndex': self.valToIndex.copy(),
                    'operation': 'getRandom',
                    'val': None,
                    'result': random_val,
                    'highlight_idx': random_idx,
                    'action': f'getRandom(): 随机选择索引 {random_idx}，返回 {random_val}',
                    'code_highlight': [0, 1, 2],
                    'explanations': [
                        f'生成随机索引 [0, {len(self.nums) - 1}]',
                        f'随机索引 = {random_idx}',
                        f'返回 nums[{random_idx}] = {random_val}'
                    ]
                })
        
        # 结束状态
        self.steps.append({
            'nums': self.nums.copy(),
            'valToIndex': self.valToIndex.copy(),
            'operation': None,
            'val': None,
            'result': None,
            'highlight_idx': None,
            'action': '✅ 所有操作完成',
            'code_highlight': [],
            'explanations': [
                f'最终数组包含 {len(self.nums)} 个元素',
                f'哈希表包含 {len(self.valToIndex)} 个映射'
            ]
        })
    
    def _draw_array(self, step_data):
        """绘制数组"""
        nums = step_data['nums']
        highlight_idx = step_data.get('highlight_idx')
        
        for idx in range(max(len(nums), 4)):
            if idx < len(nums):
                val = nums[idx]
                if idx == highlight_idx:
                    color = 'lightgreen'
                else:
                    color = 'lightblue'
            else:
                val = ''
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
    
    def _draw_hashmap(self, step_data):
        """绘制哈希表"""
        valToIndex = step_data['valToIndex']
        highlight_val = step_data.get('val')
        
        if not valToIndex:
            self.ax.text(0, -1, 'valToIndex: {}', ha='left', va='center',
                         fontsize=12, style='italic', color='gray')
            return
        
        y_start = -1.5
        y_step = -0.5
        items = list(valToIndex.items())
        
        for i, (val, idx) in enumerate(items[:8]):  # 最多显示8个
            y = y_start - i * y_step
            if val == highlight_val:
                color = 'lightgreen'
            else:
                color = 'lightyellow'
            
            rect = patches.Rectangle(
                (-0.5, y - 0.2), 4, 0.4,
                linewidth=1.5, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)
            self.ax.text(0, y, f'{val}', ha='center', va='center',
                         fontsize=12, fontweight='bold')
            self.ax.text(1.5, y, '->', ha='center', va='center',
                         fontsize=12)
            self.ax.text(3, y, f'{idx}', ha='center', va='center',
                         fontsize=12, fontweight='bold')
        
        if len(items) > 8:
            self.ax.text(0, y_start - 8 * y_step, f'... (还有 {len(items) - 8} 个)', 
                         ha='left', va='center', fontsize=10, style='italic')
    
    def _draw_code_panel(self, step_data):
        """绘制代码面板"""
        operation = step_data.get('operation')
        if not operation:
            return
        
        code_lines = self.code_lines.get(operation, [])
        highlight = set(step_data.get('code_highlight', []))
        
        start_x = self.visual_width + 1.5
        start_y = 3.5
        line_height = 0.5
        
        self.ax.text(start_x, start_y + 2.2, f'{operation}() 代码', fontsize=13,
                     fontweight='bold', ha='left',
                     bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.6))
        
        for idx, line in enumerate(code_lines):
            y = start_y - idx * line_height
            facecolor = 'peachpuff' if idx in highlight else 'white'
            self.ax.text(
                start_x, y, f'{idx + 1:02d} {line}',
                ha='left', va='center', fontsize=9, family='monospace',
                bbox=dict(boxstyle='round', facecolor=facecolor, alpha=0.9, pad=0.2)
            )
    
    def _draw_step(self):
        """绘制当前步骤"""
        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-4, 9)
        
        step_data = self.steps[self.current_step]
        
        # 标题和操作信息
        self.ax.text(
            max(self.visual_width / 2, 3), 8,
            f'步骤 {self.current_step + 1} / {len(self.steps)}',
            ha='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8)
        )
        
        self.ax.text(
            max(self.visual_width / 2, 3), 7,
            step_data['action'],
            ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )
        
        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(
                max(self.visual_width / 2, 3), 5.5,
                explain_text,
                ha='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )
        
        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            max(self.visual_width / 2, 3), 4.5,
            controls_text,
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )
        
        # 绘制数组
        self.ax.text(-0.5, 1, 'nums 数组:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_array(step_data)
        
        # 绘制哈希表
        self.ax.text(-0.5, -1, 'valToIndex 哈希表:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_hashmap(step_data)
        
        # 绘制代码面板
        self._draw_code_panel(step_data)
        
        # 图例
        legend_items = [
            ('lightblue', '数组元素'),
            ('lightgreen', '当前操作位置'),
            ('lightyellow', '哈希表映射'),
            ('lightgray', '空位置')
        ]
        for i, (color, text) in enumerate(legend_items):
            rect = patches.Rectangle((i * 2.5, 3.3), 0.5, 0.5,
                                     facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(i * 2.5 + 0.6, 3.55, text, fontsize=10, va='center')
        
        # 显示结果
        if step_data.get('result') is not None:
            result_text = f"返回值: {step_data['result']}"
            self.ax.text(-0.5, 2.5, result_text, ha='right', va='center',
                         fontsize=12, fontweight='bold',
                         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        
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
        self._draw_step()
        plt.tight_layout()
        plt.show()


def main():
    print("=" * 60)
    print("LeetCode 380. O(1) 时间插入、删除和获取随机元素 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: insert(1), remove(2), insert(2), getRandom(), remove(1), insert(2), getRandom()")
    print("2. 示例 2: 插入多个元素后删除")
    print("3. 自定义操作序列")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == '1':
        operations = [
            ('insert', 1),
            ('remove', 2),
            ('insert', 2),
            ('getRandom',),
            ('remove', 1),
            ('insert', 2),
            ('getRandom',)
        ]
    elif choice == '2':
        operations = [
            ('insert', 1),
            ('insert', 2),
            ('insert', 3),
            ('insert', 4),
            ('getRandom',),
            ('remove', 2),
            ('getRandom',),
            ('remove', 1),
            ('getRandom',)
        ]
    elif choice == '3':
        print("\n请输入操作序列（每行一个操作）：")
        print("格式：insert 1 或 remove 2 或 getRandom")
        print("输入空行结束")
        operations = []
        while True:
            line = input().strip()
            if not line:
                break
            parts = line.split()
            if parts[0] == 'insert' and len(parts) == 2:
                operations.append(('insert', int(parts[1])))
            elif parts[0] == 'remove' and len(parts) == 2:
                operations.append(('remove', int(parts[1])))
            elif parts[0] == 'getRandom':
                operations.append(('getRandom',))
            else:
                print(f"无效操作: {line}")
    else:
        print("无效选择，使用示例 1")
        operations = [
            ('insert', 1),
            ('remove', 2),
            ('insert', 2),
            ('getRandom',),
            ('remove', 1),
            ('insert', 2),
            ('getRandom',)
        ]
    
    print("\n开始演示...")
    print(f"操作序列: {operations}")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")
    
    anim = RandomizedSetAnimation(operations)
    anim.show()


if __name__ == '__main__':
    main()


"""
LeetCode 88. 合并两个有序数组 - 动画演示
使用 matplotlib 实时展示算法执行过程
支持键盘手动控制
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class MergeArrayAnimation:
    def __init__(self, nums1, m, nums2, n):
        """
        初始化动画
        
        参数:
            nums1: 第一个数组（包含预留空间）
            m: nums1 的有效元素个数
            nums2: 第二个数组
            n: nums2 的元素个数
        """
        self.nums1 = nums1.copy()
        self.m = m
        self.nums2 = nums2.copy()
        self.n = n
        
        # 初始化指针位置
        self.i = m - 1  # nums1 有效元素的最后一个位置
        self.j = n - 1  # nums2 的最后一个位置
        self.k = m + n - 1  # 合并后的位置
        
        # 记录每一步的操作历史（用于动画）
        self.steps = []
        self.current_step = 0
        
        # 执行算法并记录每一步
        self._simulate_algorithm()
        
        # 创建图形
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.fig.canvas.manager.set_window_title('合并两个有序数组 - 动画演示（手动控制）')
        self.ax.set_xlim(-1, max(m + n, 10) + 1)
        self.ax.set_ylim(-2, 9)
        self.ax.axis('off')
        
        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
        
    def _simulate_algorithm(self):
        """模拟算法执行，记录每一步的状态"""
        # 保存初始状态
        self.steps.append({
            'nums1': self.nums1.copy(),
            'nums2': self.nums2.copy(),
            'i': self.i,
            'j': self.j,
            'k': self.k,
            'action': '初始化：从后往前开始合并',
            'compare': None
        })
        
        # 主循环
        while self.i >= 0 and self.j >= 0:
            # 比较元素
            val1 = self.nums1[self.i]
            val2 = self.nums2[self.j]
            
            if val1 > val2:
                self.nums1[self.k] = val1
                action = f'比较 nums1[{self.i}]={val1} 和 nums2[{self.j}]={val2}，{val1} > {val2}，将 {val1} 放到位置 {self.k}'
                self.i -= 1
            else:
                self.nums1[self.k] = val2
                action = f'比较 nums1[{self.i}]={val1} 和 nums2[{self.j}]={val2}，{val1} <= {val2}，将 {val2} 放到位置 {self.k}'
                self.j -= 1
            
            self.k -= 1
            
            self.steps.append({
                'nums1': self.nums1.copy(),
                'nums2': self.nums2.copy(),
                'i': self.i,
                'j': self.j,
                'k': self.k,
                'action': action,
                'compare': (val1, val2)
            })
        
        # 处理 nums2 剩余元素
        while self.j >= 0:
            self.nums1[self.k] = self.nums2[self.j]
            action = f'nums2 还有剩余元素，将 nums2[{self.j}]={self.nums2[self.j]} 放到位置 {self.k}'
            self.steps.append({
                'nums1': self.nums1.copy(),
                'nums2': self.nums2.copy(),
                'i': self.i,
                'j': self.j,
                'k': self.k,
                'action': action,
                'compare': None
            })
            self.j -= 1
            self.k -= 1
        
        # 完成
        self.steps.append({
            'nums1': self.nums1.copy(),
            'nums2': self.nums2.copy(),
            'i': self.i,
            'j': self.j,
            'k': self.k,
            'action': '✅ 合并完成！',
            'compare': None
        })
    
    def _draw_array(self, arr, start_y, label, highlight_indices=None, highlight_color='yellow'):
        """绘制数组"""
        if highlight_indices is None:
            highlight_indices = []
        
        for idx, val in enumerate(arr):
            # 确定颜色
            if idx in highlight_indices:
                color = highlight_color
            elif idx < self.m and label == 'nums1':
                color = 'lightblue'  # nums1 的有效元素
            elif idx >= self.m and label == 'nums1':
                color = 'lightgray'  # nums1 的预留空间
            else:
                color = 'lightgreen'  # nums2 的元素
            
            # 绘制矩形
            rect = patches.Rectangle(
                (idx - 0.4, start_y - 0.4), 0.8, 0.8,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)
            
            # 绘制数值
            self.ax.text(idx, start_y, str(val), 
                         ha='center', va='center', fontsize=14, fontweight='bold')
            
            # 绘制索引
            self.ax.text(idx, start_y - 0.8, f'[{idx}]', 
                         ha='center', va='center', fontsize=10, color='gray')
    
    def _draw_pointers(self, step_data):
        """绘制指针"""
        i, j, k = step_data['i'], step_data['j'], step_data['k']
        
        # 绘制指针 i (nums1 有效元素指针)
        if i >= 0:
            self.ax.annotate('i', xy=(i, 1.5), xytext=(i, 2.5),
                           arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                           fontsize=14, fontweight='bold', color='blue',
                           ha='center')
            self.ax.text(i, 3.2, f'i={i}', ha='center', fontsize=12, 
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        
        # 绘制指针 j (nums2 指针)
        if j >= 0:
            self.ax.annotate('j', xy=(j, 0.5), xytext=(j, -0.5),
                           arrowprops=dict(arrowstyle='->', color='green', lw=2),
                           fontsize=14, fontweight='bold', color='green',
                           ha='center')
            self.ax.text(j, -1.2, f'j={j}', ha='center', fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
        
        # 绘制指针 k (合并位置指针)
        if k >= 0:
            self.ax.annotate('k', xy=(k, 1.5), xytext=(k, 2.8),
                           arrowprops=dict(arrowstyle='->', color='red', lw=2),
                           fontsize=14, fontweight='bold', color='red',
                           ha='center')
            self.ax.text(k, 3.5, f'k={k}', ha='center', fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    
    def _draw_step(self, step_index=None):
        """绘制当前步骤"""
        if step_index is None:
            step_index = self.current_step
        
        # 确保索引在有效范围内
        if step_index < 0:
            step_index = 0
        if step_index >= len(self.steps):
            step_index = len(self.steps) - 1
        
        self.current_step = step_index
        self.ax.clear()
        self.ax.set_xlim(-1, max(self.m + self.n, 10) + 1)
        self.ax.set_ylim(-2, 9)
        self.ax.axis('off')
        
        step_data = self.steps[step_index]
        
        # 绘制标题
        self.ax.text((self.m + self.n) / 2, 8, 
                    f'步骤 {step_index + 1}/{len(self.steps)}', 
                    ha='center', fontsize=16, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
        
        # 绘制说明文字
        action_text = step_data['action']
        self.ax.text((self.m + self.n) / 2, 7, action_text, 
                    ha='center', fontsize=12, 
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                    wrap=True)
        
        # 绘制操作提示
        controls_text = '操作提示: [空格/→]下一步  [←]上一步  [Home]开始  [End]结束  [Q/Esc]退出'
        self.ax.text((self.m + self.n) / 2, 6.3, controls_text,
                    ha='center', fontsize=11,
                    bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
        
        # 确定高亮的索引
        highlight_i = []
        highlight_j = []
        highlight_k = []
        
        if step_data['i'] >= 0:
            highlight_i.append(step_data['i'])
        if step_data['j'] >= 0:
            highlight_j.append(step_data['j'])
        if step_data['k'] >= 0:
            highlight_k.append(step_data['k'])
        
        # 绘制 nums1 数组（在 y=1.5 的位置）
        self.ax.text(-0.5, 1.5, 'nums1:', ha='right', va='center', 
                    fontsize=14, fontweight='bold')
        self._draw_array(step_data['nums1'], 1.5, 'nums1', 
                        highlight_indices=highlight_i + highlight_k,
                        highlight_color='yellow')
        
        # 绘制分隔线（区分有效元素和预留空间）
        if self.m > 0:
            self.ax.plot([self.m - 0.5, self.m - 0.5], [1.0, 2.0], 
                        'r--', linewidth=2, alpha=0.5)
            self.ax.text(self.m - 0.5, 0.7, f'm={self.m}', 
                        ha='center', fontsize=10, color='red')
        
        # 绘制 nums2 数组（在 y=0.5 的位置）
        self.ax.text(-0.5, 0.5, 'nums2:', ha='right', va='center', 
                    fontsize=14, fontweight='bold')
        self._draw_array(step_data['nums2'], 0.5, 'nums2', 
                        highlight_indices=highlight_j,
                        highlight_color='yellow')
        
        # 绘制指针
        self._draw_pointers(step_data)
        
        # 绘制图例
        legend_y = 4.5
        self.ax.text(0, legend_y, '图例:', fontsize=12, fontweight='bold')
        legend_items = [
            ('lightblue', 'nums1 有效元素'),
            ('lightgray', 'nums1 预留空间'),
            ('lightgreen', 'nums2 元素'),
            ('yellow', '当前比较/填充位置')
        ]
        for i, (color, label) in enumerate(legend_items):
            rect = patches.Rectangle((1 + i * 2, legend_y - 0.2), 0.4, 0.4,
                                   facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(1.5 + i * 2, legend_y, label, ha='left', va='center', fontsize=10)
        
        # 绘制指针说明
        pointer_y = 5.5
        self.ax.text(0, pointer_y, '指针说明:', fontsize=12, fontweight='bold')
        pointers = [
            ('blue', 'i', 'nums1 有效元素指针'),
            ('green', 'j', 'nums2 指针'),
            ('red', 'k', '合并位置指针')
        ]
        for i, (color, name, desc) in enumerate(pointers):
            self.ax.text(1 + i * 3, pointer_y, f'{name}: {desc}', 
                        color=color, fontsize=10, fontweight='bold')
        
        # 刷新画布
        self.fig.canvas.draw()
    
    def _on_key_press(self, event):
        """处理键盘按键事件"""
        if event.key == 'right' or event.key == ' ' or event.key == 'enter':
            # 下一步
            if self.current_step < len(self.steps) - 1:
                self.current_step += 1
                self._draw_step()
        elif event.key == 'left':
            # 上一步
            if self.current_step > 0:
                self.current_step -= 1
                self._draw_step()
        elif event.key == 'home':
            # 跳转到第一步
            self.current_step = 0
            self._draw_step()
        elif event.key == 'end':
            # 跳转到最后一步
            self.current_step = len(self.steps) - 1
            self._draw_step()
        elif event.key == 'q' or event.key == 'escape':
            # 退出
            plt.close(self.fig)
    
    def show(self):
        """显示动画（手动控制模式）"""
        # 绘制第一步
        self._draw_step(0)
        plt.tight_layout()
        plt.show()

def main():
    """主函数 - 运行演示"""
    print("=" * 60)
    print("LeetCode 88. 合并两个有序数组 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: nums1=[1,2,3,0,0,0], m=3, nums2=[2,5,6], n=3")
    print("2. 示例 2: nums1=[1], m=1, nums2=[], n=0")
    print("3. 示例 3: nums1=[0], m=0, nums2=[1], n=1")
    print("4. 自定义")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    if choice == '1':
        nums1 = [1, 2, 3, 0, 0, 0]
        m = 3
        nums2 = [2, 5, 6]
        n = 3
    elif choice == '2':
        nums1 = [1]
        m = 1
        nums2 = []
        n = 0
    elif choice == '3':
        nums1 = [0]
        m = 0
        nums2 = [1]
        n = 1
    elif choice == '4':
        print("\n请输入 nums1 (用空格分隔，包含预留的0): ", end='')
        nums1 = list(map(int, input().split()))
        m = int(input("请输入 m (nums1 有效元素个数): "))
        print("请输入 nums2 (用空格分隔): ", end='')
        nums2 = list(map(int, input().split()))
        n = len(nums2)
    else:
        print("无效选择，使用示例 1")
        nums1 = [1, 2, 3, 0, 0, 0]
        m = 3
        nums2 = [2, 5, 6]
        n = 3
    
    print(f"\n开始演示...")
    print(f"nums1 = {nums1}, m = {m}")
    print(f"nums2 = {nums2}, n = {n}")
    print("\n" + "=" * 60)
    print("🎮 手动控制说明：")
    print("=" * 60)
    print("  [空格键] 或 [→] : 下一步")
    print("  [←]            : 上一步")
    print("  [Home]          : 跳转到第一步")
    print("  [End]           : 跳转到最后一步")
    print("  [Q] 或 [Esc]    : 退出程序")
    print("=" * 60)
    print("\n💡 提示：")
    print("- 黄色高亮表示当前比较或填充的位置")
    print("- 蓝色箭头 i: nums1 有效元素指针")
    print("- 绿色箭头 j: nums2 指针")
    print("- 红色箭头 k: 合并位置指针")
    print("\n⚠️  注意：请确保窗口处于焦点状态，才能使用键盘控制")
    print("   如果键盘控制无效，请点击窗口后再试\n")
    
    # 创建并显示动画（手动控制模式）
    anim = MergeArrayAnimation(nums1, m, nums2, n)
    anim.show()

if __name__ == '__main__':
    main()


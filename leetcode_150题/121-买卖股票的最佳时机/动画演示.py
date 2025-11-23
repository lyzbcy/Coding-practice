"""
LeetCode 121. 买卖股票的最佳时机 - 动画演示
使用 matplotlib 手动控制贪心算法的执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class StockProfitAnimation:
    def __init__(self, prices):
        self.prices = prices.copy()
        self.length = len(prices)
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 14
        self.code_lines = [
            "int maxProfit(int* prices, int pricesSize) {",
            "    int minPrice = prices[0];",
            "    int maxProfit = 0;",
            "    for (int i = 1; i < pricesSize; i++) {",
            "        if (prices[i] < minPrice) {",
            "            minPrice = prices[i];",
            "        }",
            "        int profit = prices[i] - minPrice;",
            "        if (profit > maxProfit) {",
            "            maxProfit = profit;",
            "        }",
            "    }",
            "    return maxProfit;",
            "}",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.canvas.manager.set_window_title('买卖股票的最佳时机 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-3, 8)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录算法执行的每一步"""
        minPrice = self.prices[0]
        maxProfit = 0
        minPriceIndex = 0

        # 初始化步骤
        self.steps.append({
            'prices': self.prices.copy(),
            'current_index': None,
            'minPrice': minPrice,
            'minPriceIndex': minPriceIndex,
            'current_profit': None,
            'maxProfit': maxProfit,
            'action': '初始化：minPrice=prices[0]，maxProfit=0，准备从第2天开始遍历',
            'code_highlight': [0, 1, 2],
            'explanations': [
                f'初始化最低买入价格为 prices[0] = {minPrice}。',
                '最大利润初始化为 0。',
                '从第 2 天（索引 1）开始遍历，因为第 1 天无法卖出。'
            ]
        })

        # 遍历数组
        for i in range(1, self.length):
            current_price = self.prices[i]
            old_minPrice = minPrice
            old_maxProfit = maxProfit

            # 检查是否需要更新最低价格
            if current_price < minPrice:
                minPrice = current_price
                minPriceIndex = i
                action = f'第 {i+1} 天价格 {current_price} 更低，更新 minPrice = {minPrice}'
                code_lines = [3, 4, 5, 6]
                explanations = [
                    f'检查第 {i+1} 天（索引 {i}）的价格：prices[{i}] = {current_price}。',
                    f'因为 {current_price} < {old_minPrice}，更新最低买入价格为 {minPrice}。',
                    f'如果在这一天买入，成本更低。'
                ]
            else:
                action = f'第 {i+1} 天价格 {current_price} 不低于 minPrice={minPrice}，不更新'
                code_lines = [3, 4]
                explanations = [
                    f'检查第 {i+1} 天（索引 {i}）的价格：prices[{i}] = {current_price}。',
                    f'因为 {current_price} >= {minPrice}，最低买入价格保持不变。'
                ]

            # 计算今天卖出的利润
            profit = current_price - minPrice

            # 更新最大利润
            if profit > maxProfit:
                maxProfit = profit
                action += f'，计算利润={profit}，更新 maxProfit={maxProfit}'
                code_lines = [3, 7, 8, 9, 10]
                explanations.append(f'计算今天卖出的利润：profit = {current_price} - {minPrice} = {profit}。')
                explanations.append(f'因为 {profit} > {old_maxProfit}，更新最大利润为 {maxProfit}。')
                explanations.append(f'✅ 找到更优解：在第 {minPriceIndex+1} 天买入，第 {i+1} 天卖出，利润 = {maxProfit}。')
            else:
                action += f'，计算利润={profit}，不更新 maxProfit（当前最大利润={maxProfit}）'
                code_lines = [3, 7, 8]
                explanations.append(f'计算今天卖出的利润：profit = {current_price} - {minPrice} = {profit}。')
                explanations.append(f'因为 {profit} <= {maxProfit}，最大利润保持不变。')

            self.steps.append({
                'prices': self.prices.copy(),
                'current_index': i,
                'minPrice': minPrice,
                'minPriceIndex': minPriceIndex,
                'current_profit': profit,
                'maxProfit': maxProfit,
                'action': action,
                'code_highlight': code_lines,
                'explanations': explanations
            })

        # 完成步骤
        self.steps.append({
            'prices': self.prices.copy(),
            'current_index': None,
            'minPrice': minPrice,
            'minPriceIndex': minPriceIndex,
            'current_profit': None,
            'maxProfit': maxProfit,
            'action': f'✅ 处理完成，返回最大利润 = {maxProfit}',
            'code_highlight': [11],
            'explanations': [
                f'遍历结束，最大利润为 {maxProfit}。',
                f'最优策略：在第 {minPriceIndex+1} 天（价格 {minPrice}）买入，',
                f'在第 {self._find_best_sell_day(minPriceIndex, maxProfit)} 天卖出。'
            ]
        })

    def _find_best_sell_day(self, buy_day, profit):
        """找到最优卖出日期"""
        for i in range(buy_day + 1, self.length):
            if self.prices[i] - self.prices[buy_day] == profit:
                return i + 1
        return self.length

    def _draw_array(self, step_data):
        prices = step_data['prices']
        max_len = max(self.length, 1)
        current_idx = step_data.get('current_index')
        min_idx = step_data.get('minPriceIndex')

        # 计算价格的最大值和最小值，用于归一化显示高度
        max_price = max(prices) if prices else 1
        min_price = min(prices) if prices else 0
        price_range = max_price - min_price if max_price > min_price else 1

        for idx in range(max_len):
            price = prices[idx] if idx < len(prices) else 0
            # 归一化高度（0.3 到 1.5）
            height = 0.3 + (price - min_price) / price_range * 1.2

            # 确定颜色
            if idx == current_idx:
                color = 'yellow'  # 当前遍历位置
            elif idx == min_idx:
                color = 'lightgreen'  # 最低买入价格位置
            elif idx < current_idx if current_idx is not None else False:
                color = 'lightblue'  # 已处理
            else:
                color = 'lightgray'  # 未处理

            # 绘制价格柱状图
            rect = patches.Rectangle(
                (idx - 0.4, 0), 0.8, height,
                linewidth=2, edgecolor='black', facecolor=color
            )
            self.ax.add_patch(rect)
            self.ax.text(idx, height + 0.1, str(price), ha='center', va='bottom',
                         fontsize=12, fontweight='bold')
            self.ax.text(idx, -0.2, f'第{idx+1}天', ha='center', va='top',
                         fontsize=9, color='gray')

        # 如果有利润线，绘制连接线
        if current_idx is not None and min_idx is not None and current_idx > min_idx:
            buy_price = prices[min_idx]
            sell_price = prices[current_idx]
            profit = sell_price - buy_price
            if profit > 0:
                # 绘制利润箭头
                self.ax.annotate('', xy=(current_idx, sell_price / price_range * 1.2 + 0.3),
                                xytext=(min_idx, buy_price / price_range * 1.2 + 0.3),
                                arrowprops=dict(arrowstyle='<->', color='red', lw=2))
                mid_x = (min_idx + current_idx) / 2
                mid_y = max(buy_price, sell_price) / price_range * 1.2 + 0.5
                self.ax.text(mid_x, mid_y, f'利润={profit}', ha='center', va='bottom',
                            fontsize=11, color='red', fontweight='bold',
                            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

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
                max(self.length / 2, 3), 5.0,
                explain_text,
                ha='center', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )

        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            max(self.length / 2, 3), 4.2,
            controls_text,
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

        # 状态信息
        info_y = 3.5
        self.ax.text(-0.5, info_y, f'最低买入价: {step_data["minPrice"]}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        self.ax.text(-0.5, info_y - 0.6, f'最大利润: {step_data["maxProfit"]}', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        if step_data.get('current_profit') is not None:
            self.ax.text(-0.5, info_y - 1.2, f'当前利润: {step_data["current_profit"]}', fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))

        # 绘制价格数组
        self.ax.text(-0.5, 1.5, '价格:', ha='right', va='center',
                     fontsize=14, fontweight='bold')
        self._draw_array(step_data)

        # 绘制代码面板
        self._draw_code_panel(step_data)

        # 图例
        legend_items = [
            ('lightgreen', '最低买入价位置'),
            ('yellow', '当前遍历位置'),
            ('lightblue', '已处理'),
            ('lightgray', '未处理')
        ]
        for i, (color, text) in enumerate(legend_items):
            rect = patches.Rectangle((i * 2, 2.5), 0.5, 0.5,
                                     facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(i * 2 + 0.6, 2.75, text, fontsize=10, va='center')

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
    print("LeetCode 121. 买卖股票的最佳时机 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: prices=[7,1,5,3,6,4] (最大利润=5)")
    print("2. 示例 2: prices=[7,6,4,3,1] (最大利润=0)")
    print("3. 示例 3: prices=[1,2,3,4,5] (最大利润=4)")
    print("4. 示例 4: prices=[2,4,1] (最大利润=2)")
    print("5. 自定义输入")

    choice = input("\n请输入选择 (1-5): ").strip()

    if choice == '1':
        prices = [7, 1, 5, 3, 6, 4]
    elif choice == '2':
        prices = [7, 6, 4, 3, 1]
    elif choice == '3':
        prices = [1, 2, 3, 4, 5]
    elif choice == '4':
        prices = [2, 4, 1]
    elif choice == '5':
        prices = list(map(int, input("请输入 prices（空格分隔）: ").split()))
    else:
        print("无效选择，使用示例 1")
        prices = [7, 1, 5, 3, 6, 4]

    print("\n开始演示...")
    print(f"prices = {prices}")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = StockProfitAnimation(prices)
    anim.show()


if __name__ == '__main__':
    main()


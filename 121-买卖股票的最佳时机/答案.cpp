/**
 * LeetCode 121. 买卖股票的最佳时机
 *
 * 方法：一次遍历 + 贪心
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    int maxProfit(vector<int>& prices) {
        // 如果数组长度小于2，无法进行交易
        if (prices.size() < 2) {
            return 0;
        }
        
        // 记录到目前为止的最低买入价格
        int minPrice = prices[0];
        // 记录最大利润
        int maxProfit = 0;
        
        // 从第2天开始遍历（索引从1开始）
        for (int i = 1; i < prices.size(); i++) {
            // 如果今天的价格更低，更新最低买入价格
            if (prices[i] < minPrice) {
                minPrice = prices[i];
            }
            
            // 计算今天卖出能获得的利润并更新最大利润
            maxProfit = max(maxProfit, prices[i] - minPrice);
        }
        
        return maxProfit;
    }
};

/* 
 * 更简洁的写法
 */

/*
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int minPrice = prices[0];
        int maxProfit = 0;
        
        for (int i = 1; i < prices.size(); i++) {
            // 更新最低价格
            minPrice = min(minPrice, prices[i]);
            // 更新最大利润
            maxProfit = max(maxProfit, prices[i] - minPrice);
        }
        
        return maxProfit;
    }
};
*/


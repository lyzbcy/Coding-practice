/**
 * LeetCode 122. 买卖股票的最佳时机 II
 *
 * 方法：贪心算法
 * 核心思想：只要后一天价格比前一天高，就进行交易，捕获所有上涨区间
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

int maxProfit(int* prices, int pricesSize) {
    int maxProfit = 0;
    
    // 遍历数组，只要后一天价格比前一天高，就累加利润
    for(int i = 0; i < pricesSize - 1; i++) {
        if(prices[i+1] - prices[i] > 0) {
            maxProfit += prices[i+1] - prices[i];
        }
    }
    
    return maxProfit;
}

/* 
 * 更简洁的写法（使用三元运算符）
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

/*
int maxProfit(int* prices, int pricesSize) {
    int maxProfit = 0;
    
    for(int i = 0; i < pricesSize - 1; i++) {
        maxProfit += (prices[i+1] > prices[i]) ? (prices[i+1] - prices[i]) : 0;
    }
    
    return maxProfit;
}
*/

/* 
 * 使用临时变量的版本（更清晰）
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

/*
int maxProfit(int* prices, int pricesSize) {
    int maxProfit = 0;
    
    for(int i = 0; i < pricesSize - 1; i++) {
        int diff = prices[i+1] - prices[i];
        if(diff > 0) {
            maxProfit += diff;
        }
    }
    
    return maxProfit;
}
*/

/* 
 * 动态规划解法（参考，但贪心更简单）
 * 
 * 状态定义：
 * - dp[i][0]：第 i 天结束后，不持有股票的最大利润
 * - dp[i][1]：第 i 天结束后，持有股票的最大利润
 * 
 * 状态转移：
 * - dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])  // 不持有 = max(继续不持有, 卖出)
 * - dp[i][1] = max(dp[i-1][1], dp[i-1][0] - prices[i])  // 持有 = max(继续持有, 买入)
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)（可以优化）
 */

/*
int maxProfit(int* prices, int pricesSize) {
    int hold = -prices[0];      // 持有股票的最大利润（初始：买入第0天）
    int notHold = 0;             // 不持有股票的最大利润（初始：不买入）
    
    for(int i = 1; i < pricesSize; i++) {
        int newNotHold = (notHold > hold + prices[i]) ? notHold : hold + prices[i];
        int newHold = (hold > notHold - prices[i]) ? hold : notHold - prices[i];
        notHold = newNotHold;
        hold = newHold;
    }
    
    return notHold;  // 最后不持有股票才能获得最大利润
}
*/


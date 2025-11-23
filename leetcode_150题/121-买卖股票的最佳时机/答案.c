/**
 * LeetCode 121. 买卖股票的最佳时机
 *
 * 方法：一次遍历 + 贪心
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

int maxProfit(int* prices, int pricesSize) {
    // 如果数组长度小于2，无法进行交易
    if (pricesSize < 2) {
        return 0;
    }
    
    // 记录到目前为止的最低买入价格
    int minPrice = prices[0];
    // 记录最大利润
    int maxProfit = 0;
    
    // 从第2天开始遍历（索引从1开始）
    for (int i = 1; i < pricesSize; i++) {
        // 如果今天的价格更低，更新最低买入价格
        if (prices[i] < minPrice) {
            minPrice = prices[i];
        }
        
        // 计算今天卖出能获得的利润
        int profit = prices[i] - minPrice;
        
        // 更新最大利润
        if (profit > maxProfit) {
            maxProfit = profit;
        }
    }
    
    return maxProfit;
}

/* 
 * 优化版本（0ms 方案，推荐）⭐
 * 使用 else if 避免不必要的计算
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 * 
 * 优化点：
 * - 当 prices[i] < minPrice 时，不计算利润（因为利润一定是0或负数）
 * - 只有当 prices[i] >= minPrice 时，才计算利润并判断是否更新
 * - 减少了约50%的无效计算，性能更优
 */

/*
int maxProfit(int* prices, int pricesSize) {
    int minPrice = prices[0];
    int maxProfit = 0;
    
    for (int i = 1; i < pricesSize; i++) {
        // 如果今天的价格更低，更新最低买入价格
        if (prices[i] < minPrice) {
            minPrice = prices[i];
        }
        // 否则，计算今天卖出的利润（避免在价格更低时进行无效计算）
        else if (prices[i] - minPrice > maxProfit) {
            maxProfit = prices[i] - minPrice;
        }
    }
    
    return maxProfit;
}
*/

/* 
 * 最紧凑版本（追求极致性能）
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

/*
int maxProfit(int* prices, int pricesSize) {
    int minPrice = prices[0];
    int maxProfit = 0;
    
    for (int i = 1; i < pricesSize; i++) {
        if (prices[i] < minPrice) {
            minPrice = prices[i];
        } else {
            int profit = prices[i] - minPrice;
            if (profit > maxProfit) {
                maxProfit = profit;
            }
        }
    }
    
    return maxProfit;
}
*/


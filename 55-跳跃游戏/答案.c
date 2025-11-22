/**
 * LeetCode 55. 跳跃游戏
 *
 * 方法：贪心算法
 * 核心思想：维护当前能到达的最远位置 maxReach
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

bool canJump(int* nums, int numsSize) {
    int maxReach = 0;  // 当前能到达的最远位置
    
    for(int i = 0; i < numsSize; i++) {
        // 如果当前位置超过了能到达的最远位置，返回false
        if(i > maxReach) {
            return false;
        }
        
        // 更新能到达的最远位置
        maxReach = (maxReach > i + nums[i]) ? maxReach : (i + nums[i]);
        
        // 如果已经能到达最后一个位置，提前返回true
        if(maxReach >= numsSize - 1) {
            return true;
        }
    }
    
    return true;
}

/* 
 * 更简洁的写法（去掉提前返回）
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

/*
bool canJump(int* nums, int numsSize) {
    int maxReach = 0;
    
    for(int i = 0; i < numsSize; i++) {
        if(i > maxReach) {
            return false;
        }
        maxReach = (maxReach > i + nums[i]) ? maxReach : (i + nums[i]);
    }
    
    return true;
}
*/

/* 
 * 使用 max 函数的版本（如果支持）
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

/*
#include <stdlib.h>

bool canJump(int* nums, int numsSize) {
    int maxReach = 0;
    
    for(int i = 0; i < numsSize; i++) {
        if(i > maxReach) {
            return false;
        }
        maxReach = max(maxReach, i + nums[i]);
        if(maxReach >= numsSize - 1) {
            return true;
        }
    }
    
    return true;
}
*/

/* 
 * 动态规划解法（参考，但贪心更优）
 * 
 * 状态定义：
 * - dp[i]：表示能否到达位置 i
 * 
 * 状态转移：
 * - dp[i] = true，如果存在 j < i，使得 dp[j] = true 且 j + nums[j] >= i
 * 
 * 时间复杂度：O(n²)
 * 空间复杂度：O(n)
 */

/*
bool canJump(int* nums, int numsSize) {
    bool* dp = (bool*)malloc(numsSize * sizeof(bool));
    dp[0] = true;  // 初始位置肯定能到达
    
    for(int i = 1; i < numsSize; i++) {
        dp[i] = false;
        for(int j = 0; j < i; j++) {
            if(dp[j] && j + nums[j] >= i) {
                dp[i] = true;
                break;
            }
        }
    }
    
    bool result = dp[numsSize - 1];
    free(dp);
    return result;
}
*/


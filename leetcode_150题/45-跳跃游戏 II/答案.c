/**
 * LeetCode 45. 跳跃游戏 II
 *
 * 方法：贪心算法（边界跳跃法）
 * 核心思想：维护上一次跳跃的边界 end 和当前最远位置 maxReach
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

int jump(int* nums, int numsSize) {
    int jumps = 0;        // 跳跃次数
    int end = 0;          // 上一次跳跃能到达的最远位置（边界）
    int maxReach = 0;     // 当前能到达的最远位置
    
    // 注意：只需要遍历到 numsSize - 1（最后一个位置不需要再跳）
    for(int i = 0; i < numsSize - 1; i++) {
        // 更新当前能到达的最远位置
        maxReach = (maxReach > i + nums[i]) ? maxReach : (i + nums[i]);
        
        // 如果到达边界，需要再跳一次
        if(i == end) {
            jumps++;
            end = maxReach;
        }
    }
    
    return jumps;
}


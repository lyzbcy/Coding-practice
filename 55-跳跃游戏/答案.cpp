/**
 * LeetCode 55. 跳跃游戏
 *
 * 方法：贪心算法
 * 核心思想：维护当前能到达的最远位置 maxReach
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    bool canJump(vector<int>& nums) {
        int maxReach = 0;  // 当前能到达的最远位置
        int n = nums.size();
        
        for(int i = 0; i < n; i++) {
            // 如果当前位置超过了能到达的最远位置，返回false
            if(i > maxReach) {
                return false;
            }
            
            // 更新能到达的最远位置
            maxReach = max(maxReach, i + nums[i]);
            
            // 如果已经能到达最后一个位置，提前返回true
            if(maxReach >= n - 1) {
                return true;
            }
        }
        
        return true;
    }
};


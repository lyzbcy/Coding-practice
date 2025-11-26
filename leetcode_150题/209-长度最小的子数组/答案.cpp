#include <algorithm>
#include <climits>
#include <vector>

using namespace std;

/**
 * LeetCode 209. 长度最小的子数组
 * 
 * 使用滑动窗口（双指针）算法
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */
class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int left = 0;           // 窗口左边界
        int sum = 0;            // 当前窗口的元素和
        int minLen = INT_MAX;   // 记录满足条件的最小长度
        
        // 使用 right 指针扩展窗口
        for (int right = 0; right < nums.size(); right++) {
            // 扩展窗口：将 nums[right] 加入窗口
            sum += nums[right];
            
            // 收缩窗口：当 sum >= target 时，尝试缩小窗口以寻找更小的长度
            while (sum >= target) {
                // 更新最小长度
                minLen = min(minLen, right - left + 1);
                
                // 缩小窗口：移除 nums[left]
                sum -= nums[left];
                left++;
            }
        }
        
        // 如果未找到满足条件的子数组，返回 0
        return minLen == INT_MAX ? 0 : minLen;
    }
};




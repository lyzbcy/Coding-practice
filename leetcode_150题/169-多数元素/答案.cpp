/**
 * LeetCode 169. 多数元素
 * 
 * 使用 Boyer-Moore 投票算法
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int candidate = nums[0];  // 候选多数元素
        int count = 1;             // 候选元素的计数器
        
        // 从第二个元素开始遍历
        for (int i = 1; i < nums.size(); i++) {
            if (count == 0) {
                // 计数器为 0，前面的元素已经抵消完毕，当前元素成为新候选
                candidate = nums[i];
                count = 1;
            } else if (nums[i] == candidate) {
                // 当前元素等于候选，计数器加 1
                count++;
            } else {
                // 当前元素不等于候选，计数器减 1（抵消）
                count--;
            }
        }
        
        // 题目保证存在多数元素，直接返回候选
        return candidate;
    }
};


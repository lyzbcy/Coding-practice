/**
 * LeetCode 189. 轮转数组
 *
 * 方法一：三次反转法（推荐）
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    void rotate(vector<int>& nums, int k) {
        int n = nums.size();
        k = k % n;  // 处理 k >= n 的情况
        
        // 反转整个数组
        reverse(nums.begin(), nums.end());
        // 反转前 k 个元素
        reverse(nums.begin(), nums.begin() + k);
        // 反转后 n-k 个元素
        reverse(nums.begin() + k, nums.end());
    }
};

/* 
 * 方法二：环状替换法
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

/*
class Solution {
public:
    void rotate(vector<int>& nums, int k) {
        int n = nums.size();
        k = k % n;
        int count = 0;  // 记录已处理的元素个数
        
        for (int start = 0; count < n; start++) {
            int current = start;
            int prev = nums[start];
            
            do {
                int next = (current + k) % n;
                int temp = nums[next];
                nums[next] = prev;
                prev = temp;
                current = next;
                count++;
            } while (start != current);
        }
    }
};
*/

/*
 * 方法三：辅助数组法
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

/*
class Solution {
public:
    void rotate(vector<int>& nums, int k) {
        int n = nums.size();
        k = k % n;
        vector<int> temp(n);
        
        // 复制后 k 个元素到前 k 个位置
        for (int i = 0; i < k; i++) {
            temp[i] = nums[n - k + i];
        }
        
        // 复制前 n-k 个元素到后 n-k 个位置
        for (int i = k; i < n; i++) {
            temp[i] = nums[i - k];
        }
        
        // 复制回原数组
        nums = temp;
    }
};
*/



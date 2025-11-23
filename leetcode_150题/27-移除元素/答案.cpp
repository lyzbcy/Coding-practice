/**
 * LeetCode 27. 移除元素
 *
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <vector>
using namespace std;

class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int slow = 0;  // 慢指针，指向下一个可写入的位置
        for (int fast = 0; fast < nums.size(); fast++) {
            if (nums[fast] != val) {
                nums[slow++] = nums[fast];
            }
        }
        return slow;
    }
};




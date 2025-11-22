#include <vector>
using namespace std;

class Solution {
public:
    int removeDuplicates(vector<int> &nums) {
        if (nums.empty()) {
            return 0;
        }

        int slow = 0;
        for (int fast = 1; fast < static_cast<int>(nums.size()); ++fast) {
            // 如果 slow < 1，说明前两个元素可以直接保留
            // 如果 nums[fast] != nums[slow-1]，说明当前元素是新值或只出现了一次，可以写入
            // 如果 nums[fast] == nums[slow-1] 且 slow >= 1，说明已经有两个相同元素了，跳过
            if (slow < 1 || nums[fast] != nums[slow - 1]) {
                nums[++slow] = nums[fast];
            }
        }
        return slow + 1;
    }
};






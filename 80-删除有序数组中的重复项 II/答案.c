#include <stddef.h>

// 原地删除重复项，每个元素最多保留两次，返回有效元素数量
int removeDuplicates(int *nums, int numsSize) {
    if (nums == NULL || numsSize == 0) {
        return 0;
    }

    int slow = 0;
    for (int fast = 1; fast < numsSize; fast++) {
        // 如果 slow < 1，说明前两个元素可以直接保留
        // 如果 nums[fast] != nums[slow-1]，说明当前元素是新值或只出现了一次，可以写入
        // 如果 nums[fast] == nums[slow-1] 且 slow >= 1，说明已经有两个相同元素了，跳过
        if (slow < 1 || nums[fast] != nums[slow - 1]) {
            slow++;
            nums[slow] = nums[fast];
        }
    }

    return slow + 1;
}




#include <stddef.h>

// 原地删除重复项，返回唯一元素数量
int removeDuplicates(int *nums, int numsSize) {
    if (nums == NULL || numsSize == 0) {
        return 0;
    }

    int slow = 0;
    for (int fast = 1; fast < numsSize; fast++) {
        if (nums[fast] != nums[slow]) {
            slow++;
            nums[slow] = nums[fast];
        }
    }

    return slow + 1;
}


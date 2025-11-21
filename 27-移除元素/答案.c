/**
 * LeetCode 27. 移除元素
 *
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

int removeElement(int* nums, int numsSize, int val) {
    int slow = 0;  // 慢指针，指向下一个可写入的位置
    for (int fast = 0; fast < numsSize; fast++) {
        if (nums[fast] != val) {
            nums[slow++] = nums[fast];
        }
    }
    return slow;
}



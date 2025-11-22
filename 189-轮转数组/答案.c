/**
 * LeetCode 189. 轮转数组
 *
 * 方法一：三次反转法（推荐）
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

// 反转数组的辅助函数
void reverse(int* nums, int start, int end) {
    while (start < end) {
        int temp = nums[start];
        nums[start] = nums[end];
        nums[end] = temp;
        start++;
        end--;
    }
}

void rotate(int* nums, int numsSize, int k) {
    // 处理 k >= numsSize 的情况
    k = k % numsSize;
    
    // 反转整个数组
    reverse(nums, 0, numsSize - 1);
    // 反转前 k 个元素
    reverse(nums, 0, k - 1);
    // 反转后 n-k 个元素
    reverse(nums, k, numsSize - 1);
}

/* 
 * 方法二：环状替换法
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

/*
void rotate(int* nums, int numsSize, int k) {
    k = k % numsSize;
    int count = 0;  // 记录已处理的元素个数
    
    for (int start = 0; count < numsSize; start++) {
        int current = start;
        int prev = nums[start];
        
        do {
            int next = (current + k) % numsSize;
            int temp = nums[next];
            nums[next] = prev;
            prev = temp;
            current = next;
            count++;
        } while (start != current);
    }
}
*/

/*
 * 方法三：辅助数组法
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

/*
#include <stdlib.h>
#include <string.h>

void rotate(int* nums, int numsSize, int k) {
    k = k % numsSize;
    int* temp = (int*)malloc(sizeof(int) * numsSize);
    
    // 复制后 k 个元素到前 k 个位置
    memcpy(temp, nums + numsSize - k, k * sizeof(int));
    // 复制前 n-k 个元素到后 n-k 个位置
    memcpy(temp + k, nums, (numsSize - k) * sizeof(int));
    // 复制回原数组
    memcpy(nums, temp, numsSize * sizeof(int));
    
    free(temp);
}
*/



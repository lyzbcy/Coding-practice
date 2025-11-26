/**
 * LeetCode 42. 接雨水
 *
 * 双指针夹逼，实时维护左右最高值
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <stddef.h>

int trap(int* height, int heightSize) {
    if (height == NULL || heightSize <= 2) {
        return 0;
    }

    int left = 0;
    int right = heightSize - 1;
    int leftMax = 0;
    int rightMax = 0;
    int water = 0;

    while (left < right) {
        if (height[left] < height[right]) {
            // 左侧更低，水位由 leftMax 决定
            leftMax = leftMax > height[left] ? leftMax : height[left];
            water += leftMax - height[left];
            left++;
        } else {
            // 右侧更低或相等，水位由 rightMax 决定
            rightMax = rightMax > height[right] ? rightMax : height[right];
            water += rightMax - height[right];
            right--;
        }
    }

    return water;
}




/**
 * LeetCode 88. 合并两个有序数组
 * 
 * 时间复杂度：O(m + n)
 * 空间复杂度：O(1)
 */

#include <vector>
using namespace std;

class Solution {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        // 从后往前合并，避免覆盖未处理的元素
        int i = m - 1;      // nums1 有效元素的最后一个位置
        int j = n - 1;      // nums2 的最后一个位置
        int k = m + n - 1;  // nums1 的最后一个位置（合并后的位置）
        
        // 从后往前比较并填充
        while (i >= 0 && j >= 0) {
            if (nums1[i] > nums2[j]) {
                nums1[k--] = nums1[i--];
            } else {
                nums1[k--] = nums2[j--];
            }
        }
        
        // 如果 nums2 还有剩余元素，直接复制到 nums1
        while (j >= 0) {
            nums1[k--] = nums2[j--];
        }
        
        // 如果 nums1 还有剩余元素，它们已经在正确的位置，不需要移动
    }
};


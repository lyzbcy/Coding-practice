/**
 * LeetCode 274. H 指数
 * 
 * 方法一：排序后遍历
 * 时间复杂度：O(n log n)
 * 空间复杂度：O(1)
 */

#include <stdlib.h>

// 比较函数：降序排序
int compare(const void* a, const void* b) {
    return *(int*)b - *(int*)a;
}

int hIndex(int* citations, int citationsSize) {
    // 降序排序
    qsort(citations, citationsSize, sizeof(int), compare);
    
    // 遍历查找最大的 h
    // 如果 citations[i] >= i + 1，说明前 i+1 篇论文引用次数都 >= i+1
    // 如果 citations[i] < i + 1，说明 h 指数就是 i
    for (int i = 0; i < citationsSize; i++) {
        if (citations[i] < i + 1) {
            return i;
        }
    }
    return citationsSize;  // 所有论文都满足
}


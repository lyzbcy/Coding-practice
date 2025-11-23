/**
 * LeetCode 392. 判断子序列
 *
 * 时间复杂度：O(n)，n 是 t 的长度
 * 空间复杂度：O(1)
 */

#include <string.h>
#include <stdbool.h>

bool isSubsequence(char* s, char* t) {
    int i = 0;  // s 的指针
    int j = 0;  // t 的指针
    int len_s = strlen(s);
    int len_t = strlen(t);
    
    // 遍历 t，尝试匹配 s 中的每个字符
    while (i < len_s && j < len_t) {
        if (s[i] == t[j]) {
            i++;  // 找到了 s 中的一个字符
        }
        j++;  // 无论是否匹配，都要继续遍历 t
    }
    
    // 如果 i 到达 s 的末尾，说明全部匹配
    return i == len_s;
}


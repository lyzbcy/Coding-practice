/**
 * LeetCode 14. 最长公共前缀
 *
 * 时间复杂度：O(mn)，m 为字符串平均长度，n 为字符串数量
 * 空间复杂度：O(m)，需要存储结果字符串
 */

#include <string.h>
#include <stdlib.h>

char* longestCommonPrefix(char** strs, int strsSize) {
    // 边界检查：空数组
    if (strsSize == 0) {
        char* result = (char*)malloc(1);
        result[0] = '\0';
        return result;
    }
    
    // 以第一个字符串为基准
    int len = strlen(strs[0]);
    
    // 纵向扫描：比较每个字符位置
    for (int i = 0; i < len; i++) {
        char c = strs[0][i];
        
        // 检查所有其他字符串的第 i 个字符
        for (int j = 1; j < strsSize; j++) {
            // 如果字符串长度不足或字符不匹配
            if (i >= strlen(strs[j]) || strs[j][i] != c) {
                // 返回前 i 个字符
                char* result = (char*)malloc((i + 1) * sizeof(char));
                strncpy(result, strs[0], i);
                result[i] = '\0';
                return result;
            }
        }
    }
    
    // 所有字符都匹配，返回第一个字符串的副本
    char* result = (char*)malloc((len + 1) * sizeof(char));
    strcpy(result, strs[0]);
    return result;
}



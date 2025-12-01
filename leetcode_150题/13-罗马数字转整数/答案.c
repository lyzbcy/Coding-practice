/**
 * LeetCode 13. 罗马数字转整数
 *
 * 时间复杂度：O(n)，其中 n 是字符串的长度
 * 空间复杂度：O(1)
 */

#include <string.h>

// 辅助函数：获取字符对应的数值
int getValue(char c) {
    switch(c) {
        case 'I': return 1;
        case 'V': return 5;
        case 'X': return 10;
        case 'L': return 50;
        case 'C': return 100;
        case 'D': return 500;
        case 'M': return 1000;
        default: return 0;
    }
}

int romanToInt(char* s) {
    int result = 0;           // 结果变量
    int len = strlen(s);      // 字符串长度
    
    // 从左到右遍历字符串
    for (int i = 0; i < len; i++) {
        int current = getValue(s[i]);  // 当前字符对应的数值
        
        // 检查是否有下一个字符，且当前字符小于下一个字符
        // 这表示是特殊情况（如 IV、IX、XL、XC、CD、CM）
        if (i + 1 < len && current < getValue(s[i + 1])) {
            // 特殊情况：相减（例如 IV = 5 - 1 = 4）
            result += getValue(s[i + 1]) - current;
            i++;  // 跳过下一个字符（因为已经在本次处理了）
        } else {
            // 正常情况：直接加上当前字符的值
            result += current;
        }
    }
    
    return result;
}


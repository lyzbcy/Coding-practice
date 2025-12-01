/**
 * LeetCode 20. 有效的括号
 *
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

#include <stdbool.h>
#include <string.h>

bool isValid(char* s) {
    int len = strlen(s);
    
    // 奇数长度直接返回 false（优化）
    if (len % 2 == 1) {
        return false;
    }
    
    // 使用数组模拟栈
    char stack[10000];
    int top = -1;  // 栈顶指针，-1 表示栈为空
    
    // 遍历字符串
    for (int i = 0; i < len; i++) {
        char c = s[i];
        
        // 如果是左括号，入栈
        if (c == '(' || c == '[' || c == '{') {
            stack[++top] = c;
        }
        // 如果是右括号，检查匹配
        else {
            // 栈为空，说明没有对应的左括号
            if (top < 0) {
                return false;
            }
            
            // 获取栈顶元素，检查是否匹配
            char topChar = stack[top];
            if ((c == ')' && topChar == '(') ||
                (c == ']' && topChar == '[') ||
                (c == '}' && topChar == '{')) {
                top--;  // 匹配成功，出栈
            } else {
                return false;  // 类型不匹配
            }
        }
    }
    
    // 栈为空说明所有括号都匹配
    return top == -1;
}


/**
 * LeetCode 125. 验证回文串
 *
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <ctype.h>
#include <string.h>
#include <stdbool.h>

bool isPalindrome(char* s) {
    int left = 0;
    int right = strlen(s) - 1;
    
    while (left < right) {
        // 跳过非字母数字字符
        while (left < right && !isalnum(s[left])) {
            left++;
        }
        while (left < right && !isalnum(s[right])) {
            right--;
        }
        
        // 比较字符（转小写）
        if (tolower(s[left]) != tolower(s[right])) {
            return false;
        }
        
        left++;
        right--;
    }
    
    return true;
}


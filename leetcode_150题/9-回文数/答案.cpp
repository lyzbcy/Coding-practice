/**
 * LeetCode 9. 回文数
 * 
 * 方法：反转一半数字（推荐）
 * 时间复杂度：O(log₁₀ n)
 * 空间复杂度：O(1)
 */

class Solution {
public:
    bool isPalindrome(int x) {
        // 负数不是回文数
        if (x < 0) {
            return false;
        }
        
        // 0 是回文数
        if (x == 0) {
            return true;
        }
        
        // 以 0 结尾且不为 0 的数不是回文数
        // 例如：10, 20, 100 等
        if (x % 10 == 0) {
            return false;
        }
        
        int reversed = 0;
        // 反转后一半数字
        // 当 x <= reversed 时，说明已经反转了一半
        while (x > reversed) {
            reversed = reversed * 10 + x % 10;
            x /= 10;
        }
        
        // 偶数位数：x == reversed
        // 例如：1221 -> x=12, reversed=12
        // 奇数位数：x == reversed / 10（去掉中间位）
        // 例如：121 -> x=1, reversed=12, reversed/10=1
        return x == reversed || x == reversed / 10;
    }
};

/* 
 * 方法二：完全反转（使用 long long 避免溢出）
 * 时间复杂度：O(log₁₀ n)
 * 空间复杂度：O(1)
 */

/*
class Solution {
public:
    bool isPalindrome(int x) {
        if (x < 0) {
            return false;
        }
        if (x == 0) {
            return true;
        }
        
        long long original = x;  // 使用 long long 避免溢出
        long long reversed = 0;
        long long temp = x;
        
        // 完全反转数字
        while (temp > 0) {
            reversed = reversed * 10 + temp % 10;
            temp /= 10;
        }
        
        return original == reversed;
    }
};
*/


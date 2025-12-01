/**
 * LeetCode 13. 罗马数字转整数
 *
 * 时间复杂度：O(n)，其中 n 是字符串的长度
 * 空间复杂度：O(1)
 */

#include <string>
#include <unordered_map>
using namespace std;

class Solution {
public:
    int romanToInt(string s) {
        // 建立字符到数值的映射表
        unordered_map<char, int> map = {
            {'I', 1},
            {'V', 5},
            {'X', 10},
            {'L', 50},
            {'C', 100},
            {'D', 500},
            {'M', 1000}
        };
        
        int result = 0;           // 结果变量
        int n = s.length();       // 字符串长度
        
        // 从左到右遍历字符串
        for (int i = 0; i < n; i++) {
            int current = map[s[i]];  // 当前字符对应的数值
            
            // 检查是否有下一个字符，且当前字符小于下一个字符
            // 这表示是特殊情况（如 IV、IX、XL、XC、CD、CM）
            if (i + 1 < n && current < map[s[i + 1]]) {
                // 特殊情况：相减（例如 IV = 5 - 1 = 4）
                result += map[s[i + 1]] - current;
                i++;  // 跳过下一个字符（因为已经在本次处理了）
            } else {
                // 正常情况：直接加上当前字符的值
                result += current;
            }
        }
        
        return result;
    }
};


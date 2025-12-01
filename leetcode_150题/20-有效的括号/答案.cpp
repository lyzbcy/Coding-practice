/**
 * LeetCode 20. 有效的括号
 *
 * 时间复杂度：O(n)
 * 空间复杂度：O(n)
 */

#include <stack>
#include <unordered_map>
#include <string>
using namespace std;

class Solution {
public:
    bool isValid(string s) {
        int n = s.size();
        
        // 奇数长度直接返回 false（优化）
        if (n % 2 == 1) {
            return false;
        }
        
        // 使用栈存储左括号
        stack<char> stk;
        
        // 建立右括号到左括号的映射
        unordered_map<char, char> pairs = {
            {')', '('},
            {']', '['},
            {'}', '{'}
        };
        
        // 遍历字符串
        for (char c : s) {
            // 如果是右括号
            if (pairs.count(c)) {
                // 栈为空或不匹配，返回 false
                if (stk.empty() || stk.top() != pairs[c]) {
                    return false;
                }
                // 匹配成功，出栈
                stk.pop();
            }
            // 如果是左括号，入栈
            else {
                stk.push(c);
            }
        }
        
        // 栈为空说明所有括号都匹配
        return stk.empty();
    }
};


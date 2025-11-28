/**
 * LeetCode 14. 最长公共前缀
 *
 * 时间复杂度：O(mn)，m 为字符串平均长度，n 为字符串数量
 * 空间复杂度：O(m)，需要存储结果字符串
 */

#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        // 边界检查：空数组
        if (strs.empty()) {
            return "";
        }
        
        // 以第一个字符串为基准
        for (int i = 0; i < strs[0].length(); i++) {
            char c = strs[0][i];
            
            // 检查所有其他字符串的第 i 个字符
            for (int j = 1; j < strs.size(); j++) {
                // 如果字符串长度不足或字符不匹配
                if (i >= strs[j].length() || strs[j][i] != c) {
                    return strs[0].substr(0, i);
                }
            }
        }
        
        // 所有字符都匹配，返回第一个字符串
        return strs[0];
    }
};



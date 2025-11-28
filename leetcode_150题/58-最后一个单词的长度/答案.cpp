/**
 * LeetCode 58. 最后一个单词的长度
 *
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */

#include <string>
using namespace std;

class Solution {
public:
    int lengthOfLastWord(string s) {
        int i = s.length() - 1;  // 从字符串末尾开始
        
        // 跳过末尾空格
        while (i >= 0 && s[i] == ' ') {
            i--;
        }
        
        // 计数最后一个单词的长度
        int length = 0;
        while (i >= 0 && s[i] != ' ') {
            length++;
            i--;
        }
        
        return length;
    }
};


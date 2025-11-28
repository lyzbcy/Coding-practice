/**
 * LeetCode 383. 赎金信
 *
 * 计数数组：一次统计，一次消耗
 * 时间复杂度：O(n + m)
 * 空间复杂度：O(1)
 */

#include <string>
using namespace std;

class Solution {
public:
    bool canConstruct(string ransomNote, string magazine) {
        int count[26] = {0};

        for (char ch : magazine) {
            count[ch - 'a']++;
        }

        for (char ch : ransomNote) {
            int idx = ch - 'a';
            count[idx]--;
            if (count[idx] < 0) {
                return false;
            }
        }

        return true;
    }
};



/**
 * LeetCode 383. 赎金信
 *
 * 计数数组：统计 magazine 字符频次，再逐个消耗 ransomNote
 * 时间复杂度：O(n + m)
 * 空间复杂度：O(1)
 */

#include <stdbool.h>

bool canConstruct(char* ransomNote, char* magazine) {
    int count[26] = {0};  // 记录每个字母的剩余额度

    for (int i = 0; magazine[i] != '\0'; i++) {
        int idx = magazine[i] - 'a';
        count[idx]++;
    }

    for (int i = 0; ransomNote[i] != '\0'; i++) {
        int idx = ransomNote[i] - 'a';
        count[idx]--;
        if (count[idx] < 0) {
            return false;  // 库存不足，无法构成
        }
    }

    return true;
}



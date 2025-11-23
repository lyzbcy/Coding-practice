/**
 * LeetCode 141. 环形链表
 *
 * 时间复杂度：O(n)，n 是链表的长度
 * 空间复杂度：O(1)
 *
 * 使用快慢指针（Floyd判圈算法）：
 * - slow 指针每次移动一步
 * - fast 指针每次移动两步
 * - 如果链表有环，快慢指针最终会相遇
 */

#include <stdbool.h>

// Definition for singly-linked list.
struct ListNode {
    int val;
    struct ListNode *next;
};

bool hasCycle(struct ListNode *head) {
    // 边界条件：空链表或单节点链表
    if (head == NULL || head->next == NULL) {
        return false;
    }
    
    // 初始化快慢指针
    struct ListNode *slow = head;  // 慢指针，每次移动一步
    struct ListNode *fast = head->next;  // 快指针，每次移动两步
    
    // 快慢指针遍历链表
    while (fast != NULL && fast->next != NULL) {
        // 如果快慢指针相遇，说明有环
        if (slow == fast) {
            return true;
        }
        
        // 慢指针移动一步
        slow = slow->next;
        
        // 快指针移动两步
        fast = fast->next->next;
    }
    
    // 快指针到达链表末尾，说明没有环
    return false;
}


/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */

/**
 * LeetCode 21. 合并两个有序链表
 * 
 * 思路：双指针合并
 * 1. 同时遍历两个链表，使用两个指针分别指向两个链表的当前节点
 * 2. 比较当前节点值，选择较小的节点
 * 3. 将较小节点连接到结果链表
 * 4. 移动指针到下一个节点
 * 5. 处理剩余节点：当一个链表遍历完时，直接将另一个链表的剩余部分连接上
 * 
 * 时间复杂度：O(m + n)，其中 m 和 n 分别是两个链表的长度
 * 空间复杂度：O(1)，只使用了常数额外空间
 */

struct ListNode* mergeTwoLists(struct ListNode* list1, struct ListNode* list2) {
    // 创建虚拟头节点，简化边界处理
    struct ListNode* dummy = (struct ListNode*)malloc(sizeof(struct ListNode));
    dummy->val = 0;
    dummy->next = NULL;
    
    struct ListNode* current = dummy;
    
    // 同时遍历两个链表
    while (list1 != NULL && list2 != NULL) {
        // 选择较小的节点
        if (list1->val <= list2->val) {
            current->next = list1;
            list1 = list1->next;
        } else {
            current->next = list2;
            list2 = list2->next;
        }
        current = current->next;
    }
    
    // 处理剩余节点
    if (list1 != NULL) {
        current->next = list1;
    } else {
        current->next = list2;
    }
    
    return dummy->next;
}


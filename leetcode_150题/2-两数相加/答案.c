/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */

/**
 * LeetCode 2. 两数相加
 * 
 * 思路：模拟竖式加法
 * 1. 从低位到高位逐位相加（逆序存储正好符合这个顺序）
 * 2. 维护进位变量 carry，初始为 0
 * 3. 同时遍历两个链表，直到两个链表都遍历完
 * 4. 处理进位：如果最后还有进位，创建新节点
 * 
 * 时间复杂度：O(max(m, n))，其中 m 和 n 分别是两个链表的长度
 * 空间复杂度：O(max(m, n))，结果链表的长度最多为 max(m, n) + 1
 */

struct ListNode* addTwoNumbers(struct ListNode* l1, struct ListNode* l2) {
    // 创建虚拟头节点，简化边界处理
    struct ListNode* dummy = (struct ListNode*)malloc(sizeof(struct ListNode));
    dummy->val = 0;
    dummy->next = NULL;
    
    struct ListNode* current = dummy;
    int carry = 0;
    
    // 同时遍历两个链表，直到都遍历完且没有进位
    while (l1 != NULL || l2 != NULL || carry != 0) {
        int sum = carry;
        
        // 加上 l1 的当前位
        if (l1 != NULL) {
            sum += l1->val;
            l1 = l1->next;
        }
        
        // 加上 l2 的当前位
        if (l2 != NULL) {
            sum += l2->val;
            l2 = l2->next;
        }
        
        // 计算新的进位和当前位的值
        carry = sum / 10;
        int digit = sum % 10;
        
        // 创建新节点
        struct ListNode* newNode = (struct ListNode*)malloc(sizeof(struct ListNode));
        newNode->val = digit;
        newNode->next = NULL;
        current->next = newNode;
        current = current->next;
    }
    
    return dummy->next;
}


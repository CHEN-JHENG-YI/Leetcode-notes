---
id: 234
title: "Palindrome Linked List"
topics: ["Linked List"]        
techniques: ["Reverse Whole List", "Fast/Slow Pointers"]               
difficulty: "Easy"
slug: "palindrome-linked-list"
---

# 234. Palindrome Linked List

**Difficulty**: Easy  
**Topics**: Linked List  

---

## 🧩 Problem Link
[LeetCode 234 - Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/)

---

## 💡 Approaches
1. Approach A Fast/Slow pointer + Reverse second half.
   - Key idea:
     - Use fast/slow pointer to find the middle of list.
     - Reverse the second half list in-place.
     - Compare the first half and the reversed second half node by node.
  
   - Time  complexity: O(n)
   - Space complexity: O(1)
```cpp
class Solution {
public:
    ListNode* getMiddleNode(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        return slow; // middle (odd: middle, even: right-middle)
    }

    ListNode* reverse_list(ListNode* head) {
        ListNode* prev = nullptr;
        while (head) {
            ListNode* nxt = head->next;
            head->next = prev;
            prev = head;
            head = nxt;
        }
        return prev;
    }

    bool isPalindrome(ListNode* head) {
        if (!head || !head->next) return true;

        // Step 1. find middle
        ListNode* mid = getMiddleNode(head);

        // Step 2. reverse second half
        ListNode* second = reverse_list(mid);

        // Step 3. compare
        ListNode* p1 = head;
        ListNode* p2 = second;
        while (p2) {
            if (p1->val != p2->val) return false;
            p1 = p1->next;
            p2 = p2->next;
        }

        return true;
    }
};
```

2. Approach B Copy to array then check palindrome.
   - Key idea: 
     - Simple to implement, but requires extra space
  
   - Time  complexity: O(n)
   - Space complexity: O(n)
```cpp
class Solution {
public:
    bool isPalindrome(ListNode* head) {
        vector<int> array;

        while (head) {
            array.push_back(head->val);
            head = head->next;
        }

        int l = 0, r = array.size() - 1;

        while (l < r) {
            if (array[l++] != array[r--]) 
                return false;
        }
        return true;
    }
};
```
---

## 📝 Notes / Pitfalls
- …
- …

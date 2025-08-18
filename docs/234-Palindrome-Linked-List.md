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
  
2. Approach B Copy to array then check palindrome.
   - Key idea: 
     - Simple to implement, but requires extra space
  
   - Time  complexity: O(n)
   - Space complexity: O(n)

---

## 📝 Notes / Pitfalls
- …
- …

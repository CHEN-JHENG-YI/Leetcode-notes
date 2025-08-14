---
id: 2074
title: "Reverse Nodes in Even Length Groups"
topics: ["Linked List"]
techniques: ["Dummy Head", "Group Reversal", "Array Rebuild"]
difficulty: "Medium"
language: "C++"
slug: "reverse-nodes-in-even-length-groups"
---

# 2074. Reverse Nodes in Even Length Groups

**Difficulty**: Medium  
**Topics**: Linked List  
**Language**: C++  

---

## 🧩 Problem Link
[LeetCode 2074 - Reverse Nodes in Even Length Groups](https://leetcode.com/problems/reverse-nodes-in-even-length-groups/)

---

## 📜 Problem Summary
Split the list into groups of sizes 1,2,3,...; for each group, if the actual length is even, reverse the group; otherwise keep it as is.

---

## 💡 Approach
1. Array rebuild (teaching version): collect values → reverse even-length groups in the array → rebuild the list.
2. In-place pointer approach (optimal space): scan group by group and reverse only when the group length is even.

---

## 🖥 Code (C++ — array rebuild)
```cpp
// See your LeetCode submission file
```
---

## ⏱ Complexity
- Time: O(n)
- Space: O(n)

---

## 🧪 Test Cases
```text
Input:  [5,2,6,3,9,1,7,3,8,4]
Output: [5,6,2,3,9,1,4,8,3,7]
```

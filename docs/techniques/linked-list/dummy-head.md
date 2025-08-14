---
type: technique
name: "Dummy Head"
category: "Linked List"
aliases: ["Sentinel Node", "Fake Head"]
related: ["Reverse Sublist", "Remove N-th From End"]
---

# Dummy Head

## 簡介
在串列開頭建立一個「假頭節點」，把真實頭節點接在它後面。這樣在**需要改動頭節點**的操作（插入/刪除/反轉區間）時，就不必額外特判。

## 何時使用
- 可能會改到頭節點（例如刪除第一個、反轉從第 1 個開始的區間）。
- 想要統一處理「前一個節點」的指標，減少 if-else。

## 步驟
1. 建立 `ListNode dummy(0); dummy.next = head;`
2. 之後所有操作都以 `dummy` 當起點，完成後回傳 `dummy.next`。

## 常見坑
- 忘記回傳 `dummy.next`、而是回傳 `head`（反轉後 head 可能不再是第一個）。

## 範例程式
```cpp
ListNode dummy(0);
dummy.next = head;
// ... do operations starting from &dummy
return dummy.next;
```
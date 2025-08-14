---
type: technique
name: "Group Reversal"
category: "Linked List"
aliases: ["Chunk Reversal", "Reverse in Groups"]
related: ["Reverse k-Group", "Reverse Sublist"]
---

# Group Reversal

## 簡介
把串列切成片段（例：每 k 個、或 1/2/3/... 逐組），然後對某些片段做反轉。重點是「**準確找到一段的起訖**」與「**反轉並無縫接回**」。

## 何時使用
- 每 k 個反轉、或像 LeetCode 2074 依序 1/2/3/... 分組再決定是否反轉。

## 步驟（常見寫法）
1. 從當前節點出發，先掃出一段的**實際長度**與**下一段起點**。
2. 判斷是否需要反轉；若需要，**就地反轉**這一段，並讓上一段 `prev` 指向反轉後的新頭。
3. 將 `prev` 前進到這一段的尾巴（反轉前的頭），`curr` 移向下一段起點。

## 常見坑
- 最後一段長度不足時的長度計算（要用 `min` 取實際長度）。
- 反轉後「上一段 → 這段新頭」與「這段尾 → 下一段起點」的指標銜接。

## 範例（就地反轉一段，尾端對齊 next）
```cpp
ListNode* reverse_segment(ListNode* head, ListNode* tail_next) {
    ListNode* prev = tail_next;
    ListNode* cur = head;
    while (cur != tail_next) {
        ListNode* nxt = cur->next;
        cur->next = prev;
        prev = cur;
        cur = nxt;
    }
    return prev; // new head of this segment
}
```
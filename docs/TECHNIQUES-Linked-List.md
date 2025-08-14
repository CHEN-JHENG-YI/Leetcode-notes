
# Linked List — Techniques (single-page)
> This page consolidates common linked-list techniques for quick review.  
> Tag each note with the exact names in `techniques: [...]` to auto-link via `generate_index.py`.

---

## Dummy Head

**When to use**
- The head node may change (delete first node, reverse from position 1, etc.).
- You want to normalize the “previous node” logic and avoid special-casing the head.

**Steps**
1. `ListNode dummy(0); dummy.next = head;`
2. Use `&dummy` as the anchor for traversal/operations.
3. Return `dummy.next` at the end.

**Pitfalls**
- Returning `head` instead of `dummy.next` after mutations.

**Snippet**
```cpp
ListNode dummy(0);
dummy.next = head;
// ... operations start from &dummy
return dummy.next;
```

---

## Fast/Slow Pointers

**Use cases**
- Find the middle node (fast moves 2, slow moves 1).
- Detect cycle (Floyd): if fast meets slow, there is a cycle; reset one pointer to head and move 1-by-1 to find the entry.
- Palindrome check (find middle, reverse second half, compare).

**Middle + Palindrome**
```cpp
// find middle (for even length, this returns left-mid)
ListNode *slow=head, *fast=head;
while (fast && fast->next) { slow=slow->next; fast=fast->next->next; }

auto reverse = [&](ListNode* h){
    ListNode* prev=nullptr; ListNode* cur=h;
    while(cur){ auto nxt=cur->next; cur->next=prev; prev=cur; cur=nxt; }
    return prev;
};
ListNode* second = reverse(slow);
ListNode *p1=head, *p2=second;
bool ok = true;
while (p2) { if (p1->val!=p2->val){ ok=false; break; } p1=p1->next; p2=p2->next; }
// optional: reverse(second) again to restore
```

**Cycle detection + entry**
```cpp
ListNode *slow=head,*fast=head;
while (fast && fast->next) {
    slow=slow->next; fast=fast->next->next;
    if (slow==fast) {
        slow=head;
        while (slow!=fast) { slow=slow->next; fast=fast->next; }
        // slow (== fast) is the cycle entry
        break;
    }
}
```

---

## Reverse Whole List
```cpp
ListNode* prev=nullptr,*cur=head;
while (cur){ ListNode* nxt=cur->next; cur->next=prev; prev=cur; cur=nxt; }
return prev;
```

**Pitfall**: save `nxt` first, then change `next`.

---

## Reverse Sublist [m..n]
```cpp
ListNode dummy(0); dummy.next=head;
ListNode* pre=&dummy;
for(int i=1;i<m;i++) pre=pre->next; // node before m
ListNode* cur=pre->next;            // node at m
for(int i=0;i<n-m;i++){             // head insertion
    ListNode* move = cur->next;
    cur->next = move->next;
    move->next = pre->next;
    pre->next = move;
}
return dummy.next;
```

---

## Reverse in k-Group
```cpp
auto getk = [&](ListNode* p){
    for(int i=0;i<k && p;i++) p=p->next;
    return p; // node after k nodes or nullptr
};
ListNode dummy(0); dummy.next=head;
ListNode *pre=&dummy, *cur=head;
while(true){
    ListNode* tailNext = getk(cur);
    if(!tailNext) break;
    ListNode *prev=tailNext, *node=cur;
    for(int i=0;i<k;i++){
        ListNode* nxt=node->next;
        node->next=prev;
        prev=node;
        node=nxt;
    }
    pre->next=prev;     // connect previous part to new head
    pre=cur;            // move pre to end of this block
    cur=tailNext;       // advance cur
}
return dummy.next;
```

**Pitfalls**
- Do not reverse the last short block (< k).
- Carefully reconnect `pre->next` and the block’s tail to `tailNext`.

---

## Reverse Even-Length Groups
- Group sizes are 1,2,3,... For each group, count the **actual** length `cnt` (the last group may be shorter). Reverse iff `cnt` is even.
- Reuse the in-place “reverse segment” template with dynamic `cnt`.

**Pitfall**: always use `min(expectedSize, remaining)` for `cnt`.

---

## Group Reversal
```cpp
ListNode* reverse_segment(ListNode* head, ListNode* tail_next){
    ListNode *prev=tail_next, *cur=head;
    while(cur!=tail_next){
        ListNode* nxt=cur->next;
        cur->next=prev;
        prev=cur;
        cur=nxt;
    }
    return prev; // new head of the segment
}
```

**Steps**
1. Probe the segment to get its actual length and `tail_next`.
2. If needed, reverse the segment in-place and connect `prev->next` to the new head.
3. Move `prev` to the segment tail (old head), advance `cur` to the next start.

---

## Two Pointers from Ends
- For singly lists, often combine with “reverse second half” to compare head & tail values.
- For doubly lists or arrays, maintain `i/j` from both ends.

---

## Remove N-th From End
```cpp
ListNode dummy(0); dummy.next=head;
ListNode *fast=&dummy, *slow=&dummy;
for(int i=0;i<n;i++) fast=fast->next;
while(fast->next){ fast=fast->next; slow=slow->next; }
ListNode* del=slow->next;
slow->next=del->next;
// delete del; // optional in LC
return dummy.next;
```

---

## Merge Two Sorted Lists
```cpp
ListNode dummy(0), *tail=&dummy;
while(l1 && l2){
    if(l1->val<l2->val){ tail->next=l1; l1=l1->next; }
    else { tail->next=l2; l2=l2->next; }
    tail=tail->next;
}
tail->next = l1?l1:l2;
return dummy.next;
```

---

## Merge K Sorted Lists
```cpp
struct Cmp{ bool operator()(ListNode* a,ListNode* b)const{ return a->val>b->val; } };
priority_queue<ListNode*, vector<ListNode*>, Cmp> pq;
for(auto n:lists) if(n) pq.push(n);
ListNode dummy(0), *tail=&dummy;
while(!pq.empty()){
    auto node=pq.top(); pq.pop();
    tail->next=node; tail=tail->next;
    if(node->next) pq.push(node->next);
}
tail->next=nullptr;
return dummy.next;
```

---

## Split List to Parts
```cpp
int n=0; for(auto p=head;p;p=p->next) n++;
int q=n/k, r=n%k;
vector<ListNode*> ans(k,nullptr);
ListNode *cur=head, *prev=nullptr;
for(int i=0;i<k;i++){
    ans[i]=cur;
    int size=q+(i<r?1:0);
    for(int s=0;s<size;s++){ prev=cur; if(cur) cur=cur->next; }
    if(prev) prev->next=nullptr;
}
```

---

## Partition List (< x in front)
```cpp
ListNode d1(0), d2(0), *t1=&d1, *t2=&d2;
for(auto p=head;p;p=p->next){
    if(p->val<x){ t1->next=p; t1=t1->next; }
    else { t2->next=p; t2=t2->next; }
}
t2->next=nullptr;
t1->next=d2.next;
return d1.next;
```

---

## Reorder List (L0→Ln→L1→Ln-1…)
1) Find middle; 2) Reverse second half; 3) Weave.
```cpp
// middle
ListNode *slow=head,*fast=head;
while(fast&&fast->next){ slow=slow->next; fast=fast->next->next; }
// reverse
auto reverse=[&](ListNode* h){ ListNode* prev=nullptr,*cur=h;
    while(cur){auto nxt=cur->next; cur->next=prev; prev=cur; cur=nxt;} return prev; };
ListNode* l2=reverse(slow);
// weave
ListNode* l1=head;
while(l1&&l2){
    ListNode *n1=l1->next, *n2=l2->next;
    l1->next=l2;
    if(!n1) break;
    l2->next=n1;
    l1=n1; l2=n2;
}
```

---

## Odd-Even List
```cpp
if(!head||!head->next) return head;
ListNode *odd=head, *even=head->next, *evenHead=even;
while(even&&even->next){
    odd->next=even->next; odd=odd->next;
    even->next=odd->next; even=even->next;
}
odd->next=evenHead;
return head;
```

---

## Swap Nodes in Pairs
```cpp
ListNode dummy(0); dummy.next=head;
ListNode* pre=&dummy;
while(pre->next && pre->next->next){
    ListNode* a=pre->next, *b=a->next;
    a->next=b->next;
    b->next=a;
    pre->next=b;
    pre=a;
}
return dummy.next;
```

---

## Add Two Numbers (carry)
```cpp
ListNode dummy(0), *tail=&dummy; int carry=0;
while(l1||l2||carry){
    int sum=(l1?l1->val:0)+(l2?l2->val:0)+carry;
    carry=sum/10;
    tail->next=new ListNode(sum%10);
    tail=tail->next;
    if(l1) l1=l1->next; if(l2) l2=l2->next;
}
return dummy.next;
```

**Variant II**: digits stored in forward order → reverse both lists or use stacks.

---

## Intersection of Two Lists
```cpp
ListNode *pA=headA,*pB=headB;
while(pA!=pB){
    pA = pA? pA->next : headB;
    pB = pB? pB->next : headA;
}
return pA; // may be nullptr
```

---

## Copy List with Random Pointer (O(1) extra space)
```cpp
for(auto p=head;p;p=p->next->next){
    auto cp=new Node(p->val);
    cp->next=p->next; p->next=cp;
}
for(auto p=head;p;p=p->next->next){
    p->next->random = p->random ? p->random->next : nullptr;
}
Node* newHead=head?head->next:nullptr;
for(auto p=head;p;){
    Node* cp=p->next;
    p->next=cp->next;
    cp->next = cp->next ? cp->next->next : nullptr;
    p=p->next;
}
return newHead;
```

---

## Flatten Multilevel Doubly Linked List
```cpp
stack<Node*> st;
Node dummy(0,NULL,head,NULL), *prev=&dummy, *cur=head;
while(cur || !st.empty()){
    if(!cur){ cur=st.top(); st.pop(); prev->next=cur; cur->prev=prev; }
    prev=cur;
    if(cur->child){
        if(cur->next) st.push(cur->next);
        cur->next=cur->child;
        cur->child->prev=cur;
        cur->child=nullptr;
    }
    cur=cur->next;
}
return dummy.next;
```

---

## Linked List as Stack/Queue
**Stack (push/pop at head)**
```cpp
struct StackLL{
    ListNode* head=nullptr;
    void push(int x){ head = new ListNode(x, head); }
    int pop(){ int v=head->val; auto t=head; head=head->next; /*delete t;*/ return v; }
    bool empty() const { return !head; }
};
```

**Queue (with tail)**
```cpp
struct QueueLL{
    ListNode *head=nullptr,*tail=nullptr;
    void push(int x){
        auto node=new ListNode(x);
        if(!tail){ head=tail=node; }
        else { tail->next=node; tail=node; }
    }
    int pop(){
        int v=head->val; auto t=head; head=head->next; if(!head) tail=nullptr; /*delete t;*/ return v;
    }
    bool empty() const { return !head; }
};
```

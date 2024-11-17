from minheapnode import MinHeapNode


# Class representing the Min-Heap data structure (for waitlist)
class MinHeap:
    def __init__(self):
        self.heap = []
        self.user_map = {}  # Maps userID to index in the heap

    # Add a new node to the heap
    def push(self, priority, timestamp, userID):
        node = MinHeapNode(
            -priority, timestamp, userID
        )  # Negative priority for max-heap behavior
        self.heap.append(node)
        idx = len(self.heap) - 1
        self.user_map[userID] = idx
        self._heapify_up(idx)

    # Remove and return the node with highest priority (lowest value of negative priority)
    def pop(self):
        if not self.heap:
            return None
        root = self.heap[0]
        del self.user_map[root.userID]
        last_node = self.heap.pop()
        if self.heap:
            self.heap[0] = last_node
            self.user_map[last_node.userID] = 0
            self._heapify_down(0)
        return root

    # Remove a node with the given userID from the heap
    def remove(self, userID):
        idx = self.user_map.get(userID)
        if idx is None:
            return False  # User not found in waitlist
        del self.user_map[userID]
        last_node = self.heap.pop()
        if idx < len(self.heap):
            self.heap[idx] = last_node
            self.user_map[last_node.userID] = idx
            self._heapify_up(idx)
            self._heapify_down(idx)
        return True

    # Update the priority of a user in the heap
    def update_priority(self, userID, new_priority):
        idx = self.user_map.get(userID)
        if idx is None:
            return False  # User not found in waitlist
        node = self.heap[idx]
        node.priority = -new_priority  # Negative priority for max-heap behavior
        self._heapify_up(idx)
        self._heapify_down(idx)
        return True

    # Move the node at index idx up to maintain heap property
    def _heapify_up(self, idx):
        while idx > 0 and (
            self.heap[(idx - 1) // 2].priority > self.heap[idx].priority
            or (
                self.heap[(idx - 1) // 2].priority == self.heap[idx].priority
                and self.heap[(idx - 1) // 2].timestamp > self.heap[idx].timestamp
            )
        ):
            parent_idx = (idx - 1) // 2
            self._swap(idx, parent_idx)
            idx = parent_idx

    # Move the node at index idx down to maintain heap property
    def _heapify_down(self, idx):
        size = len(self.heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            if left < size and (
                self.heap[left].priority < self.heap[smallest].priority
                or (
                    self.heap[left].priority == self.heap[smallest].priority
                    and self.heap[left].timestamp < self.heap[smallest].timestamp
                )
            ):
                smallest = left
            if right < size and (
                self.heap[right].priority < self.heap[smallest].priority
                or (
                    self.heap[right].priority == self.heap[smallest].priority
                    and self.heap[right].timestamp < self.heap[smallest].timestamp
                )
            ):
                smallest = right
            if smallest != idx:
                self._swap(idx, smallest)
                idx = smallest
            else:
                break

    # Swap two nodes in the heap
    def _swap(self, i, j):
        self.user_map[self.heap[i].userID], self.user_map[self.heap[j].userID] = j, i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # Return the number of nodes in the heap
    def __len__(self):
        return len(self.heap)

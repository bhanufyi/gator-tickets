# Class representing a Min-Heap for seat IDs (available seats)
class SeatHeap:
    def __init__(self):
        self.heap = []

    # Add a new seat ID to the heap
    def push(self, seatID):
        self.heap.append(seatID)
        self._heapify_up(len(self.heap) - 1)

    # Remove and return the seat ID with the lowest number
    def pop(self):
        if not self.heap:
            return None
        root = self.heap[0]
        last_seat = self.heap.pop()
        if self.heap:
            self.heap[0] = last_seat
            self._heapify_down(0)
        return root

    # Move the seat ID at index idx up to maintain heap property
    def _heapify_up(self, idx):
        while idx > 0 and self.heap[(idx - 1) // 2] > self.heap[idx]:
            parent_idx = (idx - 1) // 2
            self.heap[idx], self.heap[parent_idx] = (
                self.heap[parent_idx],
                self.heap[idx],
            )
            idx = parent_idx

    # Move the seat ID at index idx down to maintain heap property
    def _heapify_down(self, idx):
        size = len(self.heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            if left < size and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < size and self.heap[right] < self.heap[smallest]:
                smallest = right
            if smallest != idx:
                self.heap[idx], self.heap[smallest] = (
                    self.heap[smallest],
                    self.heap[idx],
                )
                idx = smallest
            else:
                break

    # Return the number of seats in the heap
    def __len__(self):
        return len(self.heap)

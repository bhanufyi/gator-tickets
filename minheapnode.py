# Class representing a node in the Min-Heap (for waitlist)
class MinHeapNode:
    def __init__(self, priority, timestamp, userID):
        self.priority = priority  # Store negative priority for max-heap behavior
        self.timestamp = timestamp  # Timestamp when the user was added to waitlist
        self.userID = userID  # User ID

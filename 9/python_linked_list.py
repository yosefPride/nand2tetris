class Node:
    def __init__(self, x, y, value):
        self.x = x          # X-coordinate
        self.y = y          # Y-coordinate
        self.value = value  # Data to print
        self.next = None    # Next node
        self.prev = None    # Previous node

class CoordinateLinkedList:
    def __init__(self):
        self.head = None

    def append(self, x, y, value):
        """Add a node with coordinates (x, y) and value to the end."""
        new_node = Node(x, y, value)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        new_node.prev = current

    def prepend(self, x, y, value):
        """Add a node with coordinates (x, y) and value to the beginning."""
        new_node = Node(x, y, value)
        if not self.head:
            self.head = new_node
            return
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node

    def delete(self, x, y):
        """Delete the first node with the given (x, y) coordinates."""
        if not self.head:
            return

        if self.head.x == x and self.head.y == y:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            return

        current = self.head
        while current and (current.x != x or current.y != y):
            current = current.next

        if current:
            if current.next:
                current.next.prev = current.prev
            if current.prev:
                current.prev.next = current.next

    def display(self):
        """Print all nodes with their coordinates and values."""
        current = self.head
        while current:
            print(f"({current.x}, {current.y}): {current.value}", end=" <-> ")
            current = current.next
        print("None")

    def reverse_display(self):
        """Print all nodes in reverse order."""
        current = self.head
        if not current:
            print("None")
            return

        # Move to the tail
        while current.next:
            current = current.next

        # Traverse backwards
        while current:
            print(f"({current.x}, {current.y}): {current.value}", end=" <-> ")
            current = current.prev
        print("None")

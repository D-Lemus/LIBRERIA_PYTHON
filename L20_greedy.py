
import heapq
from functools import total_ordering

@total_ordering
class HuffmanNode:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.__build_repr())

    def __build_repr(self):
        if self.symbol is not None:
            return {self.symbol: ""}
        else:
            left_encoding = self.left.__build_repr()
            right_encoding = self.right.__build_repr()
            return {
                **{key: "0" + value for key, value in left_encoding.items()},
                **{key: "1" + value for key, value in right_encoding.items()},
            }

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __eq__(self, other):
        return self.frequency == other.frequency


# 1) Activity Selection Problem
def recursive_activity_selection(start, finish, n):
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    selected_activities = []

    def select_activities(activities, k):
        for m in range(k + 1, len(activities)):
            if activities[m][0] >= activities[k][1]:
                selected_activities.append(activities[m])
                select_activities(activities, m)
                break

    selected_activities.append(activities[0])
    select_activities(activities, 0)
    return selected_activities

def greedy_activity_selection(start, finish):
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    selected_activities = [activities[0]]
    last_finish = activities[0][1]

    for i in range(1, len(activities)):
        if activities[i][0] >= last_finish:
            selected_activities.append(activities[i])
            last_finish = activities[i][1]

    return selected_activities


# 2) Fractional Knapsack
def recursive_fractional_knapsack(items, capacity):
    items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)

    def knapsack_helper(index, remaining_capacity):
        if index == len(items) or remaining_capacity == 0:
            return 0, []

        weight, value = items[index]

        if weight <= remaining_capacity:
            total_value, picked_items = knapsack_helper(index + 1, remaining_capacity - weight)
            return total_value + value, [(weight, value)] + picked_items
        else:
            fraction = remaining_capacity / weight
            return value * fraction, [(weight, value * fraction)]

    return knapsack_helper(0, capacity)

def greedy_fractional_knapsack(items, capacity):
    items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)
    total_value = 0
    selected_items = []

    for weight, value in items:
        if capacity >= weight:
            capacity -= weight
            total_value += value
            selected_items.append((weight, value))
        else:
            fraction = capacity / weight
            total_value += value * fraction
            selected_items.append((weight, value * fraction))
            break

    return total_value, selected_items


# 3) Huffman Codes
def recursive_huffman_coding(symbols, frequencies):
    nodes = [HuffmanNode(s, f) for s, f in zip(symbols, frequencies)]

    def build_tree(nodes):
        if len(nodes) == 1:
            return nodes[0]

        nodes = sorted(nodes, key=lambda x: x.frequency)
        left = nodes.pop(0)
        right = nodes.pop(0)
        parent = HuffmanNode(None, left.frequency + right.frequency)
        parent.left = left
        parent.right = right
        nodes.append(parent)
        return build_tree(nodes)

    root = build_tree(nodes)
    return root.__build_repr__()

def iterative_huffman_coding(symbols, frequencies):
    heap = [HuffmanNode(s, f) for s, f in zip(symbols, frequencies)]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = HuffmanNode(None, left.frequency + right.frequency)
        parent.left = left
        parent.right = right
        heapq.heappush(heap, parent)

    root = heap[0]
    return root.__build_repr__()


if __name__ == "__main__":
    # Activity Selection
    start_times = [1, 3, 0, 5, 8, 5]
    finish_times = [2, 4, 6, 7, 9, 9]
    n = len(start_times)
    result = recursive_activity_selection(start_times, finish_times, n)
    print("Activity Selection (Recursive):", result)
    result = greedy_activity_selection(start_times, finish_times)
    print("Activity Selection (Greedy):", result)

    # Fractional Knapsack
    items = [(10, 60), (20, 100), (30, 120)]
    capacity = 50
    result, selected_items = recursive_fractional_knapsack(items, capacity)
    print("Fractional Knapsack (Recursive): Max value:", result, "Selected items:", selected_items)
    result, selected_items = greedy_fractional_knapsack(items, capacity)
    print("Fractional Knapsack (Greedy): Max value:", result, "Selected items:", selected_items)

    # Huffman Coding
    symbols = ["A", "B", "C", "D", "E"]
    frequencies = [45, 13, 12, 16, 9]
    root_recursive = recursive_huffman_coding(symbols, frequencies)
    print(f"Encoding (Recursive): {root_recursive}")
    root_iterative = iterative_huffman_coding(symbols, frequencies)
    print(f"Encoding (Iterative): {root_iterative}")

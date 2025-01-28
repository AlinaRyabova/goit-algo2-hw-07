import time
import matplotlib.pyplot as plt
from functools import lru_cache
from collections import namedtuple

# Структура даних для вузла Splay Tree
class SplayTreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

# Реалізація Splay Tree
class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root

            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)

            return root if root.left is None else self._rotate_right(root)
        else:
            if root.right is None:
                return root

            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)

            return root if root.right is None else self._rotate_left(root)

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def find(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayTreeNode(key, value)
            return

        self.root = self._splay(self.root, key)

        if key < self.root.key:
            node = SplayTreeNode(key, value)
            node.left = self.root.left
            node.right = self.root
            self.root.left = None
            self.root = node
        elif key > self.root.key:
            node = SplayTreeNode(key, value)
            node.right = self.root.right
            node.left = self.root
            self.root.right = None
            self.root = node

# Функція для обчислення чисел Фібоначчі з LRU-кешем
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# Функція для обчислення чисел Фібоначчі з використанням Splay Tree
def fibonacci_splay(n, tree):
    cached_value = tree.find(n)
    if cached_value is not None:
        return cached_value

    if n < 2:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)

    tree.insert(n, result)
    return result

# Порівняння продуктивності
fib_numbers = list(range(0, 951, 50))
lru_times = []
splay_times = []

for n in fib_numbers:
    # Час виконання для LRU Cache
    start_time = time.time()
    fibonacci_lru(n)
    lru_times.append(time.time() - start_time)

    # Час виконання для Splay Tree
    tree = SplayTree()
    start_time = time.time()
    fibonacci_splay(n, tree)
    splay_times.append(time.time() - start_time)

# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(fib_numbers, lru_times, label='LRU Cache', marker='o')
plt.plot(fib_numbers, splay_times, label='Splay Tree', marker='o')
plt.title('Порівняння продуктивності обчислення чисел Фібоначчі')
plt.xlabel('Число n')
plt.ylabel('Середній час виконання (секунди)')
plt.legend()
plt.grid()
plt.show()

# Виведення результатів у вигляді таблиці
print(f"{'n':<10}{'LRU Cache Time (s)':<20}{'Splay Tree Time (s)':<20}")
print("-" * 50)
for n, lru_time, splay_time in zip(fib_numbers, lru_times, splay_times):
    print(f"{n:<10}{lru_time:<20.10f}{splay_time:<20.10f}")
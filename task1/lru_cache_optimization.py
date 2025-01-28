import random
import time
from functools import lru_cache

# Константи для завдання
N = 100_000  # Розмір масиву
Q = 50_000  # Кількість запитів
K = 1000  # Максимальний розмір кешу

# Генерація випадкового масиву та запитів
array = [random.randint(1, 1000) for _ in range(N)]  # Масив з випадковими числами від 1 до 1000
queries = [
    ("Range", random.randint(0, N - 1), random.randint(0, N - 1)) if random.random() < 0.7 else ("Update", random.randint(0, N - 1), random.randint(1, 1000))
    for _ in range(Q)
]

# Забезпечення правильності запитів типу Range (L <= R)
queries = [
    (q[0], min(q[1], q[2]), max(q[1], q[2])) if q[0] == "Range" else q for q in queries
]

# Реалізація функцій без кешу

def range_sum_no_cache(array, L, R):
    """
    Обчислює суму елементів масиву на відрізку від L до R включно без використання кешу.
    """
    return sum(array[L:R + 1])

def update_no_cache(array, index, value):
    """
    Оновлює значення елемента масиву за вказаним індексом без використання кешу.
    """
    array[index] = value

# Реалізація функцій з використанням кешу

@lru_cache(maxsize=K)
def range_sum_with_cache(L, R):
    """
    Обчислює суму елементів масиву на відрізку від L до R включно, використовуючи LRU-кеш.
    Якщо результат для цього діапазону вже є в кеші, він повертається без повторних обчислень.
    """
    return sum(array[L:R + 1])

def update_with_cache(array, index, value):
    """
    Оновлює значення елемента масиву за вказаним індексом і очищує кеш, щоб уникнути використання застарілих даних.
    """
    array[index] = value
    range_sum_with_cache.cache_clear()  # Очищення кешу

# Порівняння продуктивності

# Час виконання без кешу
start_time_no_cache = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_no_cache(array, query[1], query[2])
    elif query[0] == "Update":
        update_no_cache(array, query[1], query[2])
end_time_no_cache = time.time()

# Час виконання з кешем
start_time_with_cache = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_with_cache(query[1], query[2])
    elif query[0] == "Update":
        update_with_cache(array, query[1], query[2])
end_time_with_cache = time.time()

# Виведення результатів
print("Час без використання кешу:", end_time_no_cache - start_time_no_cache, "секунд")
print("Час з використанням LRU-кешу:", end_time_with_cache - start_time_with_cache, "секунд")

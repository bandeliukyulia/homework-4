import time
from concurrent.futures import ProcessPoolExecutor

def collatz_steps(n):
    """Обчислює кількість кроків для виродження числа в 1 (градина Колатца)"""
    steps = 0
    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def process_chunk(start_end):
    """Обробляє окремий шматок (батч) чисел для економії накладних витрат потоків"""
    start, end = start_end
    total_steps = 0
    for i in range(start, end):
        total_steps += collatz_steps(i)
    return total_steps

def main():
    print("Початок паралельних обчислень для гіпотези Колатца...")
    
    total_numbers = 10_000_000
    num_workers = 4  # Можна змінити кількість потоків/процесів вручну
    
    # Розбиваємо 10 мільйонів чисел на рівні батчі для потоків, щоб не було простоїв
    chunk_size = total_numbers // num_workers
    chunks = [(i * chunk_size + 1, (i + 1) * chunk_size + 1) for i in range(num_workers)]
    
    start_time = time.time()
    
    # Запускаємо паралельні обчислення за допомогою ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(process_chunk, chunks)
        
    total_steps_all = sum(results)
    end_time = time.time()
    
    execution_time = end_time - start_time
    average_steps = total_steps_all / total_numbers
    
    # Виводимо результати, які вимагає викладач
    print("\n================ РЕЗУЛЬТАТИ ================")
    print(f"Загальна кількість чисел: {total_numbers:,}")
    print(f"Кількість задіяних потоків: {num_workers}")
    print(f"Загальний час обчислень: {execution_time:.4f} секунд")
    print(f"Середня кількість кроків до 1: {average_steps:.2f}")
    print("============================================")

if __name__ == "__main__":
    main()
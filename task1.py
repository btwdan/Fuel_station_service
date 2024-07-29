# Требуется: Написать функцию, возвращающую все простые числа до N

def get_primes(n: int) -> list[int]:
    if n < 2:
        return []

    # Изначально предполагаем, что все числа от 2 до n являются простыми
    arr = [True] * (n + 1)
    arr[0] = arr[1] = False  # 0 и 1 не являются простыми числами

    # Реализация Решета Эратосфена
    for i in range(2, int(n**0.5) + 1):
        if arr[i]:
            for multiple in range(pow(i, 2), n + 1, i):
                arr[multiple] = False

    # Составляем список простых чисел
    primes = [num for num, is_prime in enumerate(arr) if is_prime]

    return primes

print(get_primes(50))
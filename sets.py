def process(input_string: str) -> str:
    # Разделяем строку на список чисел
    numbers = list(map(int, input_string.split()))

    # Инициализируем счетчики
    above_zero = 0
    below_zero = 0
    zero = 0

    # Проходим по каждому числу и обновляем счетчики
    for num in numbers:
        if num > 0:
            above_zero += 1
        elif num < 0:
            below_zero += 1
        else:
            zero += 1

    # Формируем строку результата
    result = f"выше нуля: {above_zero}, ниже нуля: {below_zero}, равна нулю: {zero}"
    return result


# Пример использования
input_data = input("Введите введите числа через пробел: ")
output = process(input_data)
print(output)
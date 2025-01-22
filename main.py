import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("300x450")

        # Переменные для хранения состояния
        self.current_input = ""  # Текущий ввод
        self.result = None       # Результат вычисления
        self.last_operation = None  # Последняя операция (+, -, *, /, %)
        self.last_operand = None    # Последний операнд (например, 2 в случае "2 + 2")
        self.expression = ""     # Выражение для отображения

        # Создаем дисплей
        self.display = tk.Entry(root, font=('Arial', 24), justify='right', bd=10, relief=tk.RIDGE)
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Кнопки
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
            ('=', 5, 0), ('%', 5, 1)
        ]

        # Добавляем кнопки на экран
        for (text, row, col) in buttons:
            button = tk.Button(root, text=text, font=('Arial', 15), command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky="nsew")

        # Настройка веса строк и столбцов
        for i in range(6):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

    def on_button_click(self, value):
        print(f"Нажата кнопка: {value}")  # Логирование нажатия кнопки

        if value == 'C':  # Очистка всего
            self.current_input = ""
            self.result = None
            self.last_operation = None
            self.last_operand = None
            self.expression = ""
            self.display.delete(0, tk.END)
        elif value == '=':  # Вычисление результата
            try:
                if self.last_operation and self.last_operand is not None:
                    print(f"Повтор операции: {self.last_operation}, операнд: {self.last_operand}")  # Логирование
                    # Если есть последняя операция, выполняем её с текущим результатом
                    if self.last_operation == '+':
                        self.result += self.last_operand
                    elif self.last_operation == '-':
                        self.result -= self.last_operand
                    elif self.last_operation == '*':
                        self.result *= self.last_operand
                    elif self.last_operation == '/':
                        self.result /= self.last_operand
                    elif self.last_operation == '%':
                        # Вычисляем процент от текущего результата
                        percent_value = self.last_operand / 100
                        print(f"Повтор операции %: {self.result} + {self.result} * {percent_value}")  # Логирование
                        self.result += self.result * percent_value
                    # Отображаем результат
                    self.display.delete(0, tk.END)
                    self.display.insert(0, f"{self.expression} = {self.result}")
                else:
                    # Если нет последней операции, вычисляем выражение
                    self.result = eval(self.current_input)
                    self.display.delete(0, tk.END)
                    self.display.insert(0, f"{self.current_input} = {self.result}")
            except Exception as e:
                print(f"Ошибка: {e}")  # Логирование ошибки
                self.display.delete(0, tk.END)
                self.display.insert(0, "Ошибка")
        elif value == '%':  # Обработка процентов
            try:
                # Разделяем выражение на части (например, "100+3.6" -> ["100", "+", "3.6"])
                parts = []
                temp = ""
                for char in self.current_input:
                    if char in ['+', '-', '*', '/']:
                        if temp:
                            parts.append(temp)
                        parts.append(char)
                        temp = ""
                    else:
                        temp += char
                if temp:
                    parts.append(temp)

                print(f"Части выражения: {parts}")  # Логирование

                # Если последний элемент — это число, вычисляем процент от него
                if parts and parts[-1].replace('.', '').isdigit():
                    percent_value = float(parts[-1]) / 100
                    print(f"Процентное значение: {percent_value}")  # Логирование
                    # Умножаем процент на предыдущее число в выражении
                    if len(parts) >= 2 and parts[-2] in ['+', '-', '*', '/']:
                        previous_number = float(parts[-3]) if len(parts) >= 3 else 0
                        print(f"Предыдущее число: {previous_number}")  # Логирование
                        if parts[-2] == '+':
                            result = previous_number + (previous_number * percent_value)
                        elif parts[-2] == '-':
                            result = previous_number - (previous_number * percent_value)
                        elif parts[-2] == '*':
                            result = previous_number * percent_value
                        elif parts[-2] == '/':
                            result = previous_number / percent_value
                        # Сохраняем выражение для отображения
                        self.expression = f"{previous_number} + {parts[-1]}%"
                        self.current_input = str(result)
                        self.display.delete(0, tk.END)
                        self.display.insert(0, f"{self.expression} = {result}")
                        # Сохраняем последнюю операцию и операнд
                        self.last_operation = '%'
                        self.last_operand = float(parts[-1])
                    else:
                        self.current_input = str(percent_value)
                        self.display.delete(0, tk.END)
                        self.display.insert(0, self.current_input)
                else:
                    self.display.delete(0, tk.END)
                    self.display.insert(0, "Ошибка")
            except Exception as e:
                print(f"Ошибка: {e}")  # Логирование ошибки
                self.display.delete(0, tk.END)
                self.display.insert(0, "Ошибка")
        elif value in ['+', '-', '*', '/']:  # Операции
            try:
                if self.last_operation:
                    # Если уже есть операция, вычисляем результат
                    self.on_button_click('=')
                else:
                    # Сохраняем текущее значение как результат
                    self.result = float(self.current_input)
                # Сохраняем последнюю операцию и операнд
                self.last_operation = value
                self.last_operand = float(self.current_input.split(self.last_operation)[-1])
                # Добавляем операцию к текущему вводу
                self.current_input += value
                self.display.delete(0, tk.END)
                self.display.insert(0, self.current_input)
            except Exception as e:
                print(f"Ошибка: {e}")  # Логирование ошибки
                self.display.delete(0, tk.END)
                self.display.insert(0, "Ошибка")
        else:
            # Добавляем введенное значение к текущему вводу
            self.current_input += value
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current_input)

# Запуск калькулятора
if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
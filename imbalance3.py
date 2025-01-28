import requests
import pandas as pd
import matplotlib.pyplot as plt


# Функция для получения стакана ордеров
def get_order_book(symbol, limit=10):
    url = f"https://fapi.binance.com/fapi/v1/depth"
    params = {
        'symbol': symbol,  # Например, 'BTCUSDT'
        'limit': limit  # Количество уровней в стакане
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


# Функция для визуализации стакана ордеров с горизонтальными столбцами
def plot_order_book_horizontal(order_book):
    bids = pd.DataFrame(order_book['bids'], columns=['Price', 'Bid Qty'], dtype=float)
    asks = pd.DataFrame(order_book['asks'], columns=['Price', 'Ask Qty'], dtype=float)

    plt.figure(figsize=(10, 8))

    # Горизонтальные столбцы для bid (покупка)
    plt.barh(bids['Price'], bids['Bid Qty'], color='green', label='Bids')

    # Горизонтальные столбцы для ask (продажа)
    plt.barh(asks['Price'], asks['Ask Qty'], color='red', label='Asks')

    # Настройка графика
    plt.title('Order Book (Horizontal)')
    plt.xlabel('Quantity')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()


# Основной код
if __name__ == "__main__":
    symbol = 'BTCUSDT'  # Пара для анализа
    order_book = get_order_book(symbol, limit=20)

    # Визуализация стакана ордеров с горизонтальными столбцами
    plot_order_book_horizontal(order_book)
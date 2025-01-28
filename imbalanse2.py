import requests
import pandas as pd
import matplotlib.pyplot as plt


# Функция для получения стакана ордеров
def get_order_book(symbol, limit=100):
    url = f"https://fapi.binance.com/fapi/v1/depth"
    params = {
        'symbol': symbol,  # Например, 'BTCUSDT'
        'limit': limit  # Количество уровней в стакане
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


# Функция для расчета дисбаланса
def calculate_imbalance(order_book):
    bids = pd.DataFrame(order_book['bids'], columns=['Price', 'Bid Qty'], dtype=float)
    asks = pd.DataFrame(order_book['asks'], columns=['Price', 'Ask Qty'], dtype=float)

    # Суммарные объемы на покупку и продажу
    total_bid = bids['Bid Qty'].sum()
    total_ask = asks['Ask Qty'].sum()

    # Расчет дисбаланса
    imbalance = (total_bid - total_ask) / (total_bid + total_ask)
    return imbalance, total_bid, total_ask


# Функция для визуализации стакана ордеров
def plot_order_book(order_book):
    bids = pd.DataFrame(order_book['bids'], columns=['Price', 'Bid Qty'], dtype=float)
    asks = pd.DataFrame(order_book['asks'], columns=['Price', 'Ask Qty'], dtype=float)

    plt.figure(figsize=(10, 6))
    plt.bar(bids['Price'], bids['Bid Qty'], color='green', label='Bids')
    plt.bar(asks['Price'], asks['Ask Qty'], color='red', label='Asks')
    plt.title('Order Book')
    plt.xlabel('Price')
    plt.ylabel('Quantity')
    plt.legend()
    plt.show()


# Основной код
if __name__ == "__main__":
    symbol = 'BTCUSDT'  # Пара для анализа
    order_book = get_order_book(symbol, limit=20)

    # Расчет дисбаланса
    imbalance, total_bid, total_ask = calculate_imbalance(order_book)
    print(f"Total Bid: {total_bid}")
    print(f"Total Ask: {total_ask}")
    print(f"Order Book Imbalance: {imbalance:.4f}")

    # Визуализация стакана ордеров
    plot_order_book(order_book)
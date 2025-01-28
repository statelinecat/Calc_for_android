import requests


def get_order_book(symbol, limit=100):
    """
    Получает стакан ордеров для указанной торговой пары.
    """
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка получения стакана ордеров для {symbol}.")
        return None


def analyze_order_book(order_book):
    """
    Анализирует дисбаланс между заявками на покупку и продажу.
    """
    bids = order_book['bids']  # Покупки
    asks = order_book['asks']  # Продажи

    # Суммируем объемы заявок
    total_bid_volume = sum([float(bid[1]) for bid in bids])  # bid[1] = объем
    total_ask_volume = sum([float(ask[1]) for ask in asks])  # ask[1] = объем

    imbalance = (total_bid_volume - total_ask_volume) / (total_bid_volume + total_ask_volume) * 100

    return total_bid_volume, total_ask_volume, imbalance


def main():
    pair = input("Введите торговую пару (например, BTCUSDT): ").strip().upper()
    print(f"Получение стакана ордеров для {pair}...")
    order_book = get_order_book(pair)

    if order_book:
        bid_volume, ask_volume, imbalance = analyze_order_book(order_book)
        print(f"\nАнализ стакана для {pair}:")
        print(f"Общий объем покупок (bids): {bid_volume:.2f}")
        print(f"Общий объем продаж (asks): {ask_volume:.2f}")
        print(f"Дисбаланс: {imbalance:.2f}%")

        if imbalance > 10:
            print("Рынок перекуплен (давление покупателей).")
        elif imbalance < -10:
            print("Рынок перепродан (давление продавцов).")
        else:
            print("Рынок сбалансирован.")
    else:
        print("Не удалось получить данные стакана ордеров.")


if __name__ == "__main__":
    main()

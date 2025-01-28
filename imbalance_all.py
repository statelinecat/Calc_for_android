import requests

def get_futures_symbols():
    """
    Получает список всех торговых пар на фьючерсах Binance.
    """
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        symbols = [symbol['symbol'] for symbol in data['symbols']]
        return symbols
    else:
        print("Ошибка получения списка торговых пар.")
        return []

def get_order_book(symbol, limit=100):
    """
    Получает стакан ордеров для указанной торговой пары.
    """
    url = f"https://fapi.binance.com/fapi/v1/depth?symbol={symbol}&limit={limit}"
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

    if total_bid_volume == 0 and total_ask_volume == 0:
        imbalance = 0  # Если нет заявок, дисбаланс равен 0
    else:
        imbalance = (total_bid_volume - total_ask_volume) / (total_bid_volume + total_ask_volume) * 100

    return total_bid_volume, total_ask_volume, imbalance

def main():
    symbols = get_futures_symbols()
    if not symbols:
        print("Не удалось получить список торговых пар.")
        return

    total_bid_volume = 0
    total_ask_volume = 0
    total_imbalance = 0

    for symbol in symbols:
        print(f"Получение стакана ордеров для {symbol}...")
        order_book = get_order_book(symbol)

        if order_book:
            bid_volume, ask_volume, imbalance = analyze_order_book(order_book)
            total_bid_volume += bid_volume
            total_ask_volume += ask_volume
            total_imbalance += imbalance

    average_imbalance = total_imbalance / len(symbols)

    print(f"\nСуммарный анализ стаканов для всех пар:")
    print(f"Общий объем покупок (bids): {total_bid_volume:.2f}")
    print(f"Общий объем продаж (asks): {total_ask_volume:.2f}")
    print(f"Средний дисбаланс: {average_imbalance:.2f}%")

    if average_imbalance > 10:
        print("Рынок перекуплен (давление покупателей).")
    elif average_imbalance < -10:
        print("Рынок перепродан (давление продавцов).")
    else:
        print("Рынок сбалансирован.")

if __name__ == "__main__":
    main()

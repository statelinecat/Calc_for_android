import requests


def get_futures_symbols():
    """
    Получает список всех фьючерсных пар, торгуемых на Binance.
    """
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = requests.get(url)
    if response.status_code == 200:
        symbols = response.json()['symbols']
        # Фильтруем пары, которые торгуются против USDT
        usdt_pairs = [symbol['symbol'] for symbol in symbols if symbol['quoteAsset'] == 'USDT']
        return usdt_pairs
    else:
        print("Ошибка получения списка фьючерсных пар.")
        return None


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

    # Проверяем, чтобы суммарный объем не был равен нулю
    if total_bid_volume + total_ask_volume == 0:
        return total_bid_volume, total_ask_volume, 0  # Дисбаланс = 0, если объемы нулевые

    imbalance = (total_bid_volume - total_ask_volume) / (total_bid_volume + total_ask_volume) * 100

    return total_bid_volume, total_ask_volume, imbalance


def analyze_specific_pairs(specific_pairs):
    """
    Анализирует дисбаланс для конкретных пар.
    """
    print("Анализ конкретных пар:")
    for pair in specific_pairs:
        print(f"\nПолучение стакана ордеров для {pair}...")
        order_book = get_order_book(pair)

        if order_book:
            bid_volume, ask_volume, imbalance = analyze_order_book(order_book)
            print(f"Анализ стакана для {pair}:")
            print(f"Общий объем покупок (bids): {bid_volume:.2f}")
            print(f"Общий объем продаж (asks): {ask_volume:.2f}")
            print(f"Дисбаланс: {imbalance:.2f}%")

            if imbalance > 10:
                print(f"Рынок {pair} перекуплен (давление покупателей).")
            elif imbalance < -10:
                print(f"Рынок {pair} перепродан (давление продавцов).")
            else:
                print(f"Рынок {pair} сбалансирован.")
        else:
            print(f"Не удалось получить данные стакана ордеров для {pair}.")


def analyze_all_pairs(symbols):
    """
    Анализирует общий дисбаланс для всех фьючерсных пар.
    """
    total_bid_volume_all = 0
    total_ask_volume_all = 0

    for symbol in symbols:
        print(f"Получение стакана ордеров для {symbol}...")
        order_book = get_order_book(symbol)

        if order_book:
            bid_volume, ask_volume, imbalance = analyze_order_book(order_book)
            total_bid_volume_all += bid_volume
            total_ask_volume_all += ask_volume

    # Проверяем, чтобы суммарный объем не был равен нулю
    if total_bid_volume_all + total_ask_volume_all == 0:
        print("\nСуммарный объем покупок и продаж равен нулю. Невозможно рассчитать дисбаланс.")
        return

    total_imbalance = (total_bid_volume_all - total_ask_volume_all) / (
                total_bid_volume_all + total_ask_volume_all) * 100

    print("\nАнализ стакана для всех фьючерсных пар:")
    print(f"Общий объем покупок (bids): {total_bid_volume_all:.2f}")
    print(f"Общий объем продаж (asks): {total_ask_volume_all:.2f}")
    print(f"Общий дисбаланс: {total_imbalance:.2f}%")

    if total_imbalance > 10:
        print("Рынок перекуплен (давление покупателей).")
    elif total_imbalance < -10:
        print("Рынок перепродан (давление продавцов).")
    else:
        print("Рынок сбалансирован.")


def main():
    # Конкретные пары для анализа
    specific_pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "LINKUSDT", "TONUSDT"]

    # Анализ конкретных пар
    analyze_specific_pairs(specific_pairs)

    # Получение списка всех фьючерсных пар
    print("\nПолучение списка всех фьючерсных пар...")
    symbols = get_futures_symbols()

    if symbols:
        # Анализ всех фьючерсных пар
        analyze_all_pairs(symbols)
    else:
        print("Не удалось получить список фьючерсных пар.")


if __name__ == "__main__":
    main()
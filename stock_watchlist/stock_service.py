import yfinance as yf


def get_company_info(ticker):
    """
    銘柄コードから企業情報を取得
    """
    try:
        print(f"[INFO] get_company_info start ticker={ticker}")

        stock = yf.Ticker(ticker)

        print("[INFO] Ticker object created")

        info = stock.info

        print(f"[INFO] stock.info type={type(info)}")
        print(f"[INFO] stock.info={info}")

        company_name = info.get("longName")

        print(f"[INFO] longName={company_name}")

        if not company_name:
            print("[INFO] longName not found")
            return None

        result = {
            "ticker": ticker.upper(),
            "company_name": company_name
        }

        print(f"[INFO] success result={result}")

        return result

    except Exception as e:
        print(f"[ERROR] get_company_info failed")
        print(f"[ERROR] exception={repr(e)}")
        return None


def get_stock_price(ticker):
    """
    現在株価情報を取得
    """
    try:
        print(f"[INFO] get_stock_price start ticker={ticker}")

        stock = yf.Ticker(ticker)

        info = stock.info

        print(f"[INFO] stock.info={info}")

        current_price = info.get("currentPrice")
        previous_close = info.get("previousClose")

        print(f"[INFO] current_price={current_price}")
        print(f"[INFO] previous_close={previous_close}")

        if current_price is None or previous_close is None:
            print("[INFO] price data missing")
            return None

        change_percent = (
            (current_price - previous_close)
            / previous_close
        ) * 100

        result = {
            "current_price": round(current_price, 2),
            "previous_close": round(previous_close, 2),
            "change_percent": round(change_percent, 2)
        }

        print(f"[INFO] success result={result}")

        return result

    except Exception as e:
        print(f"[ERROR] get_stock_price failed")
        print(f"[ERROR] exception={repr(e)}")
        return None

# stock_service.py

import yfinance as yf


def get_company_info(ticker):
    """
    銘柄コードから企業情報を取得

    Args:
        ticker (str)

    Returns:
        dict

        成功:
        {
            "ticker": "AAPL",
            "company_name": "Apple Inc."
        }

        失敗:
        None
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        company_name = info.get("longName")

        if not company_name:
            return None

        return {
            "ticker": ticker.upper(),
            "company_name": company_name
        }

    except Exception:
        return None


def get_stock_price(ticker):
    """
    現在株価情報を取得

    Args:
        ticker (str)

    Returns:
        dict

        {
            "current_price": 210.50,
            "previous_close": 208.00,
            "change_percent": 1.20
        }

        取得失敗時:
        None
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        current_price = info.get("currentPrice")
        previous_close = info.get("previousClose")

        if current_price is None or previous_close is None:
            return None

        change_percent = (
            (current_price - previous_close)
            / previous_close
        ) * 100

        return {
            "current_price": round(current_price, 2),
            "previous_close": round(previous_close, 2),
            "change_percent": round(change_percent, 2)
        }

    except Exception:
        return None

# database.py

import sqlite3

DB_NAME = "watchlist.db"


def get_connection():
    """
    SQLite接続を取得
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    テーブル作成
    アプリ起動時に1回実行する
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE NOT NULL,
            company_name TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_all_stocks():
    """
    登録済み銘柄を全件取得

    Returns:
        list[sqlite3.Row]
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            ticker,
            company_name,
            created_at
        FROM watchlist
        ORDER BY created_at DESC
    """)

    stocks = cursor.fetchall()

    conn.close()

    return stocks


def add_stock(ticker, company_name):
    """
    銘柄を登録

    Args:
        ticker (str): 銘柄コード
        company_name (str): 企業名

    Raises:
        sqlite3.IntegrityError:
            ticker重複時
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO watchlist (
            ticker,
            company_name
        )
        VALUES (?, ?)
    """, (ticker.upper(), company_name))

    conn.commit()
    conn.close()


def delete_stock(stock_id):
    """
    銘柄を削除

    Args:
        stock_id (int): watchlist.id
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM watchlist
        WHERE id = ?
    """, (stock_id,))

    conn.commit()
    conn.close()


def ticker_exists(ticker):
    """
    tickerが登録済みか確認

    Args:
        ticker (str)

    Returns:
        bool
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM watchlist
        WHERE ticker = ?
    """, (ticker.upper(),))

    result = cursor.fetchone()

    conn.close()

    return result is not None
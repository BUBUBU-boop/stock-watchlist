# app.py

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from database import (
    init_db,
    get_all_stocks,
    add_stock,
    delete_stock,
    ticker_exists
)

from stock_service import (
    get_company_info,
    get_stock_price
)

app = Flask(__name__)
app.secret_key = "secret-key"

# DB初期化
init_db()


@app.route("/")
def index():
    """
    トップページ
    """
    stocks = get_all_stocks()

    watchlist = []

    for stock in stocks:
        price_info = get_stock_price(stock["ticker"])

        if price_info:
            watchlist.append({
                "id": stock["id"],
                "ticker": stock["ticker"],
                "company_name": stock["company_name"],
                "current_price": price_info["current_price"],
                "previous_close": price_info["previous_close"],
                "change_percent": price_info["change_percent"]
            })
        else:
            watchlist.append({
                "id": stock["id"],
                "ticker": stock["ticker"],
                "company_name": stock["company_name"],
                "current_price": "-",
                "previous_close": "-",
                "change_percent": None
            })

    return render_template(
        "index.html",
        watchlist=watchlist
    )


@app.route("/add", methods=["POST"])
def add():
    """
    銘柄登録
    """
    ticker = request.form.get("ticker", "").strip().upper()

    if not ticker:
        flash("銘柄コードを入力してください。", "danger")
        return redirect(url_for("index"))

    if ticker_exists(ticker):
        flash("この銘柄コードは既に登録されています。", "danger")
        return redirect(url_for("index"))

    company_info = get_company_info(ticker)

    if company_info is None:
        flash("存在しない銘柄コードです。", "danger")
        return redirect(url_for("index"))

    add_stock(
        company_info["ticker"],
        company_info["company_name"]
    )

    flash("銘柄を登録しました。", "success")

    return redirect(url_for("index"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    """
    銘柄削除
    """
    delete_stock(id)

    flash("銘柄を削除しました。", "success")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
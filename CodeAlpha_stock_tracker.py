import csv
import os
from datetime import date

# ─────────────────────────────────────────────
#  TASK 2 — Stock Portfolio Tracker  | 
# ─────────────────────────────────────────────

# Hardcoded stock prices (USD)
STOCK_PRICES = {
    "AAPL":  182.50,
    "TSLA":  248.00,
    "GOOGL": 175.30,
    "AMZN":  195.80,
    "MSFT":  415.00,
    "META":  530.20,
    "NFLX":  645.10,
    "NVDA":  875.50,
}


def show_available_stocks():
    print("\n   Available Stocks:")
    print(f"  {'Symbol':<8} {'Price (USD)':>12}")
    print("  " + "-" * 22)
    for symbol, price in STOCK_PRICES.items():
        print(f"  {symbol:<8} ${price:>11.2f}")
    print()


def get_portfolio():
    """Prompt user to enter stocks and quantities; return list of holdings."""
    portfolio = []
    print("  Enter your stock holdings (type 'done' when finished).\n")

    while True:
        symbol = input("  Stock symbol (or 'done'): ").strip().upper()

        if symbol == "DONE":
            break

        if symbol not in STOCK_PRICES:
            print(f"  '{symbol}' not found. Choose from the list above.\n")
            continue

        qty_input = input(f"  Quantity of {symbol}: ").strip()
        if not qty_input.isdigit() or int(qty_input) <= 0:
            print("   Please enter a positive whole number.\n")
            continue

        quantity = int(qty_input)
        price = STOCK_PRICES[symbol]
        value = price * quantity

        # Merge duplicates
        for holding in portfolio:
            if holding["symbol"] == symbol:
                holding["quantity"] += quantity
                holding["value"] = STOCK_PRICES[symbol] * holding["quantity"]
                print(f"  Updated {symbol}: total {holding['quantity']} shares.\n")
                break
        else:
            portfolio.append({
                "symbol":   symbol,
                "price":    price,
                "quantity": quantity,
                "value":    value,
            })
            print(f"  Added {quantity} × {symbol} @ ${price:.2f} = ${value:,.2f}\n")

    return portfolio


def display_portfolio(portfolio):
    """Pretty-print the portfolio summary."""
    if not portfolio:
        print("\n   Portfolio is empty.")
        return

    total = sum(h["value"] for h in portfolio)
    print("\n" + "=" * 52)
    print("          YOUR STOCK PORTFOLIO SUMMARY")
    print("=" * 52)
    print(f"  {'Symbol':<8} {'Price':>10} {'Qty':>6} {'Value (USD)':>14}")
    print("  " + "-" * 42)
    for h in portfolio:
        print(f"  {h['symbol']:<8} ${h['price']:>9.2f} {h['quantity']:>6} ${h['value']:>13,.2f}")
    print("  " + "-" * 42)
    print(f"  {'TOTAL':.<34} ${total:>13,.2f}")
    print("=" * 52)


def save_to_csv(portfolio):
    """Save the portfolio to a CSV file."""
    filename = f"portfolio_{date.today()}.csv"
    filepath = os.path.join(os.path.dirname(__file__), filename)

    total = sum(h["value"] for h in portfolio)
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Symbol", "Price (USD)", "Quantity", "Value (USD)"])
        for h in portfolio:
            writer.writerow([h["symbol"], f"{h['price']:.2f}",
                             h["quantity"], f"{h['value']:.2f}"])
        writer.writerow([])
        writer.writerow(["TOTAL", "", "", f"{total:.2f}"])

    print(f"\n  Portfolio saved to '{filename}'")
    return filepath


def main():
    print("\n  Welcome to the Stock Portfolio Tracker!")

    show_available_stocks()

    portfolio = get_portfolio()
    display_portfolio(portfolio)

    if portfolio:
        save_choice = input("\n  Save portfolio to CSV? (y/n): ").strip().lower()
        if save_choice == "y":
            save_to_csv(portfolio)

    print("\n  Thank you for using the Stock Portfolio Tracker!\n")


if __name__ == "__main__":
    main()

import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Output folder
output_dir = "bank_excel_statements__2021___2024"
os.makedirs(output_dir, exist_ok=True)

def rand_str(n):
    return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=n))

def generate_description(t_type):
    if t_type == "CR":
        templates = [
            "ACH/{company} {detail}",
            "NEFT-{bankcode}{digits}-{company}-A/C-{code}-00{digits}-YESB",
            "UPI/{handle}/Refund from {bank} {digits}/{bankcode}"
        ]
    else:
        templates = [
            "UPI/{handle}/Payment from Ph/{bank}/{digits}/{bankcode}{code}",
            "UPI/{handle}/Payment for {number}/{bank}/{digits}/{bankcode}{code}",
            "UPI/{handle}/UPIIntent/{bank}/{digits}/{paymentcode}",
            "NEFT/{bank}/{digits}/{company}/Transfer"
        ]
    template = random.choice(templates)
    replacements = {
        "company": random.choice(["Zerodha", "HDFC AMC", "CRISIL", "Mazagon Dock", "ABB Dividend", "MutualFund"]),
        "detail": f"{random.randint(1000,9999)}/PR{random.randint(1000000,9999999)}AI07",
        "bank": random.choice(["YES BANK LIMITE", "AXIS BANK", "HDFC BANK LTD", "ICICI BANK", "AIRTEL PAYMENTS"]),
        "handle": random.choice(["paytmqr6cu3by@p", "gpay-1124412000", "swiggyupi@axb", "zeptomarketplac", "blinkit.payu@hd"]),
        "digits": ''.join(random.choices("0123456789", k=12)),
        "number": str(random.randint(100, 999)),
        "bankcode": random.choice(["YBL", "AXL", "ICI", "PPPL", "RBL"]),
        "code": rand_str(16),
        "paymentcode": f"{random.choice(['PPPL', 'PYTM'])}{random.randint(1000000000000,9999999999999)}XXXXXXXXXX"
    }
    return template.format(**replacements)

def generate_transactions(start_date, end_date, total_txns=5000):
    days = (end_date - start_date).days + 1
    all_dates = [start_date + timedelta(days=i) for i in range(days)][::-1]
    txns_per_day = [total_txns // days] * days
    for i in range(total_txns % days):
        txns_per_day[i] += 1

    txns = []
    for date, count in zip(all_dates, txns_per_day):
        for _ in range(count):
            t_type = random.choices(["DR", "CR"], weights=[90, 10])[0]
            desc = generate_description(t_type)
            amt = round(random.uniform(10, 5000), 2) if t_type == "DR" else round(random.uniform(100, 30000), 2)
            txns.append([date.strftime("%d-%m-%Y"), desc, amt, t_type])
    return txns

def generate_month_pairs():
    pairs = []
    current = datetime(2024, 11, 1)
    for _ in range(25):
        start_month = current.month
        start_year = current.year
        end_month = (start_month % 12) + 1
        end_year = start_year if start_month < 12 else start_year + 1

        start_date = datetime(start_year, start_month, 1)
        end_day = (datetime(end_year, (end_month % 12) + 1, 1) - timedelta(days=1)).day
        end_date = datetime(end_year, end_month, end_day)

        pairs.append((start_date, end_date))

        if start_month <= 2:
            prev_month = 12 if start_month == 1 else 11
            prev_year = start_year - 1
        else:
            prev_month = start_month - 2
            prev_year = start_year
        current = datetime(prev_year, prev_month, 1)
    return pairs

# Main
month_pairs = generate_month_pairs()

for idx, (start_date, end_date) in enumerate(month_pairs, start=1):
    txns = generate_transactions(start_date, end_date, total_txns=5000)
    df = pd.DataFrame(txns, columns=["Date", "Description", "Amount", "Type"])

    file_label = f"{start_date.strftime('%b')}_{end_date.strftime('%b')}_{start_date.year}"
    filename_excel = f"bank_statement_{idx:02d}_{file_label}.xlsx"
    filename_csv = f"bank_statement_{idx:02d}_{file_label}.csv"

    # Save Excel
    df.to_excel(os.path.join(output_dir, filename_excel), index=False)

    # Save CSV
    df.to_csv(os.path.join(output_dir, filename_csv), index=False)

print("✅ Done: 25 Excel and 25 CSV files created with 2-month periods and 5,000 rows each.")

import pandas as pd
import re
import math
import json
from datetime import datetime
from flatten_json import flatten
from utils.config_loader import load_json_config
from io import BytesIO


# ------------------------------
# Helper Functions
# ------------------------------

def read_excel(file_stream: BytesIO, config: dict) -> pd.DataFrame:
    """
    Reads Excel file from memory and returns the relevant rows and columns as a DataFrame.
    """
    df = pd.read_excel(file_stream, header=None)
    df.columns = list(df.iloc[config["header_row_index"]].values)
    data = df[config["starting_row"]:config["ending_row"]].reset_index(drop=True)
    return data


def parse_row(row: pd.Series, config: dict) -> dict:
    """
    Parse a single row into a transaction dictionary containing
    month, type, amount (as float), category_name, and category_type.
    """
    date_val = row[config["date_column"]]
    if pd.isna(date_val):
        return None
    month = datetime.strptime(str(date_val), config["date_format"]).strftime("%b,%y")

    debit = float(row.get(config["debit_column"], 0) or 0)
    credit = float(row.get(config["credit_column"], 0) or 0)
    if debit > 0:
        transaction_type = "debit"
        amount = debit
    else:
        transaction_type = "credit"
        amount = credit

    narration = str(row.get("Narration", ""))

    # Default category
    category_name, category_type = "others", "Misc."
    for cat in config["categories"]:
        match = re.search(cat["regex"], narration)
        if match:
            groups = [re.sub(r"\s+", " ", g) for g in match.groups()]
            category_name = cat["name"].format(*groups)
            category_type = cat["type"]
            break

    return {
        "month": month,
        "transaction_type": transaction_type,
        "amount": float(amount),  # ensure float
        "category_name": category_name,
        "category_type": category_type
    }


def update_global_data(global_data: dict, parsed: dict):
    """
    Update the global_data dictionary with a single parsed transaction.
    All amounts stored as float.
    """
    month = parsed["month"]
    trans_type = parsed["transaction_type"]
    amount = float(parsed["amount"])
    cat_type = parsed["category_type"]
    cat_name = parsed["category_name"]

    if month not in global_data:
        global_data[month] = {"debit": {"total": 0.0}, "credit": {"total": 0.0}}

    gmonth = global_data[month][trans_type]
    gmonth["total"] = float(gmonth.get("total", 0.0)) + amount

    if cat_type not in gmonth:
        gmonth[cat_type] = {"total": amount, cat_name: amount}
    else:
        gmonth[cat_type]["total"] = float(gmonth[cat_type].get("total", 0.0)) + amount
        gmonth[cat_type][cat_name] = float(gmonth[cat_type].get(cat_name, 0.0)) + amount


# ------------------------------
# Main Orchestrator
# ------------------------------

def transform_excel_to_json(file_stream: BytesIO):
    """
    Orchestrates the Excel-to-JSON transformation.
    Returns a dictionary with status and global_data.
    """
    try:
        # Load configuration
        config = load_json_config("transformer_config.json")

        # Read Excel
        data = read_excel(file_stream, config)

        # Initialize global data
        global_data = {}

        # Process all rows
        for _, row in data.iterrows():
            try:
                parsed = parse_row(row, config)
                if parsed:
                    update_global_data(global_data, parsed)
            except Exception:
                continue  # skip malformed rows

        # Optional: print for debug
        # print(json.dumps(global_data, indent=4))

        return {
            "status": "success",
            "detailed_data": global_data,
            "total_months": len(global_data)
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

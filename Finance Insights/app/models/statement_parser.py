import pandas as pd
import numpy as np
import re
from itertools import permutations
from dateutil import parser


class BankStatementParser:

    def __init__(self, excel_path: str):
        self.excel_path = excel_path

        # Raw dataframe (everything)
        self.df = pd.read_excel(excel_path, header=None)

        # Numeric-only version
        self.df_num = self.df.apply(pd.to_numeric, errors="coerce")

        # Text-only version (non-text → NaN)
        self.text_df = self.df.map(lambda x: x if isinstance(x, str) else np.nan)

    # ------------------------------
    # Internal: Detect transaction rows
    # ------------------------------
    def _detect_transaction_rows(self, min_numeric_cols=2):
        numeric_count = self.df_num.notna().sum(axis=1)
        mask = numeric_count >= min_numeric_cols

        runs = []
        start = None
        for i, val in enumerate(mask):
            if val and start is None:
                start = i
            elif not val and start is not None:
                runs.append((start, i - 1))
                start = None
        if start is not None:
            runs.append((start, len(mask) - 1))
        if not runs:
            raise ValueError("No transaction table detected")
        return max(runs, key=lambda x: x[1] - x[0])

    # ------------------------------
    # Internal: Numeric column helpers
    # ------------------------------
    @staticmethod
    def _numeric_continuity(col):
        return col.notna().astype(int).groupby((col.isna()).cumsum()).sum().max()

    def _candidate_balance_columns(self, df):
        return sorted(df.columns, key=lambda c: self._numeric_continuity(df[c]), reverse=True)

    @staticmethod
    def _candidate_ledger_columns(df):
        return sorted(df.columns, key=lambda c: df[c].isna().mean(), reverse=True)

    @staticmethod
    def _balance_error(balance, credit, debit):
        delta = balance.diff()
        expected = credit.fillna(0) - debit.fillna(0)
        return (delta - expected).abs().mean()

    def _infer_amount_columns(self, df):
        balance_candidates = self._candidate_balance_columns(df)
        ledger_candidates = self._candidate_ledger_columns(df)

        best = {"error": np.inf, "balance": None, "credit": None, "debit": None}

        for bal in balance_candidates:
            for c1, c2 in permutations(ledger_candidates, 2):
                if len({bal, c1, c2}) < 3:
                    continue
                err = self._balance_error(df[bal], df[c1], df[c2])
                if err < best["error"]:
                    best.update({"error": err, "balance": bal, "credit": c1, "debit": c2})
        return best

    # ------------------------------
    # Internal: Identify date column
    # ------------------------------
    @staticmethod
    def _identify_date_column(df_table, exclude_cols):
        month_names = [
            "jan", "january", "feb", "february", "mar", "march", "apr", "april",
            "may", "jun", "june", "jul", "july", "aug", "august", "sep", "sept",
            "september", "oct", "october", "nov", "november", "dec", "december"
        ]
        month_pattern = re.compile(r"\b(" + "|".join(month_names) + r")\b", re.IGNORECASE)
        numeric_date_pattern = re.compile(r"\b\d{1,4}[-/]\d{1,2}[-/]\d{1,4}\b")
        ordinal_pattern = re.compile(r"\b\d{1,2}(st|nd|rd|th)\b", re.IGNORECASE)

        best_col, best_score = None, 0

        for col in df_table.columns:
            if col in exclude_cols:
                continue
            series = df_table[col].dropna().astype(str)
            if len(series) < 3:
                continue

            date_like, valid_len = 0, 0
            alphabet_set = set()

            for v in series:
                v = v.strip()
                if not (5 <= len(v) <= 30):
                    continue
                valid_len += 1
                alphabet_set.update(v.lower())
                has_digit = any(c.isdigit() for c in v)
                has_month = bool(month_pattern.search(v))
                has_numeric = bool(numeric_date_pattern.search(v))
                has_ordinal = bool(ordinal_pattern.search(v))
                if has_digit and (has_month or has_numeric or has_ordinal):
                    date_like += 1

            if valid_len == 0:
                continue

            date_ratio = date_like / valid_len
            alphabet_penalty = len(alphabet_set)
            score = date_ratio * 3.0 + np.log(valid_len) - alphabet_penalty * 0.05

            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    # ------------------------------
    # Internal: Identify description column
    # ------------------------------
    @staticmethod
    def _identify_description_column(df_table, exclude_cols):
        best_col, best_score = None, 0
        for col in df_table.columns:
            if col in exclude_cols:
                continue
            series = df_table[col].dropna().astype(str)
            if len(series) < 3:
                continue
            alpha_chars = sum(sum(c.isalpha() for c in v) for v in series)
            total_chars = sum(len(v) for v in series)
            unique_ratio = series.nunique() / len(series)
            if total_chars == 0:
                continue
            alpha_ratio = alpha_chars / total_chars
            score = alpha_ratio * 2.0 + unique_ratio * 1.5 + np.log(len(series))
            if score > best_score:
                best_score = score
                best_col = col
        return best_col

    # ------------------------------
    # Public API: get final transaction dataframe
    # ------------------------------
    def get_transaction_table(self):
        # Step 1: detect rows
        row_start, row_end = self._detect_transaction_rows()
        df_num_table = self.df_num.iloc[row_start:row_end + 1].reset_index(drop=True)
        df_text_table = self.text_df.iloc[row_start:row_end + 1].reset_index(drop=True)
        df_table = self.df.iloc[row_start:row_end + 1].reset_index(drop=True)

        # Step 2: amounts
        amount_cols = self._infer_amount_columns(df_num_table)
        balance_col, credit_col, debit_col = amount_cols["balance"], amount_cols["credit"], amount_cols["debit"]

        exclude = {balance_col, credit_col, debit_col}

        # Step 3: date & description
        date_col = self._identify_date_column(df_table, exclude)
        desc_col = self._identify_description_column(df_text_table, exclude | {date_col})

        # Step 4: extract final table
        df_final = pd.DataFrame({
            "date": df_table[date_col],
            "description": df_table[desc_col],
            "debit": df_table[debit_col],
            "credit": df_table[credit_col],
            "balance": df_table[balance_col]
        })

        # Robust date parsing
        def parse_date(x):
            try:
                return parser.parse(str(x), dayfirst=True).strftime("%d-%m-%Y")
            except:
                return pd.NA

        df_final["date"] = df_final["date"].map(parse_date)

        return df_final


# ------------------------------
# Example usage
# ------------------------------
if __name__ == "__main__":
    statement_parser = BankStatementParser("statement.xls")
    df_transactions = statement_parser.get_transaction_table()
    print(df_transactions.head(100).to_string())

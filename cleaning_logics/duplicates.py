def count_duplicate_rows(sales_data):
    duplicate_rows = sales_data.duplicated()

    return duplicate_rows.sum()
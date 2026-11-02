def count_duplicate_rows(sales_data):
    duplicate_rows = sales_data.duplicated()

    return duplicate_rows.sum()


def remove_duplicate_rows(sales_data):
    # Work on a copy so the original data stays unchanged
    cleaned_data = sales_data.copy()

    # Remove rows that are completely identical
    cleaned_data = cleaned_data.drop_duplicates(keep="first")

    # Reset the row numbers after removing duplicates
    cleaned_data = cleaned_data.reset_index(drop=True)

    return cleaned_data
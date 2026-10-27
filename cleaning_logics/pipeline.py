from cleaning_logics.product_names import clean_product_names
from cleaning_logics.dates import clean_sales_dates
from cleaning_logics.duplicates import (
    count_duplicate_rows,
    remove_duplicate_rows,
)


def clean_sales_data(
    sales_data,
    product_columns=None,
    date_columns=None,
):
    # Work on a copy so the original uploaded data stays unchanged
    cleaned_data = sales_data.copy()

    if product_columns is None:
        product_columns = []

    if date_columns is None:
        date_columns = []

    rows_before = len(cleaned_data)

    # Clean every product column selected by the user
    for column in product_columns:
        if column not in cleaned_data.columns:
            raise ValueError(
                f"Product column '{column}' was not found."
            )

        cleaned_data = clean_product_names(
            cleaned_data,
            column
        )

    # Clean every date column selected by the user
    for column in date_columns:
        if column not in cleaned_data.columns:
            raise ValueError(
                f"Date column '{column}' was not found."
            )

        cleaned_data = clean_sales_dates(
            cleaned_data,
            column
        )

    # Check duplicates after the other cleaning steps
    duplicate_count = count_duplicate_rows(
        cleaned_data
    )

    # Remove rows that are completely identical
    cleaned_data = remove_duplicate_rows(
        cleaned_data
    )

    rows_after = len(cleaned_data)

    summary = {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "duplicates_removed": int(duplicate_count),
        "product_columns_cleaned": len(product_columns),
        "date_columns_cleaned": len(date_columns),
    }

    return cleaned_data, summary
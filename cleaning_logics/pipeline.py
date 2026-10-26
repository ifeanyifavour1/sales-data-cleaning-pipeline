from cleaning_logics.product_names import clean_product_names
from cleaning_logics.dates import clean_sales_dates


def clean_sales_data(
    sales_data,
    product_column=None,
    date_column=None,
):
    # Work on a copy so the original uploaded data stays unchanged
    cleaned_data = sales_data.copy()

    # Clean the product column if the user selected one
    if product_column:
        if product_column not in cleaned_data.columns:
            raise ValueError("Product column was not found.")

        cleaned_data = clean_product_names(
            cleaned_data,
            product_column
        )

    # Clean the date column if the user selected one
    if date_column:
        if date_column not in cleaned_data.columns:
            raise ValueError("Date column was not found.")

        cleaned_data = clean_sales_dates(
            cleaned_data,
            date_column
        )

    return cleaned_data
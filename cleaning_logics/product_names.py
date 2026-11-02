def clean_product_names(sales_data, product_column):
    # Work on a copy so the original data stays unchanged
    cleaned_data = sales_data.copy()

    cleaned_data[product_column] = (
        cleaned_data[product_column]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.replace(r"[^\w\s&'/+.\-]", "", regex=True)
        .str.replace("_", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
    )

    return cleaned_data
def clean_product_names(receive_data, product_column):
    # Work on a copy so the original data stays unchanged
    data_to_clean = receive_data.copy()

    data_to_clean[product_column] = (
        data_to_clean[product_column]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
    )

    return data_to_clean
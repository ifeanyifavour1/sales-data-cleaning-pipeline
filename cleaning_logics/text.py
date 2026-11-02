import re
import pandas


def clean_one_text(value):
    if pandas.isna(value):
        return value

    if not isinstance(value, str):
        return value

    cleaned_text = value.strip()

    # Replace repeated spaces with one space
    cleaned_text = re.sub(
        r"\s+",
        " ",
        cleaned_text
    )

    return cleaned_text


def clean_text_columns(
    sales_data,
    text_columns
):
    cleaned_data = sales_data.copy()

    for column in text_columns:

        if column not in cleaned_data.columns:
            raise ValueError(
                f"Text column '{column}' was not found."
            )

        cleaned_data[column] = (
            cleaned_data[column]
            .apply(clean_one_text)
        )

    return cleaned_data
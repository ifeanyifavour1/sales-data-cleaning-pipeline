import pandas


def normalize_column_name(column):
    return (
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def get_sample_values(series, limit=25):
    values = []

    for value in series:
        if pandas.isna(value):
            continue

        text = str(value).strip()

        if text == "":
            continue

        values.append(text)

        if len(values) == limit:
            break

    return values


def looks_like_identifier_name(column_name):
    identifier_names = [
        "id",
        "sale_id",
        "order_id",
        "customer_id",
        "product_id",
        "transaction_id",
        "invoice_id",
        "order_no",
        "order_number",
        "reference",
        "ref",
        "sku",
        "code",
    ]

    if column_name in identifier_names:
        return True

    if column_name.endswith("_id"):
        return True

    if column_name.startswith("id_"):
        return True

    if column_name.endswith("_code"):
        return True

    return False


def looks_like_product_name(column_name):
    product_names = [
        "product",
        "product_name",
        "item",
        "item_name",
        "goods",
        "goods_name",
    ]

    if column_name in product_names:
        return True

    if "product" in column_name:
        return True

    return False


def looks_like_date_name(column_name):
    date_words = [
        "date",
        "time",
        "created",
        "updated",
        "purchased",
        "ordered",
        "delivered",
    ]

    for word in date_words:
        if word in column_name:
            return True

    return False


def detect_column_type(sales_data, column):
    column_name = normalize_column_name(column)
    series = sales_data[column]

    if looks_like_identifier_name(column_name):
        return {
            "column": column,
            "type": "identifier"
        }

    if looks_like_product_name(column_name):
        return {
            "column": column,
            "type": "product"
        }

    if pandas.api.types.is_datetime64_any_dtype(series):
        return {
            "column": column,
            "type": "date"
        }

    if looks_like_date_name(column_name):
        return {
            "column": column,
            "type": "date"
        }

    if pandas.api.types.is_numeric_dtype(series):
        return {
            "column": column,
            "type": "number"
        }

    return {
        "column": column,
        "type": "text"
    }


def detect_columns(sales_data):
    detected_columns = []

    for column in sales_data.columns:
        result = detect_column_type(
            sales_data,
            column
        )

        detected_columns.append(result)

    return detected_columns
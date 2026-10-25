import re
from datetime import date, datetime

import pandas


def clean_one_date(value):
    # Leave missing dates empty
    if pandas.isna(value) or str(value).strip() == "":
        return ""

    # Excel can sometimes give us an actual date instead of text
    if isinstance(value, (pandas.Timestamp, datetime, date)):
        return value.strftime("%Y-%m-%d")

    date_text = str(value).strip()

    # Dates where the year comes first
    year_first_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y.%m.%d",
        "%Y %m %d",
    ]

    for date_format in year_first_formats:
        try:
            clean_date = datetime.strptime(date_text, date_format)
            return clean_date.strftime("%Y-%m-%d")
        except ValueError:
            pass

    # dates written with month names
    written_date_formats = [
        "%d %B %Y",
        "%d %b %Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d-%B-%Y",
        "%d-%b-%Y",
    ]

    for date_format in written_date_formats:
        try:
            clean_date = datetime.strptime(date_text, date_format)
            return clean_date.strftime("%Y-%m-%d")
        except ValueError:
            pass

    # Dates such as 23/07/2025 or 07/23/2025
    number_date = re.fullmatch(
    r"(\d{1,2})[./-](\d{1,2})[./-](\d{4})",
        date_text
    )

    if number_date:
        first = int(number_date.group(1))
        second = int(number_date.group(2))
        year = int(number_date.group(3))

        try:
            # 23/07/2025 means day/month/year
            if first > 12 and second <= 12:
                clean_date = datetime(year, second, first)
                return clean_date.strftime("%Y-%m-%d")

            # 07/23/2025 means month/day/year
            if second > 12 and first <= 12:
                clean_date = datetime(year, first, second)
                return clean_date.strftime("%Y-%m-%d")

        except ValueError:
            return date_text

        # If both numbers can be months, do not guess
        return date_text

    # Dates that also contain time
    try:
        clean_date = datetime.fromisoformat(date_text)
        return clean_date.strftime("%Y-%m-%d")
    except ValueError:
        pass

    # Leave dates unchanged if they cannot be understood safely
    return date_text


def clean_sales_dates(sales_data, date_column):
    cleaned_data = sales_data.copy()

    cleaned_data[date_column] = (
        cleaned_data[date_column]
        .apply(clean_one_date)
    )

    return cleaned_data
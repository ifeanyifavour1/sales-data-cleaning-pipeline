from pathlib import Path
from uuid import uuid4

import pandas
from flask import Flask, render_template, request

from cleaning_logics.product_names import clean_product_names
from cleaning_logics.dates import clean_sales_dates


app = Flask(__name__, static_folder="css_styling")

# Keep uploaded data temporarily while the user moves between pages
TEMP_FOLDER = Path("temp_uploads")
TEMP_FOLDER.mkdir(exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        file = request.files.get("data_file")

        # Check that the user actually selected a file
        if file is None or file.filename == "":
            return "Please select a file."

        filename = file.filename.lower()

        # Read CSV or Excel file
        try:
            if filename.endswith(".csv"):
                sales_data = pandas.read_csv(file)

            elif filename.endswith(".xlsx"):
                sales_data = pandas.read_excel(file)

            else:
                return "Please upload a CSV or Excel file."

        except Exception as error:
            print("READ ERROR:", error)
            return "Could not read the uploaded file."

        # Show the first 10 rows of the original data
        preview = sales_data.head(10).to_html(index=False)

        # Show a few values from every column
        column_rows = []

        for column in sales_data.columns:
            sample_values = (
                sales_data[column]
                .head(3)
                .fillna("")
                .astype(str)
                .tolist()
            )

            column_rows.append({
                "Column": column,
                "Sample values": ", ".join(sample_values)
            })

        columns_preview = pandas.DataFrame(
            column_rows
        ).to_html(index=False)

        # Save a temporary copy for the cleaning steps
        file_id = uuid4().hex
        temporary_file = TEMP_FOLDER / f"{file_id}.csv"

        sales_data.to_csv(temporary_file, index=False)

        return render_template(
            "review.html",
            preview=preview,
            columns_preview=columns_preview,
            columns=sales_data.columns.tolist(),
            file_id=file_id
        )

    return render_template("index.html")


@app.route("/clean-product-names", methods=["POST"])
def clean_product_column():

    file_id = request.form.get("file_id")
    product_column = request.form.get("product_column")

    if not file_id or not product_column:
        return "Please select the column that contains product names."

    temporary_file = TEMP_FOLDER / f"{file_id}.csv"

    if not temporary_file.exists():
        return "The uploaded file could not be found. Please upload it again."

    try:
        sales_data = pandas.read_csv(temporary_file)

    except Exception as error:
        print("TEMP FILE ERROR:", error)
        return "Could not read the uploaded data."

    if product_column not in sales_data.columns:
        return "The selected column was not found."

    # Clean the selected product column
    cleaned_data = clean_product_names(
        sales_data,
        product_column
    )

    before_preview = (
        sales_data[[product_column]]
        .head(10)
        .to_html(index=False)
    )

    after_preview = (
        cleaned_data[[product_column]]
        .head(10)
        .to_html(index=False)
    )

    cleaned_preview = (
        cleaned_data
        .head(10)
        .to_html(index=False)
    )

    return render_template(
        "product_cleaning_result.html",
        product_column=product_column,
        before_preview=before_preview,
        after_preview=after_preview,
        cleaned_preview=cleaned_preview
    )


@app.route("/clean-sales-dates", methods=["POST"])
def clean_date_column():

    file_id = request.form.get("file_id")
    date_column = request.form.get("date_column")

    if not file_id or not date_column:
        return "Please select the column that contains the sales dates."

    temporary_file = TEMP_FOLDER / f"{file_id}.csv"

    if not temporary_file.exists():
        return "The uploaded file could not be found. Please upload it again."

    try:
        sales_data = pandas.read_csv(temporary_file)

    except Exception as error:
        print("TEMP FILE ERROR:", error)
        return "Could not read the uploaded data."

    if date_column not in sales_data.columns:
        return "The selected date column was not found."

    # Clean the selected date column
    cleaned_data = clean_sales_dates(
        sales_data,
        date_column
    )

    before_preview = (
        sales_data[[date_column]]
        .head(10)
        .to_html(index=False)
    )

    after_preview = (
        cleaned_data[[date_column]]
        .head(10)
        .to_html(index=False)
    )

    cleaned_preview = (
        cleaned_data
        .head(10)
        .to_html(index=False)
    )

    return render_template(
        "date_cleaning_result.html",
        date_column=date_column,
        before_preview=before_preview,
        after_preview=after_preview,
        cleaned_preview=cleaned_preview
    )


if __name__ == "__main__":
    app.run(debug=True)
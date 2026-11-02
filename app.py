from pathlib import Path
from uuid import uuid4

import pandas
from flask import (
    Flask,
    render_template,
    request,
    send_file,
)

from cleaning_logics.detection import detect_columns
from cleaning_logics.pipeline import clean_sales_data


app = Flask(
    __name__,
    static_folder="css_styling"
)

TEMP_FOLDER = Path("temp_uploads")
TEMP_FOLDER.mkdir(exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        file = request.files.get(
            "data_file"
        )

        if file is None or file.filename == "":
            return "Please select a file."

        filename = file.filename.lower()

        try:

            if filename.endswith(".csv"):
                sales_data = pandas.read_csv(
                    file
                )

            elif filename.endswith(".xlsx"):
                sales_data = pandas.read_excel(
                    file
                )

            else:
                return "Please upload a CSV or Excel file."

        except Exception as error:

            print(
                "READ ERROR:",
                error
            )

            return "Could not read the uploaded file."

        preview = (
            sales_data
            .head(10)
            .to_html(index=False)
        )

        # Detect every column
        detected_columns = detect_columns(
            sales_data
        )

        # Add sample values and suggested actions
        for result in detected_columns:

            column = result["column"]

            sample_values = (
                sales_data[column]
                .dropna()
                .head(3)
                .astype(str)
                .tolist()
            )

            result["sample_values"] = (
                ", ".join(sample_values)
            )

            detected_type = result["type"]

            if detected_type == "product":
                result["suggested_action"] = "product"

            elif detected_type == "text":
                result["suggested_action"] = "text"

            elif detected_type == "date":
                result["suggested_action"] = "date"

            else:
                # Numbers and identifiers are preserved
                result["suggested_action"] = "keep"

        file_id = uuid4().hex

        temporary_file = (
            TEMP_FOLDER /
            f"{file_id}.csv"
        )

        sales_data.to_csv(
            temporary_file,
            index=False
        )

        return render_template(
            "review.html",
            preview=preview,
            detected_columns=detected_columns,
            file_id=file_id
        )

    return render_template(
        "index.html"
    )


@app.route(
    "/clean-data",
    methods=["POST"]
)
def clean_all_data():

    file_id = request.form.get(
        "file_id"
    )

    if not file_id:
        return "The uploaded file could not be found."

    temporary_file = (
        TEMP_FOLDER /
        f"{file_id}.csv"
    )

    if not temporary_file.exists():
        return (
            "The uploaded file could not be found. "
            "Please upload it again."
        )

    try:

        sales_data = pandas.read_csv(
            temporary_file
        )

    except Exception as error:

        print(
            "TEMP FILE ERROR:",
            error
        )

        return "Could not read the uploaded data."

    column_names = request.form.getlist(
        "column_name"
    )

    cleaning_actions = request.form.getlist(
        "clean_action"
    )

    if len(column_names) != len(
        cleaning_actions
    ):
        return (
            "The cleaning selections "
            "could not be read correctly."
        )

    product_columns = []
    text_columns = []
    date_columns = []
    preserved_columns = []

    for column, action in zip(
        column_names,
        cleaning_actions
    ):

        if column not in sales_data.columns:
            return (
                f"Column '{column}' "
                "was not found."
            )

        if action == "product":
            product_columns.append(
                column
            )

        elif action == "text":
            text_columns.append(
                column
            )

        elif action == "date":
            date_columns.append(
                column
            )

        elif action == "keep":
            preserved_columns.append(
                column
            )

        else:
            return (
                f"Unknown cleaning action "
                f"for '{column}'."
            )

    try:

        cleaned_data, summary = clean_sales_data(
            sales_data,
            product_columns=product_columns,
            text_columns=text_columns,
            date_columns=date_columns
        )

    except ValueError as error:
        return str(error)

    summary["preserved_columns"] = (
        preserved_columns
    )

    # Save the complete cleaned data
    # so it can be downloaded later.
    cleaned_file = (
        TEMP_FOLDER /
        f"{file_id}_cleaned.csv"
    )

    cleaned_data.to_csv(
        cleaned_file,
        index=False
    )

    before_preview = (
        sales_data
        .head(10)
        .to_html(index=False)
    )

    after_preview = (
        cleaned_data
        .head(10)
        .to_html(index=False)
    )

    return render_template(
        "cleaning_result.html",
        before_preview=before_preview,
        after_preview=after_preview,
        summary=summary,
        file_id=file_id
    )


@app.route(
    "/download/<file_id>"
)
def download_cleaned_csv(file_id):

    cleaned_file = (
        TEMP_FOLDER /
        f"{file_id}_cleaned.csv"
    )

    if not cleaned_file.exists():
        return (
            "The cleaned file could not be found. "
            "Please clean the file again."
        ), 404

    return send_file(
        cleaned_file,
        as_attachment=True,
        download_name="cleaned_sales_data.csv",
        mimetype="text/csv"
    )


if __name__ == "__main__":
    app.run(debug=True)
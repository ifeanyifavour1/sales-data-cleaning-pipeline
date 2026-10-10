import pandas
from flask import Flask, render_template, request

from cleaning import clean_product_names

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        file = request.files.get("csv_file")

        # Check if a file was selected
        if file is None or file.filename == "":
            return "Please select a file."

        # Check if the file is a CSV
        if not file.filename.lower().endswith(".csv"):
            return "Please upload a CSV file."

        # Read the CSV file with Pandas
        try:
            sales_data = pandas.read_csv(file)
        except Exception:
            return "Could not read the CSV file."

        # Raw preview - first 10 rows
        preview = sales_data.head(10).to_html(index=False)

        # Get each column and its first 3 values
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

        # Create a small table showing column names and sample values
        columns_preview = pandas.DataFrame(column_rows).to_html(index=False)

        return render_template(
            "review.html",
            preview=preview,
            columns_preview=columns_preview
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
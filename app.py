import pandas
from flask import Flask, render_template, request

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

        # Show the first 10 rows
        preview = sales_data.head(10)

        return preview.to_html(index=False)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
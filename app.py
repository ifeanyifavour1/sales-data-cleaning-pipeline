import pandas
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        file = request.files.get("csv_file")

        if file is None or file.filename == "":
            return "Please select a file."

        if not file.filename.lower().endswith(".csv"):
            return "Please upload a CSV file."

        sales_data = pandas.read_csv(file)

        return "CSV file uploaded successfully."

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

data = pd.read_csv('data.csv')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/table')
def table():
    max_rows = max(data.axes[0])
    max_columns = len(data.axes[1])
    empty_cells = data.isna().sum().sum()
    filled_cells = data.count().sum()

    info_df = pd.DataFrame({
        "Название столбца": data.columns,
        "Тип данных": data.dtypes,
    })

    row_from = 1 if request.args.get("row_from") is None else int(request.args.get("row_from")) - 1
    row_to = 1 if request.args.get("row_to") is None else int(request.args.get("row_to"))
    column_from = 1 if request.args.get("column_from") is None else int(request.args.get("column_from")) - 1
    column_to = 1 if request.args.get("column_to") is None else int(request.args.get("column_to"))

    result = data.iloc[row_from:row_to, column_from:column_to]

    return render_template('table.html',
                           tables=[result.to_html()],
                           titles=[''],
                           max_rows=max_rows,
                           info_df=info_df,
                           max_columns=max_columns,
                           empty_cells=empty_cells,
                           filled_cells=filled_cells)


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))

from flask import Flask, render_template, request
import pandas as pd

from generateData import expand_dataset
from tableFun import dataForTable, groupData, diagramm

app = Flask(__name__)
data = pd.read_csv('data.csv')
expand_dataset(data)
expandedData = pd.read_csv('expanded_data.csv')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/table')
def table():
    fun = dataForTable(data)
    return render_template('table.html',
                           tables=[fun[0].to_html()],
                           titles=[''],
                           max_rows=fun[1],
                           info_df=fun[2],
                           max_columns=fun[3],
                           empty_cells=fun[4],
                           filled_cells=fun[5])


@app.route('/tableExpanded')
def tableExpanded():
    fun = dataForTable(expandedData)
    return render_template('table.html',
                           tables=[fun[0].to_html()],
                           titles=[''],
                           max_rows=fun[1],
                           info_df=fun[2],
                           max_columns=fun[3],
                           empty_cells=fun[4],
                           filled_cells=fun[5])


@app.route('/analyze')
def analyze():
    fun = groupData(data)
    return render_template('analyze.html',
                           oil_prices_by_country=fun[0],
                           oil_prices_by_year=fun[1],
                           unemploymentrate_by_country=fun[2],
                           unemploymentrate_by_year=fun[3])


@app.route('/analyzeExpanded')
def analyzeExpanded():
    fun = groupData(expandedData)
    return render_template('analyze.html',
                           oil_prices_by_country=fun[0],
                           oil_prices_by_year=fun[1],
                           unemploymentrate_by_country=fun[2],
                           unemploymentrate_by_year=fun[3])

#
diagramm(data)
diagramm(expandedData)



if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))

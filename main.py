from flask import Flask, render_template, request, jsonify
import pandas as pd

from BloomFilter import BloomFilter
from generateData import expand_dataset
from tableFun import dataForTable, groupData, diagramm

app = Flask(__name__)
data = pd.read_csv('data.csv')
expand_dataset(data)
expandedData = pd.read_csv('expanded_data.csv')
bloom_filter = BloomFilter(1000000, 100000)

v7 = ('stock index; country; year; index price; log_indexprice; inflationrate; oil prices; exchange_rate; '
      'gdppercent; percapitaincome; unemploymentrate; manufacturingoutput; tradebalance; USTreasury; NASDAQ; '
      'FTSE 100; Nifty 50; Nikkei 225; HSI; SZCOMP; DAX 30; CAC 40; IEX 35; United States of America; United Kingdom; '
      'India; Japan; Hong Kong; China; Germany; France; Spain').lower()

v17 = ('Price; Levy; Manufacturer; Model; year; Category; Leather interior; Fuel type; Engine volume; Mileage; '
       'Cylinders; Gear box type; Drive wheels; Doors; Wheel; Color; Airbags').lower()

kaggles = {'https://www.kaggle.com/datasets/pratik453609/economic-data-9-countries-19802020': v7.split('; '),
           'https://www.kaggle.com/datasets/deepcontractor/car-price-prediction-challenge': v17.split('; ')}

for v in kaggles.values():
    for i in v:
        bloom_filter.add_to_filter(i.lower())


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


@app.route('/filter', methods=['GET'])
def bloom_filter_page():
    return render_template('filter.html')


@app.route('/filter', methods=['POST'])
def apply_bloom_filter():
    if request.method == 'POST':
        user_input = request.form.get('user_input', '').lower()
        kaggle_link = None
        if bloom_filter.check_is_not_in_filter(user_input):
            result_text = f'The term "{user_input}" does not exist in the dataset.'
        else:
            for kaggle_url, dataset_terms in kaggles.items():
                if user_input in dataset_terms:
                    kaggle_link = kaggle_url
                    result_text = f'"{user_input}" may exist in the dataset.'
                    break
            else:
                result_text = f'"{user_input}" does not exist in the dataset.'

        return jsonify({'result_text': result_text, 'kaggle_link': kaggle_link})


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))

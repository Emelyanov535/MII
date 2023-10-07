import pandas as pd
from flask import request, render_template
import matplotlib.pyplot as plt


def dataForTable(data):
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

    return result, max_rows, info_df, max_columns, empty_cells, filled_cells


def groupData(data):
    oil_prices_by_country = data.groupby('country')['oil prices'].agg(['min', 'max', 'mean']).reset_index()
    oil_prices_by_year = data.groupby('year')['oil prices'].agg(['min', 'max', 'mean']).reset_index()
    unemploymentrate_by_country = data.groupby('country')['unemploymentrate'].agg(['min', 'max', 'mean']).reset_index()
    unemploymentrate_by_year = data.groupby('year')['unemploymentrate'].agg(['min', 'max', 'mean']).reset_index()
    return oil_prices_by_country, oil_prices_by_year, unemploymentrate_by_country, unemploymentrate_by_year

def diagramm(data):
    country = 'China'
    oil_prices = data[data['country'] == country]['oil prices']

    # Группируем данные по годам и вычисляем среднее значение цены на нефть
    avg_oil_prices_by_year = data.groupby('year')['oil prices'].mean()

    # Строим столбчатую диаграмму
    plt.bar(avg_oil_prices_by_year.index, avg_oil_prices_by_year.values, color='blue', alpha=0.7)
    plt.title(f'Средняя цена на нефть в {country} по годам')
    plt.xlabel('Год')
    plt.ylabel('Средняя цена на нефть')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()
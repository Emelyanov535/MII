import random

import pandas as pd

def expand_dataset(data):
    expanded_data = data.copy()
    num_rows_to_add = int(len(expanded_data) * 0.1)
    new_rows = []

    for _ in range(num_rows_to_add):
        new_row = {}
        for column in expanded_data.columns:
            if pd.api.types.is_numeric_dtype(expanded_data[column]):
                # Генерируем новые значения для числовых столбцов
                min_value = expanded_data[column].min()
                max_value = expanded_data[column].max()
                avg_value = expanded_data[column].mean()
                random_value = random.uniform(0, max(0, max_value - avg_value))
                random_value = random_value if column != 'year' else random.randint(1980, 2020)
                new_value = avg_value + random_value if column != 'year' else random_value
                new_row[column] = new_value
            else:
                # Используем наиболее часто встречающееся значение для текстовых столбцов
                most_common_value = expanded_data[column].mode().iloc[0]
                new_row[column] = most_common_value
        new_rows.append(new_row)

    expanded_data = pd.concat([expanded_data, pd.DataFrame(new_rows)], ignore_index=True)

    expanded_data.to_csv('expanded_data.csv', index=False)
    return expanded_data  # Возвращаем расширенный датасет
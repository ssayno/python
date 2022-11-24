#!/usr/bin/env python3
import pandas as pd
import numpy as np
import re

csv_file = 'Qteee-FSSBYBSFSYXGS-DONE.csv'
data = pd.read_csv(csv_file)
values = data['Tags'].values
results = []
for row, value in enumerate(values):
    if not pd.isna(value):
        result = re.sub(', ', '; ', value.replace(', ', ',', 2))
        results.append(result)
    else:
        results.append(np.nan)
data['Tags'] = pd.Series(results)
data.to_csv(f'{csv_file.split(".")[0]}-no-comma.csv', index=False)

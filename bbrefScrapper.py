import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

URL = 'https://www.basketball-reference.com/teams/DAL/2024.html'

def get_cols(table):
    header = table.find('thead')
    return [c['aria-label'].strip() for c in header.find('tr').findAll('th')]
def get_data(table):
    body = table.find('tbody')
    rows = body.findAll('tr')
    parsed = []
    for row in rows:
        first_data = row.find('th').text
        parsed_row = [first_data]
        parsed_row = parsed_row + [x.text for x in row.findAll('td')]
        parsed.append(parsed_row)
    return parsed


def main():
    data = requests.get(URL)
    data.content

    parsed_html = BeautifulSoup(data.content, 'html.parser')

    tables = parsed_html.findAll('div', {'class': 'table_wrapper'})

    dfs = []
    for i, tabllll in enumerate(tables):
        try:
            cols = get_cols(tabllll)
            data = get_data(tabllll)
            df = pd.DataFrame(data, columns=cols)
            dfs.append(df)
        except:
            print('error')
    folder_path = "name_of_path"
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i, df in enumerate(dfs):
        file_path = os.path.join(folder_path, f'table_{i+1}.xlsx')
        df.to_excel(file_path, index=False)
        print("table saved")

if __name__ == '__main__':
    main()
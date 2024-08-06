import requests
from bs4 import BeautifulSoup
import pandas as pd
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
    for tabllll in tables:
        try:
            cols = get_cols(tabllll)
            data = get_data(tabllll)

            dfs.append(pd.DataFrame(data, columns=cols))
        except:
            print('error')

    for df in dfs:
        print(df)

if __name__ == '__main__':
    main()

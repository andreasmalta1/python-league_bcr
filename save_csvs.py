import pandas as pd
import time

def main():
    base_url = 'https://fbref.com/en/comps/11/{}-{}/{}-{}-Serie-A-Stats'
    for year in range(1988, 2022):
        print(year)
        url = base_url.format(year, year+1, year, year+1)
        html = pd.read_html(url, header=0)
        df = html[0]
        df.to_csv(f'csvs/la_liga/la_liga_{year}-{year+1}.csv', index=False)
        print('sleeping')
        time.sleep(10)

main()
import pandas as pd
import time

def main():
    base_url = 'https://fbref.com/en/comps/13/{}-{}/{}-{}-Bundesliga-Stats'
    for year in range(1995, 2022):
        print(year)
        url = base_url.format(year, year+1, year, year+1)
        html = pd.read_html(url, header=0)
        df = html[0]
        df.to_csv(f'csvs/bundesliga/bundesliga_{year}-{year+1}.csv', index=False)
        print('sleeping')
        time.sleep(5)

main()
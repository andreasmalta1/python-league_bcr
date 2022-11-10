import pandas as pd

def main():
    df_result = pd.DataFrame()
    leagues = ['epl', 'la_liga', 'serie_a', 'ligue_1', 'bundesliga']
    for league in leagues:
        for year in range(1995, 2022):
            df_temp = pd.read_csv(f'csvs/{league}/{league}_{year}-{year+1}.csv')
            df_temp = df_temp[['Squad', 'Pts']]
            df_temp['Season'] = f'{year}/{year+1}'
            frames = [df_result, df_temp]
            df_result = pd.concat(frames)
    
    df_result.to_csv('csvs\combined_leagues.csv', index=False)


main()

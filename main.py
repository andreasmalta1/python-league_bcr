import pandas as pd
import bar_chart_race as bcr
import warnings
from moviepy.editor import *

warnings.filterwarnings("ignore")


def get_final_df():
    df_all_seasons = pd.DataFrame(columns=['Season', 'Squad','Pts'])
    base_url = 'https://fbref.com/en/comps/9/{}-{}/{}-{}-Premier-League-Stats'
    for year in range(1992, 2022):
        url = base_url.format(year, year+1, year, year+1)
        html = pd.read_html(url, header=0)
        df = html[0]
        df = df[['Squad', 'Pts']]
        df['Season'] = f'{year}/{year+1}'
        df_all_seasons = pd.concat([df_all_seasons, df], ignore_index=True)

    df = df_all_seasons.pivot_table(values='Pts', index=['Season'], columns = 'Squad')

    df.fillna(0, inplace=True)
    df.sort_values(list(df.columns),inplace=True)
    df = df.sort_index()

    df.iloc[:, 0:-1] = df.iloc[:, 0:-1].cumsum()
    return df


def get_video(df):
    bcr.bar_chart_race(df = df, 
                    n_bars = 15,
                    sort='desc',
                    title='Premier League Clubs Points Since 1992',
                    filename = 'pl_clubs.mp4',
                    filter_column_colors=True,
                    period_length=600,
                    steps_per_period=10,
                    dpi=300,
                    cmap='pastel1')


def freeze_video():
    mainclip = VideoFileClip("pl_clubs.mp4").fx(vfx.freeze, t='end', freeze_duration=1)

    final = CompositeVideoClip([mainclip])
    final.write_videofile("pl_clubs_long.mp4",fps=24,codec='libx264')


def main():
    df = get_final_df()
    get_video(df)
    freeze_video()
    

main()
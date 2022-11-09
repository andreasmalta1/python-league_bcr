import pandas as pd
import bar_chart_race as bcr
import warnings
from moviepy.editor import *
import time

warnings.filterwarnings("ignore")


def get_final_df(league_short_name, year_start):
    df_all_seasons = pd.DataFrame(columns=['Season', 'Squad','Pts'])
    for year in range(year_start, 2022):
        df = pd.read_csv(f'csvs/{league_short_name}/{league_short_name}_{year}-{year+1}.csv')
        df = df[['Squad', 'Pts']]
        df['Season'] = f'{year}/{year+1}'
        df_all_seasons = pd.concat([df_all_seasons, df], ignore_index=True)

    df = df_all_seasons.pivot_table(values='Pts', index=['Season'], columns = 'Squad')

    df.fillna(0, inplace=True)
    df.sort_values(list(df.columns),inplace=True)
    df = df.sort_index()

    df.iloc[:, 0:-1] = df.iloc[:, 0:-1].cumsum()
    return df


def get_video(df, competition_name, league_short_name, year):
    bcr.bar_chart_race(df = df, 
                    n_bars = 15,
                    sort='desc',
                    title=f'{competition_name} Clubs Points Since {year}',
                    filename = f'videos/{league_short_name}_clubs.mp4',
                    filter_column_colors=True,
                    period_length=600,
                    steps_per_period=10,
                    dpi=300,
                    cmap='pastel1')


def freeze_video(league_short_name):
    video = VideoFileClip(f"videos/{league_short_name}_clubs.mp4").fx(vfx.freeze, t='end', freeze_duration=1)
    logo = (ImageClip(f"logos/{league_short_name}.png")
          .with_duration(video.duration)
          .resize(height=95)
          .margin(right=8, top=8, opacity=0)
          .with_position(("right","top")))
    
    footer_one = (TextClip('Stats from fbref.com', font_size=25, color='black')
                        .with_position((334, video.h - 75))
                        .with_duration(video.duration)
                        .with_start(0))

    footer_two = (TextClip('Data Viz by Andreas Calleja @andreascalleja', font_size=25, color='black')
                        .with_position((330, video.h - 40))
                        .with_duration(video.duration)
                        .with_start(0))
          
    final = CompositeVideoClip([video, logo, footer_one, footer_two])
    final.write_videofile(f'videos/{league_short_name}_clubs_final.mp4',fps=24,codec='libx264')


def main():
    leagues = {'Premier League': 
                        {'shorthand': 'epl',
                        'start_year': 1992},
                    'La Liga': 
                        {'shorthand': 'la_liga',
                        'start_year': 1988},
                    'Serie A': 
                        {'shorthand': 'seria_a',
                        'start_year': 1992},
                    'Ligue 1': 
                        {'shorthand': 'ligue_1',
                        'start_year': 1995},
                    'Bundesliga': 
                        {'shorthand': 'bundesliga',
                        'start_year': 1992}}
    
    for competition_name in leagues:
        league_short_name = leagues[competition_name]['shorthand']
        year = leagues[competition_name]['start_year']
        
        df = get_final_df(league_short_name, year)
        get_video(df, competition_name, league_short_name, year)
        freeze_video(league_short_name)
    

main()

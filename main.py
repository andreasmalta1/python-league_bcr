import pandas as pd
import bar_chart_race as bcr
import warnings
from moviepy.editor import *

warnings.filterwarnings("ignore")


def get_final_df(base_url, year_start):
    df_all_seasons = pd.DataFrame(columns=['Season', 'Squad','Pts'])
    for year in range(year_start, 2022):
        print(year)
        url = base_url.format(year, year+1, year, year+1)
        html = pd.read_html(url, header=0)
        df = html[0]
        df = df[['Squad', 'Pts']]
        df['Season'] = f'{year}/{year+1}'
        df_all_seasons = pd.concat([df_all_seasons, df], ignore_index=True)
        time.sleep(10)

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
                    filename = f'video/{league_short_name}_clubs.mp4',
                    filter_column_colors=True,
                    period_length=600,
                    steps_per_period=10,
                    dpi=300,
                    cmap='pastel1')


def freeze_video(league_short_name):
    video = VideoFileClip(f"video/{league_short_name}_clubs.mp4").fx(vfx.freeze, t='end', freeze_duration=1)
    logo = (ImageClip(f"logo/{league_short_name}.png")
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
    final.write_videofile(f'{league_short_name}_clubs_final.mp4',fps=24,codec='libx264')


def main():
    pl_url = 'https://fbref.com/en/comps/9/{}-{}/{}-{}-Premier-League-Stats'
    la_liga_url = 'https://fbref.com/en/comps/12/{}-{}/{}-{}-La-Liga-Stats'
    seria_a_url = 'https://fbref.com/en/comps/11/{}-{}/{}-{}-Serie-A-Stats'
    ligue_1_url = 'https://fbref.com/en/comps/13/{}-{}/{}-{}-Division-1-Stats' # 1995
    bundesliga_url = 'https://fbref.com/en/comps/20/{}-{}/{}-{}-Bundesliga-Stats'

    league_urls = {'Premier League': 
                        {'shorthand': 'epl',
                        'url': pl_url,
                        'start_year': 1992},
                    'La Liga': 
                        {'shorthand': 'la_liga',
                        'url': la_liga_url,
                        'start_year': 1992},
                    'Serie A': 
                        {'shorthand': 'seria_a',
                        'url': seria_a_url,
                        'start_year': 1992},
                    'Ligue 1': 
                        {'shorthand': 'ligue_1',
                        'url': ligue_1_url,
                        'start_year': 1995},
                    'Bundesliga': 
                        {'shorthand': 'bundesliga',
                        'url': bundesliga_url,
                        'start_year': 1992}}
    
    for competition_name in league_urls:
        url = league_urls[competition_name]['url']
        league_short_name = league_urls[competition_name]['shorthand']
        year = league_urls[competition_name]['start_year']

        print(url)
        
        df = get_final_df(url, year)
        print(df.head())
        get_video(df, competition_name, league_short_name, year)
        freeze_video(competition_name, league_short_name)
    

main()

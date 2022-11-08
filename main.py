import pandas as pd
import bar_chart_race as bcr
import warnings
from moviepy.editor import *

warnings.filterwarnings("ignore")


def get_final_df(base_url, year_start=1992):
    df_all_seasons = pd.DataFrame(columns=['Season', 'Squad','Pts'])
    for year in range(year_start, 2022):
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


def get_video(competition, df, year=1992):
    bcr.bar_chart_race(df = df, 
                    n_bars = 15,
                    sort='desc',
                    title=f'{competition} Clubs Points Since {year}',
                    filename = f'{competition}_clubs.mp4',
                    filter_column_colors=True,
                    period_length=600,
                    steps_per_period=10,
                    dpi=300,
                    cmap='pastel1')


def freeze_video(competition):
    video = VideoFileClip(f"{competition}_clubs.mp4").fx(vfx.freeze, t='end', freeze_duration=1)
    logo = (ImageClip("pl.png")
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
    final.write_videofile(f'{competition}_clubs_long.mp4',fps=24,codec='libx264')


def main():
    pl_url = 'https://fbref.com/en/comps/9/{}-{}/{}-{}-Premier-League-Stats'
    la_liga_url = 'https://fbref.com/en/comps/12/{}-{}/{}-{}-La-Liga-Stats'
    seria_a_url = 'https://fbref.com/en/comps/11/{}-{}/{}-{}-Serie-A-Stats'
    ligue_1_url = 'https://fbref.com/en/comps/13/{}-{}/{}-{}-Division-1-Stats' # 1995
    bundesliga_url = 'https://fbref.com/en/comps/20/{}-{}/{}-{}-Bundesliga-Stats'

    league_urls = {'Premier League': pl_url,
                'La Liga': la_liga_url,
                'Serie A': seria_a_url,
                'Ligue 1': ligue_1_url,
                'Bundesliga': bundesliga_url}
    
    for competition in league_urls:
        url = league_urls[competition]
        if competition == 'Ligue 1':
            df = get_final_df(url, 1995)
            get_video(competition, 1995, df)
        else:
            df = get_final_df(url)
            get_video(competition, df)
        
        
        freeze_video(competition)


    # Combined from first available year
    # From start of every competiton
    # Combined cl group stage
    # Download logos and use logos
    # shorthand name files
    # Place videos in separte folder
    

main()

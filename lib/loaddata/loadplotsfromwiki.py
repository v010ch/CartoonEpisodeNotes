import pandas as pd

from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen



CARTONS = {'Futurama' : 0, 
          'South Park': 1,
          'Simpsons'  : 2,
          }
CARTOON_WIKI = ['Futurama', 'South_Park', 'The_Simpsons']
WIKI_SEASON_LINK = 'https://en.wikipedia.org/wiki/'


def decode_season_page(season_page, no_season: int = 0) -> pd.DataFrame:
        
    epi = season_page.find_all('table', attrs={'class': 'wikiepisodetable'})[0].find_all('tr', attrs={'class': 'vevent'})
    if len(epi) < 1:
        print('Strange things happens')
        raise ValueError(f'no episodes founds in the season {no_season} on wiki page')

        
    summary = season_page.find_all('table', attrs={'class': 'wikiepisodetable'})[0].find_all('tr', attrs={'class': 'expand-child'})
    if len(summary) < 1:
        print('Strange things happens')
        raise ValueError(f'no plots found for episodes in the season {no_season}')

        
    if len(summary) != len(epi):
        print('Strange things happens')
        raise ValueError('plots founded not for all episodes')

    
    data = {'no_overall' : [0]*len(summary),
            'no_season' :  [no_season]*len(summary),
            'no_in_season' : [0]*len(summary),
            'title':       ['']*len(summary),
            'plot_small' : ['']*len(summary),
            'link':        ['']*len(summary),
           }
    
    
    for idx, (elmnt1, elmnt2) in enumerate(zip(epi, summary)):
        #print(elmnt1.th.text)
        data['no_overall'][idx] = elmnt1.th.text 
        #episode = elmnt1.td.text
        data['no_in_season'][idx] = elmnt1.td.text 
        #title = elmnt1.find_all('td', attrs={'class': 'summary'})[0].a.text
        data['title'][idx] = elmnt1.find_all('td', attrs={'class': 'summary'})[0].a.text
        #descr = elmnt2.text
        data['plot_small'][idx] = elmnt2.text
        data['link'][idx] = elmnt1.find_all('td', attrs={'class': 'summary'})[0].a.get('href')
    
    
    return pd.DataFrame(data = data)




def get_wiki_all_seasons_pages(cartoon_name: str, numb_of_seasons: int) -> list:
    
    season_page = ['']*numb_of_seasons
    link = WIKI_SEASON_LINK + cartoon_name + '_(season_'
    
    for season_numb in range(numb_of_seasons):
        req  = Request(f'{link}{season_numb+1})'
                      ,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
                     )
        
        webpage = urlopen(req).read()
        soup = bs(webpage, 'html.parser')
        
        season_page[season_numb] = soup

        
    return season_page



def get_wiki_all_seasons_plots(cartoon_name: str, numb_of_seasons: int) -> list:
    
    if numb_of_seasons < 1:
        raise ValueError('wrong number of seasons')
    
    pages = get_wiki_all_seasons_pages(cartoon_name, numb_of_seasons)    
    
    ret_df = pd.DataFrame(columns = [''])
    for no_season, page in enumerate(pages):
        tmp_df = decode_season_page(page, no_season)
        
        ret_df = pd.concat((ret_df, tmp_df))
    
    
    return ret_df

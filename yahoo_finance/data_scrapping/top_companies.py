from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import datetime

op = webdriver.ChromeOptions()
op.add_argument('headless')
op.add_argument('--log-level=3')
op.add_argument('--ignore-certificate-errors')
op.add_argument('--ignore-ssl-errors')


def trial(func):
    i = 0
    def inner(*args, **kwargs):
        nonlocal i
        if i > 100:
            return
        try:
            returned_value = func(*args, **kwargs)
            if returned_value is None:
                raise Exception('None returned value')
            return returned_value
        except Exception as error:
            i += 1
            print(f'Error for try: {i} ', error)
            time.sleep(5)
            return inner(*args, **kwargs)
    return inner

def edit_name(name):
    returned_name = name
    returned_name = returned_name.replace(' -', '')
    returned_name = returned_name.replace(',', '')
    returned_name = returned_name.replace(' &', '')
    returned_name = returned_name.replace('&', '-')
    returned_name = returned_name.replace(' ', '-')
    returned_name = returned_name.lower()
    return returned_name

def get_data(html):
    soup = BeautifulSoup(html, "lxml")
    table = soup.find_all('table', attrs={'class':'svelte-vatrz8'})

    industries = []
    for row in table[0].tbody.find_all('tr'):
        td = row.find_all('td')
        industries.append(td[0].get_text())

    industries.pop(0)
    return industries

@trial
def get_sectors(op):
    url = 'https://finance.yahoo.com/sectors'
    driver = webdriver.Chrome(options=op)
    driver.get(url)
    html = driver.page_source
    sectors = get_data(html)
    sectors = [sector.replace(' ', '-') for sector in sectors]
    return sectors
    

@trial
def get_industires(sector, op):
    url = 'https://finance.yahoo.com/sectors/' + sector
    driver = webdriver.Chrome(options=op)
    driver.get(url)
    html = driver.page_source
    industries = get_data(html)
    industries = [edit_name(industry) for industry in industries]
    return industries


@trial
def get_top_companies(sector, industry, op):
    url = 'https://finance.yahoo.com/screener/predefined/sec-ind_ind-largest-equities_' + industry + '/?count=250'
    driver = webdriver.Chrome(options=op)
    driver.get(url)
    html = driver.page_source
    companies = get_companies_data(sector, industry, html)
    return companies

def get_companies_data(sector, industry, html):
    soup = BeautifulSoup(html, "lxml")
    table = soup.find_all('table', attrs={'class':'W(100%)'})
    symbols, names, market_caps = [], [], []
    for row in table[0].tbody.find_all('tr'):
        td = row.find_all('td')
        symbol = td[0].find_all('a')[0].get_text()
        name = td[0].find_all('a')[0]['title']
        market_cap = td[7].find_all('fin-streamer')[0]['value']
        symbols.append(symbol)
        names.append(name)
        market_caps.append(market_cap)
    symbols.pop()
    names.pop()
    market_caps.pop()
    df = pd.DataFrame({'Symbol':symbols,
                  'Name':names,
                  'Market Cap': market_caps})
    df['Industry'] = industry
    df['Sector'] = sector

    return df
start = time.time()
sectors = get_sectors(op)
i = 1
for sector in sectors:
    print(f'[{i}]-------------- Sector: {sector} --------------')
    industries = get_industires(sector, op)
    j = 1
    for industry in industries:
        print(f'[{i}][{j}]-------------- Sector: {sector}; Industry: {industry}--------------')
        if industry=='silver':
            continue
        df = get_top_companies(sector, industry, op)
        df.to_csv('data.csv', mode='a', index=False, header=(j==1 and i==1))
        j+=1
    i+=1
end = time.time()
print(f'Time for scrapping: {str(datetime.timedelta(seconds=end-start))}')

#sectors = get_sectors()
#print(sectors)
#industreis = get_industires(sectors[0])
#print(industreis)

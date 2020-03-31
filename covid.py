import COVID19Py
import pandas as pd

def getCovid():
    covid19 = COVID19Py.COVID19()

    all = pd.DataFrame(covid19.getLocations())

    all['confirmed'] = [all.latest[i]['confirmed'] for i in range(len(all))]
    all['deaths'] = [all.latest[i]['deaths'] for i in range(len(all))]
    # all['recovered'] = [all.latest[i]['recovered'] for i in range(len(all))]

    all.drop(columns = 'latest', inplace=True)

    all = all[['country', 'confirmed', 'deaths']].groupby('country').sum().reset_index()

    all.sort_values(by='confirmed', ascending=False, inplace=True)

    return all

def getTimeline(countryCode):
    covid19 = COVID19Py.COVID19()
    location = covid19.getLocationByCountryCode(countryCode, timelines=True)

    df = pd.DataFrame()
    df['date'] = location[0]['timelines']['confirmed']['timeline'].keys()
    df['confirmed'] = location[0]['timelines']['confirmed']['timeline'].values()
    df['deaths'] = location[0]['timelines']['deaths']['timeline'].values()    
    return df

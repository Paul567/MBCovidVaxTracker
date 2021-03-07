import pandas as pd
import requests
import csv
import io
import datetime

URL = 'https://health-infobase.canada.ca/src/data/covidLive/vaccination-coverage-map.csv'

class VaxData:
    __nation_dataframe = pd.DataFrame()
    __province_dataframe = pd.DataFrame()
    __province = ''
    
    def __init__(self, province: str):
        self.__province = province

    @property
    def province(self):
        return self.__province

    def __get_nation_dataframe(self):
        with requests.Session() as s:
            download = s.get(URL)
            decoded_content = download.content.decode('utf-8')  
            return pd.read_csv(io.StringIO(decoded_content))

    def __get_province_dataframe(self, province: str):
        return self.__nation_dataframe.loc[
            self.__nation_dataframe['prename'] == province
            ]
    
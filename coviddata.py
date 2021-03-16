import requests
import json

class CovidData:
    __data = [{}]
    __province = ''
    __population = -1

    def __init__(self, province):
        self.__province = province.upper()
        reports = json.loads(
            requests.get(
                'https://api.covid19tracker.ca/reports/province/' +
                 self.__province
                 ).text
        )
        self.__data = reports['data']

        provinces = json.loads(
            requests.get('https://api.covid19tracker.ca/provinces').text
        )
        for prov in provinces:
            if prov['code'].upper() == self.__province:
                self.__population = prov['population']
                break

    @property
    def __latest_data(self):
        return self.__data[-1]

    @property
    def __last_week_data(self):
        return self.__data[-7:]

    @property
    def province(self):
        return self.__province

    @property
    def date(self):
        return self.__latest_data['date']

    @property
    def new_cases(self):
        return self.__latest_data['change_cases']

    @property
    def total_active(self):
        return (
            self.__latest_data['total_cases'] - 
            self.__latest_data['total_recoveries'] - 
            self.__latest_data['total_fatalities']
            )
    
    @property
    def new_deaths(self):
        return self.__latest_data['change_fatalities']
    
    @property
    def total_deaths(self):
        return self.__latest_data['total_fatalities']

    @property
    def test_positivity(self):
        cases = 0
        tests = 0
        for data in self.__data[-5:]:
            cases += data['change_cases']
            tests += data['change_tests']
        return cases / tests

    @property
    def new_vaccinations(self):
        return self.__latest_data['change_vaccinations']
    
    @property
    def total_vaccinations(self):
        return self.__latest_data['total_vaccinations']

    @property
    def total_vaccines_recieved(self):
        return self.__latest_data['total_vaccines_distributed']

    @property
    def population(self):
        return self.__population
    
    @property
    def percent_vaccinated(self):
        return self.total_vaccinations / self.population

    @property
    def percent_vaccines_recieved(self):
        return self.total_vaccines_recieved / self.population
    
    @property
    def days_until_one_dose_per_person(self):
        vaccines = 0
        for data in self.__last_week_data:
            vaccines += data['change_vaccinations']
        vaccine_rate = vaccines / len(self.__last_week_data)
        return (
            (self.population - self.total_vaccinations) / 
            vaccine_rate
            )


if __name__ == '__main__':
    data = CovidData('MB')
    print(f'{data.province} {data.date}')
    print(f'-----------------------------------------')
    print(f'New Cases:                      {data.new_cases}')
    print(f'Total Active:                   {data.total_active}')
    print(f"Test Positivity:                {data.test_positivity:.2%}")
    print('')
    print(f'New Deaths:                     {data.new_deaths}')
    print(f'Total Deaths:                   {data.total_deaths}')
    print('')
    print(f'New Vaccinations:               {data.new_vaccinations}')
    print(f'Total Vaccinations:             {data.total_vaccinations}')
    print(f"Percent Vaccinated:             {data.percent_vaccinated:.2%}")
    print(f'Percent Vaccine Recieved:       {data.percent_vaccines_recieved:.2%}')
    print(f"Days Until One Dose Per Person: {data.days_until_one_dose_per_person:.0f}")


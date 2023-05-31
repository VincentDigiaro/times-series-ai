import wbdata
import datetime


countries = ["US", "CA", "MX"]  # codes ISO des pays
indicators = {"NY.GDP.MKTP.CD": "gdp"}  #


start_date = datetime.datetime(2010, 1, 1)
end_date = datetime.datetime(2020, 1, 1)


data = wbdata.get_dataframe(indicators, country=countries, data_date=(start_date, end_date))

print(data)
import requests
import sys
import datetime


def get_data(company_name):
    api_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + \
        company_name + '&apikey=HNTGT5T6X1C9TCS4'
    r = requests.get(api_url)
    data = r.json()

    return data

# this method receives json data and return the highest rate with it's date in a tuple between 2 given dates


def find_max(data, start_date, end_date):
    max_rate = 0
    max_date = ''
    for index in data:

        obj = data[index]
        if (start_date <= string_to_datetime2(index) and end_date >= string_to_datetime2(index)):
            if (float(obj['2. high']) > max_rate):
                max_rate = float(obj['2. high'])
                max_date = index

    return max_rate, max_date

# this method receives json data and return the highest rate with it's date in a tuple between 2 given dates


def find_min(data, start_date, end_date):
    min_rate = sys.maxsize
    min_date = ''
    for index in data:

        obj = data[index]
        if (start_date <= string_to_datetime2(index) and end_date >= string_to_datetime2(index)):
            if (float(obj['2. high']) < min_rate):
                min_rate = float(obj['2. high'])
                min_date = index

    return min_rate, min_date

# converts string date with / in between to a datetime object


def string_to_datetime(string):
    day, month, year = map(int, string.split('/'))
    return datetime.date(year, month, day)

# converts string date with - in between to a datetime object


def string_to_datetime2(string):
    year, month, day = map(int, string.split('-'))
    return datetime.date(year, month, day)

# asks for user input and prints the result


def display_max_min():
    company_name = input('Stock/Company name:\n')

    start_date_string = input(
        'Please enter the start date in DD/MM/YYYY format:\n')
    start_date = string_to_datetime(start_date_string)

    end_date_string = input(
        'Please enter the end date in DD/MM/YYYY format:\n')
    end_date = string_to_datetime(end_date_string)

    maximum = find_max(get_data(company_name)[
        "Time Series (Daily)"], start_date, end_date)
    minimum = find_min(get_data(company_name)[
        "Time Series (Daily)"], start_date, end_date)

    print("Stock: " + company_name + "\nBetween dates: " + start_date_string + " and " + end_date_string + "\nHighest value: " +
          str(maximum[0]) + " on " + maximum[1] + "\nLowest value: " + str(minimum[0]) + " on " + minimum[1])

    calc_top3(start_date, end_date)


def calc_top3(start_date, end_date):

    top_1 = [0, '']
    top_2 = [0, '']
    top_3 = [0, '']

    # Set the API key
    api_key = "HNTGT5T6X1C9TCS4"

    # Set the base URL for the API
    base_url = "https://www.alphavantage.co/query?"

    # Set the symbols for the stocks you want to retrieve data for
    symbols = ["AAPL", "GOOG", "MSFT", "IBM", "TSCO.LON",
               "SHOP.TRT", "GPV.TRV", "DAI.DEX", "RELIANCE.BSE"]

    # Set the function to retrieve daily time series data
    function = "TIME_SERIES_DAILY_ADJUSTED"

    # Make a request for each symbol
    for symbol in symbols:
        # Set the parameters for the request
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": api_key
        }

        # Send the request
        response = requests.get(base_url, params=params)

        symb_max = find_max(response.json()[
            "Time Series (Daily)"], start_date, end_date)
        symb_min = find_min(response.json()[
            "Time Series (Daily)"], start_date, end_date)

        # I know nothing of stocks so my assumptions for how good stocks go is the formula (high+low)/2
        symb_average = (symb_max[0] + symb_min[0])/2
        symb_result = [symb_average, symbol]

        if (symb_result[0] > top_1[0]):
            top_3 = top_2
            top_2 = top_1
            top_1 = symb_result
        elif (symb_result[0] > top_2[0]):
            top_3 = top_2
            top_2 = symb_result
        elif (symb_result[0] > top_3[0]):
            top_3 = symb_result

    print("The 3 best performing stocks within the interval\n" +
          "1: " + top_1[1] + "\n2: " + top_2[1] + "\n3: " + top_3[1])

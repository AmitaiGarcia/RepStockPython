import requests
import PySimpleGUI as sg
import sys
from datetime import datetime, timedelta

# checks if the user input date is right format/within scope of aphavantage.
# alphavantage goes from 20 years ago (says in their documentation)


def is_valid_date(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
        end_date = datetime.strptime(end_date_str, '%d/%m/%Y')
        twenty_years_ago = datetime.now() - timedelta(weeks=52*20)
        yesterday = datetime.now() - timedelta(days=1)
        if (twenty_years_ago <= start_date < end_date <= yesterday):
            return True
        sg.popup_error(
            "Date is incorrect.\nPlease check if you entered the right date", title="Oh Oh! incorrect date!")
        return False
    except ValueError:
        sg.popup_error(
            "Date format is incorrect.\nPlease enter the date as followed: day/month/year\nexample:10/12/2022", title="Oh Oh! incorrect date format!")

# this method requests the data from the API and return it to the caller


def get_data(company_name):

    api_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + \
        company_name + '&outputsize=full&apikey=HNTGT5T6X1C9TCS4'

    r = requests.get(api_url)
    data = r.json()
    if r.status_code != 200 or data == None:
        sg.popup_error(
            "something went wrong!\nPlease check if your Symbol name is correct and try again")
    else:
        return data


# this method receives json data and return the highest rate with it's date in a tuple between 2 given dates


def find_max(rawdata, start_date_string, end_date_string):

    start_date = string_to_datetime(start_date_string)
    end_date = string_to_datetime(end_date_string)
    max_rate = 0
    max_date = ''
    data = rawdata["Time Series (Daily)"]
    for index in data:

        obj = data[index]
        if (start_date <= string_to_datetime2(index) and end_date >= string_to_datetime2(index)):
            if (float(obj['2. high']) > max_rate):
                max_rate = float(obj['2. high'])
                max_date = index

    return max_rate, max_date

# this method receives json data and return the highest rate with it's date in a tuple between 2 given dates


def find_min(rawdata, start_date_string, end_date_string):

    start_date = string_to_datetime(start_date_string)
    end_date = string_to_datetime(end_date_string)

    min_rate = sys.maxsize
    min_date = ''
    data = rawdata["Time Series (Daily)"]
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
    return datetime(year, month, day)

# converts string date with - in between to a datetime object


def string_to_datetime2(string):
    year, month, day = map(int, string.split('-'))
    return datetime(year, month, day)

# prints the result


def display_max_min(stock_name, start_date, end_date):

    maximum = find_max(get_data(stock_name), start_date, end_date)
    minimum = find_min(get_data(stock_name), start_date, end_date)

    sg.popup_scrolled("Stock: " + stock_name + "\nBetween dates: " + start_date + " and " + end_date + "\nHighest value: " +
                      str(maximum[0]) + " on " + maximum[1] + "\nLowest value: " + str(minimum[0]) + " on " + minimum[1], title="Stock information")

# This method calculates the 3 top performing stocks between start_date and end_date
# note: Since I am not able to request multiple stocks in 1 time I need to do each request separately
# if another stock is needed please put it's symbol in the symbols list.


def calc_top3(start_date, end_date):

    top_1 = [0, '']
    top_2 = [0, '']
    top_3 = [0, '']

    # Set the API key
    api_key = "HNTGT5T6X1C9TCS4"

    # Set the base URL for the API
    base_url = "https://www.alphavantage.co/query?"

    # Set the symbols for the stocks you want to retrieve data for
    symbols = ["AAPL", "GOOG", "MSFT", "IBM", "AMZN"]

    # Set the function to retrieve daily time series data
    apifunction = "TIME_SERIES_DAILY_ADJUSTED"

    # Make a request for each symbol
    for symbol in symbols:
        # Set the parameters for the request
        params = {
            "function": apifunction,
            "symbol": symbol,
            "apikey": api_key
        }

        # Send the request
        response = requests.get(base_url, params=params)

        symb_max = find_max(response.json(), start_date, end_date)
        symb_min = find_min(response.json(), start_date, end_date)

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

    sg.popup_scrolled("The 3 best performing stocks within the interval\n" +
                      "1: " + top_1[1] + "\n2: " + top_2[1] + "\n3: " + top_3[1], title="Top 3 stocks")

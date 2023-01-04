import PySimpleGUI as sg
import functions

# GUI Definition
layout = [
    [sg.Text("Please enter the stock symbol:"), sg.Input(key="stock_name")],
    [sg.Text("Please enter the start date in DD/MM/YYYY format:"),
     sg.Input(key="start_date")],
    [sg.Text("Please enter the end date in DD/MM/YYYY format:"),
     sg.Input(key="end_date")],
    [sg.Exit(), sg.Button("Find"), sg.Button("Find 3 top performing stocks")],

]

window = sg.Window("Stock Market App", layout)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    if event == "Find":
        functions.display_max_min(
            values["stock_name"], values["start_date"], values["end_date"])
    if event == "Find 3 top performing stocks":
        functions.calc_top3(
            values["start_date"], values["end_date"])

# if __name__ == "__main__":

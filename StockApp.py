import PySimpleGUI as sg
import functions

# GUI Definition
layout = [
    [sg.Text("Welcome to the stock finder App", font=("Arial", 20))],
    [sg.Text("Note: There is only information from 20 years back till now.\n", font=(
        "Arial", 13))],
    [sg.Text("Please enter the stock symbol:"), sg.Input(key="stock_name")],
    [sg.Text("Please enter the start date in DD/MM/YYYY format:"),
     sg.Input(key="start_date")],
    [sg.Text("Please enter the end date in DD/MM/YYYY format:"),
     sg.Input(key="end_date")],
    [sg.Exit(button_color="tomato"), sg.Button("Find stock information"),
     sg.Button("Find 3 top performing stocks"), sg.Button("How it works")],

]

window = sg.Window("Stock Market App", layout)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    if event == "Find stock information":
        if (functions.is_valid_date(values["start_date"], values["end_date"])):
            functions.display_max_min(
                values["stock_name"], values["start_date"], values["end_date"])
    if event == "Find 3 top performing stocks":
        if (functions.is_valid_date(values["start_date"], values["end_date"])):
            functions.calc_top3(
                values["start_date"], values["end_date"])
    if event == "How it works":
        sg.Popup("Hi!\n\nTo find information about a specific stock.\nFill in all the information and click the 'Find stock information' button\n\nTo find the 3 best performing stocks within a time period.\nFill in the dates and click the 'Find 3 top perfoming stocks' button.\n\nTo Exit... click the exit button!", title="Help!")

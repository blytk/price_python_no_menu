import json
import re
import requests
import os
import sys


def main():
    # I check if the program is executed with an argument, in which case we will execute current_price() passing the first additional arg
    # This way the program can be quickly used to check current price and exit
    clear_terminal()
    if len(sys.argv) > 1:
        arg_token = sys.argv[1]
        check_current_price(arg_token)
        print()
        sys.exit()

    print_welcome()
    menu()
    return 0

# print_welcome() just prints a welcome message
def print_welcome():
    # clear_terminal()
    print()
    print("*" * 80)
    print("*     /$$$$$$$        /$$$$$$$        /$$$$$$        /$$$$$$        /$$$$$$$$  *")
    print("*    | $$__  $$      | $$__  $$      |_  $$_/       /$$__  $$      | $$_____/  *")
    print("*    | $$  \\ $$      | $$  \\ $$        | $$        | $$  \\__/      | $$        *")
    print("*    | $$$$$$$/      | $$$$$$$/        | $$        | $$            | $$$$$     *")
    print("*    | $$____/       | $$__  $$        | $$        | $$            | $$__/     *")
    print("*    | $$            | $$  \\ $$        | $$        | $$    $$      | $$        *")
    print("*    | $$            | $$  | $$        /$$$$$$     |  $$$$$$/      | $$$$$$$$  *")
    print("*    |__/            |__/  |__/       |______/       \\______/       |________/ *")
    print("*                                                                              *")
    print("*" * 80)

# print_menu() prints the menu with the available options to the screen
def print_menu():
    print_blank_space()
    print("1 - CHECK API STATUS")
    print("2 - DOWNLOAD LIST OF AVAILABLE TOKENS")
    print("3 - SEARCH TOKEN")
    print("4 - CHECK PRICE FROM PAST DATE")
    print("5 - CHECK CURRENT PRICE")
    print("6 - CHECK BTC PRICE")
    print("7 - EXIT")
    return 0

# menu() will take care of the flow and execute different functions for each of the menu options selected by the user
def menu():
    # while the user doesn't select 7 ("EXIT") or executes and EOF command (CONTROL + D), the program runs
    while True:
        print_menu()
        user_input = input("Enter a digit to choose an option: ")
        if user_input == "7":
            clear_terminal()
            return 0
        if user_input == "1":
            check_api_status()
        if user_input == "2":
            download_token_list()
        if user_input == "3":
            search_token()
        if user_input == "4":
            check_price_from_date()
        if user_input == "5":
            check_current_price()
        if user_input == "6":
            check_btc_price()


def check_api_status():
    clear_terminal()
    # We create a requests response object and send a get request to the ping api address
    response = requests.get("https://api.coingecko.com/api/v3/ping")
    # The response object will store an status code. We need to receive a status code 200 in order for the API to be working ok
    if response.status_code != 200:
        print(response.status_code)
        print_blank_space()
        print(f"THE API IS NOT WORKING PROPERLY, returned status code {response.status_code}")
        print_blank_space()
        return 1
    else:
        print_blank_space()
        print("THE API IS WORKING OK")
        print_blank_space()
        return 0


def download_token_list():
    clear_terminal()
    # create a file on the hard drive with a list of all available tokens
    response = requests.get("https://api.coingecko.com/api/v3/coins/list?include_platform=false")
    # I should receive a list of dictionaries, each one with the keys "id", "symbol", "name"
    # Can I unpack the content with json?
    # Yes, this is called deserialization, and it can be done with the method json.loads(<string_to_deserialize>)
    json_deserialized = json.loads(response.text)
    output_txt = ""
    # I create a new tokens.txt, empty (or overwrite an already existing one)
    file = open("tokens.txt", "w")
    file.write("")
    file.close()
    with open("tokens.txt", "a") as file:
        for element in json_deserialized:
            id = element["id"]
            symbol = element["symbol"]
            name = element["name"]
            output_string = f"ID: {id} | SYMBOL: {symbol} | NAME: {name}"
            # Now here I print each line into a .txt file
            file.write(output_string + "\n")
    print_blank_space()
    print("A file tokens.txt has been generated in the folder of the program with a list of all the tokens available")
    print_blank_space()
    return 0


def search_token():
    clear_terminal()
    # Get user input to search for a token in the downloaded list tokens.txt
    print_blank_space()
    user_input = input("Please, enter the name of the token you are looking in order to receive a list of possible matches: ")
    clear_terminal()
    token_matches = []
    try:
        with open("tokens.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if re.search(user_input, line, re.IGNORECASE):
                    # Now I need to capture the string after "ID:" and before "|"
                    id, symbol, name = line.split("|")
                    id = re.sub("ID:", "", id, re.IGNORECASE)
                    id = id.strip()
                    print(id)
        #print(token_matches)
        return 0
    except FileNotFoundError:
        print("You need to download the list of tokens first")
        print("The program will download it now")
        download_token_list()
        return 0


def check_price_from_date():
    clear_terminal()
    try:
        print()
        # Get token from user (the function checks that it exists too)
        user_token = get_user_token()
        # Get date from user (the function does an initial format check (does NOT guarantee results))
        user_date = get_user_date()
        # Check the price in the API using the token and date entered by the user
        url = f"https://api.coingecko.com/api/v3/coins/{user_token}/history?date={user_date}&localization=false"
        response = requests.get(url)
        if response.status_code != 200:
            print("Error contacting the API")
            return 1
        # response.json() will decode the json received and transform into a native Python structure (list, dict, etc)
        # This call raises an exception if JSON decoding fails
        data = response.json()
        # We have now a dictionary with tons of keys
        # We are interested in 'name' to print the name
        # data['name']
        # Display the price in usd / eur. Price has ton of decimals, round to 4.
        # data['market_data']['current_price']['usd']
        # data['market_data']['current_price']['eur']
        clear_terminal()
        print(f"The price of {data['name']} on the {user_date} was ${data['market_data']['current_price']['usd']:4f} / €{data['market_data']['current_price']['eur']:4f}")
        # The :4f might be an issue for tokens where the price has a lot of 0 on preceding the first non-zero decimal digits
        return 0
    except:
        return 1


def check_current_price(argument=None):
    clear_terminal()
    if argument != None:
        try:
            user_token = argument
        except:
            print("Invalid token")
            return 1
    else:
        user_token = get_user_token()
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={user_token}&vs_currencies=usd%2Ceur"
        response = requests.get(url)
        if response.status_code != 200:
            print("Error contacting the API")
            return 1
        data = response.json()
        print()
        print(f"The current price of {user_token.capitalize()} is ${data[user_token]['usd']:4f} / €{data[user_token]['eur']:4f}")
        return 0
    except:
        print("Error")
        return 1


def check_btc_price():
    clear_terminal()
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd%2Ceur"
        response = requests.get(url)
        if response.status_code != 200:
            print("Error contacting the API")
            return 1
        data = response.json()
        print()
        print(f"The current price of Bitcoin is ${data['bitcoin']['usd']} / €{data['bitcoin']['eur']}")
        return 0
    except:
        print("Error")
        return 1


def print_blank_space():
    print("\n\n")


def get_user_token():
    clear_terminal()
    try:
        file = open("tokens.txt", "r")
    # If tokens.txt hasn't been generated yet, generate it
    except FileNotFoundError:
        print("It's necessary to generate a file with all the available tokens before using this functionality")
        print("The program will generate it for you now")
        download_token_list()
        file = open("tokens.txt", "r")
    # Now the file should exist even if the user didn't execute the function, and be open
    # Get token from user

    # Check that the token is correct against tokens.txt
    # Check whether the token exists or not
    lines = file.readlines()
    while True:
        break_while = False
        user_token = input("Enter the exact name of the token: ")
        # I add spaces on the sides so re.search will only find
        # exact matches. I feel there must be a better way but this
        # seems to work
        user_token = " " + user_token + " "
        for line in lines:
            # Split each line as we only interested in the id for searching through the API
            id, symbol, name = line.split("|")
            match = re.search(user_token, id, re.IGNORECASE)
            if match:
                # If there is a match, we break the while loop
                # Otherwise it will keep prompting until a match is found
                break_while = True
                break
        if break_while == True:
            break
        else:
            clear_terminal()
            print("No token has been found with that name")
    # I added spaces before to the string to isolate the name, I need to remove them now (.strip())
    return user_token.strip().lower()



    # If no token is found, user should be able to try again:
    return 1


def get_user_date():
    clear_terminal()
    while True:
        user_date = input("Enter the date in dd-mm-yyyy format to check the price of the token: ")
        matches = re.search(r"^(\d\d)-(\d\d)-(\d\d\d\d)$", user_date)
        if matches:
            try:
                day = int(matches.group(1))
                month = int(matches.group(2))
                year = int(matches.group(3))
                if day < 0 or day > 31:
                    clear_terminal()
                    print("Invalid day")
                    raise ValueError
                if month < 0 or month > 12:
                    clear_terminal()
                    print("Invalid month")
                    raise ValueError
                if year < 2000:
                    clear_terminal()
                    print("Invalid year")
                    raise ValueError
                break
            # If there are issues unpacking I should get a ValueError
            except ValueError:
                clear_terminal()
                print("Incorrect Format")
    # If we reach this point, we passed the first input control
    # and we have a user_date that is in correct format
    # (not necessarily valid for the token we are looking for)
    return user_date


def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


if __name__ == "__main__":
    main()
# price_python

#### Video Demo: https://youtu.be/tLGeTXB8LFU

#### Description:

Display the current or from a specific date price of different cryptocurrencies.

Working thanks to the coingecko API: www.coingecko.com.

##### REQUIREMENTS:
A Linux operating system, an internet connection, Python, and the installation of the module requests.

##### MODULES USED:

* The communication with the API is handled using the requests module: https://pypi.org/project/requests/
* The json module will be used to manipulate the data received from the API server: https://docs.python.org/3/library/json.html
* Some function from the re module are used for string pattern detection and manipulation: https://docs.python.org/3/library/re.html
* The os module is only used to detect the operating system where the application is running: https://docs.python.org/3/library/os.html
* The sys module will be used to detect if additional arguments are passed when executing the program, and if so, act accordingly
* pytest will be used to run some tests

##### HOW IT WORKS:

-The main way of using the program will be to execute the program without any argument from a terminal command line, executing the command: python project.py

Once the program is executed, a menu will be displayed with 7 different options. We need to enter a digit and press enter:

    * 1: The program will check if communication with the API is working adequately when executed.
    * 2: Option number two will create a file tokens.txt inside the program's directory. tokens.txt includes a list with all the available tokens.
    in the API.
    * 3: Option number three will allow us to find the exact name of a token, displaying in the terminal possible matches for a query substring. This is important as the program needs the exact API name for each token, otherwise it won't be able to fetch the price (options 4 and 5). It will use the list from tokens.txt in order to help us find our token. In case option number 2 has not been executed, the program will automatically generate tokens.txt (so it's not necessary to manually execute option number two before this one).
    * 4: Prompt the user for a token name and a date. The program will check, using tokens.txt, whether the token exists in the API or not, and it will keep prompting the user until a valid token name is entered (case insensitive). Once a valid token is recognized, we need to enter the date we are interested in, to check the price of the token at such date. If an obviously wrong date is entered, the program will keep prompting (it performs a basic check, so the day is not 0 or higher than 31, the month is not 0 or higher than 12 and the year is 2000 or later; this does not guarantee a price return, as we are still able to request price from a day that does not exist for that month, like the 31 of February(in this case we will receive an API error and we will be back at option selection.))

    * 5: Prompt the user for a token, operating in the same way as option number four, and display the current price of such token.

    * 6: Shortcut for the current price of Bitcoin.

    * 7: Exit the program


- Another way of executing the program, if we are familiar with the token we need, is to add the name of the token as an argument. So: python project.py name_of_the_token. This will simply display the current price of the token (as long as the API is operating properly) and return to the terminal.

##### COMMENTS:

I have considered using a library like curses or urwid in order to create a better user experience, but I like how it works already, so I have decided to not waste more time (from past experience, I would have probably spent a week or two polishing everything, and the end result would not be necessarily more practical or functional, just a bit nicer with some colors and a couple of unnecessary visuals).

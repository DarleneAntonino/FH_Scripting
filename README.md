# QuoteChecker

## About
### Authors/Contributors
* [Darlene Antonino](mailto:darlene.antonino@edu.fh-joanneum.at)
* [Viola Schlocker](mailto:viola.schlocker@edu.fh-joanneum.at)

### Description
> We are planning to read an inputfile and compare it to a database of quotes. If the inputfile matches one of the quotes, you will recive an email with this quote to an email address of your choice.


This "project" contains/will implement/focus on:
* Access to Files
* Access to Database (if we build it our own)
* Regex
* External Data Sources (if we use an already existing database)
* Notifications

We created a program you can either read a file into or give it a single keyword/-phrase. Depending on your input it will show you several quotes which you can either view in the terminal or get send per email. The quotes will be saved into a database which will be created on start of the program IF it is not existing jet.

Quotes were taken from: www.quotes.net, www.goodreads.com, screenrant.com, www.rottentomatoes.com
contains no quotes of Donald Trump and J. K. Rowling


## Installation/Prerequisites for your repository

First of all, you want to install Python 3. Click the following Link (https://www.python.org/downloads/) and follow the instructions. 
To be able to connect to the database first run ‘python -m pip install mysql-connector-python’ in your Terminal. It might will ask you to upgrade/update (at least on windows). Just run the provided command.
Also make sure to run XAMPP and start Apache and MySQL! Otherwise you won’t be able to connect to the database.
It is also recommended to prepare a text file in the directory you store the script in. The content of this yourFilename.txt can be chosen freely by you. Nonetheless you want to either enter the name of an author, actor, politician,… or a keyword or even a whole quote. Remember you can enter multiple values, but you must use a new line for every value. We included an example file in the project.

Possible file content:
Pum
Einstein
Groovy
Music
I have

If you do not want to use a file, you can enter one keyword (or phrase) and will have the same result.


## Run/Execute

To run the program, you can either double-click on the file or run it in your terminal. When on Windows just write ‘quotechecker.py’, on iOS ‘python quotechecker.py’.
After the greeting, you can choose to read a file or enter a word/phrase on the terminal.
If you choose the file, you will be asked to enter the path to your file.txt. If the file is located in the same directory as the script it is enough to only write the name of the file. Remember not to forget the postfix ‘.txt’.
The content of your file will be read and compared to our database. The same happens with your input in the terminal. You will get a noise notification when it has finished. If there are no matches, you will be informed immediately, and the program will end. If there are matches you will be asked if you want to get them per email or shown in the terminal. After you decided the program is finished and you will be asked if you want to go again or not.


### Custom Configuration

As mentioned before, you can choose a file to read. You do not have to take our prepared file but if you create one yourself, be sure to make it a .txt file and remember where you saved it because you might have to type the whole path when asked for it.


## Documentation
> WIP

## Known Issues

If you use this program multiple times in a short amount of time and send an email every time, it can be put into your SPAM directory. If you “do not get an email” take a look into your SPAM directory. Normally it is enough to declare it as NO SPAM once.


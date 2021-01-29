#!/usr/bin/env python3
## test.py

#imports for E-Mail
from smtplib import SMTP
from email.message import EmailMessage
#imports for regex
import re
#import for sound notification
import winsound
#import for db
import mysql.connector


# ----- FUNCTIONS -----

#get the pw for sending the email
def getSenderPW():
	cursor = connection.cursor()
	cursor.execute("SELECT pw FROM e_mail_data WHERE email='quote.checker@gmx.at'")
	pw = cursor.fetchall()

	password = str(pw[0])

	return password[2:18]


#creates the E-Mail content dependig on the input
def getEmailMSG(liste):
	output = ""

	for x in range(len(liste)):
		toConvert = str(liste[x])
		s = convertString(toConvert)
		output += s + "\n"

	return output


#gets the users E-Mail; REGEX
def getEmailRecipient():
	regexEmail = (r'^[A-Za-z0-9]+[\._-]?[A-Za-z0-9]+[@].+[\.]\w{2,3}$')
	emailRec = input("Please enter your email: ")

	while True:
		if(re.search(regexEmail,emailRec)):
			print("Thank you! You will recive your E-Mail shorty.\n")
			break
		else:
			print("Invalid Email! Please try again!\n")
			emailRec = input("Please enter your email: ")

	return emailRec


#connects to the Email Server and sends an E-Mail to the user
def sendEmail(liste):
	SENDER = 'quote.checker@gmx.at'
	RECIPIENT = getEmailRecipient()
	SMTP_USER = SENDER

	SMTP_PASS = getSenderPW()

	SMPT_HOST = 'mail.gmx.net'
	SMTP_PORT = 587
	msg = EmailMessage()
	msg.set_content("Dear QuoteChecker-User,\n\n\n" + getEmailMSG(liste) + "\n\nThank you for using our Service.\n\nKind regards,\nQuoteChecker")
	msg['Subject'] = 'QuoteChecker has your quote'
	msg['From'] = SENDER
	msg['To'] = RECIPIENT

	try:
	    with SMTP(host=SMPT_HOST, port=SMTP_PORT) as smtp:
	        smtp.starttls()
	        smtp.login(SMTP_USER, SMTP_PASS)
	        smtp.send_message(msg)
	except Exception as e:
	    print('Something went wrong')
	    print(e)
	    exit(1)

	return


#asks for filename; will return content of the file in form of list (one field per line)
def getFileContent():
	lines = []

	while True:
		try:
			fileName = getFileName()
			file = open(fileName, 'r')
			break
		except Exception as e:
			print(e)
			print("Sorry! Something went wrong. Please check your path.\n")

	content = ""
	for line in file:
		content = line
		lines.append(content)

	file.close()

	return lines


#gets the Filename; REGEX
def getFileName():
	regexFile = (r'(^(?:\\|\/).+(?:\\|/).+\.txt)|.+\.txt')
	name = input("Please enter the path to your text file: ")

	while True:
		if(re.search(regexFile,name)):
			print("Thank you! We will now try to read the Content of your File.\n")
			break
		else:
			print("Invalid path! Please try again!\n")
			name = input("Please enter the path to your file: ")
	return name


#will compare the cotent of the file with our Database (Quote)
def compareWithDBQuote(inpu):
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM quotes WHERE (quote_text LIKE '%"+inpu+"%' OR author LIKE '%"+inpu+"%')")
	quotes = cursor.fetchall()
	
	return quotes


#make a sound
def sound():
	duration = 1000
	freq = 300
	winsound.Beep(freq, duration)
	return


#formats the String in a more beautiful way for the email output
def convertString(s):
	end = 0
	start = 10000000
	endA = 0
	startA = 1000000
	for x in range(len(s)):
		if (s[x] == "'" or s[x] == "\"") and x > start:
			end = x + 1
			break
		elif (s[x] == "'" or s[x] == "\"") and end == 0:
			start = x

	for y in range(end, len(s)):
		if (s[y] == "'" or s[y] == "\"") and y > startA:
			endA = y
			break
		elif (s[y] == "'" or s[y] == "\"") and endA == 0:
			startA = y

	quoteText = s[start:end]
	authorText = s[startA+1:endA]

	return quoteText + " - " + authorText + "\n"


#mainly to keep the main tidy
def choseTerminal(foundQuotes):
	terminalInput = input("You choose the terminal. Please enter your keyword now: ")
	print("Thank you, you will hear a noise-notification when we are done.")
	foundQuotes = compareWithDBQuote(terminalInput)

	return foundQuotes


#mainly to keep the main tidy
def choseFile(foundQuotes):
	print("You chose to read a file.\n")
	fileContent = getFileContent()
	print("Thank you, you will hear a noise-notification when we are done.")

	for x in range(len(fileContent)):
		compareToThis = str(fileContent[x])
		inter = compareWithDBQuote(compareToThis.strip(" \n"))
		foundQuotes.extend(inter)

	return foundQuotes



# ----- MAIN -----
try:
	connection = mysql.connector.connect(host = "localhost", user = "ro_user", passwd = "RsycY3f1zIWn18MP", db = "quote_checker")
except:
	print ("Keine Verbindung zum Server")
	exit(0)

again = True
fileContent = []
foundQuotes = []
msg = "Dear QuoteChecker-User,\n\nWe are sorry to tell you, that our programm could not find any quotes or authors matching your text.\nWe hope to see you again soon!\n\nRegards,\nQuoteChecker"

print("Welcome to QuoteChecker!\n")
while again:
	print("Would you like to read a file to enter multiple keywords(f) or enter one word manually in this terminal (t)?")

	while True:
		inpuBoo = input("file or terminal? (f/t): ")
		if inpuBoo == "F" or inpuBoo == "f":
			foundQuotes = choseFile(foundQuotes)
			sound()
			if type(foundQuotes) != list:
				print(msg)
				exit(0)
			break
		elif inpuBoo == "T" or inpuBoo == "t":
			foundQuotes = choseTerminal(foundQuotes)
			sound()
			if len(foundQuotes) == 0:
				print(msg)
				exit(0)
			break
		else:
			print("Please only type 'f' or 't'!\n")

	print("Would you like to get an E-Mail (e) with the findings or display them in the terminal(t)?")
	while True:
		sendBoo = input("Email or terminal? (e/t): ")
		if sendBoo == "e" or sendBoo == "E":
			sendEmail(foundQuotes)
			break
		elif sendBoo == "t" or sendBoo == "T":
			print(getEmailMSG(foundQuotes))
			break
		else:
			print("Please only type 'e' or 't'!\n")

	while True:
		sendBoo = input("Would you like to search for more? (y/n): ")
		if sendBoo == "y" or sendBoo == "Y":
			break
		elif sendBoo == "n" or sendBoo == "N":
			again = False
			break
		else:
			print("Please only type 'y' or 'n'!\n")	


print("We hope to see you again soon!")
connection.close()

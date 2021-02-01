#!/usr/bin/env python3
## test.py

#imports for E-Mail
from smtplib import SMTP
from email.message import EmailMessage
#imports for regex
import re
#import for db
import mysql.connector
#import for os recognicion
import platform


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
		content = line.replace("'", "")
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
	quotes = ""
	if inpu != "":
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


#to avoid SQL-Injections; REGEX
def getValidInput():
	validInput = (r'^[A-Za-z, ]')
	usersInput = input("You chose the terminal. Please enter your keyword now: ")

	while True:
		if(re.search(validInput,usersInput)):
			print("Thank you, you will hear a noise-notification when we are done.\n")
			break
		else:
			print("Invalid keyword! Please only use letters and commas!\n")
			usersInput = input("Please enter your keyword now: ")

	return usersInput


#mainly to keep the main tidy
def choseTerminal(foundQuotes):
	terminalInput = getValidInput()
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

	outer = len(foundQuotes)
	inner = len(foundQuotes)
	y = 0
	z = 0
	for k in range(100):
		for y in range(outer):
			if y < outer-1:
				for z in range(inner):
					if z < inner-1:					
						if (str(foundQuotes[y]) == str(foundQuotes[z])) and (z != y):
							del foundQuotes[z]
							
						outer = len(foundQuotes)
						inner = len(foundQuotes)

	return foundQuotes


#to create database
def dbSetup():
	try:
		connection = mysql.connector.connect(host = "localhost", user = "root", passwd = "")
		cursor = connection.cursor()
	except:
		print ("Keine Verbindung zum Server")
		exit(0)

	cursor.execute("CREATE DATABASE IF NOT EXISTS quote_checker;")
	cursor.execute("USE quote_checker;")
	cursor.execute("CREATE TABLE IF NOT EXISTS e_mail_data (email varchar(255), pw varchar(255) DEFAULT 'not needed');")
	cursor.execute("CREATE TABLE IF NOT EXISTS quotes (quote_count int(11) PRIMARY KEY, quote_text varchar(3072), author varchar(255));")
	
	#seed quotes
	valuesDB = []
	while True:
		try:
			file = open("src/quote_checker.sql", 'r')
			break
		except Exception as e:
			print(e)
			print("Sorry! Something went wrong. Please check if all your files are still in one directory and restart.\n")
			exit(0)

	for line in file:
		valuesDB.append(line)

	file.close()
	for x in valuesDB:
		cursor.execute("SELECT MAX(quote_count) FROM quotes;")
		count = str(cursor.fetchone()).replace(",", "")
		count = count.replace("(", "")
		count = count.replace(")", "")
		if count == "None":
			count = 0
		if int(count) < 100:
			cursor.execute("INSERT INTO quotes(quote_count, quote_text, author) VALUES " + x + " ;")
	
	#seed email
	while True:
		try:
			file = open("src/e_mail_data.sql", 'r')
			break
		except Exception as e:
			print(e)
			print("Sorry! Something went wrong. Please check if all your files are still in one directory and restart.\n")
			exit(0)
	
	for y in file:
		cursor.execute("SELECT pw FROM e_mail_data;")
		pwTest = str(cursor.fetchone()).replace(",", "")
		pwTest = pwTest.replace("(", "")
		pwTest = pwTest.replace(")", "")
		if pwTest == "None":
			pwTest = "0"
		if pwTest == "0":
			cursor.execute("INSERT INTO e_mail_data(email, pw) VALUES " + y + " ;")
	file.close()
	
	cursor.execute("CREATE USER IF NOT EXISTS 'ro_user' IDENTIFIED BY 'RsycY3f1zIWn18MP';")
	connection.close()

	return

# ----- MAIN -----
dbSetup()

try:
	connection = mysql.connector.connect(host = "localhost", user = "ro_user", passwd = "RsycY3f1zIWn18MP", db = "quote_checker")
except:
	print ("Keine Verbindung zum Server")
	exit(0)

again = True
msg = "\n\nWe are sorry to tell you, that our programm could not find any quotes or authors matching your text.\n\n"

print("Welcome to QuoteChecker!\n")
while again:
	fileContent = []
	foundQuotes = []
	booFound = True
	print("Would you like to read a file to enter multiple keywords(f) or enter one word manually in this terminal (t)?")

	while True:
		inpuBoo = input("file or terminal? (f/t): ")
		if inpuBoo == "F" or inpuBoo == "f":
			foundQuotes = choseFile(foundQuotes)
			if type(foundQuotes) != list:
				print(msg)
				booFound = False
			break
		elif inpuBoo == "T" or inpuBoo == "t":
			foundQuotes = choseTerminal(foundQuotes)
			if len(foundQuotes) == 0:
				print(msg)
				booFound = False
			break
		else:
			print("Please only type 'f' or 't'!\n")

	if platform.system() == "Windows":
		#import for sound on Windows
		import winsound
		sound()
	elif platform.system() == "Linux":
		#import for sound on Linux
		import os
		os.system('spd-say "Done"')
	else:
		#import for sound on iOS
		import os
		os.system('say "Done"')

	if booFound:
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

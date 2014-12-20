from Tkinter import *
from tkFileDialog import askopenfilename, askdirectory
from tkMessageBox import askyesno, showerror, showinfo

import pymssql, _mssql, decimal, uuid, pkg_resources, os, re, sys, inspect, fnmatch, win32com.client
import __main__ as main


userID = ''
String = ''
myFolder = ''
total = 0
checkBox = 0

def select_folder():
	global String
	global userID
	global myFolder
	global total
	global checkBox

	print(main.CheckVar1.get())

	String = ''
	myFolder = ''
	total = 0
	checkBox = main.CheckVar1.get()
	directory = askdirectory(title='Select folder to read')

	main.label_response.pack_forget()
	main.label_progress_folder.pack_forget()
	main.label_progress_file.pack_forget()

	if directory != '' :
		myFolder = unicode(directory).encode("utf-8")
		String = 'FOLDER: %s \n------------------------------------------------- REPORT -------------------------------------------------\n' %myFolder
		disabled_btn()
		show_response({'label_text' : "Processing...", 'label_background' : "#ffba00"})

		if checkBox == 0:
			folder_reader(directory)
		else:
			directorySplit = unicode(directory).encode("utf-8").split('/')
			userID = '%s' %directorySplit[len(directorySplit)-1].split('_')[0]
			subfolder_reader(directory)

	else:
		show_response({'label_text' : "Please select a folde", 'label_background' : "#006B6B"})

def folder_reader(directory):
	global userID
	global String
	try:
		subDir = os.listdir(directory)

		for i in range(len(subDir)):
			userID = '%s' %unicode(subDir[i]).encode("utf-8").split('_')[0]
			show_progress_folder({'label_text' : "%d/%d - %s" %((i+1), len(subDir), userID), 'label_background' : "#ffffff"}, False)

			if os.path.isdir(os.path.join(directory,subDir[i])):
				String += '------------------------------------------- Customer ID = %s -------------------------------------------\nSubFolder : %s \n' %(userID, unicode(subDir[i]).encode("utf-8"))
				subfolder_reader(os.path.join(directory,subDir[i]))

		show_response({'label_text' : "Successfully exported", 'label_background' : "#03db09"}, True)
	except:
		show_response({'label_text' : "Error in folder_reader", 'label_background' : "#db0303"}, True, True)
				
def subfolder_reader(directory):
	global userID
	global String
	global total
	global checkBox

	try:
		matches = []
		for root, dirnames, filenames in os.walk(directory):
			for filename in fnmatch.filter(filenames, '*.*'):
				filenameSplit = filename.split('.')
				if filenameSplit[len(filenameSplit)-1] != 'db' and filenameSplit[len(filenameSplit)-1] != 'doc' and filenameSplit[len(filenameSplit)-1] != 'docx':
					matches.append(os.path.join(root, filename))

		for i in range(len(matches)):
			splitURL = unicode(matches[i]).encode("utf-8").split('\\')
			name = '%s' %splitURL[len(splitURL)-1]
			show_progress_file({'label_text' : "%d/%d - %s" %((i+1),len(matches),name), 'label_background' : "#ffffff"},False)
			String += '%d) File Name = %s \n--Local Path = %s \n' %(i+1, name,unicode(matches[i]).encode("utf-8"))
			print(sql)
			total += 1


		if checkBox == 1:
			show_response({'label_text' : "Successfully Single Folder exported", 'label_background' : "#03db09"}, True)

		String += '---------------------------------TOTAL FILE IN SUBFOLDER = %d ---------------------------------\n\n' %len(matches)
	except:
		error = '%s - %s' %('Error in subfolder ' , userID)

		if checkBox == 0:
			show_response({'label_text' : error, 'label_background' : "#db0303"}, False, True)
		else:
			show_response({'label_text' : error, 'label_background' : "#db0303"}, True, True)	
	
def show_response(args, activate=False, error=False):
	global String
	global myFolder
	global total

	main.label_response.config( text=args['label_text'], width = 100, foreground="#fcfcfc", background=args['label_background'])
	main.label_response.pack( side ='top')

	Tk.update(main.root)

	if error == True:
		String += "%s \n" %args['label_text']
		String += "TOTAL FILE PROCESSED BEFORE THIS ERROR = %d \n\n" %(total)
	else :
		String += "TOTAL FILE PROCESSED IN FOLDER %s = %d \n" %(myFolder,total)

	if activate == True:
		activate_btn()
		folderNameSplit = myFolder.split('/')
		reportName = 'Report_%s.txt' %folderNameSplit[len(folderNameSplit)-1]
		text_file = open(reportName, "w")
		text_file.write(String)
		text_file.close()
	
def show_progress_folder(args, activate=False):
	main.label_progress_folder.config( text=args['label_text'], width = 100, foreground="#cccccc", background=args['label_background'])
	main.label_progress_folder.pack( side ='top')

	Tk.update(main.root)
	
def show_progress_file(args, activate=False):
	main.label_progress_file.config( text=args['label_text'], width = 100, foreground="#cccccc", background=args['label_background'])
	main.label_progress_file.pack( side ='top')

	Tk.update(main.root)

def activate_btn():
	main.exit_btn.config(state='normal')
	main.select_btn.config(state='normal')

def disabled_btn():
	main.exit_btn.config(state='disabled')
	main.select_btn.config(state='disabled')

def exit():
	sys.exit(0)
from Tkinter import *
from os.path import abspath, basename, join
from PIL import Image, ImageTk

import appCore as Core
import sys
import os

def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)

def center(win):
	win.update_idletasks()
	width = win.winfo_width()
	height = win.winfo_height()
	x = win.winfo_screenwidth() // 2 - width // 2
	y = win.winfo_screenheight() // 2 - height // 2
	win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

class SplashScreen(Toplevel):
	def __init__(self, master, image=None, timeout=1000):
		Toplevel.__init__(self, master, relief='ridge', borderwidth=2)
		self.main = master
		self.main.withdraw()
		self.overrideredirect(1)
		im = Image.open(image)
		self.image = ImageTk.PhotoImage(im)
		self.after_idle(self.centerOnScreen)
		self.update()
		self.after(timeout, self.destroy)
	def centerOnScreen(self):
		self.update_idletasks()
		width, height = self.width, self.height = \
						self.image.width(), self.image.height()
		xmax = self.winfo_screenwidth()
		ymax = self.winfo_screenheight()
		x0 = self.x0 = xmax // 2 - width//2
		y0 = self.y0 = ymax // 2 - height//2
		self.geometry('{}x{}+{}+{}'.format(width, height, x0, y0))
		self.createWidgets()
	def createWidgets(self):
		self.canvas = Canvas(self, width=self.width, height=self.height)
		self.canvas.create_image(0,0, anchor=NW, image=self.image)
		self.canvas.pack()
	def destroy(self):
		self.main.update()
		self.main.deiconify()
		self.withdraw()

if __name__ == "__main__":
	icon = resource_path('data/img/icon.ico')
	log = resource_path('data/img/logo.gif')
	splash =  resource_path('data/img/logo.jpg')

	root = Tk()
	rtitle = root.title("Folder Reader")

	root.minsize(600,270)
	root.maxsize(600,270)
	root.configure(background='#fff')
	root.iconbitmap(default=icon)

	label = Label(root, text="Folder Reader",  font="Helvetica 20 bold ", background='#006B6B', foreground="#fff")
	label.config( width = 100)
	label.pack( side ='top')

	img_logo = PhotoImage(file=log)
	logo = Label(root, background='#fff', image=img_logo)
	logo.config( width = 1000, height=50)
	logo.pack( side ='top')

	global CheckVar1
	CheckVar1 = IntVar()
	check_box = Checkbutton(root, text = "Single Folder", variable = CheckVar1, onvalue = 1, offvalue = 0, height=1, width = 15, background='#fff')
	check_box.pack(side ='top')

	label_response = Label(root, font="Helvetica 15 bold", text="Please select a folder", background='#006B6B', foreground="#fff")
	label_response.config( width = 100)
	label_response.pack( side ='top')
	label_progress_folder = Label(root, font="Helvetica 10 bold")
	label_progress_file = Label(root, font="Helvetica 10 bold")

	label_copyright = Label(root, font="Helvetica 5", text='Copyright 2014 Marco Somma', foreground="#fff", background='#333',  width = 200, height = 1 )
	label_copyright.pack(side ='bottom', pady=1)

	botton_lable = Label(root, background='#006B6B')
	botton_lable.config( width = 100)
	botton_lable.pack( side ='bottom', fill='both',)

	exit_btn = Button(botton_lable, text="Exit", font="Helvetica 10 bold", background='#fff', foreground="#333", cursor="hand2", command=Core.exit)
	exit_btn.config( height = 1, width = 30, overrelief='sunken')
	exit_btn.pack(side=RIGHT, fill='both', expand=False, padx=35, pady=10)

	select_btn = Button(botton_lable, text="Select", font="Helvetica 10 bold", background='#fff', foreground="#333", cursor="hand2", command=Core.select_folder)
	select_btn.config( height = 1, width = 30, overrelief='sunken')
	select_btn.pack(side=LEFT, fill='both', expand=False, padx=35, pady=10)	

	assert splash
	s = SplashScreen(root, timeout=1000, image=splash)
	center(root)
	root.mainloop()
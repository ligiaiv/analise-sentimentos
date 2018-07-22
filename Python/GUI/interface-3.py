from tkinter import *
# import tkFileDialog
from tkinter import filedialog

from tkinter import ttk
from tkinter.filedialog import askopenfilename
from sentiment_analizer import *

TEXT_FILE = ''
WEIGHT_FILE = ''
OUT_FILE = ''
LANGUAGE = ''
EXPORT = ''

def ask_textFile():
	global TEXT_FILE
	TEXT_FILE = askopenfilename()
	textFile_label.config(text = TEXT_FILE)

def ask_weightFile():
	global WEIGHT_FILE

	WEIGHT_FILE = askopenfilename()
	weightFile_label.config(text = WEIGHT_FILE)

def ask_outFile():
	global OUT_FILE
	OUT_FILE = filedialog.asksaveasfilename()
	outFile_label.config(text = OUT_FILE)

def calcular(TEXT_FILE,WEIGHT_FILE,OUT_FILE,export_format,language):
	print(export_format)
	process(TEXT_FILE,WEIGHT_FILE,OUT_FILE,export_format,language)
def setFrame(x,y,frame):
	for i in range(0,y-1):
		frame.rowconfigure(i, weight=1)
	for i in range(0,x-1):
   		frame.columnconfigure(i,weight=1)
mainframe = Tk()
mainframe.title("Ainda to Decidindo")
mainframe.geometry("500x500") #You want the size of the app to be 500x500
setFrame(5,10,mainframe)
# root.resizable(0, 0)
# mainframe = Frame(root)
# mainframe.grid(column = 0, row = 0, sticky = (N,W,E,S))

# mainframe.columnconfigure(0,weight = 1)
# var = StringVar()
# # LOGO = PhotoImage(file = "BigFiles/teste2.png")
# # LOGO.zoom(50,50 )
LANGUAGE = StringVar()
EXPORT = StringVar()

titleLabel = Label(mainframe,text="Ainda não Decidi",font = ('times', 20, 'bold'))
titleLabel.grid(row = 0,column=0)

textFile_button = Button(mainframe,text="Arquivo de texto",command= ask_textFile)
textFile_label = Label(mainframe,width = 30,background = "white",relief = SUNKEN)
textFile_button.grid(row = 1,column = 0)
textFile_label.grid(row = 1,column = 2)
weightFile_button = Button(mainframe,text="Arquivo com pesos",command= ask_weightFile)
weightFile_label = Label(mainframe,width = 30,background = "white",relief = SUNKEN)
weightFile_button.grid(row = 2,column = 0)
weightFile_label.grid(row = 2,column = 2)

outFile_button = Button(mainframe,text="Arquivo de Saída",command= ask_outFile)
outFile_label = Label(mainframe,width = 30,background = "white",relief = SUNKEN)
outFile_button.grid(row = 3,column = 0)
outFile_label.grid(row = 3,column = 2)

# calc_button = Button(mainframe,text="Calcular",command= methodcaller("calcular",TEXT_FILE,WEIGHT_FILE,OUT_FILE,EXPORT,LANGUAGE))
calc_button = Button(mainframe,text="Calcular",command= lambda: calcular(TEXT_FILE,WEIGHT_FILE,OUT_FILE,EXPORT.get(),LANGUAGE.get()))


calc_label = Label(mainframe,width = 30,background = "white",relief = SUNKEN)
calc_button.grid(row = 7,column = 0)
calc_label.grid(row = 7,column = 2)


ET1 = Radiobutton(mainframe, text="EXCEL", variable=EXPORT, value="EXCEL")
ET2 = Radiobutton(mainframe, text="CSV", variable=EXPORT, value="CSV")
ET1.grid(row = 4,column = 0)
ET2.grid(row = 4,column = 1)

# language = StringVar()
# export = StringVar()
Lport = Radiobutton(mainframe, text="Português", variable=LANGUAGE, value="portuguese")
Leng = Radiobutton(mainframe, text="Inglês", variable=LANGUAGE, value="english")
Lport.grid(row = 5,column = 0)
Leng.grid(row = 5,column = 1)

mainframe.mainloop()
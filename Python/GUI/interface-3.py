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
TITLE = '  Análise de Sentimentos - Processamento'
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
	result = process(TEXT_FILE,WEIGHT_FILE,OUT_FILE,export_format,language)
	if(result == 'OK'):
		calc_label.config(text = "Processo Concluído.")
def setFrame(x,y,frame):
	for i in range(0,y-1):
		frame.rowconfigure(i, weight=1)
	for i in range(0,x-1):
   		frame.columnconfigure(i,weight=1)
mainframe = Tk()
mainframe.title(TITLE)
mainframe.geometry("500x500") #You want the size of the app to be 500x500
# setFrame(10,10,mainframe)

for i in range(0,9):
	mainframe.rowconfigure(i, weight=1)
for i in range(0,5):
	mainframe.columnconfigure(i,weight=0)

mainframe.iconbitmap('@BigFiles/logo.XBM')
# root.resizable(0, 0)
# mainframe = Frame(root)
# mainframe.grid(column = 0, row = 0, sticky = (N,W,E,S))

# mainframe.columnconfigure(0,weight = 1)
# var = StringVar()
# LOGO = PhotoImage(file = "BigFiles/logo.png")
# # LOGO.zoom(50,50 )
LANGUAGE = StringVar()
EXPORT = StringVar()

titleLabel = Label(mainframe,text=TITLE,font = ('times', 20, 'bold'))
titleLabel.grid(row = 0,column=0,columnspan = 5)

textFile_button = Button(mainframe,text="Arquivo de texto",command= ask_textFile,width = 18)
textFile_label = Label(mainframe,width = 30,background = "white",relief = SUNKEN)
textFile_button.grid(row = 1,column = 0)
textFile_label.grid(row = 1,column = 2,columnspan = 3)
weightFile_button = Button(mainframe,text="Arquivo com pesos",command= ask_weightFile,width = 18)
weightFile_label = Label(mainframe,width = 30,background = "white",relief = SUNKEN)
weightFile_button.grid(row = 2,column = 0)
weightFile_label.grid(row = 2,column = 2,columnspan = 3)

outFile_button = Button(mainframe,text="Arquivo de Saída",command= ask_outFile,width = 18)
outFile_label = Label(mainframe,width = 30,background = "white",relief = SUNKEN)
outFile_button.grid(row = 3,column = 0)
outFile_label.grid(row = 3,column = 2,columnspan = 3)

# calc_button = Button(mainframe,text="Calcular",command= methodcaller("calcular",TEXT_FILE,WEIGHT_FILE,OUT_FILE,EXPORT,LANGUAGE))
calc_button = Button(mainframe,text="Calcular",command= lambda: calcular(TEXT_FILE,WEIGHT_FILE,OUT_FILE,EXPORT.get(),LANGUAGE.get()))


calc_label = Label(mainframe,width = 30,background = "white",relief = SUNKEN)
calc_button.grid(row = 7,column = 0)
calc_label.grid(row = 7,column = 2,columnspan = 3)

exportLabel = Label(mainframe,text="Tipo do arquivo de saída: ",width = 25)
exportLabel.grid(row = 4,column=0,columnspan = 2)

ET1 = Radiobutton(mainframe, text="EXCEL", variable=EXPORT, value="EXCEL")
ET2 = Radiobutton(mainframe, text="CSV", variable=EXPORT, value="CSV")
ET1.grid(row = 4,column = 2,sticky=W)
ET2.grid(row = 4,column = 3,sticky=W)
ET1.select()


# language = StringVar()
# export = StringVar()
languageLabel = Label(mainframe,text="Linguagem do DataSet: ",width = 25)
languageLabel.grid(row = 5,column=0,columnspan = 2)
Lport = Radiobutton(mainframe, text="Português", variable=LANGUAGE, value="portuguese")
Leng = Radiobutton(mainframe, text="Inglês", variable=LANGUAGE, value="english")
Lport.grid(row = 5,column = 2,sticky=W)
Leng.grid(row = 5,column = 3,sticky=W)
Lport.select()

mainframe.mainloop()
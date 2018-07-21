from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename


TEXT_FILE = ''
WEIGTH_FILE = ''
def ask_textFile():
	TEXT_FILE = askopenfilename()
	textFile_label.config(text = TEXT_FILE)
def ask_weightFile():
	WEIGTH_FILE = askopenfilename()


root = Tk()
root.title("Ainda to Decidindo")
root.geometry("500x500") #You want the size of the app to be 500x500
root.resizable(0, 0)
mainframe = Frame(root)
# mainframe.grid(column = 0, row = 0, sticky = (N,W,E,S))
# mainframe.columnconfigure(0,weight = 1)
presentation= Frame(mainframe)
# presentation.grid(column = 0,row = 0,rowspan = 2)
presentation.place(x = 0,y = 0,width = 500, height = 100)
controls= Frame(mainframe,background = 'red')
# controls.grid(column = 0,row = 3,rowspan = 4)
controls.place(x = 0,y =200 ,width = 500, height = 400)

var = StringVar()
# LOGO = PhotoImage(file = "BigFiles/teste2.png")
# LOGO.zoom(50,50 )
titleLabel = Label(presentation,text="Ainda não Decidi",font = ('times', 20, 'bold'))
titleLabel.pack()

textFile_button = Button(controls,text="Arquivo de texto",command= ask_textFile)

textFile_button.pack()# textFile_button.grid(row = 3,column = 0)
textFile_label = Label(controls,width = 30,background = "white",relief = SUNKEN)
# textFile_label.grid(row = 3,column = 1)
textFile_label.pack()

root.mainloop()
import tkinter
from . import autoCompleteAlgorithm
root = tkinter.Tk()
root.geometry('500x500')

entryBox = tkinter.Entry(
    master = root,width = 30
)
entryBox.place(x = 100,y = 100)
string = ""
def callback(event):
    entryBox.focus_set()
def keyPressed(event):
    global string
    char = event.char
    if(char!="\x08" and char!="\r" and char!="\t" and char!=""):
        print(type(char))
        string += event.char
        print(string)
    elif(char=="\x08"):
        string = string[:len(string)-1]
obj = autoCompleteAlgorithm.autoCompleteAlgo("diseaseDictionary")
d = obj.getDictionary()
print(d)
entryBox.bind("<Button-1>",callback)
entryBox.bind("<Key>",obj.returnSuggestion)
root.mainloop()
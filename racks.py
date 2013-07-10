import import_file
objects = import_file.import_file('objects.py')
import Tkinter as tk       
import openpyxl as xl

class Application(tk.Frame):              
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)   
        self.grid()                       
        self.createWidgets()
        self.r = objects.Routers()

    def createWidgets(self):
        # Labels
        self.inputlab = tk.Label(self,text='Input')
        self.outputlab = tk.Label(self,text='Output')
        self.inputlab.grid(row=0,column=0)
        self.outputlab.grid(row=1,column=0)
        
        # Input fields
        self.inputnum = tk.IntVar()
        self.outputnum = tk.IntVar()
        self.enterInput = tk.Entry(self,textvariable=self.inputnum,width=5)
        self.enterOutput = tk.Entry(self,textvariable=self.outputnum,width=5)
        self.enterInput.grid(row=0,column=1)
        self.enterOutput.grid(row=1,column=1)

        # Go button
        self.gobutton = tk.Button(self,command=self.go,text='Go')
        self.gobutton.grid(row=0,column=2,rowspan=2)

        # Output
        self.out = tk.Label(self)
        self.out.grid(row=0,column=3,rowspan=2)

    def go(self):
        output = self.r.find(self.inputnum.get(),self.outputnum.get())
        self.out.configure(text='MER-'+output[0]+' Row '+str(output[1])+
                           ' Position '+str(output[2]))

root = tk.Tk()
app = Application()                       
app.master.title('Racks on Racks')
root.geometry('300x50')
app.mainloop()  

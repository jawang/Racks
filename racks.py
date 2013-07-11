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
        self.outlab = [tk.Label(self,width=8) for i in range(3)]
        self.outlab[0].configure(text='Rack')
        self.outlab[1].configure(text='Row')
        self.outlab[2].configure(text='Position')
        self.out = [tk.Label(self) for i in range(3)]
        for i in range(3):
            #self.outlab[i].grid_propagate(0)
            self.outlab[i].grid(row=0,column=3+i)
            self.out[i].grid(row=1,column=3+i)

        self.err = tk.Label(self)
        self.err.grid(row=2,column=3,columnspan=3)

    def go(self,event=None):
        if self.inputnum.get() not in range(1,641) or \
           self.outputnum.get() not in range(1,641):
            self.err.configure(text='Error: No such combination')
        else:
            self.err.configure(text='')
            output = self.r.find(self.inputnum.get(),self.outputnum.get())
            for i in range(3):
                self.out[i].configure(text=str(output[i]))

root = tk.Tk()
app = Application()                       
app.master.title('Racks on Racks')
app.bind_all('<Return>',app.go)
root.geometry('300x75')
app.mainloop()  

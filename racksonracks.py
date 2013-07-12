import Tkinter as tk       
import openpyxl as xl

class Routers:
    def __init__(self):
        self.groups = []
        for i in range(5):
            self.groups.append(Group(i))

    def find(self, inputval, outputval):
        if inputval not in range(1,641) or outputval not in range(1,641):
            return 'Error'
        
        gindex = (outputval-1)/128
        group = self.groups[gindex]
        box = group.boxes[((inputval-1)/64)/4][((inputval-1)/64)%4]
        bindex = outputval - gindex * 128
        if bindex in range(1,33):
            position = box.MIDT
        elif bindex in range(33,65):
            position = box.TOP
        elif bindex in range(65,97):
            position = box.MIDB
        elif bindex in range(97,129):
            position = box.BOT
        return ["MER1-"+box.rackname, box.row+1 , position]
        

class Group:
    def __init__(self, col):
        self.boxes = [[],[],[]]
        self.racks = []
        self.col = col
        
        for i in range(3):
            for j in range(4):
                self.boxes[i].append(Box(j,i))
            

        rackfile = xl.load_workbook('racks.xlsx')
        rackdata = rackfile.get_sheet_by_name('racks')
        
        for i in range(3):
            self.racks.append(
                Rack(str(rackdata.cell(row=col+1,column=i+1).value)))
            self.racks[i].boxes = self.boxes[i]
            for box in self.racks[i].boxes:
                box.rackname = self.racks[i].name


class Rack:
    def __init__(self, name):
        self.boxes = []
        self.name = name
        

class Box:
    def __init__(self,row,col):
        self.rackname = ''
        self.TOP = 1
        self.MIDT = 2
        self.MIDB = 3
        self.BOT = 4
        self.row = row
        self.col = col

class Application(tk.Frame):              
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)   
        self.grid()                       
        self.createWidgets()
        self.r = Routers()

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

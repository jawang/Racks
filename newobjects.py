import Tkinter as tk

# Racks
racks = [['L28','L27','L26','L25'],
         ['L20','L19','L18','L17'],
         ['M17','M18','M19','M20'],
         ['M21','M22','M23','M24'],
         ['M25','M26','M27','M28'],
         ['N27','N26','N25'],
         ['N24','N23','N22']]

count = {0:'zeroeth',
         1:'first',
         2:'second',
         3:'third',
         4:'fourth',
         5:'fifth',
         6:'sixth',
         7:'seventh',
         8:'eighth',
         9:'ninth',
         10:'tenth'}

# type constants
OLD = 0
NEW = 1

class Routers:
    def __init__(self):

        # set up old groups
        self.groups = [Group(OLD) for i in range(5)]
        for i in range(5):
            for j in range(0,4):
                self.groups[i].boxes[j].rackname = \
                    racks[i][0]
            for j in range(4,8):
                self.groups[i].boxes[j].rackname = \
                    racks[i][1]
            for j in range(8,10):
                self.groups[i].boxes[j].rackname = \
                    racks[i][2]
            for j in range(10,13):
                self.groups[i].boxes[j].rackname = \
                    racks[i][3]

        # set up new groups
        self.groups += [Group(NEW) for i in range(2)]
        for i in range(5,7):
            for j in range(0,5):
                self.groups[i].boxes[j].rackname = \
                    racks[i][1]
            for j in range(5,7):
                self.groups[i].boxes[j].rackname = \
                    racks[i][2]
            self.groups[i].boxes[j+1].rackname = \
                racks[i][0]

    def find(self,inputnum,outputnum):
        cindex = 0
        card = 0
        # find the group by output
        # old groups
        if outputnum in range(1,513):
            gindex = (outputnum-1)/128
            group = self.groups[gindex]
            
            # find the box by input
            # old boxes
            if inputnum in range(1,641):
                bindex = (inputnum-1)/64 
                box = group.boxes[bindex]
                if bindex in range(0,4):
                    rindex = bindex
                elif bindex in range(4,8):
                    rindex = 7 - bindex
                elif bindex in range(8,10):
                    rindex = bindex - 8

                # get card number and chassis
                if (outputnum-1)%128 in range(0,32):
                    cindex = rindex*3+2
                    chassis = box.chassis[1]
                    card = 1
                elif (outputnum-1)%128 in range(32,64):
                    cindex = rindex*3+1
                    chassis = box.chassis[0]
                    card = 7
                elif (outputnum-1)%128 in range(64,96):
                    cindex = rindex*3+2
                    chassis = box.chassis[1]
                    card = 6
                elif (outputnum-1)%128 in range(96,128):
                    cindex = rindex*3+2
                    chassis = box.chassis[1]
                    card = 7

                #print [box.rackname, cindex+1, card]
                
            # new boxes
            elif inputnum in range(641,1025):
                bindex = (inputnum-641)/128+10
                box = group.boxes[bindex]
                cindex = 13 - bindex 
                chassis = box.chassis[0]
                if (outputnum-1)%128 in range(0,64):
                    if (inputnum-1)%128 in range(0,64):
                        card = 4
                    elif (inputnum-1)%128 in range(64,128):
                        card = 3
                elif (outputnum-1)%128 in range(64,128):
                    if (inputnum-1)%128 in range(0,64):
                        card = 2
                    elif (inputnum-1)%128 in range(64,128):
                        card = 1
        # new groups
        elif outputnum in range(513,1025):
            gindex = (outputnum-513)/256+5
            group = self.groups[gindex]
            bindex = (inputnum-1)/128
            box = group.boxes[bindex]
            if bindex in range(0,5):
                cindex = 5 - bindex
            elif bindex in range(5,7):
                cindex = 7 - bindex
            elif bindex == 7:
                cindex = 1
            chassis = box.chassis[0]

            if (inputnum-1)%128 in range(0,64):
                if (outputnum-1)%256 in range(0,64):
                    card = 8
                elif (outputnum-1)%256 in range(64,128):
                    card = 7
                elif (outputnum-1)%256 in range(128,192):
                    card = 6
                elif (outputnum-1)%256 in range(192,256):
                    card = 5
            elif (inputnum-1)%128 in range(64,128):
                if (outputnum-1)%256 in range(0,64):
                    card = 4
                elif (outputnum-1)%256 in range(64,128):
                    card = 3
                elif (outputnum-1)%256 in range(128,192):
                    card = 2
                elif (outputnum-1)%256 in range(192,256):
                    card = 1
        else:
            print 'Invalid output '+str(outputnum)
            return

        return [box.rackname, cindex, card, box, chassis]

# A Group represents a cluster of routers that share the same output range    
class Group:
    def __init__(self,gtype):
        if gtype==OLD:
            self.type = 'OLD'
            self.boxes = [Box(OLD,OLD) for i in range(10)]
            self.boxes += [Box(OLD,NEW) for i in range(3)]
        elif gtype==NEW:
            self.type = 'NEW'
            self.boxes = [Box(NEW,NEW) for i in range(8)]
        else:
            print 'Invalid gtype '+str(gtype)
   
# A Box represents a subset of a Group that shares an input range
class Box:
    def __init__(self,gtype,btype):
        self.rackname = ''
        if gtype==OLD:
            if btype==OLD:
                self.type = 'XD BOX'
                self.chassis = [Chassis(OLD,OLD) \
                                for i in range(3)]
            elif btype==NEW:
                self.type = 'ECLIPSE BOX'
                self.chassis = [Chassis(OLD,NEW)]
            else:
                print 'Invalid btype '+str(btype)
        elif gtype==NEW:
            if btype==NEW:
                self.type = 'ECLIPSE BOX'
                self.chassis = [Chassis(NEW,NEW)]
            else:
                print 'Invalid pair ('+str(gtype)+','+str(btype)+')'
        else:
            print 'Invalid gtype '+str(gtype)

# A Chassis represents an individual router box
class Chassis:
    def __init__(self,gtype,btype):
        if gtype==OLD:
            if btype==OLD:
                self.type = 'TRS'
            elif btype==NEW:
                self.type = 'ECLIPSE'
            else:
                print 'Invalid btype '+str(btype)
        elif gtype==NEW:
            if btype==NEW:
                self.type = 'ECLIPSE'
            else:
                print 'Invalid pair ('+str(gtype)+','+str(btype)+')'
        else:
            print 'Invalid gtype '+str(gtype)


#############################################################################
# APPLICATION / GUI
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
        self.outlab[1].configure(text='Chassis')
        self.outlab[2].configure(text='Card')
        self.out = [tk.Label(self) for i in range(3)]
        for i in range(3):
            #self.outlab[i].grid_propagate(0)
            self.outlab[i].grid(row=0,column=3+i)
            self.out[i].grid(row=1,column=3+i)

        self.err = tk.Label(self)
        self.err.grid(row=2,column=3,columnspan=3)

        self.instructions = tk.Text(self,width=30,height=10,wrap=tk.WORD)
        self.instructions.grid(row=3,column=0,columnspan=6)

        # Canvas
        self.draw = tk.Canvas(self,relief='sunken',bd=1,width='8c',height='6c',
                              bg='white')
        self.draw.grid(row=0,column=6,rowspan=4)
        

    def go(self,event=None):
        # Clear Text box
        self.instructions.delete(1.0,tk.END)
        # Make sure inputs are valid
        try:
            self.inputnum.get()
            self.outputnum.get()
        except Exception:
            self.instructions.insert(tk.INSERT,'Error: Invalid input')
            for i in range(3):
                self.out[i].configure(text='N/A')
            return
        if self.inputnum.get() not in range(1,1025) or \
           self.outputnum.get() not in range(1,1025):
            #self.err.configure(text='Error: No such combination')
            self.instructions.insert(tk.INSERT,'Error: No such combination')
            for i in range(3):
                self.out[i].configure(text='N/A')
        else:
            #self.err.configure(text='')
            output = self.r.find(self.inputnum.get(),self.outputnum.get())
            for i in range(3):
                self.out[i].configure(text=str(output[i]))

            self.instructions.insert(tk.INSERT,
                    'Go to rack MER1-'+output[0]+'.\n\nOpen the '+
                    str(count[output[1]])+' chassis from the top.\n\n'+
                    'Within the chassis, find the '+str(count[output[2]])+
                    ' card from the top.')

            # If old XD router
            if output[2] in range(1,8):
                chassis = self.draw.create_rectangle(50,50,250,210)

                cards = [self.draw.create_line(
                        50,50+20*(i+1),250,50+20*(i+1)) for i in range(7)]
                #print cards
                self.draw.itemconfig(cards[output[2]-1],fill='red')
                    

root = tk.Tk()
app = Application()                       
app.master.title('Racks on Racks')
app.bind_all('<Return>',app.go)
root.geometry('290x250')
app.mainloop()  

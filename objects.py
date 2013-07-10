import openpyxl as xl

class Routers:
    def __init__(self):
        self.groups = []
        for i in range(5):
            self.groups.append(Group(i))

    def find(self, inputval, outputval):
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
        return [box.rackname, box.row+1 , position]
        

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

### test ###
'''
r = Routers()

print r.find(1,1)
print r.find(64,128)
print r.find(65,129)
'''

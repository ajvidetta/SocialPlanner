'''
main social plan program.

opens default with my timetable

MODES:
    - view mode, showing my timetbale
    - new table mode, with entry for name and blank timetable
    - edit mode with users in drop down instead of entry
    - compare mode (YET TO DECIDE HOW THE COMPARISONS ARE CHOSEN)
        ~   it makes sense for all comparisons to be against mine (the users) timetable, perhaps a drop down in place of day labels?
        ~   for comparisons, only one day needs to be shown, giving five possible comparisons for each day column

    - need a status bar at the bottem, and buttons allowing user to switch modes.

''' 

from tkinter import *
from tkmacosx import Button
from tkinter import messagebox
from datetime import date
import calendar

root = Tk()
root.wm_title("Social Planner")
root.configure(bg='grey93')

##==================================================================================================
##========================================== SAVE TABLE ============================================
##==================================================================================================

def save():
    
    if editModeButton["fg"] == "black":
        name = nameEntry.get()

    else:
        name = tkvar.get()

    count = 0
    for i in range(5):
        day = []
        for o in range(11):
            if button[count]["bg"] == "green":
                day.append(1)
                button[count].configure(bg="white")
            else:
                day.append(0)
            count+=1
        contents[i][name] = day
    print("AFTER")
    print(contents)
    
    nameEntry.delete(0, 'end')

    f = open("/Users/ajvidetta/Desktop/python/timetable arrange/info.txt", "w+")
    f.write(str(contents))
    f.close()
    print("SAVED")

##==================================================================================================
##========================================== Change mode ===========================================
##==================================================================================================
def changeMode(val):
    for i in range(55):
        button[i].configure(bg="white")
        button[i].configure(fg="black")

    if val == 0:
        editModeButton.configure(fg="black")
        newUser.configure(fg="black")
        compareButton.configure(fg="green")
        print("setting to compare mode")
        for i in range(len(dayLabels)):
            dayLabels[i].grid_forget()
            nameDropDowns[i].grid(row=2, column=i)

        nameEntry.grid_forget()
        dateLabel.grid_forget()
        Save.grid_forget()
        deleteButton.grid_forget()
        dropdown.grid_forget()
        infoLabel.grid_forget()

        dayDropDown.grid(row=0, column=2)

        clearButton.grid(row=0, column=0, sticky=W)
        RIPNoodsButt.grid(row=0, column=0, sticky=E)
        newRowButton.grid(row=0, column=4, sticky=E, pady = 5)
        

    if val == 1:
        print("setting to edit mode")
        editModeButton.configure(fg="green")
        newUser.configure(fg="black")
        compareButton.configure(fg="black")

        infoLabel.grid_forget()
        nameEntry.grid_forget()
        dateLabel.grid_forget()
        
        dropdown.grid(row=1,column=0,columnspan = 3)
        Save.grid(row=1, column=4)
        deleteButton.grid(row=1, column=3)

        dayDropDown.grid_forget()

        clearButton.grid_forget()
        newRowButton.grid_forget()
        RIPNoodsButt.grid_forget()

        for i in range(len(dayLabels)):
            dayLabels[i].grid(row=2,column=i)
        for i in range(len(tkvars)):
            nameDropDowns[i].grid_forget()

    elif val == 2:
        print("setting to new table mode")
        newUser.configure(fg="green")
        editModeButton.configure(fg="black")
        compareButton.configure(fg="black")

        dropdown.grid_forget()
        dateLabel.grid_forget()

        dayDropDown.grid_forget()

        clearButton.grid_forget()
        newRowButton.grid_forget()
        RIPNoodsButt.grid_forget()

        infoLabel.grid(row=0,column=0,columnspan = 5)

        nameEntry.grid(row=1,column=0,columnspan = 4)
        Save.grid(row=1, column=4)
        deleteButton.grid_forget()
        for i in range(len(dayLabels)):
            dayLabels[i].grid(row=2,column=i)
            nameDropDowns[i].grid_forget()

##==================================================================================================
##======================================= TIMETABLE WIDGETS ========================================
##==================================================================================================
def hit(num):
    print(num)
    if button[num]["bg"] != "green":
        button[num].configure(bg="green")
    else:
        button[num].configure(bg="white")

Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
dayLabels = []
for i in range(len(Days)):
    dayLabels.append(Label(root, text = Days[i],bg = "grey93", font=("Courier", 9)))
    dayLabels[i].grid(row=2,column=i)

button = []
rows = 3
cols = 0

for i in range(55):

    button.append(Button(root, text=str(rows+5)+":00", command=lambda i=i: hit(i)))
    button[i].grid(row = rows, column = cols)
    if rows == 13:
        cols+=1
        rows = 3
    else:
        rows+=1
TotalButtons = 55

##==================================================================================================
##============================================ EDIT MODE ===========================================
##==================================================================================================

editModeButton = Button(root, text = "EDIT", fg = "black", height = 40, command=lambda: changeMode(1))
editModeButton.grid(row=14, column=1)


#get users names by reading info.txt (contains all timetables + names)
f = open("/Users/ajvidetta/Desktop/python/timetable arrange/info.txt", "r")
contents = eval(f.read())
f.close

names = []
for key in contents[0]:
    names.append(key)
print(names)


def change_dropdown(*args):
    name = tkvar.get()
    print(name)

    count = 0
    if name in names:
        for i in range(5):
            day = contents[i][name]
            print(day)
            for o in range(11):
                button[count].configure(bg="white")
                if day[o] == 1:
                    button[count].configure(bg="green")
                
                count+=1

#set users names to options in a dropdown
tkvar = StringVar(root)
tkvar.set(names[0])
dropdown = OptionMenu(root, tkvar, *names)
tkvar.trace('w', change_dropdown)

def DeleteUser():
    user = tkvar.get()

    if user in names:

        print("BEFORE")
        print(contents)
        if messagebox.askokcancel("Delete User", "Are you sure you want to delete {}?".format(user)) == True:
            for i in range(len(contents)):
                del contents[i][user]
        print("AFTER")
        print(contents)
        f = open("/Users/ajvidetta/Desktop/python/timetable arrange/info.txt", "w+")
        f.write(str(contents))
        f.close()
        print("DELETED")
    for i in range(55):
        button[i].configure(bg="white")

deleteButton = Button(root, text = "Delete", command=lambda: DeleteUser())


##==================================================================================================
##============================================= HOME ===============================================
##==================================================================================================
date = date.today()
writtenDate = date.strftime("%B %d, %Y")

day = calendar.day_name[date.weekday()]

print(date, day)
dateLabel = Label(root, text = " Welcome, Alex!  {}, {} ".format(day, writtenDate), bg="grey93")
dateLabel.grid(row=1,column=0,columnspan = 5)
##date.grid(row=0,column=0,columnspan = 5)??????

count = 0

for i in range(5):
    day = contents[i]["Alex"]
    print(day)
    for o in range(11):
        button[count].configure(bg="white")
        if day[o] == 1:
            button[count].configure(bg="green")
        
        count+=1

##==================================================================================================
##=====================================  NEW USER MODE WIDGETS =====================================
##==================================================================================================

infoLabel = Label(root, text = "Please enter your name and select the hours you are BUSY", font=("Courier", 12), bg="grey93", foreground="black")


newUser = Button(root, text = "NEW", fg = "black", height = 40, command=lambda: changeMode(2))
newUser.grid(row=14, column=2)

#create name input space
nameEntry = Entry(root, bg = "grey93")

#save button, used to edit & new user
Save = Button(root, text="Save!", command=lambda: save())

##==================================================================================================
##===========================================  COMPARE  ============================================
##==================================================================================================

def personSelection(*args):
    people = []
    for i in range(len(tkvars)):
        people.append(tkvars[i].get())

    print(people)
    for i in range(len(people)):
        if people[i] != "choose":
            print("column: {}".format(i))
            dropDownTracks[i] = people[i]
            day_ = Days.index(dayVar.get())
            print("DAY: {}".format(day_))
            print("{}\n".format(contents))
            
            dayPlan = contents[day_][people[i]]
            dayPlansss = contents[day_]

            print(dayPlan)
            print(contents[day_])

            for o in range(11):
                button[o + 11*i].configure(fg="black")
                if dayPlan[o] == 1:
                    button[o + 11*i].configure(bg="black")

                else:
                    for u in dayPlansss:
                        if (dayPlansss[u][o] == 1) and (u in people):
                            button[o + 11*i].configure(bg="grey50")
                            break
                        
                        else:
                            button[o + 11*i].configure(bg="white")
        else:
            for o in range(11):
                button[o + 11*i].configure(fg="white", bg="white")

tkvars = []
nameDropDowns = []
dropDownTracks = []

dayVar = StringVar(root)
dayVar.set("Monday")
dayDropDown = OptionMenu(root, dayVar, *Days, command = personSelection)

for i in range(5):
    tkvars.append(StringVar(root))
    tkvars[i].set("choose")
    dropDownTracks.append("choose")

    nameDropDowns.append(OptionMenu(root, tkvars[i], "choose", *names, command=personSelection))
    #tkvarMult.trace('w', personSelection())

def clearMatchScreen():
    global button, TotalButtons, tkvars, dropDownTracks, nameDropDowns, cols

    for i in range(len(tkvars)):
        tkvars[i].set("choose")
    for i in range(55):
        button[i].configure(bg="white")
        button[i].configure(fg="black")

    #delete possible extra hour buttons that could have been made
    for i in range(55, TotalButtons):
        button[i].grid_forget()
    button = button[:55]
    TotalButtons = 55

    #delete possible extra name drop downs
    for i in range(5, len(nameDropDowns)):
        nameDropDowns[i].grid_forget()
    tkvars = tkvars[:5]
    nameDropDowns = nameDropDowns[:5]
    dropDownTracks = dropDownTracks[:5]
    cols = 5


def NewColumn():
    global rows, cols, TotalButtons

    tkvars.append(StringVar(root))
    tkvars[-1].set("choose")
    dropDownTracks.append("choose")

    nameDropDowns.append(OptionMenu(root, tkvars[-1], "choose", *names, command=personSelection))
    nameDropDowns[len(tkvars)-1].grid(row=2, column=len(tkvars)-1)


    for i in range(11):

        button.append(Button(root, text=str(rows+5)+":00", command=lambda i=i: hit(i + TotalButtons)))
        button[i + TotalButtons].grid(row = rows, column = cols)
        if rows == 13:
            cols+=1
            rows = 3
        else:
            rows+=1
    
    TotalButtons += 11

def noodsCompar():
    #make table space 8 columns, set all drop downs to names in noods
    for i in range(3):
        NewColumn()

    members = ['Alex', 'Ben', 'James', 'Sophia', ' Marissa', 'Tasman', 'Gemma', 'Lucia']

    for i in range(len(members)):
        tkvars[i].set(members[i])
        dropDownTracks[i] = members[i]
    personSelection()

clearButton = Button(root, text="clear", width = 45 ,command=lambda: clearMatchScreen())
newRowButton = Button(root, text="+", width = 45, command=lambda: NewColumn())
RIPNoodsButt = Button(root, text="n", width = 45, command=lambda: noodsCompar())


compareButton = Button(root, text="MATCH", fg = "black", height = 40, command=lambda: changeMode(0))
compareButton.grid(row=14, column=0, pady = 7)

##==================================================================================================
##========================================= root.mainloop() ========================================
##==================================================================================================

root.mainloop()
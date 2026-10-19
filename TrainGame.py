import pygame
import time
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import Entry
from tkinter import messagebox
import random
import math

#Login Page ----------------------------------------------------------------------------------------

#Global Variables
PageNumber = "P1"
CurrentUsername = " "
CheckQuit = False
IsLoggedIn = False

#load Database
with sqlite3.connect("TrainGameDataBase2.db") as db:
    cursor = db.cursor()

#Displaying pages
class Page(tk.Frame):
    def __init__(self,*args, **kwargs):
        tk.Frame.__init__(self,*args, **kwargs)

    def show(self):
        self.lift()

    def hide(self):
        self.lower()

#page for logins
class LoginPage(Page):
    def __init__(self,*args, **kwargs):
        Page.__init__(self,*args, **kwargs)
        global IsLoggedIn

        MainTitle = Label(self, text="My Game", background="#dc1414", font="Arial 12 bold")
        MainTitle.place(x=175, y=40, width=300, height=25)

        def ShowMenu():
            global CurrentUsername

            CurrentUsername = username.get() #gets username and password
            CurrentPassword = password.get()
            
            if CurrentUsername == "" or CurrentPassword == "":
                messagebox.showinfo("Invalid Message", " Not entered anything in the box") #if empty display error
            
            if len(CurrentUsername) >= 30  or len(CurrentPassword) >= 30:
                messagebox.showinfo("Invalid Message", " Input exceeds max characters (30)") #if too long display error
            
            cursor.execute("SELECT Username, Password FROM Player") #get info form database
            
            InvalidUser = True

            for count in cursor.fetchall():
                TempUser = count[0] #save info into temporory variables
                TempPass = count[1]
                
                
                if TempUser == CurrentUsername and TempPass == CurrentPassword: #if username and password are correct
                
                    global PageNumber
                    global IsLoggedIn
                    PageNumber = "P2" #go to next page
                    main = MainView(self)
                    main.pack(side="top", fill="both", expand=True)
                    InvalidUser = False
                    IsLoggedIn = True #as apposed to guest mode

            if InvalidUser:
                messagebox.showinfo("Invalid Message", " Data Incorrect")

        usernamelbl = Label(self, text="Username", background="#dc1414", font="Arial 12 bold")
        usernamelbl.place(x=175, y=90, width=200, height=25) #box for title of username

        username = tk.Entry(self, text="")
        username.place(x=400, y=90, width=100, height=25) #text entry for username
        username.focus()

        passwordlbl = Label(self, text="Password", background="#dc1414", font="Arial 12 bold")
        passwordlbl.place(x=175, y=140, width=200, height=25) #box for title of password

        password = tk.Entry(self, text="", show=("*"))
        password.place(x=400, y=140, width=100, height=25) #text entry for password showing "*" instead of password when typed
        password.focus()

        Loginpagebtn = Button(self, text="Login", background="#047434", font="Arial 12 bold", command=ShowMenu) #executes this subroutine when clicked
        Loginpagebtn.place(x=200, y=230, width=105, height=25) #button which logs you in

        def ShowUser():
            global PageNumber
            PageNumber = "P3" #go to next page
            main = MainView(self)
            main.pack(side="top", fill="both", expand=True)

        Loginpagebtn = Button(self, text="Create User", background="#8c1c4c", font="Arial 12 bold", command=ShowUser) #executes this subroutine when clicked
        Loginpagebtn.place(x=200, y=270, width=105, height=25) #button for creating new users

        def Guest():
            global CheckQuit
            answer = messagebox.askquestion("Are You Sure?", "Scores Will Not Be Saved", icon="warning") #warning message
            if answer == "yes":
               root.quit() #quits tkinter
               CheckQuit = True 
               IsLoggedIn = False 

        Loginpagebtn = Button(self, text="Play As Guest", background="#b46404", font="Arial 12 bold", command=Guest)
        Loginpagebtn.place(x=200, y=310, width=105, height=25) #play as guest button

class MenuPage(Page):
    def __init__(self,*args, **kwargs):
        Page.__init__(self,*args, **kwargs)

        MainTitle = Label(self, text="My Menu", background="#047434", font="Arial 12 bold")
        MainTitle.place(x=175, y=40, width=300, height=25) #title

        def ShowUser():
            global PageNumber
            PageNumber = "P3" #go to this page
            main = MainView(self)
            main.pack(side="top", fill="both", expand=True)

        Loginpagebtn = Button(self, text="Create User", background="#8c1c4c", font="Arial 12 bold", command=ShowUser) #executes this subroutine when clicked
        Loginpagebtn.place(x=200, y=185, width=105, height=25) #button with title text

        def ShowScores():
            global PageNumber
            PageNumber = "P4" #go to this page
            main = MainView(self)
            main.pack(side="top", fill="both", expand=True)

        Loginpagebtn = Button(self, text="High Score", background="#2d2b80", font="Arial 12 bold", command=ShowScores) #executes this subroutine when clicked
        Loginpagebtn.place(x=200, y=230, width=105, height=25) #button with title text

        def ShowEdit():
            global PageNumber
            PageNumber = "P5" #go to this page
            main = MainView(self)
            main.pack(side="top", fill="both", expand=True)

        Loginpagebtn = Button(self, text="Edit Users", background="#eca4b4", font="Arial 12 bold", command=ShowEdit) #executes this subroutine when clicked
        Loginpagebtn.place(x=200, y=275, width=105, height=25) #button with title text

        def Quit():
            global CheckQuit
            root.quit()
            CheckQuit = True #quits tkinter

        Loginpagebtn = Button(self, text="Play Game", background="#b46404", font="Arial 12 bold", command=Quit) #executes this subroutine when clicked
        Loginpagebtn.place(x=200, y=430, width=105, height=25) #button with title text


class CreateNewUser(Page):
    def __init__(self,*args, **kwargs):
        Page.__init__(self,*args, **kwargs)

        MainTitle = Label(self, text="Create New User", background="#8c1c4c", font="Arial 12 bold")
        MainTitle.place(x=175, y=40, width=300, height=25) #text box

        Namelbl = Label(self, text="Please enter your name", background="#8c1c4c", font="Arial 12 bold")
        Namelbl.place(x=175, y=90, width=400, height=25) #text box

        Name = tk.Entry(self, text="")
        Name.place(x=600, y=90, width=150, height=25) #allows you to enter text
        Name.focus()

        Usernamelbl = Label(self, text="Please enter your username", background="#8c1c4c", font="Arial 12 bold")
        Usernamelbl.place(x=175, y=140, width=400, height=25) #text box

        Username = tk.Entry(self, text="")
        Username.place(x=600, y=140, width=150, height=25) #allows you to enter text
        Username.focus()

        Passwordlbl = Label(self, text="Please enter your password", background="#8c1c4c", font="Arial 12 bold")
        Passwordlbl.place(x=175, y=190, width=400, height=25) #text box

        Password = tk.Entry(self, text="")
        Password.place(x=600, y=190, width=150, height=25) #alllows you to enter text
        Password.focus()

        def ClearUser():
            Name.delete(0, END)
            Username.delete(0, END) #clears boxes
            Password.delete(0, END)

        def AddUser():
            TempName = Name.get()
            TempUser = Username.get() #get input from text boxes
            TempPass = Password.get()

            if TempUser == "" or TempPass == "" or TempName == "":
                messagebox.showinfo("Invalid Message", " Not entered anything in the box") #makes sure they arent empty
                ValidUser = False

            elif len(TempUser) >= 30 or len(TempPass) >= 30 or len(TempName) >= 30:
                messagebox.showinfo("Invalid Message", " Input exceeds max characters (30)") #makes sure they arent empty
                ValidUser = False
            
            else:
               ValidUser = True
            
            cursor.execute("SELECT Username FROM Player") #loads all usernames from database
            for count in cursor.fetchall():
                User = count[0]

                if TempUser == User:
                    ValidUser = False
                    messagebox.showinfo("Invalid User", "Username Taken") #makes sure it isnt a repeat

            if ValidUser:
                cursor.execute("INSERT INTO Player(Name, Username, Password) VALUES (?, ?, ?)",(TempName, TempUser, TempPass)) #inserts info into database
                db.commit()
                cursor.execute("INSERT INTO Achievements(Username,TotalConnections,TotalStations,TotalTrains,AchievementsGot,TotalMoney) VALUES(?, ?, ?, ?, ?, ?)",(TempUser, 0, 0, 0, "0000000000000000000000000", 0)) #sets empty records into achievement table
                db.commit()
                messagebox.showinfo("User Information", "User successfully entered into database") #output to user
                ClearUser()
            
        Loginpagebtn = Button(self, text="Add User", background="#8c1c4c", font="Arial 12 bold", command=AddUser)
        Loginpagebtn.place(x=175, y=240, width=105, height=25) #button which executes subroutine when clicked

        def Return():
            global PageNumber
            PageNumber = "P2" #go back a page
            main = MainView(self)
            main.pack(side="top", fill="both", expand=True)
     
        def Return2x():
            global PageNumber
            PageNumber = "P1" #go back to first page
            main = MainView(self)
            main.pack(side="top", fill="both", expand=True)

        if IsLoggedIn:  
            Loginpagebtn = Button(self, text="Return", background="#047434", font="Arial 12 bold", command=Return) #if theyre logged in go back once
        else:
            Loginpagebtn = Button(self, text="Return", background="#047434", font="Arial 12 bold", command=Return2x) #if not go back to start because they need to log in first

        Loginpagebtn.place(x=175, y=550, width=105, height=25)


class HighScorePage(Page):
    def __init__(self,*args, **kwargs):
        Page.__init__(self,*args, **kwargs)

        MainTitle = Label(self, text="High Scores", background="#2d2b80", font="Arial 12 bold")
        MainTitle.place(x=175, y=40, width=300, height=25) #show text box

        MyList = Listbox(self)
        MyList.insert(END, "Date" + "             " + "Score") #headers for table
        global CurrentUsername
    
        cursor.execute("select Player.Name, Player.Username, Stats.Date, Stats.Score from Player INNER JOIN Stats where Stats.Username = '%s'" % (CurrentUsername)) #get stats
        
        for count in cursor.fetchall():
            if count[1] == CurrentUsername: #info from stats gets saved
                TempName  = count[0]
                TempDate  = count[2]
                TempScore = count[3]


                SubTitle = Label (self, text="Welcome " + TempName + " See below your high scores", background= '#2d2b80', font='Arial 12 bold') 
                SubTitle.place(x=175, y=90, width=600, height=25) #text box


                MyList.insert(END, TempDate + " "+ str(TempScore)) #show stats line by line
                MyList.place(x=175, y=140, width=300, height=125)
        
        cursor.execute("select min (Score) as MinScore, count (Stats.Username) as count, max(Score) as MaxScore from Player INNER JOIN Stats where Stats.Username = '%s'" % (CurrentUsername)) #shows the highscore
        
        for count in cursor.fetchall():
            TempMin = count[0]
            TempCount = count[1]
            TempMax = count[2]
        
        HighScorelbl = Label(self, text="My Highest Score is " + str(TempMax), background='#2d2b80', font='Arial 12 bold') 
        HighScorelbl.place(x=175, y=290, width=600, height=25) #displays player specific stats for hishest lowest and times played
        
        HighScorelbl = Label(self, text="My Lowest Score is " + str(TempMin), background= '#2d2b80', font='Arial 12 bold') 
        HighScorelbl.place(x=175, y=390, width=600, height=25)

        HighScorelbl = Label (self, text="Number of times I have played the game " + str(TempCount//2), background='#2d2b80', font='Arial 12 bold') 
        HighScorelbl.place (x=175, y=490, width=600, height=25)

        def Return():
            global PageNumber
            PageNumber = "P2" #go back one page
            main = MainView(self)
            main.pack(side="top", fill="both", expand=True)
        
        Loginpagebtn = Button(self, text="Return", background="#047434", font="Arial 12 bold", command=Return)
        Loginpagebtn.place(x=175, y=550, width=105, height=25) #display back button

class EditUser(Page):
    def __init__(self,*args, **kwargs):
        Page.__init__(self,*args, **kwargs)
        
        user = []
        name1 = StringVar()
        password1 = StringVar()

        cursor.execute("SELECT Username FROM Player")
        for count in cursor.fetchall(): #load username from account logged in
            user.append(str(count[0]))

        Usernamelbl = Label(self, text="Select Username", background='#eca4b4', font='Arial 12 bold') 
        Usernamelbl.place(x=175, y=90, width=300, height=25) #text box

        user1 = StringVar(self)
        Username = OptionMenu(self, user1, *user, 1)
        Username.place(x=600, y=90, width=150, height=25) #dropdown box for players
        Username.focus()

        MainTitle = Label(self, text="Edit User", background='#eca4b4', font='Arial 12 bold') 
        MainTitle.place(x=175, y=40, width=300, height=25) #text box

        Namelbl = Label(self, text="Name", background='#eca4b4', font='Arial 12 bold') 
        Namelbl.place(x=175, y=140, width=300, height=25) #text box

        EditName = tk.Entry(self, textvariable=name1)
        EditName.place(x=600, y=140, width=150, height=25) #allows you to enter new name
        EditName.focus()

        Passwordlbl = Label(self, text="Password", background='#eca4b4', font='Arial 12 bold') 
        Passwordlbl.place(x=175, y=190, width=300, height=25) #text box

        EditPassword = tk.Entry(self, textvariable=password1)
        EditPassword.place(x=600, y=190, width=150, height=25) #allows you to enter new password
        EditPassword.focus()

        def DeleteUser():
            answer = messagebox.askquestion("Delete a user?", "Are you sure?", icon="warning") #verifies input
            if answer == "yes":
                TempUser = user1.get()
                cursor.execute("SELECT Username FROM Player WHERE Username = '%s'"%(TempUser)) #loads username selected

                for count in cursor.fetchall():
                    cursor.execute("DELETE FROM Player WHERE Username = '%s'"%(TempUser)) #delete record from table which matches username selected
                    db.commit()
                    cursor.execute("DELETE FROM Achievements WHERE Username = '%s'"%(TempUser)) #delete record from achievements table too
                    db.commit()

                    messagebox.showinfo("User Information Deleted", "Successfully deleted user")

        addbtn = Button(self, text="Delete User", background="#eca4b4", command=DeleteUser)
        addbtn.place(x=175, y=400, width=100, height=25) #button which deletes users

        def EditUser():
            
            cursor.execute("SELECT Name, Username, Password FROM Player") 
            for count in cursor.fetchall():
                if str(count[1]) == user1.get():
                    name1.set(str(count[0]))
                    password1.set(str(count[2]))
            
        EditUser = Button(self, text="Edit User", background="#eca4b4", command=EditUser)
        EditUser.place(x=325, y=400, width=100, height=25) #text box

        def UpdateUser():
            TempName = EditName.get()
            TempUsername = user1.get() #load info on player input into text boxes
            TempPassword = EditPassword.get()

            if TempName == "" or TempPassword == "":
                messagebox.showinfo("Invalid Message", " Not entered anything in the box") #makes sure not empty
            else:
                cursor.execute("SELECT Username FROM Player WHERE Username = '%s'"%(TempUsername)) #does what it looks like

                for count in cursor.fetchall():
                    cursor.execute("UPDATE Player SET Name =?, Username =?, Password =? WHERE Username=?", (TempName, TempUsername, TempPassword, TempUsername))
                    db.commit() #updates record of username and password with new info

                messagebox.showinfo("User Info Updated", "Successfully updated into database")

        UpdateUser = Button(self, text="Update User", background="#eca4b4", command=UpdateUser)
        UpdateUser.place(x=475, y=400, width=100, height=25) #text box

        def Return():
            global PageNumber
            PageNumber = "P2" #go back one page
            main = MainView(self)
            main.pack(side="top", fill="both", expand=True)
        
        Loginpagebtn = Button(self, text="Return", background="#047434", font="Arial 12 bold", command=Return)
        Loginpagebtn.place(x=175, y=550, width=105, height=25) #button thet goes back a page


class MainView(tk.Frame):
    def __init__(self,*args, **kwargs):
        tk.Frame.__init__(self,*args, **kwargs)
        p1 = LoginPage(self, background="#eeeeee")
        p2 = MenuPage(self, background="#eeeeee")
        p3 = CreateNewUser(self, background="#eeeeee") #class which displays the pages
        p4 = HighScorePage(self, background="#eeeeee")
        p5 = EditUser(self, background="#eeeeee")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        global PageNumber

        if PageNumber == "P1":
            p1.show()
        elif PageNumber == "P2":
            p2.show()
        elif PageNumber == "P3":
            p3.show()
        elif PageNumber == "P4":
            p4.show()
        elif PageNumber == "P5":
            p5.show()
        else:
            p1.show()


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("Menu")
    root.wm_geometry("1220x600")
    root.mainloop()

#Login Page ----------------------------------------------------------------------------------------

# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()


white      = ("#ffffff")

brown      = ("#b46404")
red        = ("#dc1414")
yellow     = ("#fccc05")
green      = ("#047434") #all the colours used in the connections
pink       = ("#eca4b4")
purple     = ("#8c1c4c")
blue       = ("#2d2b80")
light_blue = ("#049cdc")

colourfeed = [brown, red, yellow, green, purple, blue, pink, light_blue] #list of the colours to cycle through

colourselected = 0 #pointer

redlight   = ("#ff0000")
greenlight = ("#00ff00") #primary colours
bluelight  = ("#0000ff")

marker    = [("#040404"),
             ("#646464")] #black colour which has a lighter version for when hovering over
bgcolour   = ("#eeeeee") #background colour
rail       = ("#7d7d7d") #unused colour fron early version

gridToggle = False #determines wether to show the grid
buildToggle = False #is build mode on
deleteToggle = False #is delete mode on?
editToggle = False #is edit mode on
secretmode = False #is secret mode on
pauseScreen = True #is the game paused
trainScreen = False #is the train purchace screen open
helpScreen = True #is the help screen open
upgradeScreen = False #is the upgrade screen open
AchievementScreen = False #is the achievement screen open
controllScreen = False #i sthe controlls screen open
cooldown = True # can you click on buttons right tnow
showPathToggle = False #will the thin green line show the trains path
achievementsGot = "00000000000000000000000000" #25 bit binary number that represents the unlocked state of all the achievements stored as a string
secretFound = 0 #has the secret been found (integer to work with progress bar)

TotalTrains = 0 #the loaded totals across the player's games
TotalConnections = 0
TotalMoney = 0
TotalStations = 0

Quiting = False #are you quitting

if IsLoggedIn:
     cursor.execute("SELECT TotalTrains, TotalStations, TotalConnections, TotalMoney, AchievementsGot FROM Achievements WHERE Username =?", (CurrentUsername,))
     for count in cursor.fetchall():
          TotalTrains = count[0]
          TotalStations = count[1]
          TotalConnections = count[2] #if youre logged in then load all the totals from the database
          TotalMoney = count[3]
          achievementsGot = count[4]


splashfont = pygame.font.SysFont('MV Boli',30) 
debugfont = pygame.font.SysFont('Courier Std',10) #font used when i was debugging the code
moneyfont = pygame.font.SysFont('Dubai Medium',30) #i used to use this to show the money
tflFont = pygame.font.Font('Johnston100 W03 Medium.ttf', 20) #this is the font used in all the menus

mouse = pygame.mouse.get_pos()

stations = [] #list of all the coordinates of the stations built

#

class BankAccount():

     def __init__(self, money):
          self.money = money

     def deposit(self,amount):
          self.money += amount #add money to bank account

     def withdrawl(self,amount):
          self.money -= amount #take it away

     def getMoney(self):
          i = self.money #gets the value
          return i

bank = BankAccount(500) #gives you 425 money to start off with (enough for 1 train 2 stations and a connection between them)

# Train -----------------------------------------------------------------------------
#    ██████  ██████  ██████  ██████  ██████
#      ██    ██  ██  ██  ██    ██    ██  ██
#      ██    ████    ██████    ██    ██  ██
#      ██    ██  ██  ██  ██    ██    ██  ██
#      ██    ██  ██  ██  ██  ██████  ██  ██
# Train -----------------------------------------------------------------------------

def flipInput(input): #subroutine for flipping a list
          temp = []
          for i in range(len(input)):
                  temp.append(input[len(input)-i-1])
          return temp

class Train:

    def __init__(self):
        self.xpos = 1000 #x position of train
        self.ypos = 1000 #y position of train
        self.upgradelvl = 1 #capacity of train
        self.colour = (25,25,25) #train colour
        self.path = [] #the path that the train takes
        self.pathindex = [] #the path but with the indexes of the train list
        self.speed = 1 #speed of train
        self.passengers = 0 #passengers on the train
        self.bought = False #is it bought
        self.iprogress = 0 #progress of the train on its path
        self.jprogress = 0 #progress of the train between stations on the path
        self.tenth = 0 #global tenth of seecond at current time
        self.timemark = 0.0 
        self.cost = [100,100] #cost of the upgrades
        self.givesMoney = True #when arriving at station does it give money
        self.storageToggle = False  #is it in storage

    def waitWithoutPause(self): #this is needed to increment movement without pausing the entire game
     temp = str(time.time())[str(time.time()).find(".")+1] #finds the current tenth of second
     if temp != str(self.tenth): #checks it against the last saved one
          self.tenth = temp #if not update the last saved one
          return True 
     else: #true and false mean has the correct time elapsed
          return False
    
    def showTrain(self): #displaying the train at the x and y coordinates
     if not self.storageToggle and len(self.pathindex) > 1:
          pygame.draw.circle(screen, self.colour,
               (self.xpos,self.ypos), 10, 0)
    
    def showPath(self): #shows the trains path in thin green line
         if len(self.path) > 1:
               for i in range(len(self.path)-1):
                     pygame.draw.line(screen, "#00ff00" ,
                                 [self.path[int(i)][0], self.path[int(i)][1]], 
                                 [self.path[int(i)+1][0], self.path[int(i)+1][1]], 3)# goes through each entry and draws line between them all

    def buy(self):
          if bank.getMoney() >= 200:
               self.bought = True #if you have enough money it will allow it to be bought
               bank.withdrawl(200)

    def sell(self):
          global trainSelected
          if trainSelected >= trainsOwnedCount(): #if the selected train is being resold
               trainSelected = trainsOwnedCount()-1 #make selected train be last owned one
          self.bought = False #make it not bought
          bank.deposit(200) #refund money
          self.delPath()
          self.storageToggle = True #put off screen
          self.iprogress = 0 #make movement progress reset
          self.jprogress = 0
          
    def addToPath(self): #for adding stations to the path
          global stations
          global connections
          if self.bought: #only if its bought
               tempplace = 0
               if editToggle: #if edit mode is on
                    tempplace = (stations[buttonover(stations)]) #save the station and its index in temporary variables
                    tempindex = buttonover(stations)
               temp = []
               fliptemp = []
               if len(self.path) >0: #if the path is bigger than 0
                    temp.append(self.pathindex[len(self.pathindex)-1])
                    temp.append(tempindex) #append the previous and current station in temporary list
                    fliptemp  = [tempindex,temp[0]] #has a flipped one too
                    if temp in connections or fliptemp in connections:
                         self.path.append(tempplace) #checks the temporary lists to amke sure that the train's path is on a connection
                         self.pathindex.append(tempindex)
               elif buttonover(stations) != -1:
                    self.path.append(tempplace) #if the path has no entries then it doesnt need to check anything so just adds it as long as a stations is selected
                    self.pathindex.append(tempindex)
                    self.storageToggle = False

    def cutPath(self): #remove end of trains path
         self.iprogress = 0 #puts the trains progress back to 0 so it doesnt go off the path
         self.jprogress = 0
         if len(self.path) > 1: #if its larger than 1
              self.path = self.path[0:len(self.path)-1] #removes the end
              self.pathindex = self.pathindex[0:len(self.pathindex)-1]
         elif len(self.path) == 1:
              self.delPath() #if its only 1 long deletes it
              self.storageToggle = True #puts it in storage
     
    def delPath(self): #for deleting the path completely
         self.storageToggle = True #puts it in storage
         self.iprogress = 0 #sets progress to 0
         self.jprogress = 0
         if len(self.path) > 0:
              self.path = [] #deletes the path
              self.pathindex = []
    
    def move(self): #for moving the train
        if self.waitWithoutPause(): #if its waited for 0.1 second
          if len(self.path)>1: #if it has a path longer than 1 entry
              self.storageToggle = False #take it out of storage
              diffx = 0 #initialise variables for finding distance between stations
              diffy = 0
              diffx = self.path[self.iprogress+1][0] - self.path[self.iprogress][0] #find the distance between them
              diffy = self.path[self.iprogress+1][1] - self.path[self.iprogress][1]
              displacement = 0 #variable for diagonal distance
              displacement = math.sqrt(diffx**2 + diffy**2) #pythagoras to find it with the distances
              if displacement == 0: #if there is no distance dont go anywhere and dont give money
                   steps = 1
                   self.givesMoney = False 
              else:
                   steps = displacement // self.speed #if not then the amount of steps it takes are based on the speed of the train
                   self.givesMoney = True #will give money

              if self.jprogress == 0: #if it has began
                   self.xpos = self.path[self.iprogress][0] #place it on the stations location so no rounding error
                   self.ypos = self.path[self.iprogress][1]
                   self.jprogress += 1 #increment progress
              elif self.jprogress == steps: #if it has arrived
                 self.xpos = self.path[self.iprogress+1][0] #place it on the stations location so no rounding error
                 self.ypos = self.path[self.iprogress+1][1]
                 self.jprogress = 0 #restart progress
                 if len(self.path) == 2: #if its between 2 stations then go backwards always
                      self.path = flipInput(self.path)
                 else:
                      if self.iprogress == len(self.path)-2: #if it has reached end of path
                        self.iprogress = 0 #reset progress
                        if self.path[0] != self.path[len(self.path)-1]: #if the path is not a loop then go backwards
                         self.path = flipInput(self.path)
                      else:
                        self.iprogress += 1 #if its not there yet then just increment
              else: #if train not at a station yet
                   self.showTrain() #display the train
                   self.xpos += diffx / steps #move it along the distance according to the speed
                   self.ypos += diffy / steps
                   self.jprogress += 1 #increment progress
    
    def colourchange(self,choice):
        self.colour = choice #if i wanted to change the colour of the train
    
    def offonload(self): #for onloading passengers and offloading once at a station
        maxpassengers = 10*self.upgradelvl #the max is 10 passengers per capacity level
        if len(self.path) >= 2 and self.givesMoney:    #if the train has a path and is allowed to give money
          for i in range(len(self.path)):
              if (self.xpos == self.path[i][0] and self.ypos == self.path[i][1]) and ((self.timemark + 1) < (time.time())): #if train is at station and the time is correct
                  randomnumber = random.randint(1,3) #number of pasengers getting off
                  if randomnumber > self.passengers:
                       self.passengers = 0 #if the random number is bigger than number of passengers then just empty the train
                  else:
                       self.passengers -= randomnumber*self.upgradelvl #if not then take away that amount
                  bank.deposit(randomnumber*5) #give 5 money per passenger disembarked
                  randomnumber = random.randint(1,3) #passengers getting on
                  if randomnumber > (maxpassengers - self.passengers): #if more try to get on then allowed then just max the train out
                      self.passengers = maxpassengers
                  else:
                      self.passengers += randomnumber #iff not then embark them like normal
                  self.timemark = time.time() #mark down current time

    def upgrade(self): #for upgrading the train
         if mouse[0] < 200: #if the mouse is over the capacity button
              if bank.getMoney() > self.cost[0] and self.upgradelvl <= 4: #if you have enough money and upgrades arent maxed out
               bank.withdrawl(self.cost[0]) #take away the money
               self.upgradelvl += 1 #increment level
               self.cost[0] *= 2 #double the cost for next time
         elif mouse[0] > 200: #if the mouse is over the speed button
              if bank.getMoney() > self.cost[1] and self.speed <= 4: #if you have enough money and upgrades arent maxed out
               bank.withdrawl(self.cost[1]) #take away the money
               self.speed += 1 #increment level
               self.cost[1] *= 2 #double the cost for next time

          

# Train --------------------------------------------------------------------------------

trainSelected = 0 #pointer for selected train

Train1 = Train() #initialise all trains
Train2 = Train()
Train3 = Train()
Train4 = Train()
Train5 = Train()
Train6 = Train()
Train7 = Train()
Train8 = Train()

def drawstations(station,colour,index):    #for drawing the stations     
     if buttonover(stations) == index: #if mouse is hovering over this station
          pygame.draw.circle(screen, colour[1], #draw the station in given place and lighter colour
                  (station[0],station[1]), 20, 0)
          pygame.draw.circle(screen, bgcolour,
                  (station[0],station[1]), 13, 0)
     else: #if not
          pygame.draw.circle(screen, colour[0], #draw the station in given place and normal colour
                  (station[0],station[1]), 20, 0)
          pygame.draw.circle(screen, bgcolour,
                  (station[0],station[1]), 13, 0)

def checkmenucollision(colours): #check collision for colour menu
     flag = False
     for i in range(len(colours)): #for each colour check if mouse is over button
          if ((40*i)+20 < mouse[0] < (40*i)+40) and (Y-40 < mouse[1] < Y-20):
               return i
               flag = True #if so return true at the end
     if not flag: #if not return flase at the end
          return -1

def drawmenu():      #for displaying the colour menu at bottom   
     altcount = 0
     count = 20
     for i in colourfeed: #for each colour
          if i == colourfeed[colourselected]: #if its selected draw an exra box around the icon
               pygame.draw.rect(screen, marker[0],
                       [count-4, Y-44, 28, 28], 0)
               pygame.draw.rect(screen, bgcolour,
                       [count-2, Y-42, 24, 24], 0)
               pygame.draw.rect(screen, marker[0],
                       [count, Y-40, 20, 20], 0)
               pygame.draw.rect(screen, i,
                       [count+2, Y-38, 16, 16], 0)
          if checkmenucollision(colourfeed) == altcount: #if mouse is over then make box thicker
               pygame.draw.rect(screen, marker[0],
                       [count, Y-40, 20, 20], 0)
               pygame.draw.rect(screen, i,
                       [count+3, Y-37, 14, 14], 0)
          else:
               pygame.draw.rect(screen, marker[0], #if not draw as normal
                       [count, Y-40, 20, 20], 0)
               pygame.draw.rect(screen, i,
                       [count+2, Y-38, 16, 16], 0)
          count += 40 #move over to the next box
          altcount += 1

def drawall(stations,colour): #draw all the stations in the list using that subroutine
     for i in range(len(stations)):
          drawstations(stations[i],colour,i) #also returns index for hover over subroutine to check against

def removeend(list): #subroutine for removing the end off of a list
     output = []
     if len(list) > 1:
          for item in range(len(list)-1):
               output.append(list[item])
          return output
     elif len(list) ==1:
          return([])

def atomise(matrix): #makes sure there thet the last entry is not a repeat
     new = []
     last = []
     if len(matrix) > 1:
          last = matrix[len(matrix)-1]
          reverse = [last[1],last[0]]
          new = removeend(matrix)
          if last in new:
               return True
          elif reverse in new:
               return True
          else:
               return False
     else:
          return False
     
def changecolours(colour,feed): #for changing the colour selected
     if colour == len(feed)-1:
          colour = 0 #go back to start when at end
     else:     
          colour += 1
     return colour

connections=[] #list of connections between stations
colourlist = [] #list of the colour of those connections

def connect(matrix,locations,feed): #for showing the connections
     try:
          count = 0
          for connection in matrix: #for each item in the connections draw a line for it in the colour in which it is
               if connection[1] == -1: #if not selected end point draw to mouse
                    pygame.draw.line(screen, feed[colourselected], 
                           [locations[connection[0]][0], locations[connection[0]][1]], 
                           [mouse[0], mouse[1]], 12)
               else: #if so draw as normal
                    pygame.draw.line(screen, feed[colourlist[count]], 
                           [locations[connection[0]][0], locations[connection[0]][1]], 
                           [locations[connection[1]][0], locations[connection[1]][1]], 12)
               count += 1
     except:
          pass  

def checkcollision(location): #for checking if the mouse is over a station
     try:
          if (location[0]-20 < mouse[0] < location[0]+20) and (location[1]-20 < mouse[1] < location[1]+20):
               return True
     except:
          pass

def buttonover(locations): #returns which station the mouse is over
     answer = 0
     flag = False
     if len(locations) == 1: #if there is only one
          if checkcollision([locations[0][0],locations[0][1]]):
               return answer
               flag = True
          else:
               answer += 1
     else:
          for location in locations: #if there are multiple
               if checkcollision(location):
                    return answer
                    flag = True
               else:
                    answer += 1
     if flag == False:
          return -1

def makeConnection():
     global connections
     global colourlist
     if buttonover(stations) != -1: #if mouse is over a station
          if bank.getMoney() >= 25: #and you ahve enough money
               if connections == []: #if there arent any connections yet
                    connections.append([buttonover(stations),-1]) #add the value of that station and a temporary value
               elif connections[len(connections)-1][1] == -1: #if that temporary value is still there                        
                    if connections[len(connections)-1][0] == buttonover(stations): #if your mouse is over the first station
                         connections[len(connections)-1][1] = buttonover(stations) #set the end value to that station
                         connections = removeend(connections) #remove the unnecesary connection
                    else:
                         connections[len(connections)-1][1] = buttonover(stations) # set it to the staton that they're now over
                         colourlist.append(colourselected) #add the colour selected to this list
                         if not atomise(connections): #if this isn't a repeat
                              bank.withdrawl(25) #take the money
               else:
                    connections.append([buttonover(stations),-1]) #if anything else (has values but not ending in the temp value) add it like line 1486
          if atomise(connections): #if there is a repeat in the list
               connections = removeend(connections) #remove the repeat

def showError(): #draws a big red x
     pygame.draw.line(screen, (255,0,0), 
                      [((round(mouse[0]/50)*50)//1)-20,((round(mouse[1]/50)*50)//1)-20],
                      [((round(mouse[0]/50)*50)//1)+20,((round(mouse[1]/50)*50)//1)+20], 5)
     pygame.draw.line(screen, (255,0,0), 
                      [((round(mouse[0]/50)*50)//1)+20,((round(mouse[1]/50)*50)//1)-20],
                      [((round(mouse[0]/50)*50)//1)-20,((round(mouse[1]/50)*50)//1)+20], 5)

def addstation(locations): #for adding new stations
     if (49 < mouse[0] < X-99) and (99 < mouse[1] < Y-99): #if mouse is in bounds
          placement = []
          placement.append((round(mouse[0]/50)*50)//1) #adds the rounded locations of the mouse to temp list
          placement.append((round(mouse[1]/50)*50)//1) #is rounded so its on the grid
          if placement not in locations: #if its not overlapping
               if bank.getMoney() >= 100:
                    locations.append(placement) #take off money if you can afford it
                    bank.withdrawl(100)
               else:
                    showError() #if you cant afford it draw big red x

def removeStation(): #for removing stations
     if buttonover(stations) != -1: #make sure station is selected
          stationRaw = [(round(mouse[0]/50)*50)//1, (round(mouse[1]/50)*50)//1] #location of station
          for i in connections: #for every connection
               if buttonover(stations) in i: #if deleted station in in that connection
                    connections.remove(i) #remove it
                    bank.deposit(25) #refund money for it
          removeStationAllTrains(stationRaw) #removing it for all train's paths
          stations.remove(stationRaw) #remove it from the list
          bank.deposit(100) #refunds money

def showhover(): #shows a little grey circle over the grid location your mouse rounds to
     if (49 < mouse[0] < X-99) and (99 < mouse[1] < Y-99):
          pygame.draw.circle(screen, (200,200,200),
                       (((round(mouse[0]/50)*50)//1),
                        ((round(mouse[1]/50)*50)//1)), 7, 0)

def showTrainSelected(location): #shows the png image for which train you have selected
     file = "images\Trainselect"
     file += str(trainSelected) + ".png"
     if trainSelected > 8 or trainSelected < 0: #makes sure that input is correct and has a png image
          file = "images\placeholder.png"
     imp = pygame.image.load(file).convert() #draw the image
     screen.blit(imp, (location))
     

def showgrid(): #for showing the grid
     for i in range((X//50)-2):
          pygame.draw.line(screen, (200,200,200), #draw lines across the board and again in the other way etc
                           [(i*50)+50, 100], 
                           [(i*50)+50, Y-100], 3)
     for i in range((Y//50)-3):
          pygame.draw.line(screen, (200,200,200), 
                           [50,(i*50)+100], 
                           [X-100, (i*50)+100], 3)

def showmode(): #defunct
     pygame.draw.rect(screen, marker[0],
                    [X-60, 10, 20, 20], 0)
     if buildToggle:
          pygame.draw.rect(screen, greenlight,
                    [X-57, 13, 14, 14], 0)          
     elif editToggle:
          pygame.draw.rect(screen, bluelight,
                    [X-57, 13, 14, 14], 0)
     else:
          pygame.draw.rect(screen, redlight,
                    [X-57, 13, 14, 14], 0)   

def ifOverEdit(): #defunct
     if X-60 >= mouse[0] >= X-40 and 10 > mouse[1] > 30:
          return True
     else:
          return False

def countColours(): #counts the amount of colours youve used in your connections
     global colourlist
     plist = []
     for i in colourlist: #adds them to a temp list if theyre unique
          if i not in plist:
               plist.append(i)
     return len(plist) #returns amount of unique colours


def splashScreen():  #this displays the splash screen when you start up the game
     pygame.display.update()
     screen.fill(bgcolour)
     imp = pygame.image.load("Logo.png").convert() #loads the logo and waits for 3 seconds
     screen.blit(imp, (35,75))
     pygame.display.update()
     time.sleep(3)

def ProgressBar(xpos, ypos, amount, requirement): #for drawing the progress bars
     pygame.draw.rect(screen, ("#000000"),
                              [xpos, ypos, 200, 10], 0) #background of bar in loaction given
     if amount <= requirement: #if it is not full
          pygame.draw.rect(screen, ("#eeeeee"),
                              [xpos+2, ypos+2, 196, 6], 0) #draw white space in bar
          pygame.draw.rect(screen, ("#0fb42a"),
                              [xpos+2, ypos+2, ((amount/requirement)*196), 6], 0) #draw progress bar relative to size of the bar
     else:
          pygame.draw.rect(screen, ("#0fb42a"),
                              [xpos+2, ypos+2, 196, 6], 0) #if requirements are met or past met draw bar full

def trainsOwnedCount(): #for each train check if its bought and if so add it to total and return it
     number = 0
     if Train1.bought:
          number += 1
     if Train2.bought:
          number += 1
     if Train3.bought:
          number += 1
     if Train4.bought:
          number += 1
     if Train5.bought:
          number += 1
     if Train6.bought:
          number += 1
     if Train7.bought:
          number += 1
     if Train8.bought:
          number += 1
     return number

pageSheet = [[["Obtain 500 Money","Obtain 1000 Money","Obtain 2000 Money","Obtain 5000 Money","Purchase 1 Train"], #text (description)
              [TotalMoney,TotalMoney,TotalMoney,TotalMoney, TotalTrains], #input
              [500,1000,2000,5000,1], #requirement
              ["M1","M2","M3","M4","T1"]], #images (letternumber)
             [["Purchase 4 Trains","Purchase 8 Trains","Build 1 Connection","Build 5 Connections","Build 10 Connections"],
              [TotalTrains,TotalTrains, TotalConnections, TotalConnections, TotalConnections],
              [4,8,1,5,10],
              ["T2","T3","C1","C2","C3"]],
             [["Build 20 Connections","Use 2 Different Colours","Use All The Colours","Upgrade Capacity","Max Out Capacity"],
              [TotalConnections, countColours(),countColours(),Train1.upgradelvl-1,Train1.upgradelvl-1 ],
              [20,2,8,1,5],
              ["C4","C5","C6","U1","U2"]],
             [["Upgrade Speed","Max Out Speed","Secret Achievement","Build 1 Station","Build 3 Stations"],
              [Train1.speed-3,Train1.speed-3,secretFound,TotalStations,TotalStations],
              [1,5,1,1,3],
              ["U3","U4","Secret","S1","S2"]],
             [["Build 5 Stations","Build 10 Stations","Obtain 25000 Money","Build 50 Conncetions","Purchase 40 Trains"],
              [TotalStations,TotalStations,TotalMoney,TotalConnections,TotalTrains],
              [5,10,25000,50,40],
              ["S3","S4","G1","G2","G3"]]]

#3d list with all achievement info for displaying on the page
#in the order of Page, Attributes, Achievements
#Attributes are: Description, current stat input, requirement, image reference

def updatePageSheet(): #for updating the 3d list with current stats
     global pageSheet
     pageSheet[0][1] = [TotalMoney+bank.getMoney(),TotalMoney+bank.getMoney(),TotalMoney+bank.getMoney(),TotalMoney+bank.getMoney(), TotalTrains+trainsOwnedCount()]
     pageSheet[1][1] = [TotalTrains+trainsOwnedCount(),TotalTrains+trainsOwnedCount(), TotalConnections+len(connections), TotalConnections+len(connections), TotalConnections+len(connections)]
     pageSheet[2][1] = [TotalConnections+len(connections), countColours(),countColours(),Train1.upgradelvl-1,Train1.upgradelvl-1 ]
     pageSheet[3][1] = [Train1.speed-1,Train1.speed-1,secretFound,TotalStations+len(stations),TotalStations+len(stations)]
     pageSheet[4][1] = [TotalStations+len(stations),TotalStations+len(stations),TotalMoney+bank.getMoney(),TotalConnections+len(connections),TotalTrains+trainsOwnedCount()]

page = 0
def ShowAchievementScreen():
     if AchievementScreen: #if the screen is open
          global page
          pygame.draw.rect(screen, ("#000000"),
                              [10, 10, X-20, Y-20], 0) #draw bounding box for page
          pygame.draw.rect(screen, ("#eeeeee"),
                              [15, 15, X-30, Y-30], 0)
          imp = pygame.image.load("images\GuiGoBack.png").convert() #draw button image for going back a page
          screen.blit(imp, (340, 20))
          imp = pygame.image.load("images\GuiForward.png").convert() #draw button image for going forward a page
          screen.blit(imp, (310, 330))
          imp = pygame.image.load("images\GuiBack.png").convert() #draw button image for exiting achievement screen
          screen.blit(imp, (50, 330))
          textline = tflFont.render(("Achievements Screen"),True , ("#000000")) #display title for page
          screen.blit(textline , (50,50))
          AchievementPage(pageSheet[page][0],pageSheet[page][1],pageSheet[page][2],pageSheet[page][3]) #display info on achievements with subroutine below
               
def AchievementPage(texts,amounts,requirements,images): #uses inputs from page sheet
     for i in range(5): #draws 5 per screen
          textline = tflFont.render((texts[i]),True , ("#000000")) #draw description
          screen.blit(textline , (100,80+(i*50)))
          if achievementsGot[i+(page*5)] == "0":
               imp = pygame.image.load("images\AchievementSecret2.png").convert() #if achievement is locked draw lock icon
               screen.blit(imp, (50, 80+(i*50)))
               ProgressBar(100, 110+(i*50), amounts[i], requirements[i]) #draw progress bar as normal
          else:
               imp = pygame.image.load("images\Achievement" + images[i] + ".png").convert() #if unlocked draw icon for that achievement
               screen.blit(imp, (50, 80+(i*50)))
               ProgressBar(100, 110+(i*50), 1, 1) #draw progress bar as full

def addAchievement(number): #for setting specific achievements to the achieved state
     global achievementsGot
     plist = []
     output = ""
     for i in achievementsGot: #turns string into list containing all characters
          plist.append(i)
     plist[number] = "1" #assign index for achievement as collected
     for i in plist:
          output += i #turn list back into string
     return output #this must be done to assign index's value in a string

def DetectAch(): #for telling when an achievement is collected
     global achievementsGot
     for i in range(5): #per page
          for j in range(5): #per achievement
               if achievementsGot[(j)+(i*5)] == "0": #if its not already collected
                    if pageSheet[i][1][j] >=  pageSheet[i][2][j]: #check if requirements are met by referencing the 3d list from before
                         achievementsGot = addAchievement((j)+(i*5)) #use previous subroutine to update index for achievement

def Date(): #for recording and formatting the date
     date = ""
     for i in range(3): #for day month and year
         if i != 2 and len(str(time.gmtime()[2-i])) == 1: #if it is a day or month 1 digit long
             date += "0" + str(time.gmtime()[2-i]) #add a leading 0
         else:
             date += str(time.gmtime()[2-i]) #if it is a 2 digit day or month or is the year, add as normal
         date += "/" #add / for format
     date = date[0:len(date)-1] #get rid of ending /
     return date

def ShowPausedScreen(): 
     if pauseScreen:
          pygame.draw.rect(screen, ("#000000"),
                              [90, 165, 220, 70], 0) #draw box for pause screen
          pygame.draw.rect(screen, ("#eeeeee"),
                              [95, 170, 210, 60], 0)
          imp = pygame.image.load("images\GuiGear.png").convert() #display button image for controlls page
          screen.blit(imp, (105, 180))
          imp = pygame.image.load("images\GuiHelp.png").convert() #display button image for languages page (not used)
          screen.blit(imp, (155, 180))
          imp = pygame.image.load("images\GuiTrophy.png").convert() #display button image for achievements page
          screen.blit(imp, (205, 180))
          imp = pygame.image.load("images\GuiGoBack.png").convert() #display button image for exiting pause screen
          screen.blit(imp, (255, 180))

def controlsDisplay(): #showing controlls screen
     lines = ["Pause","Cycle Colour","Toggle Build Mode","Toggle Grid Display","Toggle Edit Mode","Save Score And Quit","Train Menu","Select Train"] #actions
     buttons = ["P","C","B","G","E","Esc","T","0"] #buttons indexes
     if controllScreen:
          pygame.draw.rect(screen, ("#000000"), #draw box for controlls screen
                    [20, 5, X-40, Y-10], 0)
          pygame.draw.rect(screen, ("#eeeeee"),
                    [25, 10, X-50, Y-20], 0)
          for i in range(len(lines)): #for each line
               file = "images\Buttons" #adds prefix
               file += buttons[i] + ".png" #adds index and suffix
               imp1 = pygame.image.load(file).convert() #loads the image for the button
               screen.blit(imp1, (50,22+(i*45))) #on the correct line
               pausetextline = tflFont.render((lines[i]),True , ("#000000")) #draw the description of what the button does from the list
               screen.blit(pausetextline , (100,32+(i*45))) #on the correct line
          imp = pygame.image.load("images\GuiGoBack.png").convert() #draw button for exiting the controlls screen
          screen.blit(imp, (330, 15))

def MoneyDisplay(): #for displaying current balance
     imp = pygame.image.load("images\MoneyNote.png").convert() #draw the background of the money display
     screen.blit(imp, (5,0))
     money = 0
     money = bank.getMoney() #get the current value
     for i in range(len(str(money))): #for each digit
          file = "images\BackgroundNotepad" #add prefix
          file += str(money)[i] + ".png" #add the digit and the suffix
          imp1 = pygame.image.load(file).convert() #draw the image for that digit
          screen.blit(imp1, ((15+(20*i)+i),11)) #in the correct place


#P = Pause\nC = Cycle Colour\nB = Toggle Build Mode\nG = Toggle Grid Display\nE = Toggle Edit Mode\nEsc = Save Score And Quit
helpPage = 0 #page which the help screen is on

linesList = [["Help Screen","Stations","Connections","Routes","Trains","Upgrades"],
             ["Stations Help","Click to build station (100)","Toggles Delete mode","Click station to delete","Toggles Grid","Can only guild on Grid"],
             ["Connections Help","Click on first Station","Click on second station","Or click first to cancel","Costs 25","Change colour with C",],
             ["Routing Help","Select Train With Keys 1-8","Click station to add","Toggles Route Visability","Removes Last station","Deletes Route"],
             ["Train Help","Max of 8 Trains","Trains Cost 200","Refunds Train purchase","Can only select train","If you own it"],
             ["Upgrades Help","Upgrades Selected Train","Upgrades increase in price","Upgrades Train Capacity","Also increases sales","Upgrades Train Speed"]] #list of lines
imageList = [["None","Build","Connector","Conduct","Train","Upgrade"],
             ["None","Build","Undo","None","Grid","None"],
             ["None","Connector","None","Undo","None","None"],
             ["None","Train","Conduct","Path","Undo","Delete"],
             ["None","Train","None","Undo","None","None"],
             ["None","Upgrade","None","Purple","None","Yellow"]] #list of images

def ShowHelpScreen(page):
     if helpScreen:
          pygame.draw.rect(screen, ("#000000"),
                              [10, 10, X-20, Y-20], 0) #draw bounding box for page
          pygame.draw.rect(screen, ("#eeeeee"),
                              [15, 15, X-30, Y-30], 0)
          global linesList
          global imageList
          for i in range(len(linesList)): #for every line and image (both lists are same length)
               if imageList[page][i] != "None": #if there is an image
                    location = "images\Gui" + imageList[page][i] + ".png" #make file location string for each image in list
                    imp = pygame.image.load(location).convert() #draw button image for line 
                    screen.blit(imp, (50,30+(60*i))) 
               helptextline = tflFont.render((linesList[page][i]),True , ("#000000")) #draw title
               screen.blit(helptextline , (100,40+(60*i)))
          
          if page == 0:
               imp = pygame.image.load("images\GuiGoBack.png").convert() #draw button image for exititng the help screen
          else:
               imp = pygame.image.load("images\GuiUndo.png").convert() #draw button image for going back
          screen.blit(imp, (340, 20))   

def BuyTrainScreen():
     if trainScreen: #if the train screen is open
          colour1 = "#008000"
          colour2 = "#50ff50"
          colour3 = "#00ff00"
          
          if trainsOwnedCount() == 8: #if you have the max trains have the colours as red versions
               colour1 = "#800000"
               colour2 = "#ff5050"
               colour3 = "#ff0000"

          pygame.draw.rect(screen, ("#000000"), #draw the box for the train screen
                         [10, 10, X-20, Y-20], 0)
          pygame.draw.rect(screen, ("#eeeeee"),
                         [15, 15, X-30, Y-30], 0)
          traintextline = tflFont.render(("Train Screen"),True , ("#000000")) #draw title
          screen.blit(traintextline , (50,50))
          showTrainSelected((295,20)) #draw the indicator image on the page
          traintextline = tflFont.render(("Trains Owned : " + str(trainsOwnedCount()) + "/8"),True , ("#000000")) #for showing how many you have
          screen.blit(traintextline , (50,87))
          traintextline = tflFont.render(("Buy Train for 200"),True , ("#000000")) #title of what the button does
          screen.blit(traintextline , (50,122))
          pygame.draw.rect(screen, ("#000000"), #draw box for train buy button
                         [50, 150, 100, 100], 0)
          if 50 <= mouse[0] <= 150 and 150 <= mouse[1] <= 250: #if mouse is hovering over the button
               pygame.draw.rect(screen, (colour1), #draw shadow
                         [55, 155, 90, 90], 0)
               pygame.draw.rect(screen, (colour2), #draw lighter colour
                         [57, 157, 88, 88], 0)
          else:
               pygame.draw.rect(screen, (colour3), #draw normal colour for the button
                         [55, 155, 90, 90], 0)
          imp = pygame.image.load("images\GuiGoBack.png").convert() #draw button image for exititng the train screen
          screen.blit(imp, (340, 20))
          imp = pygame.image.load("images\GuiUndo.png").convert() #draw button image for undoing train purchase
          screen.blit(imp, (340, 100))

checker = False
checkere = ""

def ShowUpgradeScreen(): #for showing the upgrades screen
     if upgradeScreen: #if the upgrade screen is open
          pygame.draw.rect(screen, ("#000000"),
                              [10, 10, X-20, Y-20], 0)
          pygame.draw.rect(screen, ("#eeeeee"),
                              [15, 15, X-30, Y-30], 0) #draw the box for the screen
          
          if trainsOwnedCount() == 0:
               textline = tflFont.render(("Buy a Train by pressing (T)"),True , ("#000000")) #if you do not own any trains
          elif trainSelected == 0:
               textline = tflFont.render(("Select a Train by pressing (0-9)"),True , ("#000000")) #if no train is selected
          else:
               textline = tflFont.render(("Upgrade Train Number " + str(trainSelected)),True , ("#000000")) #if theres one selected
          screen.blit(textline , (50,50))
          
          pygame.draw.rect(screen, ("#000000"), #draw box for buttons
                              [50, 100, 300, 150], 0)
          if 60 < mouse[0] < 195 and 110 < mouse[1] < 240:
               pygame.draw.rect(screen, ("#6F00AF"), #if mouse is over draw colour lighter
                              [60, 110, 135, 130], 0)
          else:
               pygame.draw.rect(screen, ("#3C005F"), #if not draw noramlly
                                   [60, 110, 135, 130], 0)
          if 205 < mouse[0] < 340 and 110 < mouse[1] < 240:
               pygame.draw.rect(screen, ("#F7C43A"), #if mouse is over draw colour lighter
                              [205, 110, 135, 130], 0)
          else:
               pygame.draw.rect(screen, ("#E7AA00"), #if not draw normally
                                   [205, 110, 135, 130], 0)
          pygame.draw.rect(screen, ("#000000"), #draw background for text
                              [50, 270, 300, 100], 0)
          capacitytextline = tflFont.render(("Capacity Level " + str(TrainGrabber("C",trainSelected)) + "/5 Cost :" + str(costGrabber(trainSelected)[0])),True , ("#3C005F")) #display the current upgrade level and the max and the cost
          speedtextline = tflFont.render(("Speed Level " + str(TrainGrabber("S",trainSelected)) + "/5 Cost :" + str(costGrabber(trainSelected)[1])),True , ("#E7AA00")) #display the current upgrade level and the max and the cost
          screen.blit(capacitytextline , (80,290))
          screen.blit(speedtextline , (80,330))
          imp = pygame.image.load("images\GuiGoBack.png").convert() #display the back button
          screen.blit(imp, (340, 20))

def TopBar(): #shows the images for the gui
     imp = pygame.image.load("images\GuiBuild.png").convert() #build button
     screen.blit(imp, (130, 7))
     imp = pygame.image.load("images\GuiConnector.png").convert() #connect mode button
     screen.blit(imp, (174, 7))
     imp = pygame.image.load("images\GuiConduct.png").convert() #conductor mode button
     screen.blit(imp, (218, 7))
     imp = pygame.image.load("images\GuiTrain.png").convert() #train screen button
     screen.blit(imp, (262, 7))
     imp = pygame.image.load("images\GuiUpgrade.png").convert() #upgrade screen button
     screen.blit(imp, (306, 7))
     imp = pygame.image.load("images\GuiPause.png").convert() #pause button
     screen.blit(imp, (350, 7))

def sideBar(): #side bar for conductor mode
     global buildToggle
     global editToggle
     if buildToggle: # if build mode is on
          if deleteToggle: #if delete mode is on
               imp = pygame.image.load("images\GuiUndoRed.png").convert() #undo path button red
               screen.blit(imp, (350, 130))
          else: #if not
               imp = pygame.image.load("images\GuiUndo.png").convert() #undo path button default
               screen.blit(imp, (350, 130))
          imp = pygame.image.load("images\GuiGrid.png").convert() #draw the toggle grid button
          screen.blit(imp, (350, 180))
     elif editToggle: #if conductor mode (edit mode) is on
          imp = pygame.image.load("images\GuiUndo.png").convert() #undo path button
          screen.blit(imp, (350, 130))
          imp = pygame.image.load("images\GuiDelete.png").convert() #delete path button
          screen.blit(imp, (350, 180))
          imp = pygame.image.load("images\GuiPath.png").convert() #show path button
          screen.blit(imp, (350, 230))

def checkbool(number,pin): #this was just used for debug
     if pin:
          pygame.draw.rect(screen, ("#2FCA00"),
                              [200 + 30*number, 200, 20, 20], 0)
     else:
          pygame.draw.rect(screen, ("#CA0000"),
                              [200 + 30*number, 200, 20, 20], 0)
 
def GuiButtonOver(): #for clicking on the top bar buttons
     global trainScreen
     global upgradeScreen
     global pauseScreen #load all these variables
     global editToggle
     global buildToggle
     if not trainScreen and not upgradeScreen and not pauseScreen and cooldown: #if these 3 screens are closed and the cooldown is over
          number = 0
          if 7 < mouse[1] < 47: #if the mouse is on the correct y level
               if 130 < mouse[0] < 170: #goes through each button location and sets a number for each
                    number =  1
               elif 174 < mouse[0] < 214:
                    number =  2
               elif 218 < mouse[0] < 258:
                    number =  3
               elif 262 < mouse[0] < 302:
                    number =  4
               elif 306 < mouse[0] < 346:
                    number =  5
               elif 350 < mouse[0] < 396:
                    number = 6

          if number != 0: #if a button was clicked disable each mode so only one mode is enabled at a time
               trainScreen = False
               upgradeScreen = False
               pauseScreen = False
               buildToggle = False
               editToggle = False

               if number == 1: #for each number make that buttons mode be enabled
                    buildToggle = True
               if number == 2:
                    pass #since the connection mode is default it doesnt enable any mode
               elif number == 3:
                    editToggle = True
               elif number == 4:
                    trainScreen = True
               elif number == 5:
                    upgradeScreen = True
               elif number == 6:
                    pauseScreen = True

def cutIt(number): #takes input and does this subroutine for that object
     if number == 1:
          Train1.cutPath() #this is for removing the end of a path (line 539)
     if number == 2:
          Train2.cutPath()
     if number == 3:
          Train3.cutPath()
     if number == 4:
          Train4.cutPath()
     if number == 5:
          Train5.cutPath()
     if number == 6:
          Train6.cutPath()
     if number == 7:
          Train7.cutPath()
     if number == 8:
          Train8.cutPath()

def delIt(number): #takes input and does this subroutine for that object
     if number == 1:
          Train1.delPath() #this is for removing the path (line 603)
     if number == 2:
          Train2.delPath()
     if number == 3:
          Train3.delPath()
     if number == 4:
          Train4.delPath()
     if number == 5:
          Train5.delPath()
     if number == 6:
          Train6.delPath()
     if number == 7:
          Train7.delPath()
     if number == 8:
          Train8.delPath()

def showIt(number): #if the show path button was clicked, takes input and does this subroutine for that object
     if showPathToggle:
          if number == 1:
               Train1.showPath() #this is for displaying the current path of the object (line 560)
          if number == 2:
               Train2.showPath()
          if number == 3:
               Train3.showPath()
          if number == 4:
               Train4.showPath()
          if number == 5:
               Train5.showPath()
          if number == 6:
               Train6.showPath()
          if number == 7:
               Train7.showPath()
          if number == 8:
               Train8.showPath()

def costGrabber(number): #takes input and returns that object's cost attribute and if none selected return 0 to not crash
     if number == 1:
          return Train1.cost
     if number == 2:
          return Train2.cost
     if number == 3:
          return Train3.cost
     if number == 4:
          return Train4.cost
     if number == 5:
          return Train5.cost
     if number == 6:
          return Train6.cost
     if number == 7:
          return Train7.cost
     if number == 8:
          return Train8.cost
     if number == 0:
          return [0,0]

def Upgrader(number): #if the cooldown is over, takes input and does this subroutine for that object then restarts the cooldown
     global cooldown
     if cooldown:
          if number == 1:
               Train1.upgrade() #this is for upgrading the train (line 672)
          if number == 2:
               Train2.upgrade()
          if number == 3:
               Train3.upgrade()
          if number == 4:
               Train4.upgrade()
          if number == 5:
               Train5.upgrade()
          if number == 6:
               Train6.upgrade()
          if number == 7:
               Train7.upgrade()
          if number == 8:
               Train8.upgrade()
          cooldown = False

def TrainGrabber(choice,number): #returns either the speed or upgradelvl attribute according to the choice parameter of the object given by the number parapeter
     if number == 1:
          if choice == "S":
               return Train1.speed
          elif choice == "C":
               return Train1.upgradelvl
     if number == 2:
          if choice == "S":
               return Train2.speed
          elif choice == "C":
               return Train2.upgradelvl
     if number == 3:
          if choice == "S":
               return Train3.speed
          elif choice == "C":
               return Train3.upgradelvl
     if number == 4:
          if choice == "S":
               return Train4.speed
          elif choice == "C":
               return Train4.upgradelvl
     if number == 5:
          if choice == "S":
               return Train5.speed
          elif choice == "C":
               return Train5.upgradelvl
     if number == 6:
          if choice == "S":
               return Train6.speed
          elif choice == "C":
               return Train6.upgradelvl
     if number == 7:
          if choice == "S":
               return Train7.speed
          elif choice == "C":
               return Train7.upgradelvl
     if number == 8:
          if choice == "S":
               return Train8.speed
          elif choice == "C":
               return Train8.upgradelvl
     if number == 0: #return 0 if nothing selected to not crash
          return 0

def buyNewTrain(): #runs this subroutine for this object if the cooldown is over and you dont have the max amount of trains
     global cooldown
     if trainsOwnedCount() != 8 and cooldown:
          cooldown = False
          if trainsOwnedCount() == 0:
               Train1.buy() #this is for taking the money owed and setting the object's attribute to true (line 567)
          elif trainsOwnedCount() == 1:
               Train2.buy()
          elif trainsOwnedCount() == 2:
               Train3.buy()
          elif trainsOwnedCount() == 3:
               Train4.buy()
          elif trainsOwnedCount() == 4:
               Train5.buy()
          elif trainsOwnedCount() == 5:
               Train6.buy()
          elif trainsOwnedCount() == 6:
               Train7.buy()
          elif trainsOwnedCount() == 7:
               Train8.buy()

def UndoTrain(): #runs this subroutine for this object if the cooldown is over and you have a train
     global cooldown
     if trainsOwnedCount() != 0 and cooldown:
          cooldown = False
          if trainsOwnedCount() == 1:
               Train1.sell() #this is for giving back money and making train unavaliable
          elif trainsOwnedCount() == 2:
               Train2.sell()
          elif trainsOwnedCount() == 3:
               Train3.sell()
          elif trainsOwnedCount() == 4:
               Train4.sell()
          elif trainsOwnedCount() == 5:
               Train5.sell()
          elif trainsOwnedCount() == 6:
               Train6.sell()
          elif trainsOwnedCount() == 7:
               Train7.sell()
          elif trainsOwnedCount() == 8:
               Train8.sell()

def addingToThePath(number): #runs this subroutine for the object given by the number parameter
     if number == 1: #goes through each number
          Train1.addToPath() #this adds a station to the path (line 572)
          if len(Train1.path) == 1: #if the train's path now has 1 item
               Train1.storageToggle = False #move the train out of storage
     if number == 2:
          Train2.addToPath()
          if len(Train2.path) == 1:
               Train2.storageToggle = False
     if number == 3:
          Train3.addToPath()
          if len(Train3.path) == 1:
               Train3.storageToggle = False
     if number == 4:
          Train4.addToPath()
          if len(Train4.path) == 1:
               Train4.storageToggle = False
     if number == 5:
          Train5.addToPath()
          if len(Train5.path) == 1:
               Train5.storageToggle = False
     if number == 6:
          Train6.addToPath()
          if len(Train6.path) == 1:
               Train6.storageToggle = False
     if number == 7:
          Train7.addToPath()
          if len(Train7.path) == 1:
               Train7.storageToggle = False
     if number == 8:
          Train8.addToPath()
          if len(Train8.path) == 1:
               Train8.storageToggle = False

def removeStationAllTrains(station): #does this subroutine for each object
     if station in Train1.path : Train1.delPath() #deletes paths with deleted station
     if station in Train2.path : Train2.delPath()
     if station in Train3.path : Train3.delPath()
     if station in Train4.path : Train4.delPath()
     if station in Train5.path : Train5.delPath()
     if station in Train6.path : Train6.delPath()
     if station in Train7.path : Train7.delPath()
     if station in Train8.path : Train8.delPath()

def showAllTrains(): #does this subroutine for each object
     Train1.showTrain() #this is for showing the position of the train (line 555)
     Train2.showTrain()
     Train3.showTrain()
     Train4.showTrain()
     Train5.showTrain()
     Train6.showTrain()
     Train7.showTrain()
     Train8.showTrain()

def moveAllTrains(): #does this subroutine for each object
     if not Train1.storageToggle: Train1.move() #this is for moving the train along the path (line 611)
     if not Train2.storageToggle: Train2.move()
     if not Train3.storageToggle: Train3.move()
     if not Train4.storageToggle: Train4.move()
     if not Train5.storageToggle: Train5.move()
     if not Train6.storageToggle: Train6.move()
     if not Train7.storageToggle: Train7.move()
     if not Train8.storageToggle: Train8.move()

def offOnloadAll(): #does this subroutine for each object
     Train1.offonload() #this is for onloading and offloading apssengers and giving money (line 564)
     Train2.offonload()
     Train3.offonload()
     Train4.offonload()
     Train5.offonload()
     Train6.offonload()
     Train7.offonload()
     Train8.offonload()

def Score(): #this calculates the player's score
     return (bank.getMoney() + (len(stations)*50) + ((len(connections)*50))) # money + (50 x stations) + (50 x stations)

trainlist = []

def setStats():
     global trainlist
     trainlist = [(Train1.upgradelvl*10 + Train1.speed),
                  (Train2.upgradelvl*10 + Train2.speed),
                  (Train3.upgradelvl*10 + Train3.speed),
                  (Train4.upgradelvl*10 + Train4.speed),
                  (Train5.upgradelvl*10 + Train5.speed),
                  (Train6.upgradelvl*10 + Train6.speed),
                  (Train7.upgradelvl*10 + Train7.speed),
                  (Train8.upgradelvl*10 + Train8.speed)]

def saveStats(): #this is for saving the stats to the database
     global trainlist
     setStats()
     cursor.execute("INSERT INTO Stats(Username, Score, Date, Stations, Connections, Trains, Money) VALUES(?, ?, ?, ?, ?, ?, ?)",(CurrentUsername, Score(), Date(), len(stations), len(connections), trainsOwnedCount(), bank.getMoney()))
     db.commit() #inserts new row into the table Stats
     cursor.execute("INSERT INTO TrainStats(Username, Train1, Train2, Train3, Train4, Train5, Train6, Train7, Train8) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",(CurrentUsername, trainlist[0], trainlist[1], trainlist[2], trainlist[3], trainlist[4], trainlist[5], trainlist[6], trainlist[7]))
     db.commit() #inserts new row into the table TrainStats with upgrade levels for trains in an integer of length 2 where first digit is capacity and second digit is speed

def saveAchievements(): #this is for saving which achievements a player has collected
     global GlobalUsername
     
     cursor.execute("UPDATE Achievements SET Username =?, TotalConnections =?, TotalStations =?, TotalTrains =?, AchievementsGot =?, TotalMoney =? WHERE Username=?", (CurrentUsername,TotalConnections+len(connections),TotalStations+len(stations),TotalTrains+trainsOwnedCount(),achievementsGot,TotalMoney+bank.getMoney(),CurrentUsername))
     db.commit() #updates the row of the player where the username matches and updates it with the the values provided here

# assigning values to X and Y variable for the screen
X = 400
Y = 400

screen = pygame.display.set_mode((X, Y)) #draw the pygame window
pygame.display.set_caption('Train Game') #give it this title

# infinite loop

splashScreen() #draw the splash screen first

makeit = False #debugging

while not Quiting: #while you havent selected quit
     for event in pygame.event.get(): #for each event
          if event.type == pygame.QUIT: #if it is quit
               pygame.quit #do so
               quit()
          if event.type == pygame.MOUSEBUTTONDOWN: #if player has clicked
               
               if not pauseScreen and not helpScreen and not trainScreen and not upgradeScreen: #if not in any screen that appears infornt of gui
                    if not buildToggle and not editToggle: #if youre on the connection mode (default)
                         makeConnection()

                    if checkmenucollision(colourfeed) != -1: #if mouse is over a colour button
                         colourselected = checkmenucollision(colourfeed) #change the selected colour to that one

                    if buildToggle: #if build mode is on
                         if 350 < mouse[0] < 390 and 130 < mouse[1] < 170: #if mouse is over the undo button
                              if cooldown:#if cooldown is over
                                   deleteToggle = not deleteToggle #toggle delete mode  
                         if 350 < mouse[0] < 390 and 180 < mouse[1] < 220: #if mouse is over the grid button
                              gridToggle = not gridToggle #toggle the grid mode
                         else:
                              if deleteToggle and cooldown: #if deleme mode is on and cooldown is over
                                   removeStation() #remove that station
                              else:
                                   addstation(stations) #build a station 

                    if editToggle: #if edit mode is on
                         if 350 < mouse[0] < 390 and 130 < mouse[1] < 170: #if mouse is over the undo button
                              cutIt(trainSelected) #remove the end item from the path
                         if 350 < mouse[0] < 390 and 180 < mouse[1] < 220: #if mouse is over the delete button
                              delIt(trainSelected) #remove the path
                         if 350 < mouse[0] < 390 and 230 < mouse[1] < 270: #if mouse is over the show path button
                              showPathToggle = not showPathToggle #toggle the show path variable
                         else:
                              addingToThePath(trainSelected) #if not over a button then add this station to the path
               
               if trainScreen: #if train screen is open
                    if 50 <= mouse[0] <= 150 and 150 <= mouse[1] <= 250: #if mouse is over the buy train button
                         buyNewTrain() #buy a train
                    elif 340 < mouse[0] < 380 and 100 < mouse[1] < 140: #if mouse over undo button
                         UndoTrain()# undo train purchase
                    elif 340 < mouse[0] < 380 and 20 < mouse[1] < 60: #if mouse over back button
                         trainScreen = False #close the train screen
                         cooldown = False #restart the cooldown
                    

               if upgradeScreen: #if upgrade screen is open
                    if 60 < mouse[0] < 195 and 110 < mouse[1] < 240 and trainSelected != 0: #if mouse is over an upgrade button and a train is selected
                         Upgrader(trainSelected) #upgrade that train
                    elif 205 < mouse[0] < 340 and 110 < mouse[1] < 240 and trainSelected != 0: #if mouse is over the other upgrade button and a train is selected
                         Upgrader(trainSelected) #upgrade that train
                    elif 340 < mouse[0] < 380 and 20 < mouse[1] < 60: #if mouse is over the back button
                         upgradeScreen = False #close the screen
                         cooldown = False #restart the cooldown
               
               if pauseScreen: #if the pause screen is open
                    if 180 < mouse[1] < 220: #if mouse is on correct y level
                         if 105 < mouse[0] < 145: #if mouse over controlls button
                              controllScreen = True #open controlls screen
                         if 155 < mouse[0] < 195: #if mouse over help button
                              helpScreen = True
                         if 205 < mouse[0] < 245: #if mouse over achievement button
                              AchievementScreen = True #open achievements screen
                              page = 0 #to the first page
                         if 255 < mouse[0] < 295: #if mouse over back button
                              pauseScreen = False #close the screen
                    cooldown = False #restart cooldown

               if controllScreen: #if controll screen is open
                    if 330 < mouse[0] < 370 and 15 < mouse[1] < 55: #if mouse is over back button
                         controllScreen = False #close the screen
               
               if helpScreen: #if help screen is open
                    if helpPage == 0:
                         if 50 < mouse[0] < 90 and 90 < mouse[1] < 130: #if mouse over build button
                              helpPage = 1 #go to that page
                         if 50 < mouse[0] < 90 and 150 < mouse[1] < 190: #if mouse over connections button
                              helpPage = 2 #go to that page
                         if 50 < mouse[0] < 90 and 210 < mouse[1] < 250: #if mouse over routes button
                              helpPage = 3 #go to that page
                         if 50 < mouse[0] < 90 and 270 < mouse[1] < 310: #if mouse over trains button
                              helpPage = 4 #go to that page
                         if 50 < mouse[0] < 90 and 330 < mouse[1] < 370: #if mouse over upgrades button
                              helpPage = 5 #go to that page
                         if 340 < mouse[0] < 380 and 20 < mouse[1] < 60: #if mouse over back button
                              helpScreen = False #close the help screen
                              cooldown = False #restart the cooldown
                    else:
                         if 340 < mouse[0] < 380 and 20 < mouse[1] < 60: #if mouse over back button
                              helpPage = 0 #go back to first page

               
               if AchievementScreen: #if achievement screen is open
                    if 340 < mouse[0] < 380 and 20 < mouse[1] < 60: #if mouse over back button
                         AchievementScreen = False #close screen
                         cooldown = False #restart cooldown
                    if 310 < mouse[0] < 350 and 330 < mouse[1] < 370: #if mouse over go forward button
                         if page != 4: #and if not on last page
                              page += 1 #go to next page
                    if 50 < mouse[0] < 90 and 330 < mouse[1] < 370: #if mouse over the go back button
                         if page != 0: #if page isnt the first one
                              page -= 1 #go back a page

               GuiButtonOver() #run the function defined on line 1183

          if event.type == pygame.KEYDOWN: #if a keyboard button is pressed
               
               if event.key == pygame.K_0: #if button is 0
                    trainSelected = 0 #deselect train
               if event.key == pygame.K_1: #for each number to 8
                    if Train1.bought: #if it is bought
                         trainSelected = 1 #set selected train to that number
               if event.key == pygame.K_2: 
                    if Train2.bought:
                         trainSelected = 2
               if event.key == pygame.K_3: 
                    if Train3.bought:
                         trainSelected = 3
               if event.key == pygame.K_4: 
                    if Train4.bought:
                         trainSelected = 4
               if event.key == pygame.K_5: 
                    if Train5.bought:
                         trainSelected = 5
               if event.key == pygame.K_6: 
                    if Train6.bought:
                         trainSelected = 6
               if event.key == pygame.K_7: 
                    if Train7.bought:
                         trainSelected = 7
               if event.key == pygame.K_8: 
                    if Train8.bought:
                         trainSelected = 8
               
               if event.key == pygame.K_c: #if c is pressed
                    colourselected = changecolours(colourselected, colourfeed) #cycle through the colours
               elif event.key == pygame.K_g: #if g is pressed
                    gridToggle = not gridToggle #toggle the grid
               elif event.key == pygame.K_s: #if s is pressed
                    secretmode = not secretmode #toggle secret mode
                    secretFound = 1 #once it is enabled this is set to 1 for the achievement
               elif event.key == pygame.K_p: #if p is pressed
                    pauseScreen = not pauseScreen #toggle the pause screen
               elif event.key == pygame.K_b: #if b is pressed
                    editToggle = False #disable edit mode
                    buildToggle = not buildToggle #toggle the build mode
               elif event.key == pygame.K_t: #if t is pressed
                    if not pauseScreen: #if pause screen is closed
                         trainScreen = not trainScreen #toggle train screen
                         upgradeScreen = False #close upgrade screen
                         AchievementScreen = False #close achievement screen
               elif event.key == pygame.K_u: #if u is pressed
                    if not pauseScreen: #if pause screen is closed
                         upgradeScreen = not upgradeScreen #toggle upggrade screen
                         trainScreen = False #close train screen
                         AchievementScreen = False #close achievement screen
               elif event.key == pygame.K_a: #if a is pressed
                    if not pauseScreen: #if pause screen is closed
                         AchievementScreen = not AchievementScreen #toggle achievements screen
                         trainScreen = False #close train screen
                         upgradeScreen = False #close upgrade screen
               elif event.key == pygame.K_e: #if e is pressed
                    buildToggle = False #exit build mode
                    editToggle = not editToggle #toggle edit mode
               elif event.key == pygame.K_ESCAPE: #if Esc is pressed
                    Quiting = True #exit this while loop
                    if IsLoggedIn: #if youre logged in
                         saveStats() #does what it looks like
                         saveAchievements()
          
          if event.type != pygame.MOUSEBUTTONDOWN: #if mouse is not pressed
               cooldown = True #end the cooldown (stops accidental clicks from held mouse input)

     screen.fill(bgcolour) #clear the screen
     mouse = pygame.mouse.get_pos() #get the location of the mouse cursor
     if gridToggle: #if grid is toggled
         showgrid() #does what it says
     if buildToggle and gridToggle: #if build mode is on and grid is too
         showhover() #show hover for where station would be placed
     connect(connections,stations,colourfeed) #connect up the stations with connections with correct colours
     showIt(trainSelected) #show the train selected's path
     drawall(stations,marker) #draw all stations
     drawmenu() #show the menu
     DetectAch() #check for achievements collected
     showTrainSelected((350,350)) #display image in corner for selected train
     showAllTrains() #does what it says
     moveAllTrains()
     offOnloadAll() #offload and onload all trains
     TopBar() #display the top bar gui
     sideBar() #display the side bar gui
     BuyTrainScreen() #display train screen if opened
     ShowUpgradeScreen()#display upgrade screen if opened
     ShowPausedScreen()#display paused screen if opened
     MoneyDisplay() #display current balance
     updatePageSheet() #update the progress of achievements
     ShowAchievementScreen()#display achievement screen if opened
     ShowHelpScreen(helpPage)#display help screen if opened
     controlsDisplay() #display controls screen if opened
     if secretmode: #if secret mode on
          imp = pygame.image.load("images\Train.png").convert() #draw png of train 
          screen.blit(imp, (Train1.xpos-20, Train1.ypos-20)) #on location of train1
     
     pygame.display.update() #update the display

pygame.quit() #quit out when while loop ends








    
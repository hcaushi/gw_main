import pickle
import pymysql
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import numpy
import matplotlib.pyplot as plt
import pygame
import time
try:
    import create_leaderboards #Create all of the leaderboards if they don't already exist
except:
    print("Could not connect to SQL: leaderboard creation aborted")

##########################
#####BEGIN FUNCTIONS######
##########################

#Function to remove all widgets: Removes all widgets in the list widgets
#Args: none
def remove_widgets():                           #Better to use "remove" than "delete" because "delete" implies removal from memory as well as from screen
    for widget in widgets:
        widget.grid_forget()

    #Clear widgets list
    global widgets
    widgets = []
#End function

#Function to get leaderboard entries
#Args: none
def get_leaderboard(level):
    try:
        leaderboard_name = "leaderboard_" + level
        hst = []                                                    #hst stores up to 10 top scores and their usernames

        leaderboard = pymysql.connect(host = "localhost",
                                      user = "root",
                                      passwd = "Password1",
                                      db = "gw_leaderboard",
                                      autocommit = True)
        #Connect to the leaderboard

        c = leaderboard.cursor()
        selection = c.execute("SELECT * FROM " + leaderboard_name + " ORDER BY money_remaining DESC LIMIT 10;")
        #The above row modifies c such that it now contains rows
        #We can now iterate through the first 10 of these

        for row in c:                                               #For every row that's been selected...
            username = row[0]                                       #Our one use for functions' local variables!
            money_remaining = row[1]
            hst.append((username,money_remaining))                  #Add the entry to hst

        c.close()                                                   #Close the cursor to halt memory leaks
        leaderboard.close()

        return hst
    
    except:
        #Could not get the SQL leaderboard
        print("Could not get SQL leaderboard.")
        return False
#End function

#Function to change the currently selected level
#Args:
#level: The new level to switch to
def change_level(event):
    try:
        if str(event.widget["state"]) == "disabled": return False     #Catch if the level was not yet unlocked

        for i in level_buttons:                     #Try to find the button which was clicked
            if i[1] == event.widget: level = i[0]   #i[1] is the button, while i[0] represents its level
        global level_selected
        level_selected = level
        
    except:
        level = "main_1"
        global level_selected
        level_selected = "main_1"

    new_leaderboard = "Leaderboard\n"                        #This will be the label we'll give to the leaderboard

    #Set the money remaining to the level's budget
    global money_remaining
    money_remaining = budget[level_selected]

    #Get the leaderboard for the level
    hst = get_leaderboard(level_selected)
    if hst != False:
        for i in hst:
            new_leaderboard = new_leaderboard + str(i[0]) + " " + str(i[1]) +"\n"
        new_leaderboard =  new_leaderboard.rstrip() #Remove \n from the end of the label

    else:
        #If the game couldn't load SQL, output this to the user.
        new_leaderboard = "Leaderboard\nSQL is not installed!"
        
    global phot_levelselected
    phot_levelselected = ImageTk.PhotoImage(level_thumbnails[level])       #Change the thumbnail displayed

    budget_widget.config(text = "Budget: "+str(budget[level_selected])+"\nRemaining: "+str(budget[level_selected])+"\nLeft-click places troops.\nRight-click removes them.")

    leaderboard.config(text = new_leaderboard)  #Change the display for the leaderboard so that it contains the newly selected level
    print("Switched to level "+level+".")
    return True
#End function

#Function to switch to the main menu: Calls remove_widgets and then spawns the relevant widgets
#Args: none
def go_mainmenu():
    print("Switched to main menu.")
    global current_room
    current_room = "main_menu"
    remove_widgets()

    #Grid widgets
    for x in range(4):                                              #For each column...
        root.columnconfigure(x, weight = 3)                             #Set its weight to 3
    for y in range(7):                                              #For each row...
        root.rowconfigure(y, weight = 1)                                #Set its weight to 1

    #Remove weight from all empty cells
    for x in range(4,800):
        root.columnconfigure(x,weight = 0)
    for y in range(7,600):
        root.rowconfigure(y, weight = 0)
    root.columnconfigure(1, weight = 1)                             #Set the 2nd and 3rd columns to 2...
    root.columnconfigure(2, weight = 1)                             #To make the gaps wider than the buttons themselves

    title.grid(row = 1, column = 1,
               sticky = W+E+N+S,
               columnspan = 2)

    usernamebox.grid(row = 2, column = 1,
                     sticky = W+E+N+S)

    check.grid(row = 2, column = 2,
               sticky = W+E+N+S)

    start.grid(row = 3, column = 1,
               sticky = W+E+N+S,
               columnspan = 2)

    settings.grid(row = 4, column = 1,
                  sticky = W+E+N+S,
                  columnspan = 2)

    exitbutton.grid(row = 5, column = 1,
                    sticky = W+E+N+S, columnspan = 2)

    #Add widgets to list of widgets
    widgets.append(title)
    widgets.append(usernamebox)
    widgets.append(check)
    widgets.append(start)
    widgets.append(settings)
    widgets.append(exitbutton)
#End function

#Function to switch to the settings room: Calls remove_widgets and then spawns the relevant widgets
#Args: none
def go_settings():
    print("Switched to settings.")
    global current_room
    current_room = "settings"
    remove_widgets()

    #Adjust cell weight
    root.columnconfigure(0, weight = 1)
    root.columnconfigure(1, weight = 1)
    root.columnconfigure(2, weight = 3)
    root.columnconfigure(3, weight = 1)
    root.columnconfigure(4, weight = 3)
    root.columnconfigure(5, weight = 2)

    root.rowconfigure(0, weight = 2)
    root.rowconfigure(1, weight = 1)
    root.rowconfigure(2, weight = 1)
    root.rowconfigure(3, weight = 3)
    root.rowconfigure(4, weight = 1)
    root.rowconfigure(5, weight = 2)

    #Remove weight from all empty cells
    for x in range(6,800):
        root.columnconfigure(x, weight = 0)
    for y in range(6,600):
        root.rowconfigure(y, weight = 0)

    speed_slider.grid(row = 2, column = 2, sticky = W+E+N+S)
    volume_slider.grid(row = 2, column = 4, sticky = W+E+N+S)
    back.grid(row = 4, column = 1, sticky = W+E+N+S)
    settings_title.grid(row = 0, column = 3, sticky = W+E+N+S)
    speed_header.grid(row = 1, column = 2, sticky = W+E+N+S)
    volume_header.grid(row = 1, column = 4, sticky = W+E+N+S)

    #Add widgets to list of widgets
    widgets.append(speed_slider)
    widgets.append(volume_slider)
    widgets.append(back)
    widgets.append(settings_title)
    widgets.append(speed_header)
    widgets.append(volume_header)
#End function

#Function to switch to the level select menu: Calls remove_widgets and then spawns the relevant widgets
#Args: none
def go_levelselect():
    global current_room
    current_room = "level_select"
    remove_widgets()

    #Adjust cell weight
    for x in range(17):
        root.columnconfigure(x, weight = 1)
    root.columnconfigure(13, weight = 1)

    for y in range(9):
        root.rowconfigure(y, weight = 1)
    root.rowconfigure(8, weight = 2)

    #Remove weight from all empty cells
    for x in range(14,800):
        root.columnconfigure(x, weight = 0)
    for y in range(8,600):
        root.columnconfigure(y, weight = 0)

    #Remove all troops from the field
    for troop in Troop.all_troops:
        Troop.all_troops.remove(troop)                              #...remove it from all_troops...
        del troop                                                   #...then remove it from memory

    for enemy in Enemy.all_enemies:
        Enemy.all_enemies.remove(enemy)                             #...remove it from all_enemies...
        del enemy                                                   #...then remove it from memory

    global troops_placed
    troops_placed = []
    #Any objects which somehow escape deletion will eventually get garbage collected

    Troop.all_troops = []
    Enemy.all_enemies = []
    
    remove_widgets()

    #Reset all grid buttons before loading the widgets
    global grid
    for x in range(10):                                                  #Remove everything from the grid
        for y in range(10):
            grid[x][y] = None
            grid_buttons[x][y].config(bg=SystemButtonFace)
    resize_sprites(leaderboard)

    global money_remaining
    money_remaining = budget[level_selected]
    
    levelselect_title.grid(row = 0, column = 0, sticky = W+E+N+S, columnspan = 17)
    leaderboard.grid(row = 0, column = 12, sticky = W+E+N+S, rowspan = 3)
    back.grid(row = 6, column = 1, sticky = W+E+N+S)
    play.grid(row = 6, column = 12, sticky = W+E+N+S)

    level_info.grid(row = 1, column = 1, columnspan = 2, rowspan = 2, sticky = W+E+N+S)

    mainlevel_frame.grid(row = 3, column = 1, sticky = W+E+N+S, columnspan = 10) #Grid the main level buttons
    widgets.append(mainlevel_frame)

    if beaten["main"] == 10:                                                     #If level 10 has been beaten...
        exlevel_frame.grid(row = 5, column = 5, sticky = W+E+N+S, columnspan = 6)#...also grid the EX level buttons
        widgets.append(exlevel_frame)

    #Add widgets to list of widgets
    widgets.append(levelselect_title)
    widgets.append(leaderboard)
    widgets.append(back)
    widgets.append(play)
    widgets.append(level_info)

    print("Switched to level select menu.")
#End function

#Function to switch to the troop placement room: Calls remove_widgets and then spawns the relevant widgets
#Args: none
def go_troopplacement(**args):
    global troops_placed
    global current_room
    current_room = "troop_placement"

    #If there is a comparison graph open, close it now
    try:
        plt.close()
    except:
        pass

    #Reset army strength variables
    Troop.troop_strength = 0
    Enemy.enemy_strength = 0
    Troop.troop_strength_timeline = []
    Enemy.enemy_strength_timeline = []

    #Remove all currently placed units, if any
    for troop in Troop.all_troops:
        Troop.all_troops.remove(troop)                              #...remove it from all_troops...
        del troop                                                   #...then remove it from memory

    for enemy in Enemy.all_enemies:
        Enemy.all_enemies.remove(enemy)                             #...remove it from all_enemies...
        del enemy                                                   #...then remove it from memory
    #Any objects which somehow escape deletion will eventually get garbage collected

    Troop.all_troops = []
    Enemy.all_enemies = []
    
    remove_widgets()

    global grid
    for x in range(10):                                                  #Remove everything from the grid
        for y in range(10):
            grid[x][y] = None

    #Initialise all troops
    for troop in troops_placed:
        troop[0](troop[1],troop[2])                                 #Initialise Troop(x,y)
    
    #Initialise all enemies
    for enemy in enemy_pool[level_selected]:
       enemy[0](enemy[1],enemy[2])                                  #Initialise Enemy(x,y)

    troops_placed = []
    resize_sprites(leaderboard)

    #Adjust cell weight
    for x in range(5):
        root.columnconfigure(x, weight = 1)
    for y in range(9):
        root.rowconfigure(y, weight = 1)

    root.columnconfigure(2, weight = 5)

    #Remove weight from all empty cells
    for x in range(5,800):
        root.columnconfigure(x, weight = 0)
    for y in range(9,600):
        root.rowconfigure(y, weight = 0)

    #Grid all widgets
    play.grid(row = 7, column = 4, sticky = W+E+N+S)
    back.grid(row = 7, column = 0, sticky = W+E+N+S)
    troopbutton_frame.grid(row = 1, column = 0, rowspan = 5, sticky = W+E+N+S)
    leaderboard.grid(row = 4, column = 4, rowspan = 3, sticky = W+E+N+S)
    budget_widget.grid(row = 1, column = 4, sticky = W+E+N+S)
    grid_frame.grid(row = 1, column = 1, rowspan = 7, columnspan = 3, sticky = W+E+N+S)

    #Add widgets to the list of widgets
    widgets.append(play)
    widgets.append(back)
    widgets.append(leaderboard)
    widgets.append(budget_widget)
    widgets.append(grid_frame)
    widgets.append(troopbutton_frame)

    print("Switched to troop placement")
#End function

#Function to go to the battle screen
#Args: none
def go_battle(**args):
    print("Now in battle.")
    global current_room
    current_room = "battle"

    #Set up a new global variable that stores a list of where the player's troops started
    global troops_placed
    troops_placed = []

    #Preserve all troops and all enemies by storing 3-tuples of their troops
    #We can restore from this when we go back to the troop placement screen
    for troop in Troop.all_troops:
        troops_placed.append((type(troop),troop.x,troop.y))

    #Remove the play button from the screen for the time being
    play.grid_forget()
    widgets.remove(play)

    #Start the army comparison timeline with the y value at x=0
    Troop.troop_strength_timeline.append(Troop.troop_strength)
    Enemy.enemy_strength_timeline.append(Enemy.enemy_strength)

    while current_room == "battle":
        if len(Enemy.all_enemies) == 0:
            #Player wins
            print("You win!")
            plt.suptitle("You win!", fontsize=16)

            #Construct a troop comparison graph
            try:
                save_progress(level_selected)
            except:
                print("Couldn't save progress!")
            plt_x = range(len(Troop.troop_strength_timeline))
            player_timeline = plt.plot(plt_x, Troop.troop_strength_timeline, color = "blue", label = "Your army")
            enemy_timeline = plt.plot(plt_x, Enemy.enemy_strength_timeline, color = "red", label = "Enemy army")
            plt.xlabel("Number of turns")
            plt.ylabel("Strength")
            plt.show()
            plt.clf()

        elif len(Troop.all_troops) == 0:
            #Player loses
            print("You lose!")
            plt.suptitle("You lose!", fontsize=16)

            #Construct a troop comparison graph
            plt_x = range(len(Troop.troop_strength_timeline))
            player_timeline = plt.plot(plt_x, Troop.troop_strength_timeline, color = "blue", label = "Your army")
            enemy_timeline = plt.plot(plt_x, Enemy.enemy_strength_timeline, color = "red", label = "Enemy army")
            plt.xlabel("Number of turns")
            plt.ylabel("Strength")
            plt.show()
            plt.clf()
            break

        else:
            #During battle, call every object's Act method
            for troop in Troop.all_troops:
                troop.act()

            for enemy in Enemy.all_enemies:
                enemy.act()

            #Commit all changes from troops and enemies
            resolve_all()

            #Wait for the next turn
            time.sleep(1/game_speed)

#Function to save the player's username, game_volume and game_speed
#Args: none
def save_data():
    global game_speed, game_volume
    game_speed = speed_slider.get()
    game_volume = volume_slider.get()

    #Save data to file
    with open("gw_data.txt","w") as file:                           #Open gw_data.txt...
        file.write(username+"\n"+str(game_speed)+"\n"+str(game_volume))  #...and save the player's username to it

    #Set the game volume
    try:
        sword_mp3.set_volume(game_volume)
        archer_mp3.set_volume(game_volume)
        magic_mp3.set_volume(game_volume)
    except:
        print("Could not set game volume.")

    print("Data saved!")
#End function

#Function to save the player's progress
#Args:
#level_selected: Equal to the global variable level_selected; the level that was just beaten
def save_progress(level_selected):
    #If the level was a main level, and it was the next level, increase the number of main levels beaten...
    global beaten, username, money_remaining

    if "main" in level_selected:
        level_number = int(level_selected.split("_")[1])
        if level_number > beaten["main"]: beaten["main"] = level_number

        #...then unlock the next level, except for Level 10 (which unlocks EX levels instead)
        level_buttons[level_number-1][1].config(bg = "green")
        
        if level_number < 10:
            level_buttons[level_number][1].config(state = NORMAL)

    #Otherwise, set the win state for the EX level beaten to 1
    else:
        level_number = int(level_selected.split("_")[1]) + 10
        beaten[level_selected] = 1
        level_buttons[level_number-1][1].config(bg = "green")       #Make the level's button green

    #Save game progress
    pickle.dump(beaten,open("beaten.p","wb"))

    #Save the user's score to SQL
    try:
        leaderboard = pymysql.connect(host = "localhost",
                                      user = "root",
                                      passwd = "Password1",
                                      db = "gw_leaderboard",
                                      autocommit = True)
        c = leaderboard.cursor()
    except:
        #Could not connect to SQL
        pass

    #If the player does not yet have an entry on the given leaderboard, add their score to the list
    try:
        insert_data = ("INSERT INTO leaderboard_"+str(level_selected)+"(username, money_remaining) VALUES ('"+str(username)+"', "+str(money_remaining)+");").replace("\n","")
        c.execute(insert_data)                                      #Execute the given command
        c.close()                                                   #Close the cursor to prevent memory leaks
        leaderboard.close()                                         #Close the leaderboard after the operation is closed for the same reason
        print("Record saved!")
        return True

    except:
        selection = c.execute(("SELECT * FROM leaderboard_" + level_selected + " WHERE username = '"+username+"';").replace("\n",""))

        for row in c:                                               #Go into the one row the statement returns
            print(row)
            old_record = row[1]                                     #Define the old record

            #If the player has a higher money remaining than last time, save the new record to the SQL database
            if money_remaining > old_record:
                c.execute(("DELETE FROM leaderboard_"+level_selected+" WHERE username = '"+username+"';").replace("\n",""))
                c.execute(("INSERT INTO leaderboard_"+str(level_selected)+" (username, money_remaining) VALUES ('"+username+"', "+str(money_remaining)+");").replace("\n",""))
                c.close()                                           #Close the cursor to prevent memory leaks
                leaderboard.close()                                 #Close the leaderboard after the operation is closed for the same reason
                print("Record saved!")

            #Otherwise, preserve the previous entry
            else: print("Record not submitted.")

    #Save changes to the leaderboard
    c.close()
#End function

#Function to reduce a number to either 1, 0 or -1 depending on whether it's 0, positive or negative
#Args:
#n: A positive integer
def reduce(n):
    if n > 0: return 1
    if n < 0: return -1
    return 0
#End function

##########################
######BEGIN CLASSES#######
##########################
#Function to move a troop: Attempts to move a troop by a given x and y position
#Args:
#unit: The unit to attempt to move
#dx: The differential in x by which to attempt to move the unit
#dy: The differential in y by which to attempt to move the unit
def move(unit,dx,dy):
    new_x = unit.x+dx                           #Create a local variable for the new x position
    new_y = unit.y+dy                           #Same for the new y position

    if (new_x not in range(10)) or (new_y not in range(10)):
        return False

    if grid[new_x][new_y] == None:
        all_actions.append((unit,new_x,new_y))  #Add the movement to a list of actions
        grid[new_x][new_y] = "busy"             #So that no other troop will attempt to move there
        return True

    else:                                       #Move failed
        return False
#End function

#Function to move all troops according to the list all_actions, and remove all troops with 0 HP from play
def resolve_all():
    global grid, all_actions, grid_buttons, all_attack_sounds

    for x in all_actions:
        #Move the unit where it needs to go
        #x[0] represents the unit; x[1] represents its new x value and x[2] represents its new y value
        grid_buttons[x[0].x][x[0].y].config(image = sprite_photos[None], bg=SystemButtonFace)
        grid[x[0].x][x[0].y] = None             #Empty the currently occupied square
        grid[x[1]][x[2]] = x[0]                 #Set the new grid square so the troop can be displayed
        x[0].x = x[1]                           #Set the x value of the troop
        x[0].y = x[2]                           #Set the y value of the troop

    all_actions = []                            #Empty all_actions

    for troop in Troop.all_troops:
        if troop.hp <= 0:                       #If the troop has 0 or less HP...
            grid[troop.x][troop.y] = None       #...remove the grid reference to the troop...
            grid_buttons[troop.x][troop.y].config(image = sprite_photos[None], bg=SystemButtonFace)
            Troop.all_troops.remove(troop)      #...remove it from all_troops...
            Troop.troop_strength -= troop.cost  #...reduce the player's strength by the troop's cost
            del troop                           #...then remove it from memory

        else:
            #Set the unit's "health colour" on the grid
            hp_ratio = troop.hp/troop.maxhp
            try:
                if hp_ratio < 1: bg_colour = "#%02x%02x%02x" % (int(255*(1-hp_ratio)), int(255*hp_ratio), 0)
                else: bg_colour = SystemButtonFace
                grid_buttons[troop.x][troop.y].config(image = sprite_photos[type(troop)], bg=bg_colour)
            except: grid_buttons[troop.x][troop.y].config(image = sprite_photos[type(troop)], bg=SystemButtonFace)

    for enemy in Enemy.all_enemies:
        if enemy.hp <= 0:                       #If the troop has 0 or less HP...
            grid[enemy.x][enemy.y] = None       #...remove the grid reference to the enemy...
            grid_buttons[enemy.x][enemy.y].config(image = sprite_photos[None], bg=SystemButtonFace)
            Enemy.all_enemies.remove(enemy)     #...remove it from all_troops...
            Enemy.enemy_strength -= enemy.cost  #...reduce the opposition's strength by the enemy's cost
            del enemy                           #...then remove it from memory

        else:
            #Set the unit's "health colour" on the grid
            hp_ratio = enemy.hp/enemy.maxhp
            try:
                if hp_ratio < 1: bg_colour = "#%02x%02x%02x" % (int(255*(1-hp_ratio)), int(255*hp_ratio), 0)
                else: bg_colour = SystemButtonFace
                grid_buttons[enemy.x][enemy.y].config(image = sprite_photos[type(enemy)], bg=bg_colour)
            except: grid_buttons[enemy.x][enemy.y].config(image = sprite_photos[type(enemy)], bg=SystemButtonFace)

    #Play all sounds that need to be played
    for unit in [Swordsman, Goblin, Grunt]:
        if unit in all_attack_sounds:
            try:
                sword_mp3.play()
            except:
                pass

    if Archer in all_attack_sounds:
        try:
            archer_mp3.play()
        except:
            pass

    for unit in [Magician, Cleric]:
        if unit in all_attack_sounds:
            magic_mp3.play()

    all_attack_sounds = []

    Troop.troop_strength_timeline.append(Troop.troop_strength)
    Enemy.enemy_strength_timeline.append(Enemy.enemy_strength)
    resize_sprites(leaderboard)
#End function

##########################
#######BEGIN CLASSES######
##########################

class Troop:
    all_troops = []
    troop_strength = []                     #Stores the total cost of the player's army at the moment
    troop_strength_timeline = []            #Stores the total cost of the player's army over time

    def __init__(self,cost,atk,hp,x,y):     #The method which runs when a Troop is initialised or constructed
        self.cost = cost
        self.atk = atk
        self.maxhp = hp
        self.hp = hp
        self.x = x
        self.y = y
        grid[x][y] = self

        Troop.all_troops.append(self)           #Adds itself to the list of all Troop instances
        Troop.troop_strength += cost


    def getNearestEnemy(self):
        distances = []
        if Enemy.all_enemies == []:
            return None #Do nothing if no enemies exist

        else:
            for enemy in Enemy.all_enemies:
                distance = ((self.x-enemy.x)**2 + (self.y-enemy.y)**2)**0.5 #Use the Pythagorean method to calculate approximate distance
                distances.append((enemy,distance))                          #Add the troop and its distance to a local list
            return sorted(distances, key=lambda x: x[1])[0][0]              #Return the first item in this list once it's ordered

    def getNearestTroop(self):
        distances = []

        if len(Troop.all_troops) == 1:
            return None

        for troop in Troop.all_troops:
            distance = ((self.x-troop.x)**2 + (self.y-troop.y)**2)          #Use the Pythagorean method to calculate approximate distance (no need to square root the distances, they'll still be in order)
            distances.append((troop,distance))                              #Add the troop and its distance to a local list
        return sorted(distances, key=lambda x: x[1])[1][0]                  #Return the SECOND item in this list once it's ordered
                                                                            #(the first item is the troop that's calling it)

    def getVector(self,target):                 #Returns the vector from the unit to the target
        dx = target.x-self.x
        dy = target.y-self.y
        return (dx,dy)                          #Return a 2-tuple of the vector

    def move(self,target):
        dx = reduce(self.getVector(target)[0])       #Call the reduce function on the x component of the vector to target
        dy = reduce(self.getVector(target)[1])       #Call the reduce function on the y component of the vector to target

        if not move(self,dx,dy):                              #Try to move in both directions towards the target
            if not move(self,0,dy):                           #Try to move in one direction towards the target
                if not move(self,dx,0):                       #Try to move in the other direction towards the target
                    if dx == 0 and dy != 0:
                        if not move(self,1,dy):               #Try to move in one direction, but away in the other direction, towards the target
                            if not move(self,-1,-dy):
                                pass
                    elif dy == 0 and dx != 0:
                        if not move(self,dx,1):
                            if not move(self,dx,-1):
                                pass                          #In this case, the troop should stay where it is
                    else:
                        if not move(self,-dx,dy):
                            if not move(self,dx,-dy):
                                pass

    def attack(self,enemy):
        enemy.hp -= self.atk
        global all_attack_sounds
        if type(self) not in all_attack_sounds:
            all_attack_sounds.append(self)

    def act(self):
        target = self.getNearestEnemy()                                     #Initialise variables for the target and vector to the target
        if target != None:
            dx = self.getVector(target)[0]
            dy = self.getVector(target)[1]

            if abs(dx) <= 1 and abs(dy) <= 1:                               #If the target is right next to the unit...
                self.attack(target)                                         #Call the troop's attack method on it

            else:
                self.move(target)                                           #Otherwise, move towards the nearest enemy

class Enemy:
    all_enemies = []
    enemy_strength = 0                                                      #Stores the total cost of the enemy's army at the moment
    enemy_strength_timeline = []                                            #Stores the total cost of the enemy's army over time

    def __init__(self,cost,atk,hp,x,y):                                     #The method which runs when an Enemy is initialised or constructed
        self.cost = cost                                                    #Legacy cost value which simply affects the value of an Enemy (for comparative performance graphs)
        self.atk = atk
        self.maxhp = hp
        self.hp = hp
        self.x = x
        self.y = y
        grid[x][y] = self

        Enemy.all_enemies.append(self)
        Enemy.enemy_strength += self.cost

    def getNearestEnemy(self):
        distances = []

        if len(Enemy.all_enemies) == 1:
            return None

        for enemy in Enemy.all_enemies:
            distance = ((self.x-enemy.x)**2 + (self.y-enemy.y)**2)          #Use the Pythagorean method to calculate approximate distance (no need to square root the distances, they'll still be in order)
            distances.append((enemy,distance))                              #Add the troop and its distance to a local list
        return sorted(distances, key=lambda x: x[1])[1][0]                  #Return the SECOND item in the list once it's ordered
                                                                            #(the first is the enemy calling the method)

    def getNearestTroop(self):
        distances = []
        if Troop.all_troops == []:
            return None #Do nothing if no troops exist

        else:
            for troop in Troop.all_troops:
                distance = ((self.x-troop.x)**2 + (self.y-troop.y)**2)**0.5 #Use the Pythagorean method to calculate approximate distance
                distances.append((troop,distance))                          #Add the troop and its distance to a local list
            return sorted(distances, key=lambda x: x[1])[0][0]              #Return the first item in this list once it's ordered

    def getVector(self,target):                                             #Return the vector from the unit to the target
        dx = target.x-self.x
        dy = target.y-self.y
        return (dx,dy)                                                      #Return a 2-tuple of the vector

    def move(self,target):
        dx = reduce(self.getVector(target)[0])                              #Call the reduce function on the x component of the vector to target
        dy = reduce(self.getVector(target)[1])                              #Call the reduce function on the y component of the vector to target

        if not move(self,dx,dy):                                            #Try to move in both directions towards the target
            if not move(self,0,dy):                                         #Try to move in one direction towards the target
                if not move(self,dx,0):                                     #Try to move in the other direction towards the target
                    if dx == 0 and dy != 0:
                        if not move(self,1,dy):                             #Try to move in one direction, but away in the other direction, towards the target
                            if not move(self,-1,-dy):
                                pass
                    elif dy == 0 and dx != 0:
                        if not move(self,dx,1):
                            if not move(self,dx,-1):
                                pass                                        #In this case, the enemy should stay where it is
                    else:
                        if not move(self,-dx,dy):
                            if not move(self,dx,-dy):
                                pass

    def attack(self,troop):                                                 #This is identical to the Troop.attack() method
        troop.hp -= self.atk
        if type(self) not in all_attack_sounds:
            all_attack_sounds.append(self)

    def act(self):
        target = self.getNearestTroop()                                     #Initialise variables for the target and vector to the target
        if target != None:
            dx = self.getVector(target)[0]
            dy = self.getVector(target)[1]

            if abs(dx) <= 1 and abs(dy) <= 1:                               #If the target is right next to the unit...
                self.attack(target)                                         #Call the troop's attack method on it

            else:
                self.move(target)                                           #Otherwise, move towards the nearest troop

#Troops
class Peasant(Troop):
    cost = 400
    atk = 2
    maxhp = 8

    def __init__(self,x,y):
        Troop.__init__(self,400,2,8,x,y)

class Swordsman(Troop):
    cost = 700
    atk = 3
    hp = 14

    def __init__(self,x,y):
        Troop.__init__(self,700,3,14,x,y)

class Phalanx(Troop):
    cost = 1100
    atk = 4
    maxhp = 30

    def __init__(self,x,y):
        Troop.__init__(self,1100,3,30,x,y)

class Knight(Troop):
    cost = 1200
    atk = 7
    maxhp = 14

    def __init__(self,x,y):
        Troop.__init__(self,1200,7,14,x,y)

class Archer(Troop):
    cost = 700
    atk = 3
    maxhp = 7

    def __init__(self,x,y):
        Troop.__init__(self,700,3,7,x,y)

    def act(self):
        target = self.getNearestEnemy()
        if target != None:
            dx = self.getVector(target)[0]
            dy = self.getVector(target)[1]
            if abs(dx) <= 3 and abs(dy) <= 3: self.attack(target)           #Attack from a range of up to 3...
            else: self.move(target)                                         #...otherwise move as normal

class Cleric(Troop):
    cost = 1500
    atk = 2
    maxhp = 12

    def __init__(self,x,y):
        Troop.__init__(self,1500,2,12,x,y)

    def heal(self,troop):
        troop.hp = min(troop.hp + 2, troop.maxhp)                           #Increase the target troop's HP by 2

    def getNearestInjured(self):
        #Like Troop.getNearestTroop, but we're iterating through all of the
        distances = []
        if len(Troop.all_troops) == 1:
            return None

        for troop in Troop.all_troops:
            distance = (troop.x-self.x)**2+(troop.y-self.y)**2               #The square of the distance to the troop
            if troop != self and troop.hp < troop.maxhp:                     #This time we're forbidding the cleric itself from being added to the list, and only adding troops not at max HP
                distances.append((troop,distance))

        try:
            return sorted(distances, key=lambda x: x[1])[0][0]                   #Sort the list by increasing distance and return the first entry
        except:
            return None

    def act(self):
        #The cleric will decide whether an injured troop or an enemy is more important to focus on
        #If given the opportunity, however, it can do both at the same time
        target = self.getNearestEnemy()                                     #Initialise variables for the target and vector to the target
        injured = self.getNearestInjured()

        if target != None:
            dx1 = self.getVector(target)[0]
            dy1 = self.getVector(target)[1]

        else:                                                               #If no such values exist, make dx1 and dy1 values which will never be the closest
            dx1 = 1000
            dy1 = 1000

        if injured != None:
            dx2 = self.getVector(injured)[0]
            dy2 = self.getVector(injured)[1]

        else:
            dx2 = 1000
            dy2 = 1000

        movecomplete = False                                                #If this is still false at the end of the method, it will allow the cleric to move

        if abs(dx1) <= 1 and abs(dy1) <= 1:
            self.attack(target)
            movecomplete = True

        if abs(dx2) <= 1 and abs(dy2) <= 1:
            self.heal(injured)
            movecomplete = True

        if not movecomplete:
            if dx1**2 + dy1**2 <= dx2**2 + dy2**2: self.move(target)                    #Prioritise moving towards enemies
            else: self.move(injured)

#Enemies
class Chicken(Enemy):
    cost = 50
    atk = 1
    maxhp = 3

    def __init__(self,x,y):
        Enemy.__init__(self,50,1,3,x,y)

class Goblin(Enemy):
    cost = 150
    atk = 1
    maxhp = 5

    def __init__(self,x,y):
        Enemy.__init__(self,150,1,5,x,y)

class SpearOrc(Enemy):
    cost = 500
    atk = 3
    maxhp = 10

    def __init__(self,x,y):
        Enemy.__init__(self,500,3,10,x,y)

    def act(self):
        target = self.getNearestTroop()                                     #Get the nearest target
        if target != None:
            dx = self.getVector(target)[0]
            dy = self.getVector(target)[1]
            if abs(dx) <= 2 and abs(dy) <= 2: self.attack(target)           #Attack from a range of up to 2...
            else: self.move(target)                                         #...otherwise move as normal

class Grunt(Enemy):
    cost = 1000
    atk = 6
    maxhp = 20

    def __init__(self,x,y):
        Enemy.__init__(self,1000,6,20,x,y)

class Magician(Enemy):
    #The magician can attack all troops in a 3×3 grid
    cost = 1200
    atk = 3
    maxhp = 12

    def __init__(self,x,y):
        Enemy.__init__(self,1200,3,12,x,y)

    def act(self):
        movecomplete = False
        troops = []                                                         #Get an ordered list of all possible targets
        for troop in Troop.all_troops:
            troops.append(troop)

        troops = sorted(troops, key = lambda troop: (self.x-troop.x)**2+(self.y-troop.y**2))

        #Attack every troop within reach
        for troop in troops:
            dx = self.getVector(troop)[0]
            dy = self.getVector(troop)[1]

            if dx <= 1 and dy <= 1:
                self.attack(troop)
                movecomplete = True                                         #Prevents the Magician from moving after attacking
            else:
                break                                                       #Prevent it from using memory when no further troops will be attacked anyway

        if not movecomplete: self.move(self.getNearestTroop())              #Moves the Magician if it hasn't attacked yet

#Bosses
class Griffin(Enemy):
    def __init__(self,x,y):
        Enemy.__init__(self,2000,3,150,x,y)

class Dragon(Enemy):
    def __init__(self,x,y):
        Enemy.__init__(self,3000,3,50,x,y)

    def act2(self):                                                         #This one is literally the same as most other units' act method, but we're using act2 in order to allow act to call act2 twice
        target = self.getNearestTroop()                                     #Initialise variables for the target and vector to the target
        if target != None:
            dx = self.getVector(target)[0]
            dy = self.getVector(target)[1]

            if abs(dx) <= 1 and abs(dy) <= 1:                               #If the target is right next to the unit...
                self.attack(target)                                         #Call the troop's attack method on it

            else:
                self.move(target)                                           #Otherwise, move towards the nearest troop

    def act(self):
        self.act2()
        self.act2()

class ChickenMan(Enemy):
    def __init__(self,x,y):
        Enemy.__init__(self,2000,2,75,x,y)

    def act(self):                                                          #Like the normal act except that it can also spawn chickens
        def get_space(x,y):                                                 #Yes, it's an inner function. These are useful so that they don't exist outside the scope of this method
            for dx in [0,-1,1]:                                             #(We need the inner function in order to break out of a 2-dimensional iteration without using a more naïve approach)
                for dy in range(-1,2):
                    try:
                        if grid[x+dx][y+dy] == None:
                            return (x+dx,y+dy)
                    except:
                        pass
            return False

        target = self.getNearestTroop()                                     #Initialise variables for the target and vector to the target
        if target != None:
            dx = self.getVector(target)[0]
            dy = self.getVector(target)[1]

            if abs(dx) <= 1 and abs(dy) <= 1:                               #If the target is right next to the unit...
                self.attack(target)                                         #Call the troop's attack method on it

            else:
                self.move(target)                                           #Otherwise, move towards the nearest troop

            space = get_space(self.x,self.y)
            if space != False:                                              #If a space has been found...
                Chicken(space[0],space[1])                                  #Spawn a chicken

class ChickenManMan(Enemy):
    def __init__(self,x,y):
        Enemy.__init__(self,2000,2,75,x,y)

    def act(self):                                                          #Like the normal act except that it can also spawn chickens
        def get_space(x,y):                                                 #Yes, it's an inner function. These are useful so that they don't exist outside the scope of this method
            for dx in [0,-1,1]:                                             #(We need the inner function in order to break out of a 2-dimensional iteration without using a more naïve approach)
                for dy in range(-1,2):
                    try:
                        if grid[x+dx][y+dy] == None:
                            return (x+dx,y+dy)
                    except:
                        pass
            return False

        target = self.getNearestTroop()                                     #Initialise variables for the target and vector to the target
        if target != None:
            dx = self.getVector(target)[0]
            dy = self.getVector(target)[1]

            if abs(dx) <= 1 and abs(dy) <= 1:                               #If the target is right next to the unit...
                self.attack(target)                                         #Call the troop's attack method on it

            else:
                self.move(target)                                           #Otherwise, move towards the nearest troop

            space = get_space(self.x,self.y)
            if space != False:                                              #If a space has been found...
                ChickenMan(space[0],space[1])                               #Spawn a chicken man

class Basilisk(Enemy):
    def __init__(self,x,y):
        Enemy.__init__(self,7500,0,20,x,y)

    def attack(self,target):
        target.hp = 0

class GoldenMan(Enemy):
    def __init__(self,x,y):
        Enemy.__init__(self,5000,4,150,x,y)

    def attack(self,target):
        target.hp -= self.atk
        if target.hp <= 0:                      #If the target is dead, convert it to an equivalent enemy
            if type(target) == Peasant:
                Goblin(target.x,target.y)
            elif type(target) == Swordsman:
                Grunt(target.x,target.y)
            elif type(target) == Phalanx:
                Grunt(target.x,target.y)
            elif type(target) == Knight:
                Grunt(target.x,target.y)
            elif type(target) == Archer:
                SpearOrc(target.x,target.y)
            elif type(target) == Cleric:
                Magician(target.x,target.y)

            Troop.all_troops.remove(target)
            del target

class TreeMan(Enemy):
    def __init__(self,x,y):
        Enemy.__init__(self,5000,1,1000,x,y)

    def attack(self,target):
        target.hp -= self.atk

##########################
#BEGIN TKINTER FUNCTIONS##
##########################

#Function that resizes the title
def resize_title(event):
    new_width = event.width*6//7
    new_height = event.height*10//14
    img_title = img_title_copy.resize((new_width,new_height))
    phot_title = ImageTk.PhotoImage(img_title)
    title.config(image = phot_title)
    title.image = phot_title

#Function that resizes the level info
def resize_levelinfo(event):
    new_width = int(event.width*11/14)
    new_height = int(event.height*11/14)
    img_levelselected = level_thumbnails[level_selected].resize((new_width,new_height))
    phot_levelselected = ImageTk.PhotoImage(img_levelselected)
    level_info.config(image = phot_levelselected)
    level_info.image = phot_levelselected

#Function that resizes unit sprites
def resize_sprites(event, **args):
    global sprite_photos
    global sprites
    #Define the size of the sprites
    new_width = 60
    new_height = 60

    #Resize the sprites using ImageTk
    for obj in [None, Peasant, Swordsman, Phalanx, Knight, Archer, Cleric, Chicken, Goblin, SpearOrc, Grunt, Magician, Griffin, Dragon, ChickenMan, Basilisk, ChickenManMan, TreeMan, GoldenMan]:
        sprite_photos[obj] = sprites[obj].resize((new_width,new_height))
        sprite_photos[obj] = ImageTk.PhotoImage(sprite_photos[obj])

    #Assign the newly resized sprites to all Buttons that need them
    for x in range(10):
        for y in range(10):
            if grid[x][y] != None:
                grid_buttons[x][y].config(image = sprite_photos[type(grid[x][y])])
            else:
                grid_buttons[x][y].config(image = sprite_photos[None])

#Function to test if the player's username is valid
def check_username(**args):
    username_to_check = usernamebox.get()                       #Get the username the player has input

    if len(username_to_check) > 0 and len(username_to_check) <= 10: #Valid username
        check.config(text = "Username OK")                      #Change the check box's username to "Username OK"
        start.config(state = NORMAL)                            #Unlock the start button
        global username
        username = username_to_check                            #Set the player's username
        save_data()

    else:
        usernamebox.delete(0, END)                              #Remove all text from the username box
        usernamebox.insert(0, "Invalid username!")              #Then insert "Invalid username!" to it
#End function

#Function that is called when the exit button is clicked
def exit_clicked(**args):
    exit()                                                      #Close the program

def play_clicked(**args):
    if current_room == "level_select":
        go_troopplacement()

    elif current_room == "troop_placement":
        go_battle()

#Generic function that is called when any back button is clicked
def go_back(**args):
    if current_room == "settings":
        game_speed = speed_slider.get()                         #Save game_speed
        game_volume = volume_slider.get()                       #Save game_volume
        save_data()
        go_mainmenu()

    elif current_room == "level_select":
        go_mainmenu()

    elif current_room == "troop_placement":
        go_levelselect()

    elif current_room == "battle":
        go_troopplacement()

    #Catch any attempts to call the function in rooms where the button should not exist
    else:
        return False

#Function to change the currently selected troop
def change_troop(event):
    global troop_selected
    troops = [Peasant, Swordsman, Phalanx, Knight, Archer, Cleric]

    troop_selected = troops[troop_buttons.index(event.widget)]

#Function to place a troop if the player has enough money
def place_troop(event):
    global money_remaining

    #Check if the player can afford the troop
    if current_room != "troop_placement":                           #Prevent troops from being placed during combat
        print("Cannot place Troops while in combat!")
        return False

    if troop_selected.cost > money_remaining:
        print("Can't afford that!")
        return False

    if grid[event.widget.x][event.widget.y] != None:
        print("Square is already occupied!")
        return False

    if event.widget.y > 4:
        print("Cannot place Troops on enemy squares!")
        return False

    money_remaining -= troop_selected.cost                          #Subtract the cost of the troop from the player's money
    new_troop = troop_selected(event.widget.x, event.widget.y)      #Initialize the troop, and place it on the grid
    print("Placed new troop at "+str(event.widget.x)+","+str(event.widget.y)+".")

    budget_widget.config(text = "Budget: "+str(budget[level_selected])+"\nRemaining: "+str(money_remaining)+"\nLeft-click places troops.\nRight-click removes them.")
    resize_sprites(event)

#Function to remove a troop by right-clicking on it
def remove_troop(event):
    global money_remaining
    if current_room != "troop_placement":                           #Prevent troops from being placed during combat
        print("Cannot remove Troops while in combat!")
        return False

    x = event.widget.x
    y = event.widget.y

    troop = grid[x][y]

    if not isinstance(troop, Troop):
        print("Something went wrong while trying to remove something.")
        return False

    try:                                                            #Try removing the troop
        money_remaining += troop.cost
        grid[troop.x][troop.y] = None                               #...remove the grid reference to the troop...
        Troop.all_troops.remove(troop)                              #...remove it from all_troops...
        del troop
        budget_widget.config(text = "Budget: "+str(budget[level_selected])+"\nRemaining: "+str(money_remaining)+"\nLeft-click places troops.\nRight-click removes them.")
        resize_sprites(event)
        return True

    except:                                                         #Second validation step
        print("Something went wrong while trying to remove something.")
        return False

##########################
####BEGIN GLOBAL SETUP####
##########################

#Images for level thumbnails
level_thumbnails = {"main_1": Image.open("level_01.png"),                   #Dictionary used to store all of the level thumbnail images...
                    "main_2": Image.open("level_02.png"),                   #...so that they can be used, and won't get GC'ed
                    "main_3": Image.open("level_03.png"),
                    "main_4": Image.open("level_04.png"),
                    "main_5": Image.open("level_05.png"),
                    "main_6": Image.open("level_06.png"),
                    "main_7": Image.open("level_07.png"),
                    "main_8": Image.open("level_08.png"),
                    "main_9": Image.open("level_09.png"),
                    "main_10": Image.open("level_10.png"),
                    "ex_1": Image.open("level_ex_01.png"),
                    "ex_2": Image.open("level_ex_02.png"),
                    "ex_3": Image.open("level_ex_03.png"),
                    "ex_4": Image.open("level_ex_04.png"),
                    "ex_5": Image.open("level_ex_05.png")}

level_thumbnails_copy = {"main_1": Image.open("level_01.png"),                   #Prevents the original files from being overwritten
                        "main_2": Image.open("level_02.png"),
                        "main_3": Image.open("level_03.png"),
                        "main_4": Image.open("level_04.png"),
                        "main_5": Image.open("level_05.png"),
                        "main_6": Image.open("level_06.png"),
                        "main_7": Image.open("level_07.png"),
                        "main_8": Image.open("level_08.png"),
                        "main_9": Image.open("level_09.png"),
                        "main_10": Image.open("level_10.png"),
                        "ex_1": Image.open("level_ex_01.png"),
                        "ex_2": Image.open("level_ex_02.png"),
                        "ex_3": Image.open("level_ex_03.png"),
                        "ex_4": Image.open("level_ex_04.png"),
                        "ex_5": Image.open("level_ex_05.png")}

sprites =      {None: Image.open("Empty.png"),
                Peasant: Image.open("Peasant.png"),                   #Dictionary used to store all of the Troop/Enemy sprites
                Swordsman: Image.open("Swordsman.png"),
                Phalanx: Image.open("Phalanx.png"),
                Knight: Image.open("Knight.png"),
                Swordsman: Image.open("Swordsman.png"),
                Archer: Image.open("Archer.png"),
                Cleric: Image.open("Cleric.png"),
                Goblin: Image.open("Goblin.png"),
                Chicken: Image.open("Chicken.png"),
                SpearOrc: Image.open("SpearOrc.png"),
                Grunt: Image.open("Grunt.png"),
                Magician: Image.open("Magician.png"),
                Griffin: Image.open("Griffin.png"),
                Dragon: Image.open("Dragon.png"),
                ChickenMan: Image.open("ChickenMan.png"),
                Basilisk: Image.open("Basilisk.png"),
                ChickenManMan: Image.open("ChickenManMan.png"),
                GoldenMan: Image.open("GoldenMan.png"),
                TreeMan: Image.open("Treeman.png")}

sprite_photos = {None: Image.open("Empty.png"),
                 Peasant: Image.open("Peasant.png"),                   #Allows us to preserve the original sprites
                 Swordsman: Image.open("Swordsman.png"),
                 Phalanx: Image.open("Phalanx.png"),
                 Knight: Image.open("Knight.png"),
                 Swordsman: Image.open("Swordsman.png"),
                 Archer: Image.open("Archer.png"),
                 Cleric: Image.open("Cleric.png"),
                 Goblin: Image.open("Goblin.png"),
                 Chicken: Image.open("Chicken.png"),
                 SpearOrc: Image.open("SpearOrc.png"),
                 Grunt: Image.open("Grunt.png"),
                 Magician: Image.open("Magician.png"),
                 Griffin: Image.open("Griffin.png"),
                 Dragon: Image.open("Dragon.png"),
                 ChickenMan: Image.open("ChickenMan.png"),
                 Basilisk: Image.open("Basilisk.png"),
                 ChickenManMan: Image.open("ChickenManMan.png"),
                 GoldenMan: Image.open("GoldenMan.png"),
                 TreeMan: Image.open("Treeman.png")}

#Variables used in navigation and similar
username = ""
current_room = "main_menu"                                                  #Rooms may be main_menu, settings, level_select, troops_placed or battle
level_selected = "main_1"
beaten = {"main": 0,                                                       #Dictionary which stores all levels beaten.
          "ex_1": 0,                                                        #"main" keys to an int equal to the number of main levels beaten (max 10)
          "ex_2": 0,                                                        #"ex_1" through "ex_5" key to Boolean values equal to whether the level has been beaten
          "ex_3": 0,
          "ex_4": 0,
          "ex_5": 0}

#Variables that can be modified in the settings menu
game_speed = 1
game_volume = 1

#Variables that are relevant in Troop Placement
money_remaining = 0
troop_selected = Peasant
troops_placed = []                                                        #Rather than constantly refreshing as Troop.all_troops does, this list preserves the layout for when the battle ends and troops need to be replaced

#Variables that are relevant in battle
all_actions = []
all_attack_sounds = []
grid = [[None for i in range(10)] for j in range(10)]

#Import level data
budget = {"main_1": 2000,                                                      #Stores the budget for each level
          "main_2": 3000,
          "main_3": 4500,
          "main_4": 3000,
          "main_5": 5500,
          "main_6": 5000,
          "main_7": 7000,
          "main_8": 5000,
          "main_9": 8000,
          "main_10": 13000,
          "ex_1": 4000,
          "ex_2": 4000,
          "ex_3": 25000,
          "ex_4": 7500,
          "ex_5": 2500}

enemy_pool = {"main_1": [(Goblin,2,9),(Goblin,3,8),(Goblin,4,8),(Goblin,5,8),(Goblin,6,8),(Goblin,7,9)],                                                                #List of enemies to load in each level
              "main_2": [(SpearOrc,3,8),(SpearOrc,4,8),(SpearOrc,5,8),(SpearOrc,6,8)],                                                                                  #If editing the levels, in general, bosses should be placed at 5,9, and should be placed last
              "main_3": [(Goblin,3,8),(Goblin,4,8),(Goblin,5,8),(Goblin,6,8),(SpearOrc,3,9),(SpearOrc,4,9),(SpearOrc,5,9),(SpearOrc,6,9)],                              #In the format (Enemy,x,y)
              "main_4": [(Goblin,1,7),(Goblin,1,9),(Goblin,0,8),(Goblin,2,8),(Goblin,8,7),(Goblin,8,9),(Goblin,9,8),(Goblin,7,8),(SpearOrc,1,8),(SpearOrc,8,8)],
              "main_5": [(SpearOrc,0,8),(SpearOrc,1,8),(SpearOrc,0,9),(SpearOrc,1,9),(SpearOrc,9,8),(SpearOrc,9,9),(SpearOrc,8,9),(SpearOrc,8,8)],
              "main_6": [(Grunt,4,8),(Grunt,5,8)],
              "main_7": [(Grunt,4,8),(Grunt,5,8),(SpearOrc,3,8),(SpearOrc,6,8),(SpearOrc,3,9),(SpearOrc,4,9),(SpearOrc,5,9),(SpearOrc,6,9)],
              "main_8": [(Griffin,4,8),(SpearOrc,3,9),(SpearOrc,4,9),(SpearOrc,5,9)],
              "main_9": [(Goblin,0,9),(Goblin,1,9),(Goblin,2,9),(Grunt,3,9),(Magician,4,9),(Magician,5,9),(Grunt,6,9),(Goblin,7,9),(Goblin,8,9),(Goblin,9,9)],
              "main_10": [(Magician,2,9),(Magician,7,9),(SpearOrc,3,9),(SpearOrc,4,9),(SpearOrc,5,9),(SpearOrc,6,9),(Goblin,0,8),(Goblin,1,8),(Goblin,2,8),(Goblin,3,8),(Goblin,4,8),(Goblin,5,8),(Goblin,6,8),(Goblin,7,8),(Goblin,8,8),(Goblin,9,8),(Dragon,4,9)],
              "ex_1": [(Chicken,0,9),(Chicken,1,9),(Chicken,2,9),(Chicken,3,9),(Chicken,5,9),(Chicken,6,9),(Chicken,7,9),(Chicken,8,9),(Chicken,9,9),(ChickenMan,4,9)],
              "ex_2": [(Grunt,3,9),(Grunt,5,9),(Basilisk,4,9)],
              "ex_3": [(ChickenManMan,4,9)],
              "ex_4": [(Goblin,2,9),(Goblin,3,9),(Goblin,5,9),(Goblin,6,9),(GoldenMan,4,9)],
              "ex_5": [(TreeMan,5,9)]}

#Import all level progress data
try:                                                            #If pickled save data exists...
    beaten = pickle.load(open("beaten.p","rb"))                 #...load that data into the memory
    print("Progress loaded successfully.")
except:                                                         #If save data doesn't exist...
    pickle.dump(beaten,open("beaten.p","wb"))                   #Save data
    print("No save data found, creating new save file...")

try:
    #Load sounds
    sword_mp3 = pygame.mixer.Sound("sword.wav")
    sword_mp3.set_volume(game_volume)

    archer_mp3 = pygame.mixer.Sound("archer.wav")
    archer_mp3.set_volume(game_volume)

    magic_mp3 = pygame.mixer.Sound("magic.wav")
    magic_mp3.set_volume(game_volume)

except:
    print("Could not load sound for some reason.")

##########################
####BEGIN GLOBAL SETUP####
##########################

widgets = []

#Introduce the window
root = Tk()                                                     #Create a new window
root.title = "Grid Wars"                                        #Change the name of the window
root.geometry("800x600")                                        #Set the default window size to 800×600px

for x in range(4):                                              #For each column...
    root.columnconfigure(x, weight = 3)                             #...set its weight to 3
for y in range(7):                                              #For each row...
    root.rowconfigure(y, weight = 1)                                #...set its weight to 1

root.columnconfigure(1, weight = 1)                             #Set the 2nd and 3rd columns to 2...
root.columnconfigure(2, weight = 1)                             #...to make the gaps wider than the buttons themselves

#Initialize frames
mainlevel_frame = Frame(root)
exlevel_frame = Frame(root)
grid_frame = Frame(root)
troopbutton_frame = Frame(root)

#Initialize widgets
img_title = Image.open("Grid Wars Title.png")
img_title_copy = img_title.copy()
phot_title = ImageTk.PhotoImage(img_title)
title = Label(root, image = phot_title)                         #The title of the game
title.image = phot_title                                        #Prevents the image from being garbage collected!
title.bind("<Configure>", resize_title)

usernamebox = Entry(root, text = "Text1")                       #The username entry box

check = Button(root, text = "Check", command = check_username,
               width = 7)                                       #The button which checks the username

start = Button(root, text = "Start", state = DISABLED,          #The start button
               command = go_levelselect)

settings = Button(root, text = "Settings",
                  command = go_settings)                        #The settings button

exitbutton = Button(root, text = "Exit",                        #The exit button
                    command = exit_clicked)

speed_slider = Scale(root, from_ = 0.5, to = 3,
                     orient=HORIZONTAL)                         #The game_speed slider
speed_slider.set(game_speed)                                    #Match the slider's value to the current game_speed

volume_slider = Scale(root, from_ = 0, to = 2,
                      orient=HORIZONTAL)                        #The game_volume slider
volume_slider.set(game_volume)                                  #Match the slider's value to the current game_volume

back = Button(root, text = "Back",
              command = go_back)

settings_title = Label(root, text = "Settings",
                       font = ("Arial", 44))                    #Title for the settings room

speed_header = Label(root, text = "Speed",
                     font = ("Arial", 20))                      #Label for the speed slider

volume_header = Label(root, text = "Volume",
                      font = ("Arial", 20))                     #Label for the volume slider

levelselect_title = Label(root, text = "Level Select",
                       font = ("Arial", 44))                    #Title for the level select room

leaderboard = Label(root, text = "Loading...", width = 10, height = 20, font = ("Arial",10))                  #Leaderboard

phot_levelselected = ImageTk.PhotoImage(level_thumbnails[level_selected])
level_info = Label(root, image = phot_levelselected)            #Contains the thumbnail for the selected level
level_info.bind("<Configure>", resize_levelinfo)

level_buttons = [("main_1", Button(mainlevel_frame, text = "1")),          #All buttons can be looked up (indexed) via a list
                 ("main_2", Button(mainlevel_frame, text = "2", state = DISABLED)),
                 ("main_3", Button(mainlevel_frame, text = "3", state = DISABLED)),
                 ("main_4", Button(mainlevel_frame, text = "4", state = DISABLED)),
                 ("main_5", Button(mainlevel_frame, text = "5", state = DISABLED)),
                 ("main_6", Button(mainlevel_frame, text = "6", state = DISABLED)),
                 ("main_7", Button(mainlevel_frame, text = "7", state = DISABLED)),
                 ("main_8", Button(mainlevel_frame, text = "8", state = DISABLED)),
                 ("main_9", Button(mainlevel_frame, text = "9", state = DISABLED)),
                 ("main_10", Button(mainlevel_frame, text = "10", state = DISABLED)),
                 ("ex_1", Button(exlevel_frame, text = "1")),                     #EX levels aren't initially disabled because they're invisible anyway...
                 ("ex_2", Button(exlevel_frame, text = "2")),                     #...though they're always available once unlocked
                 ("ex_3", Button(exlevel_frame, text = "3")),
                 ("ex_4", Button(exlevel_frame, text = "4")),
                 ("ex_5", Button(exlevel_frame, text = "5"))]
ex_label = Label(exlevel_frame, text = "EX")                             #The "EX" Label for the EX levels
ex_label.pack(side = LEFT, expand = True, fill = BOTH)

for level in range(10):                                         #Put the main level buttons into a frame
    level_buttons[level][1].pack(side = LEFT, expand = True, fill = BOTH)

for level in range(10,15):                                      #Put the EX level buttons into a frame
    level_buttons[level][1].pack(side = LEFT, expand = True, fill = BOTH)

for level in range(beaten["main"]):                             #Progress check main
    level_buttons[level][1].config(bg = "green")
    level_buttons[level+1][1].config(state = NORMAL)

for i in range(5):                                              #Progress check EX
    if beaten["ex_"+str(i+1)] == True: level_buttons[i+10][1].config(bg = "green")

play = Button(root, text = "Play", command = play_clicked)                              #"Play" button for level select and troop placement rooms
budget_widget = Label(root, text = "")

for button in level_buttons:
    button[1].bind("<1>", lambda event: change_level(event))

grid_buttons = [[None for i in range(10)] for j in range(10)]       #The grid of grid button widgets
#This closely links to the grid[][] matrix

for x in range(10):
    grid_frame.grid_columnconfigure(x, weight = 1, uniform = "x")

for y in range(10):
        grid_frame.grid_rowconfigure(y, weight = 1, uniform = "y")

#Assign functionality to the buttons
for x in range(10):
    for y in range(10):
        grid_buttons[x][y] = Label(grid_frame, relief = "raised")
        grid_buttons[x][y].bind("<1>", lambda event: place_troop(event))
        grid_buttons[x][y].bind("<3>", lambda event: remove_troop(event))
        grid_buttons[x][y].x = x
        grid_buttons[x][y].y = y
        grid_buttons[x][y].image = None
        grid_buttons[x][y].grid(row = y, column = x)
grid_buttons[0][0].bind("<Configure>", lambda event: resize_sprites(event))

troop_button_labels = ["Peasant (£400)\n2 ATK 8 HP", "Swordsman (£700)\n3 ATK 14 HP", "Phalanx (£1100)\n4 ATK 30 HP", "Knight (£1200)\n7 ATK 14 HP", "Archer (£700)\n3 ATK 7 HP", "Cleric (£1500)\n2 ATK 12 HP"]
troop_buttons = []
for i in range(6):
    troop_buttons.append(Button(troopbutton_frame, text = troop_button_labels[i]))
    troop_buttons[i].bind("<1>", lambda event: change_troop(event))
    troop_buttons[i].pack(side = TOP, expand = True, fill = BOTH)

SystemButtonFace = grid_buttons[0][0].cget("background")
go_mainmenu()
change_level(None)

try:                                                            #Try opening text-based data (username)
    with open("gw_data.txt","r") as file:
        lines = file.readlines()
        username = lines[0]                                     #The first line represents the player's username
        game_speed = int(lines[1])                              #The second line represents game_speed
        game_volume = int(lines[2])                             #The third line represents game_volume
        print("Settings loaded successfully.")                  #No need to do anything if the username doesn't exist, we will create the file later anyway

    usernamebox.insert(0,username)                              #If it can load the username, load it into usernamebox...
    check_username()                                            #...and then unlock the start button
except:
    #Check if there is a whitespace line in gw_data.txt...
    try:
        with open("gw_data.txt","r") as file:
            lines = file.readlines()
            username = lines[0]                                     #The first line represents the player's username
            game_speed = int(lines[2])                              #The second line represents game_speed
            game_volume = int(lines[3])                             #The third line represents game_volume
            print("Settings loaded successfully.")                  #No need to do anything if the username doesn't exist, we will create the file later anyway

        usernamebox.insert(0,username)                              #If it can load the username, load it into usernamebox...
        check_username()                                            #...and then unlock the start button

    except:
        print("Settings not loaded, will create settings when able.")

##########################
#####BEGIN MAIN LOOP######
##########################

print("Starting Grid Wars...")
root.mainloop()                                                 #Open the window using Tkinter

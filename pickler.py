import pickle

#Get all level progress data
try:                                                    #If save data exists...
    beaten = pickle.load(open("beaten.p","rb"))
except:                                                 #If save data doesn't exist...
    beaten = {"main": 0,
              "ex_1": 0,                                #Create new save data
              "ex_2": 0,
              "ex_3": 0,
              "ex_4": 0,
              "ex_5": 0}
    pickle.dump(beaten,open("beaten.p","wb"))           #Save data

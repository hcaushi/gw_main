import pymysql

leaderboard = pymysql.connect(host = "localhost",
                              user = "root",
                              passwd = "Password1",
                              db = "gw_leaderboard")
#Connect to the MySQL database

try:
    for i in range(15): #Because we want to create 15 leaderboards
        if i <= 9:
            createdb = "CREATE TABLE IF NOT EXISTS leaderboard_main_"+str(i+1)+"(username VARCHAR(10) NOT NULL UNIQUE, money_remaining INT UNSIGNED NOT NULL, date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (username));" #leaderboard_main 1 to 10

        else:
            createdb = "CREATE TABLE IF NOT EXISTS leaderboard_ex_"+str(i-9)+"(username VARCHAR(10) NOT NULL UNIQUE, money_remaining INT UNSIGNED NOT NULL, date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (username));" #leaderboard_ex_1 to 5

        c = leaderboard.cursor()
        c.execute(createdb) #Execute the given command
        c.close() #Close the cursor to halt memory leaks
    leaderboard.close() #Close the leaderboard after the operation is
    #complete

except (pymysql.Error, Exception) as error: #If MySQL returns an error…
    print(error) #…return the error passed by MySQL

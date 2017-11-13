'''

This file is used to delete temporary files in our temp directory

'''

import os

# This function makes a list of all '.txt' files 
# in our temp folder and removes them
def cleanupTxtFiles():
    mydir = os.getcwd() + '/temp'
    filelist = [f for f in os.listdir(mydir) if f.endswith(".txt")]
    for f in filelist:
        os.remove(os.path.join(mydir,f))
    print("Txt files deleted.")

# This function makes a list of all '.csv' files 
# in our temp folder and removes them
def cleanupCsvFiles():
    mydir = os.getcwd() + '/temp'
    filelist = [f for f in os.listdir(mydir) if f.endswith(".csv")]
    for f in filelist:
        os.remove(os.path.join(mydir,f))
    print("CSV files deleted.")

# The function allows the user to choose which
# data they want to keep and what they would like to delete
def cleanupPrompt():
    option1 = raw_input("Would you like to delete the temp folder and all tempory files \n" + 
        " created during this simulation? (y/n)\n").lower()
    if(option1 == 'y'):
        cleanupTxtFiles()
        cleanupCsvFiles()
        os.rmdir(os.getcwd() + '/temp')
        return
    option2 = raw_input("Would you like to delete TXT files with average queue wait time " +
         "\n and length statistical data from this simulation? (y/n)\n").lower()
    if(option2 == 'y'):
        cleanupTxtFiles()
    
    option3 = raw_input("Would you like to delete CSV files with average queue wait time " +
        "\n and length from this simulation? (y/n)\n").lower()
    if(option3 == 'y'):
        cleanupCsvFiles()

cleanupPrompt()
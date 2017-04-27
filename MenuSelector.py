# Game Menu for GoldDigger
# (C) 2017 By Eric Bennett
# Under Terms of CC License

# We need to import game and os to be able to call functions
import goldDigger
import os


# Begin Credits
def creditsGold():
    os.system('cls')
    print ("""
    GOLDDIGGER

    Created By:
    ...........Eric Bennett
    ...........Aaron Jeffers
    ...........Zach Polwrek

    Golddigger was created as a group project
    for our programming fundementals course at
    Holyoke Community College. For updates, view
    our Git at https://github.com/ebthepcguy/golddigger
    """)
    print("\n")
    input("Press enter to return to the main menu.")
    os.system('cls')
    mainMenu()
    menuOptions()

# Begin text for the main menu
def mainMenu():
    print ("""

 _____       _     _______ _                       
|  __ \     | |   | |  _  (_)                      
| |  \/ ___ | | __| | | | |_  __ _  __ _  ___ _ __ 
| | __ / _ \| |/ _` | | | | |/ _` |/ _` |/ _ \ '__|
| |_\ \ (_) | | (_| | |/ /| | (_| | (_| |  __/ |   
 \____/\___/|_|\__,_|___/ |_|\__, |\__, |\___|_|   
                              __/ | __/ |          
                             |___/ |___/           

    """)

    print ("""
===========================================
                 Main Menu
===========================================
-------------------------------------------
 Welcome to GoldDigger. Please select an 
 option from the list below & press enter
-------------------------------------------
""")

# Begin Dynamic Menu Options
def menuOptions():
    print ("""
[1.] Launch GoldDigger  [2.] View Credits

[3.] Load Saved Game    [4.] Exit Game   
--------------------------------------------
""")
    getInput = input("Select an option: ")

    if getInput == '1':
        main()

    if getInput == '2':
        creditsGold()

    if getInput == '3':
        input("Feature coming soon. Press enter.")
        os.system('cls')
        mainMenu()
        menuOptions()

    if getInput == '4':
        exit


mainMenu()
menuOptions()

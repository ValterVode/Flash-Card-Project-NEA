from customtkinter import *
from CTkMessagebox import CTkMessagebox
import random
import time
import os

Fails = 0
Count = 0
Time_Taken = 0


def SelectFile(File):
    if (open(File, "r")):
        return File
    else:
        return -1


def CreateFile(File, Contents):
    with open(File, "w") as F:
        for i in Contents:
            F.write(i)
            F.write("\n")


def DeleteFile(File):
    if (open(File, "r")):
        os.remove(File)
        return File
    else:
        return -1


Main_W = CTk()
Main_W.geometry("400x500")
set_appearance_mode("dark")
Title_L = CTkLabel(Main_W, text="Flash Card Quiz", font=("aerial", 20))
# Buttons and their subroutines
Current_File = "KeyWords.txt"


def Play():
    Main_W.withdraw()
    msg = CTkMessagebox(title="Start Quiz?", message="The quiz can be timed or untimed.\nDo you want to start?",
                        icon="question", option_1="No", option_2="Untimed", option_3="Timed")
    response = msg.get()

    if response == "Timed":
        Timed = True
        Quiz(Timed)

    elif response == "Untimed":
        Timed = False
        Quiz(Timed)
    else:
        Main_W.deiconify()


def Quiz(Timed):
    Quiz_W = CTk()
    Quiz_W.geometry("500x400")
    Quiz_Arr = []
    Fails = 0
    Count = 0
    Time_Start = time.time()
    Time_Taken = 0
    # Creates two arrays
    with open(Current_File, "r") as F:
        FILE_ARR = F.read().split("\n")
        for i in range(0, len(FILE_ARR), 2):
            Quiz_Arr.append([FILE_ARR[i], FILE_ARR[i+1], 0])
        Def_Arr = Quiz_Arr

    def Quiz_Loop():
        global Count
        if Count <= len(Quiz_Arr)-1:
            temp = []

            # Creates the answer and adds to temp array
            Keyword = Quiz_Arr[Count][0]
            Definition = Quiz_Arr[Count][1]
            temp.append(Quiz_Arr[Count][1])

            # Creates two random non-identical false answers
            Loop = 0
            while Loop < 2:
                temp_ = random.randint(0, len(Quiz_Arr)-1)
                if Quiz_Arr[temp_][1] not in temp:
                    temp.append(Quiz_Arr[temp_][1])
                    Loop += 1

            # randomly assigns the Definitions
            Definition_A = temp.pop(random.randint(0, len(temp)-1))
            Definition_B = temp.pop(random.randint(0, len(temp)-1))
            Definition_C = temp.pop(0)

            Keyword_L.configure(text=Keyword)
            Definition_A_L.configure(text=f"A) {Definition_A}")
            Definition_B_L.configure(text=f"B) {Definition_B}")
            Definition_C_L.configure(text=f"C) {Definition_C}")
            return Definition, Keyword, Definition_A, Definition_B, Definition_C
        else:
            Count = 0
            Definition, Keyword, Definition_A, Definition_B, Definition_C = Quiz_Loop()
            return Definition, Keyword, Definition_A, Definition_B, Definition_C

    if Count <= len(Quiz_Arr):
        temp = []

        # Creates the answer and adds to temp array
        Keyword = Quiz_Arr[Count][0]
        Definition = Quiz_Arr[Count][1]
        temp.append(Quiz_Arr[Count][1])

        # Creates two random non-identical false answers
        Loop = 0
        while Loop < 2:
            temp_ = random.randint(0, len(Quiz_Arr)-1)
            if Quiz_Arr[temp_][1] not in temp:
                temp.append(Quiz_Arr[temp_][1])
                Loop += 1

        # randomly assigns the Definitions
        Definition_A = temp.pop(random.randint(0, len(temp)-1))
        Definition_B = temp.pop(random.randint(0, len(temp)-1))
        Definition_C = temp.pop(0)

    def Answer(Response, Definition):
        global Count
        global Time_Taken
        if Response == Definition and Quiz_Arr[Count][2] == 1:
            Quiz_Arr.pop(Count)

        elif Response == Definition and Quiz_Arr[Count][2] != 1:
            Quiz_Arr[Count][2] += 1

        else:
            global Fails
            Fails += 1

        Count += 1
        print(Count)
        if len(Quiz_Arr) != 0:
            Definition, Keyword, Definition_A, Definition_B, Definition_C = Quiz_Loop()
        else:
            Quiz_W.destroy()
            if Timed:
                Time_End = time.time()
                Time_Taken += Time_End - Time_Start
                Foramted_Time = time.strftime(
                    "%H:%M:%S", Time_Taken)  # formats time
                Try_Again = CTkMessagebox(
                    title="Try_Again?", message=f"You failed {Fails} many times and you took {Foramted_Time} seconds long,Would you like to try again?", icon="question", option_1="No", option_2="Yes")
            else:
                pass
                Try_Again = CTkMessagebox(
                    title="Try_Again?", message=f"You failed {Fails} many times.Would you like to try again?", icon="question", option_1="No", option_2="Yes")
            response = Try_Again.get()
            if response == "Yes":
                Play()

            else:

                Main_W.deiconify()

    def Pause():
        global Time_Taken
        Quiz_W.withdraw()
        Pause_Start = time.time()
        Pause_M = CTkMessagebox(title="Paused", message="Continue quiz or leave?",
                                icon="question", option_1="Leave", option_2="Continue")
        response = Pause_M.get()
        if response == "Continue":
            Pause_End = time.time()
            Time_Taken -= Pause_End-Pause_Start
            Quiz_W.deiconify()
        else:
            Quiz_W.destroy()
            Main_W.deiconify()

    Title_L = CTkLabel(Quiz_W, text="Quiz")
    Keyword_L = CTkLabel(Quiz_W, text=f"{Keyword}:")
    Definition_A_L = CTkLabel(Quiz_W, text=f"A) {Definition_A}")
    Definition_B_L = CTkLabel(Quiz_W, text=f"B) {Definition_B}")
    Definition_C_L = CTkLabel(Quiz_W, text=f"C) {Definition_C}")

    Answer_A_B = CTkButton(Quiz_W, command=lambda: Answer(
        Definition_A, Definition), text="A", width=28)
    Answer_B_B = CTkButton(Quiz_W, command=lambda: Answer(
        Definition_B, Definition), text="B", width=28)
    Answer_C_B = CTkButton(Quiz_W, command=lambda: Answer(
        Definition_C, Definition), text="C", width=28)
    Pause_B = CTkButton(Quiz_W, command=lambda: Pause(), text="Pause")
    print(Count)
    Title_L.place(relx=0.2, rely=0.05, anchor='center')
    Keyword_L.place(relx=0.2, rely=0.2, anchor='center')
    Definition_A_L.place(relx=0.5, rely=0.3, anchor='center')
    Definition_B_L.place(relx=0.5, rely=0.5, anchor='center')
    Definition_C_L.place(relx=0.5, rely=0.7, anchor='center')

    Answer_A_B.place(relx=0.2, rely=0.9, anchor='center')
    Answer_B_B.place(relx=0.3, rely=0.9, anchor='center')
    Answer_C_B.place(relx=0.4, rely=0.9, anchor='center')
    Pause_B.place(relx=0.8, rely=0.05, anchor='center')

    Quiz_W.mainloop()


def Options():
    # Array which holds the data which is put into
    Add_File_Arr = []

    Main_W.withdraw()
    Options_W = CTk()
    Options_W.geometry("400x500")

    # Events for Options buttons
    def Select():
        global Current_File
        File = Select_T.get()
        File = File + ".txt"
        Current_File = File

    def Add(Add_File_Arr):
        Keyword = Keyword_T.get()
        Definition = Definition_T.get()
        Add_File_Arr.append(Keyword)
        Add_File_Arr.append(Definition)

    def Create(Add_File_Arr):
        File = File_Name_T.get()
        File = File + ".txt"
        CreateFile(File, Add_File_Arr)

    def Delete():
        File = Delete_T.get()
        File = File + ".txt"
        DeleteFile(File)

    def Back():
        Options_W.destroy()
        Main_W.deiconify()

    # Adds Lables for Options Window
    Select_L = CTkLabel(Options_W, text="Select:")
    File_Name_L = CTkLabel(Options_W, text="File_Name:")
    Keyword_L = CTkLabel(Options_W, text="Keyword:")
    Definition_L = CTkLabel(Options_W, text="Definition:")
    Delete_L = CTkLabel(Options_W, text="Delete:")
    # Adds Textboxes for Options Window
    Select_T = CTkEntry(Options_W)
    File_Name_T = CTkEntry(Options_W)
    Keyword_T = CTkEntry(Options_W)
    Definition_T = CTkEntry(Options_W)
    Delete_T = CTkEntry(Options_W)

    # Adds Buttons for Options Window
    Select_B = CTkButton(Options_W, command=Select, text="Select File")
    Add_B = CTkButton(Options_W, command=lambda: Add(
        Add_File_Arr), text="Add Contents")
    Create_B = CTkButton(Options_W, command=lambda: Create(
        Add_File_Arr), text="Create File")
    Delete_B = CTkButton(Options_W, command=Delete, text="Delete File")
    Back_B = CTkButton(Options_W, command=Back, text="Back")

    # Places all objects onto options window
    Select_L.place(relx=0.2, rely=0.05, anchor='center')
    File_Name_L.place(relx=0.2, rely=0.15, anchor='center')
    Keyword_L.place(relx=0.8, rely=0.15, anchor='center')
    Definition_L.place(relx=0.2, rely=0.25, anchor='center')
    Delete_L.place(relx=0.2, rely=0.45, anchor='center')

    Select_T.place(relx=0.25, rely=0.1, anchor='center')
    File_Name_T.place(relx=0.25, rely=0.2, anchor='center')
    Keyword_T.place(relx=0.75, rely=0.2, anchor='center')
    Definition_T.place(relx=0.25, rely=0.3, anchor='center')
    Delete_T.place(relx=0.25, rely=0.5, anchor='center')

    Select_B.place(relx=0.75, rely=0.1, anchor='center')
    Add_B.place(relx=0.75, rely=0.3, anchor='center')
    Create_B.place(relx=0.5, rely=0.4, anchor='center')
    Delete_B.place(relx=0.75, rely=0.5, anchor='center')
    Back_B.place(relx=0.25, rely=0.9, anchor='center')

    Options_W.mainloop()


def Quit():
    Main_W.destroy()


Play_B = CTkButton(Main_W, command=Play, text="Play")
Options_B = CTkButton(Main_W, command=Options, text="Options")
Quit_B = CTkButton(Main_W, command=Quit, text="Quit")

# Placing onto the Window relative to the window
Title_L.place(relx=0.5, rely=0.1, anchor='center')
Play_B.place(relx=0.5, rely=0.6, anchor='center')
Options_B.place(relx=0.5, rely=0.7, anchor='center')
Quit_B.place(relx=0.5, rely=0.8, anchor='center')

# Loop of window
Main_W.mainloop()

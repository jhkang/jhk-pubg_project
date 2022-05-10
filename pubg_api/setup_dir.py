import os

if os.path.isdir("Data") == False:
    os.mkdir("Data")
    os.mkdir("Data/Error_log")
    os.mkdir("Data/Train_data")
    print("Make directory: Data")

if os.path.isdir("DB") == False:
    os.mkdir("DB")
    print("Make directory: DB")

if os.path.isdir("Example/Data") == False:
    os.mkdir("Example/Data")
    os.mkdir("Example/Data/Error_log")
    os.mkdir("Example/Data/Train_data")
    print("Make directory: Example/Data")
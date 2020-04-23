import sys
import os
import pickle
import difflib
import datetime

def create_snapshot():
    input_path = input("Enter the path of which snapshot is to be taken: ") 
    entries = [] #This list will store the names of all files and directories present within the path directory
    length = len(input_path) #Path string length
    for path,dirs,files in os.walk(input_path):
        for i in dirs:
            entries.append(path[length:]+'/'+i)
        for j in files:
            entries.append(path[length:]+'/'+j)

    if not (os.path.exists(os.getcwd()+'/snapshots')): #It will create a 'snapshots' directory in the CWD if 'snapshots' directory does not exist
        os.mkdir('snapshots')
    
    dictOfMtimes = {i : os.path.getmtime(input_path+i) for i in entries} # Dictionary for storing the filenames and their modification times
    # print(dictOfMtimes)
    with open('snapshots/'+str(datetime.datetime.today()),'wb') as f: #Pickling the dictOfMtimes object, file will be named as present datetime
        pickle.dump(dictOfMtimes,f)


def list_snap_files():
    print("The snapshots files present are: ")
    for files in os.listdir(os.getcwd()+'/snapshots'):
        print(files)

def compare_snapshots(file1,file2):
    with open('snapshots/'+file1,'rb') as f1:
        obj1 = pickle.load(f1)
    with open('snapshots/'+file2,'rb') as f2:
        obj2 = pickle.load(f2)

    list1=[]
    list2=[]
    for item in obj1.keys():
        list1.append(item)
    for item in obj2.keys():
        list2.append(item)
    
    added = []
    removed = []
    common_files = []
    modified = []
    diff = difflib.ndiff('\n'.join(list1).splitlines(),'\n'.join(list2).splitlines())
    for l in diff:
        if l.startswith('-'):
            removed.append(l[1:])
        elif l.startswith('+'):
            added.append(l[1:])
        else:
            common_files.append(l.strip())

    for files in common_files:
        if obj1[files]!=obj2[files]:
            modified.append(files)

    print("Files/Directories removed from current snapshots: ")
    for i in removed:
        print(i)
    print("Files/Directories added in current snapshots: ")
    for i in added:
        print(i)
    print("Files/Directories modified: ")
    for i in modified:
        print(i)
    

def compare_files():
    list_of_files = os.listdir(os.getcwd()+'/snapshots')
    dictOfFiles = { i+1 : list_of_files[i] for i in range(len(list_of_files))}
    print("Index        File Name")
    print("======================")
    for i,j in dictOfFiles.items():
        print(f"{i}     ->    {j}")
    print("Enter the indexes of snapshots you want to compare: ")
    a = int(input("Index of older snapshot: "))
    b = int(input("Index of newer snapshot: "))
    compare_snapshots(dictOfFiles[a],dictOfFiles[b])

    
def show_help():
    print("For help, refer documentation")


def main():
    print("DIRECTORY/FILE COMPARISON TOOL")
    print("=================================")
    print("Please type a number and press enter: \n")
    print("1. Create a snapshot")
    print("2. List snapshot files")
    print("3. Compare Snapshots")
    print("4. Help")
    print("5. Exit")
    choice = int(input("Enter your choice: "))
    
    if(choice == 1):
        create_snapshot()
    elif(choice == 2):
        list_snap_files()
    elif(choice == 3):
        compare_files()
    elif(choice == 4):
        show_help()
    elif(choice == 5):
        sys.exit()
    else:
        print("Invalid choice!")


if __name__=="__main__":
    main()

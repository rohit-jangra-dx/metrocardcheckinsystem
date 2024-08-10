from sys import argv
from src.MetroCard import MetroCard
from src.CheckInSystem import CheckInSystem

def main():

    # if len(argv) != 2:
    #     raise Exception("File path not entered")
    
    file_path = "./sample_input/input2.txt"
    f = open(file_path, 'r')
    Lines = f.readlines()
    
    check_in_system = CheckInSystem( fileInput= Lines)
    
    check_in_system.print_summary('CENTRAL')
    check_in_system.print_summary('AIRPORT')

if __name__ == "__main__":
    main()
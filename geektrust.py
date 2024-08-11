from sys import argv
from src.MetroCard import MetroCard
from src.CheckInSystem import CheckInSystem

def main():

    if len(argv) != 2:
        raise Exception("File path not entered")
    
    file_path = argv[1]
    f = open(file_path, 'r')
    Lines = f.readlines()
    
    check_in_system = CheckInSystem( fileInput= Lines)
    
    check_in_system.print_summary('CENTRAL')
    check_in_system.print_summary('AIRPORT')

    # print(check_in_system.metrics_summary_obj)

if __name__ == "__main__":
    main()
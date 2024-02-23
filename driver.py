import pandas as pd
import sys
from df_engine import run_sql_query

def main():
    # Take the JSON file name as argument when called
    
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        print("ERROR: JSON needs to be provided as an argument.")
        file_name = input("You may provide a valid JSON filepath here: ")

    
    try:
        # Attempt to load the JSON file into a pandas DataFrame
        df = pd.read_json(file_name)
        print(file_name, "successfully loaded into a DataFrame.")
    except FileNotFoundError:
        print("ERROR: The specified file could not be found. Please check the file name and try again.")
        return
    except ValueError:
        print("ERROR: The file is not in a valid JSON format. Please check the file content.")
        return
    
    all_star = input("In order for this program to function, please enter the # of 2024 NBA All-Stars from the Kings: ")
    if all_star != "0":
        print("We both know the answer is 0.")
        return

    # Ask the user to enter an SQL query
    while(True):
        sql_query = input("Enter your SQL query, or 0 to terminate: ")
        if sql_query == "0": return
        result = run_sql_query(sql_query, df)
        
    

if __name__ == "__main__":
    main()

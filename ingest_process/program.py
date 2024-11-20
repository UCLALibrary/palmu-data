import os
import pandas as pd

def add_program_column_to_csvs(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.csv'):  # Process only CSV files
                file_path = os.path.join(root, file)
                try:
                    # Read the CSV into a DataFrame
                    df = pd.read_csv(file_path)
                    
                    # Add the 'Program' column with the value for all rows
                    df['Program'] = 'International Digital Ephemera Project'
                    
                    # Save the updated DataFrame back to the file
                    df.to_csv(file_path, index=False)
                    print(f"Added 'Program' column to: {file_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    # Ask user for the folder path
    folder_path = input("Enter the path to the folder containing CSV files: ").strip()
    if os.path.exists(folder_path):
        add_program_column_to_csvs(folder_path)
    else:
        print("The provided folder path does not exist.")

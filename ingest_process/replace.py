import os
import pandas as pd

def rename_csv_headers(folder_path):
    # Walk through the directory up to 2 levels deep
    for root, dirs, files in os.walk(folder_path):
        # Calculate depth to limit recursion to 2 levels
        depth = root[len(folder_path):].count(os.sep)
        if depth > 2:
            continue
        
        for file in files:
            if file.endswith('.csv'):  # Process only CSV files
                file_path = os.path.join(root, file)
                try:
                    # Read the CSV into a DataFrame
                    df = pd.read_csv(file_path)
                    
                    # Rename the column if "newtitle" exists
                    if "newtitle" in df.columns:
                        df.rename(columns={"newtitle": "Title"}, inplace=True)
                        # Save the updated CSV back to the same file
                        df.to_csv(file_path, index=False)
                        print(f"Updated column in: {file_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    # Ask user for the folder path
    folder_path = input("Enter the path to the folder containing CSV files: ").strip()
    if os.path.exists(folder_path):
        rename_csv_headers(folder_path)
    else:
        print("The provided folder path does not exist.")

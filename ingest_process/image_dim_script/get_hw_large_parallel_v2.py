import pandas as pd
from PIL import ImageFile, Image
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os
import time
import logging
import sys

batch = sys.argv[1]

logger = logging.getLogger(__name__)

logging.basicConfig(filename=f'{batch}.log', encoding='utf-8', level=logging.INFO)

# Get CSV file to output errors
# Check to see if there is an existing errors csv otherwise create one
if os.path.isfile("errors.csv"): 
    errs = pd.read_csv("errors.csv")
else:
    errs = pd.DataFrame(columns=["csv file", "row number", "error message"])

def timer(s, msg):
    for _ in tqdm(range(s*2), desc=msg):
            time.sleep(0.5)

def get_csv_file(path):    
    # Get input CSV file path from user and strip extra whitespace
    csv_file_path = path.strip()
    # Extract file name without extension
    file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    complete = False
    # Check to see if there is an existing csv otherwise read CSV file

    if os.path.isfile(file_name + "_dim.csv"):
        df = pd.read_csv(file_name + "_dim.csv")
        print(f"found existing csv {file_name}_dim.csv")
        logger.info(f"found existing csv {file_name}_dim.csv")
        if df["media.height"].isna().sum() == 1 and df["media.width"].isna().sum()==1:
            print(f"No errors detected in {file_name}_dim.csv")
            logger.info(f"No errors detected in {file_name}_dim.csv")
            complete = True
    else:
        df = pd.read_csv(csv_file_path)
        df['media.height'] = None # Create new columns for height and width
        df['media.width'] = None
    return df, complete

    
row_count = 0 #start counter for number of rows processed
# Function to get image dimensions from URL
# If try catch encounters an error will append to the errors csv
def get_image_dimensions(url, index, file_name):
    try:
        Image.MAX_IMAGE_PIXELS = None
        size = int(requests.get(url).headers.get("content-length"))        
        resume_header = {'Range': f'bytes=0-{size*0.001}'}    ## the amount of bytes you will download
        response = requests.get(url, stream = True, headers = resume_header)
        response.raise_for_status()  # Check that the request was successful
        p = ImageFile.Parser()
        p.feed(response.content)    ## feed the data to image parser to get photo info from data headers
        if p.image:
            width, height = p.image.size
        else:
            raise Exception("Error getting image")
        return width, height
    except Exception as e:
        print(f"Error getting dimensions for {url}: {e}")
        logger.error(f"{file_name}.csv row {index}, Error getting dimensions for {url}: {e}")
        errs.loc[len(errs)] = [file_name + ".csv", index, f"Error getting dimensions for {url}: {e}" ]
        return None, None

# Function to update DataFrame with image dimensions
def update_dimensions(index, row, file_name):
    if row["Object Type"] == "Work" and (pd.isnull(row["media.height"]) == True or pd.isnull(row["media.width"]) == True):
        global row_count
        row_count +=1
        image_url_column = 'IIIF Access URL'
        image_url = row[image_url_column]
        width, height = get_image_dimensions(image_url, index, file_name)
        df.at[index, 'media.width'] = width
        df.at[index, 'media.height'] = height

def process_csv(df, file_name):
    start_time = time.time()
    # Update DataFrame with image dimensions in parallel using concurrent.futures module

    with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers based on your system
        futures = [executor.submit(update_dimensions, index, row, file_name) for index, row in df.iterrows()]
        for future in tqdm(futures, total=len(futures), desc=f"Processing images for {filename}"):
            future.result()


    # Save the updated DataFrame to a new CSV file with original file name
    output_csv_file_path = f'{file_name}_dim.csv'
    df.to_csv(output_csv_file_path, index=False)

    # Check to see if errors were generated, if so export errors file, if not discard
    if len(errs) > 0:
        errs.to_csv("errors.csv", index=False)

    # Print out a confirmation message
    print(f"Image dimensions added and saved to {output_csv_file_path}")
    logger.info(f"Image dimensions added and saved to {output_csv_file_path}")
    print(f"Rows processed: {row_count}  Time Elapsed: {time.time() - start_time} seconds" )
    logger.info(f"{output_csv_file_path} Rows processed: {row_count}  Time Elapsed: {time.time() - start_time} seconds" )

# Main behavior or script



print(f"fetching dimensions for {batch} csv files in ingest_process/need-dims/")
logger.info(f"fetching dimensions for {batch} csv files in ingest_process/need-dims/")
for filename in sorted(os.listdir(f"ingest_process/need-dims/{batch}")):
    df, complete = get_csv_file(f"ingest_process/need-dims/{batch}/{filename}")
    if complete == False:
        print(f"getting dimensions for {filename}")
        process_csv(df, filename[:-4])
        df, complete = get_csv_file(f"ingest_process/need-dims/{batch}/{filename}")
        if complete == False:
            timer(60, "Waiting 1min run again and fix any errors")
            process_csv(df, filename)
        timer(120, "Waiting 2min to fetch next csv")



print(f"Finished fetching dimensions for {batch} csv files in ingest_process/need-dims/")
logger.info(f"Finished fetching dimensions for {batch} csv files in ingest_process/need-dims/")
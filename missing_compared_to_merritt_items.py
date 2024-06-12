import pandas as pd, numpy as np, re, os
from numpy import nan 

merritt_items  = pd.read_csv("file-lists/PalMu_Merritt_objects.csv")
merritt_items["Path"] = merritt_items["Path"].apply(lambda x: x[:-4])

full_metadata = pd.read_csv("file-lists/pm_export_2022-12-08_combined_dlp (1).csv")


missing_box_items = pd.read_csv("file-lists/missing.csv")
missing_box_items ["file"] = missing_box_items ["file"].apply(lambda x: x[:-4])


Box_Contents_Results_Compared_To_Merritt = pd.DataFrame(columns=['file', 'In Merritt'])
# Are there any images in the missing folder that are either/both: also in Merritt DO NOT have a metadata record
#the merrit comparison is an image to image comparison and the metadata comparison is a record level comparison
for index, row in missing_box_items.iterrows():
    result = [row["file"], ""]
    print(row["file"])
    if len(merritt_items[merritt_items["Path"] == row["file"]]) == 1:
        result[1] = "Yes"
        Box_Contents_Results_Compared_To_Merritt.loc[index] = result
            

Box_Contents_Results_Compared_To_Merritt.to_csv("Box_Contents_Results_Compared_To_Merritt.csv", index= False)


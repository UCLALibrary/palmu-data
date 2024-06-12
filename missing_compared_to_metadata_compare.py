import pandas as pd, numpy as np, re, os
from numpy import nan 

merritt_items  = pd.read_csv("file-lists/PalMu_Merritt_objects.csv")
merritt_items["Path"] = merritt_items["Path"].apply(lambda x: x[:-4])

full_metadata = pd.read_csv("file-lists/pm_export_2022-12-08_combined_dlp (1).csv")


missing_box_items = pd.read_csv("file-lists/missing.csv")


Box_Contents_Results_Compared_To_Metadata_Record = pd.DataFrame(columns=['Local ID', 'Metadata Record'])

for index, row in missing_box_items.head(1000).iterrows():
    result = [row["object"],""]
    if len(full_metadata[full_metadata["local ID"] == row["object"]]) == 0:
        result[2] = "No"
    Box_Contents_Results_Compared_To_Metadata_Record.loc[index] = result

Box_Contents_Results_Compared_To_Metadata_Record.to_csv("Box_Contents_Results_Compared_To_Metadata_Record.csv", index= False)
    
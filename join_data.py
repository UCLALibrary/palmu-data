import pandas as pd, numpy as np, re, os, functools as ft
from numpy import nan 

missing_box_items = pd.read_csv("file-lists/missing.csv")
missing_box_items ["file"] = missing_box_items ["file"].apply(lambda x: x[:-4])

Box_Contents_Results_Compared_To_Metadata = pd.read_csv("Box_Contents_Results_Compared_To_Metadata.csv")

Box_Contents_Results_Compared_To_Merritt = pd.read_csv("Box_Contents_Results_Compared_To_Merritt.csv")

dfs = [missing_box_items, Box_Contents_Results_Compared_To_Metadata, Box_Contents_Results_Compared_To_Merritt]
join_data = ft.reduce(lambda left, right: pd.merge(left, right, on='file',  how='outer'), dfs)

join_data.loc[join_data["Has Metadata record"].isnull(),'Has Metadata record'] = "No"
join_data.loc[join_data["In Merritt"].isnull(),'In Merritt'] = "No"

join_data.to_csv("Missing_compared_to_metadata_and_merritt.csv")
import hashlib
from tqdm import tqdm
import csv
import json
# f = open("chembl_22_clean_1576904_sorted_std_final.smi", "r")
target_hash = "1c602d1f2b2e45361760adfae4f2e5b99c976a34daea4a92a42abc6bc6556c5f"
# file = "SMILES_Big_Data_Set.csv"
file = "Pitt_Quantum_Repository_Data.json"

data = json.load(open(file, "r"))

for x in tqdm(data):
    if "smiles" not in x:
        continue
    smi = x["smiles"]
    hash_object = hashlib.sha256(smi.encode())
    hex_dig = hash_object.hexdigest()
    if hex_dig == target_hash:
        print(f"Found: {smi}")
        break
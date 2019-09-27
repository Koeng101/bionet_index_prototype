import requests
import subprocess
import re
import pandas as pd
import io
from tinydb import TinyDB, Query
db = TinyDB('db.json')



parts = requests.get('https://api.freegenes.org/parts/').json()
df = pd.read_csv("files/info_igem.csv")
df["Seq"] = df["Info"].apply(lambda x: x.replace("('","").replace("'","").split(",")[0])

f = open("blastdb/blast.fasta", "w")
for part in parts:
    if type(part['optimized_sequence']) == str:
        f.write(">{}".format(part['gene_id']))
        f.write("\n")
        f.write(part['optimized_sequence'])
        f.write("\n")

pattern = "^[atgcATGC]*$"
for i,row in df.iterrows():
    s = str(row['Seq']).replace("\\n","").replace("\n","")
    if bool(re.match(pattern,s)) == True:
        f.write(">{}\n".format(row['Name']))
        f.write(s + "\n")

for i in db:
    df = pd.read_csv(io.StringIO(requests.get(i['url'].rsplit('/',1)[0] + '/export?format=csv').content.decode('utf-8')))
    for i,row in df.iterrows():
        f.write(">{}".format(row['Name']))
        f.write("\n")
        f.write(row['Sequence'])
        f.write("\n")
 
f.close()

subprocess.check_output('cd blastdb && ./makeblast_database.sh && cd ..',shell=True)


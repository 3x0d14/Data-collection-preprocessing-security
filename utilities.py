from datetime import datetime
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
import secrets
import os

def Gen_Key_File():
    out_f = "PK_"+str(int(datetime.timestamp(datetime.now())))
    with open(out_f,"wb") as out:
        key = secrets.token_bytes(32)
        out.write(key)
    return out_f

def Enc_csv(file,key):
    n = secrets.token_bytes(12)
    with open(key,"rb") as k:
        pk = k.read()
    encryptor = AESCCM(pk)
    out = "_".join(os.path.split(file)[-1].split(".")[:-1]) + "_CYPH_"+ key.split("_")[1]
    with open(file,"rb") as in_file:
        data = in_file.read()
    
    cypher = n + encryptor.encrypt(n,data,b"")
    with open(out,"wb") as out_file:
        out_file.write(cypher)


def Dec_csv(file,key):
    with open(key,"rb") as k:
        pk = k.read()
    encryptor = AESCCM(pk)
    ori =  os.path.split(file)[-1]
    ori_s = ori.split("_")
    out = "".join(ori_s[:-2]) + "_"+ori_s[-1] + ".csv"
    with open(file,"rb") as in_file:
        cypher = in_file.read()
    data = encryptor.decrypt(cypher[:12],cypher[12:],b"")
    with open(out,"wb") as out_file:
        out_file.write(data)

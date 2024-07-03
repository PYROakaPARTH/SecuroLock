import zipfile as z
import shutil
import os

# fileName = "xxPYROxx"


target = "C:/Users/Parth/Desktop/Python projects/Project/User Folders/kkPYROkk_decrypted.zip"
    
root = z.ZipFile(target)
    
root.extractall("C:/Users/Parth/Desktop/Python projects/Project/User Folders/kkPYROkk_decrypted")
    
root.close()


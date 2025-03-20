#To Do - Script to sort images in a folder based on their face profile
# uninstall deepface and install from github

import os
import numpy as np
import shutil
from dotenv import load_dotenv
from deepface import DeepFace as df
from utility import utils as ut


load_dotenv()


output_path = os.getenv('OUTPUT_PATH')
input_path = os.getenv('INPUT_PATH')


os.makedirs(output_path, exist_ok=True)



def sorting_process():
    folder_db={}
    embedding_db={}
    counter=1
    embedding_db=ut.generate_embedding()
    #print(embedding_db)
    for image,embedding in embedding_db.items():
        if len(folder_db)==0:
            os.makedirs(output_path+f'/Person_{counter}', exist_ok=True)
            shutil.copy(input_path+'/'+image, output_path+f'/Person_{counter}')
            folder_db[output_path+f'/Person_{counter}']=image
            counter+=1
        else:
            for folder,img in folder_db.items():
                if df.verify(img1_path=input_path+'/'+image, img2_path=input_path+'/'+img)['verified']:
                    shutil.copy(input_path+'/'+image, folder)
                    break
            else:
                os.makedirs(output_path+f'/Person_{counter}', exist_ok=True)
                shutil.copy(input_path+'/'+image, output_path+f'/Person_{counter}')
                folder_db[output_path+f'/Person_{counter}']=image
                counter+=1
    print('Sorting completed')
    
if __name__ == '__main__':
    sorting_process()





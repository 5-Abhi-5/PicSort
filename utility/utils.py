import os
import shutil
from dotenv import load_dotenv
from deepface import DeepFace as df

load_dotenv()

input_path = os.getenv('INPUT_PATH')
output_path = os.getenv('OUTPUT_PATH')

def check_valid_ext(image_path: str):
    ext = image_path.split('.')[-1]
    if ext.lower() not in ['jpg', 'jpeg', 'png']:
        return False
    return True
    
def generate_embedding():
    db={} #Database to store embeddings
    for image in os.listdir(input_path):
        if check_valid_ext(image):
            print('Valid image found:', image)
            try:
                embedding = df.represent(input_path+'/'+image)
                db[image] = embedding
                #print(embedding)
            except Exception as e:
                print('Error in embedding:', e)
                os.makedirs(output_path+'/NO_FACE', exist_ok=True)
                shutil.copy(input_path+'/'+image, output_path+'/NO_FACE/'+image)
                continue
        else:
            print('Invalid image found:', image)
            os.makedirs(output_path+'/invalid', exist_ok=True)
            shutil.copy(input_path+'/'+image, output_path+'/invalid/'+image)
            continue
    return db
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from script import sorting_process
import shutil
import zipfile
import os
from dotenv import load_dotenv

load_dotenv()

input_path = os.getenv('INPUT_PATH')
upload_path = os.getenv('UPLOAD_PATH')
output_path = os.getenv('OUTPUT_PATH')
root_limit=os.getenv('ROOT_LIMIT')
upload_limit=os.getenv('UPLOAD_LIMIT')


limiter = Limiter(
    key_func=get_remote_address,
)

app = FastAPI(
    title="PicSort API",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
@limiter.limit(root_limit)
async def root(request: Request):
    return {"message":"Hey You've reached PicSort Backend!"}


#input file is a zip file with folder containing images
@app.post("/uploadfile")
@limiter.limit(upload_limit)
async def upload_file(request: Request, file: UploadFile):
    
    os.makedirs(input_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)
    
    zip_path = os.path.join(input_path, file.filename)

    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file.file.close()

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(upload_path)
    
    os.remove(zip_path)
    
    sorting_process()
      
    zip_output_path = os.path.join(output_path, "sorted_images.zip")  
    shutil.make_archive(base_name=zip_output_path.replace(".zip", ""), format="zip", root_dir=output_path)  
     
    return FileResponse(
        path=zip_output_path,
        media_type="application/zip",
        filename="sorted_images.zip",
    )
        
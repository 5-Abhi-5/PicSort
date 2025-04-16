# PicSort - Face-Based Image Sorter API

**PicSort** is a FastAPI-based mini backend that takes a zipped folder of images, detects and analyzes faces using DeepFace, and returns a zipped folder of images grouped into folders by unique faces. It also detects and separates images with:

- **No faces** (in a `no_faces` folder)
- **Invalid/corrupt files** (in an `invalid` folder)

---

## Features

- Upload a zipped folder of images
- Automatically detect and group similar faces into individual folders
- Separate:
  - Images with no face
  - Corrupted or unreadable files
- Download a zipped, sorted version of your original dataset
- In-memory face matching using DeepFace + Facenet (no database required)
- CORS-enabled for frontend integration

---

## Tech Stack

- **Python 3.8+**
- **FastAPI**
- **DeepFace** (with Facenet and VGG model)
- **OpenCV, shutil**
- **Uvicorn** (ASGI server)

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/5-Abhi-5/PicSort.git
cd picsort
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
uvicorn main:app --reload
```

---

## Endpoint

### 🔹 `POST /uploadfile` — Upload a Zipped Folder of Images
- **Description:** Upload a `.zip` file containing folder with images. The server processes and groups them by face similarity.
- **Request Body:** `multipart/form-data`
  - **Field:** `file` (type: File)
- **Response:** `200 OK` with downloadable zipped file.  


### Curl Example (localhost)
```bash
curl -X POST "http://127.0.0.1:8000/uploadfile" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/images_path.zip;type=application/x-zip-compressed"

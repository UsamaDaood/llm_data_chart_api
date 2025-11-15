from fastapi import APIRouter, UploadFile, HTTPException
from uuid7 import uuid7
import pandas as pd
from app.storage import DATASETS
from app.models import UploadResponse

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile):
    try:
        fname = file.filename.lower()
        if fname.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif fname.endswith(".json"):
            df = pd.read_json(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use CSV or JSON.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {e}")

    dataset_id = str(uuid7())
    DATASETS[dataset_id] = df
    return UploadResponse(dataset_id=dataset_id)

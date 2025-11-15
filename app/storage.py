# Simple in-memory storage; replace with DB/S3 in production.
from typing import Dict
import pandas as pd

DATASETS: Dict[str, pd.DataFrame] = {}
CHARTS: Dict[str, dict] = {}

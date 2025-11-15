from pydantic import BaseModel, Field
from typing import Optional, Literal

class UploadResponse(BaseModel):
    dataset_id: str = Field(...)

class QueryRequest(BaseModel):
    dataset_id: str = Field(...)
    query: str = Field(..., min_length=2)
    chart_lib: Literal["matplotlib", "plotly"] = "matplotlib"

class QueryResponse(BaseModel):
    chart_id: str = Field(...)
    chart_type: Literal["png", "html"] = Field(...)
    meta: Optional[dict] = None

class ChartResponse(BaseModel):
    chart_id: str = Field(...)
    chart_type: Literal["png", "html"] = Field(...)
    payload_base64: Optional[str] = None
    payload_html: Optional[str] = None

from fastapi import APIRouter, HTTPException
from uuid7 import uuid7
from app.storage import DATASETS, CHARTS
from app.models import QueryRequest, QueryResponse, ChartResponse
from app.services.schema import dataframe_schema
from app.services.llm import generate_plot_code
from app.services.sandbox import run_plot_code, SandboxError
from app.services.chart import chart_payload

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_chart(req: QueryRequest):
    df = DATASETS.get(req.dataset_id)
    if df is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    schema = dataframe_schema(df)
    plan = generate_plot_code(req.query, schema, lib=req.chart_lib)

    missing = [c for c in plan["requirements"] if c not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {missing}")

    try:
        result = run_plot_code(plan["code"], df=df, lib=plan["lib"])
    except SandboxError as e:
        raise HTTPException(status_code=400, detail=str(e))

    chart_type, payload = chart_payload(result)
    chart_id = str(uuid7())
    CHARTS[chart_id] = {"chart_type": chart_type, **payload}

    return QueryResponse(chart_id=chart_id, chart_type=chart_type, meta={"lib": plan["lib"]})

@router.get("/{chart_id}", response_model=ChartResponse)
async def get_chart(chart_id: str):
    chart = CHARTS.get(chart_id)
    if chart is None:
        raise HTTPException(status_code=404, detail="Chart not found")

    return ChartResponse(
        chart_id=chart_id,
        chart_type=chart["chart_type"],
        payload_base64=chart.get("payload_base64"),
        payload_html=chart.get("payload_html"),
    )

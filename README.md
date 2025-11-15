# 📊 LLM-Powered Data-to-Chart Converter (Backend API)

A backend-only FastAPI service that:

- Accepts **CSV/JSON uploads**
- Interprets **natural language queries** with an LLM (stubbed by default)
- Generates **charts** using Matplotlib or Plotly
- Returns chart assets via **API responses** (PNG base64 or HTML)

This project is designed to be consumed by **mobile or web apps** as an API layer.

## 📂 Project Structure

```bash

llm_data_chart_api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entrypoint
│   ├── config.py               # Environment settings
│   ├── models.py               # Pydantic models for requests/responses
│   ├── storage.py              # In-memory dataset & chart storage
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm.py              # Stubbed LLM query → plotting code
│   │   ├── schema.py           # Extract dataframe schema
│   │   ├── sandbox.py          # Restricted code execution
│   │   └── chart.py            # Chart payload formatting
│   └── routers/
│       ├── __init__.py
│       ├── health.py           # Health check endpoint
│       ├── datasets.py         # Upload CSV/JSON
│       └── charts.py           # Query dataset & retrieve chart
├── tests/
│   └── test_api.py             # Basic API tests
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .env.example                # Example environment variables

```

# ⚙️ Setup Instructions

Clone the repo

```bash
git clone https://github.com/UsamaDaood/llm_data_chart_api.git
cd llm_data_chart_api
```

## Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

## Install dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

💡 If you encounter metadata-generation-failed, upgrade pip/setuptools/wheel as shown above. Some packages (e.g., RestrictedPython) may require Python ≤3.11. If you’re on Python 3.12+, loosen the pin in requirements.txt.

## Run the server

```bash
uvicorn app.main:app --reload
```

## 🚀 Usage

#### 1. Upload a dataset

```bash
http
POST /datasets/upload
Content-Type: multipart/form-data
file=@sales.csv
Response:

json
{ "dataset_id": "123e4567-e89b-12d3-a456-426614174000" }
```

#### 2. Query the dataset

```bash
http
POST /charts/query
Content-Type: application/json

{
  "dataset_id": "123e4567-e89b-12d3-a456-426614174000",
  "query": "show me sales growth over time",
  "chart_lib": "matplotlib"
}
Response:

json
{
  "chart_id": "abcd1234",
  "chart_type": "png",
  "meta": { "lib": "matplotlib" }
}
```

#### 3. Retrieve the chart

```bash
http
GET /charts/abcd1234
Response (PNG base64):

json
{
  "chart_id": "abcd1234",
  "chart_type": "png",
  "payload_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
For Plotly charts, you’ll get:

json
{
  "chart_id": "efgh5678",
  "chart_type": "html",
  "payload_html": "<div>...</div>"
}
```

### 🛡️ Security Notes

Sandbox execution: Generated plotting code runs in a restricted environment.

Validation: Queries are checked against dataset columns.

Authentication: Add JWT/API keys before production use.

Storage: Currently in-memory; swap for DB/S3 in production.

### ✅ Testing

Run tests with:

```bash
pytest tests/
```

### 📌 Example Workflow

Upload sales.csv with columns date, revenue.

Query: "show me revenue growth over time".

Retrieve chart → mobile/web app renders PNG or embeds Plotly HTML.

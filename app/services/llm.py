# Stubbed LLM that converts NL queries + schema into plotting instructions.
# Replace with real provider integration when ready.

from typing import Dict

def generate_plot_code(query: str, schema: Dict, lib: str = "matplotlib") -> Dict:
    """
    Returns a dict with:
    - 'language': 'python'
    - 'lib': 'matplotlib'|'plotly'
    - 'code': Python code string that expects a 'df' variable available
    - 'chart_type': 'png'|'html'
    - 'requirements': list of column names used
    """
    cols = [c["name"] for c in schema["columns"]]
    chart_type = "png" if lib == "matplotlib" else "html"

    code_templates = {
        "matplotlib_line": """
import matplotlib.pyplot as plt
import io
buf = io.BytesIO()
x_col = '{x}'
y_col = '{y}'
plt.figure(figsize=(8, 4))
plt.plot(df[x_col], df[y_col], marker='o')
plt.title('Line: ' + y_col + ' over ' + x_col)
plt.xlabel(x_col); plt.ylabel(y_col)
plt.tight_layout()
""",
        "plotly_bar": """
import plotly.express as px
fig = px.bar(df, x='{x}', y='{y}', title='Bar: {y} by {x}')
html = fig.to_html(include_plotlyjs='cdn', full_html=False)
""",
    }

    q = query.lower()
    x = cols[0] if cols else "x"
    y = cols[1] if len(cols) > 1 else "y"

    if "growth" in q or "trend" in q or "over time" in q:
        code = code_templates["matplotlib_line"].format(x=x, y=y)
        return {
            "language": "python",
            "lib": "matplotlib",
            "code": code,
            "chart_type": "png",
            "requirements": [x, y],
        }
    elif "by" in q or "compare" in q or "versus" in q:
        code = code_templates["plotly_bar"].format(x=x, y=y)
        return {
            "language": "python",
            "lib": "plotly",
            "code": code,
            "chart_type": "html",
            "requirements": [x, y],
        }
    else:
        code = code_templates["matplotlib_line"].format(x=x, y=y)
        return {
            "language": "python",
            "lib": lib,
            "code": code,
            "chart_type": chart_type,
            "requirements": [x, y],
        }

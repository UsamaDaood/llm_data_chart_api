# Restricted execution of generated Python plotting code.
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins
from types import MappingProxyType

class SandboxError(Exception):
    pass

def run_plot_code(code: str, df, lib: str):
    """
    Executes plotting code in a restricted environment.
    Requires that the code uses 'df' and writes either:
      - Matplotlib: a PNG into BytesIO 'buf' and leaves it seeked to 0
      - Plotly: an 'html' variable with the chart string
    """
    byte_code = compile_restricted(code, filename="<llm>", mode="exec")
    if not byte_code:
        raise SandboxError("Compilation failed")

    builtins = dict(safe_builtins)
    globals_dict = {
        "__builtins__": MappingProxyType(builtins),
    }
    locals_dict = {"df": df}

    try:
        exec(byte_code, globals_dict, locals_dict)
    except Exception as e:
        raise SandboxError(f"Execution error: {e}")

    if lib == "matplotlib":
        buf = locals_dict.get("buf")
        if buf is None:
            raise SandboxError("Matplotlib buffer 'buf' not found")
        buf.seek(0)
        return {"type": "png", "bytes": buf.read()}
    elif lib == "plotly":
        html = locals_dict.get("html")
        if html is None:
            raise SandboxError("Plotly 'html' string not found")
        return {"type": "html", "html": html}

    raise SandboxError("Unknown lib")

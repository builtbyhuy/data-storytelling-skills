from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

d = dfs[0].copy()
# No event-membership table or field is supplied. Count the supplied product records.
s = d.groupby('Product_Name', sort=True).size().sort_values(kind='stable')
h.bar(plt, s, 'Supplied products by name (event membership unavailable)', 'Product name', 'Number of product records')

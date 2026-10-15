from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

products, complaints = [d.copy() for d in dfs]
d = complaints.merge(products[['product_id','product_category_code']], on='product_id', how='inner')
p = d.groupby(['product_category_code','complaint_status_code'], sort=True).size().unstack(fill_value=0)
h.stacked(plt, p, 'Complaints by product category and status', 'Product category', 'Number of complaints')

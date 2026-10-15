from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

d = dfs[0].groupby('product_type_code', sort=True)['product_price'].agg(minimum='min', maximum='max').reset_index()
h.scatter(plt, d, 'minimum', 'maximum', 'Minimum and maximum product prices', 'Minimum product price', 'Maximum product price', 'product_type_code')

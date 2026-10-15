from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

definitions, attributes = [d.copy() for d in dfs]
d = attributes[pd.to_numeric(attributes['attribute_value'], errors='coerce').eq(0)].merge(definitions, on='attribute_id', how='inner')
s = d.groupby('attribute_name', sort=True).size().sort_index()
h.bar(plt, s, 'Attributes with value 0', 'Attribute name', 'Number of attributes')

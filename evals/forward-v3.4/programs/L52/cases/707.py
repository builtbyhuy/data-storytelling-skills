from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

counties, cities = [d.copy() for d in dfs]
d = cities.merge(counties[['County_ID','Crime_rate']], on='County_ID', how='inner')
h.scatter(plt, d, 'White', 'Crime_rate', 'City white population share and county crime rate', 'White population (%)', 'County crime rate')

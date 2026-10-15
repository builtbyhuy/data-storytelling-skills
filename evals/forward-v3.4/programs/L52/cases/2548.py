from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

d = dfs[0].groupby('PetType', sort=True)['pet_age'].agg(average_age='mean',maximum_age='max').reset_index()
h.scatter(plt, d, 'average_age', 'maximum_age', 'Average and maximum age per pet type', 'Average pet age', 'Maximum pet age')

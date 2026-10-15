from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

ships, deaths = [d.copy() for d in dfs]
d = deaths.merge(ships[ships['tonnage'].eq('t')][['id']], left_on='caused_by_ship_id', right_on='id', how='inner')
h.scatter(plt, d, 'killed', 'injured', 'Deaths and injuries for ships with tonnage code t', 'Number killed', 'Number injured')

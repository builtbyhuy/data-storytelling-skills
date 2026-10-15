from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

d = dfs[0].copy()
d['start_year'] = pd.to_numeric(d['Start_from'], errors='coerce')
p = d.groupby(['start_year','Is_full_time'], sort=True).size().unstack(fill_value=0).sort_index()
h.lines(plt, p, 'Hiring starts by year and full-time status', 'Start year', 'Number of starts')

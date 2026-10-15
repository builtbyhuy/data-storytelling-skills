from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

d = dfs[0].groupby('gender', sort=True).agg(dorms=('dormid','count'),capacity=('student_capacity','sum')).reset_index()
h.scatter(plt, d, 'dorms', 'capacity', 'Dorm count and capacity by gender', 'Number of dorms', 'Total student capacity', 'gender')

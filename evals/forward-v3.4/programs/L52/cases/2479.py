from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

journalists, reports = [d.copy() for d in dfs]
d = reports.merge(journalists, on='journalist_ID', how='inner')
d = d.groupby('Work_Type', sort=True).agg(average_age=('Age','mean'),average_experience=('Years_working','mean')).reset_index()
h.scatter(plt, d, 'average_age', 'average_experience', 'Journalist age and experience by role', 'Average age (years)', 'Average working experience (years)', 'Work_Type')

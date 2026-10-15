from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

enrolments, tests = [d.copy() for d in dfs]
d = tests[tests['test_result'].eq('Pass')].merge(enrolments, on='registration_id', how='inner')
s = d.groupby('date_of_enrolment', sort=True).size().sort_index()
fig, ax = h.frame(plt, 'Passed tests by enrolment timestamp', 'Date of enrolment', 'Number of passed test records')
ax.plot(s.index.astype(str), s.to_numpy(), marker='o')
ax.tick_params(axis='x', labelrotation=45)
ax.set_ylim(bottom=0)
h.finish(fig, ax, 'line')

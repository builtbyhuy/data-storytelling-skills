from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

d = dfs[0].copy()
d = d[d['test_result'].eq('Pass')]
s = d.groupby('date_test_taken', sort=True).size()
fig, ax = h.frame(plt, 'Passed tests by test timestamp', 'Date test taken', 'Number of passed tests')
ax.plot(s.index.astype(str), s.to_numpy(), marker='o')
ax.tick_params(axis='x', labelrotation=45)
ax.set_ylim(bottom=0)
h.finish(fig, ax, 'line')

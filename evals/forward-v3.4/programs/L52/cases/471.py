from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

d = dfs[0].copy()
s = d.groupby('Openning_year', sort=True)['Capacity'].mean()
fig, ax = h.frame(plt, 'Average cinema capacity by opening year', 'Opening year', 'Average capacity')
ax.plot(s.index, s.to_numpy(), marker='o')
ax.set_ylim(bottom=0)
h.finish(fig, ax, 'line')

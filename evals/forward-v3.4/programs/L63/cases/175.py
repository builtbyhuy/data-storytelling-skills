from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from chart_tools import render
_data = {Path(_path).stem: _frame.copy() for _path, _frame in zip(tables, dfs)}
render('175', _data, nl_query, plt)

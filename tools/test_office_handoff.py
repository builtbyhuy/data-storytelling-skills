"""Parser regression controls, not a test of presentation quality or Office rendering."""
import importlib.util
from pathlib import Path
import tempfile
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("office_checker", ROOT / "skills/data-story-redteam/scripts/check_office_handoff.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
C = checker.NS["c"]
S = checker.NS["s"]


def series(labels, numbers):
    points = "".join(f'<c:pt idx="{i}"><c:v>{x}</c:v></c:pt>' for i, x in enumerate(labels))
    values = "".join(f'<c:pt idx="{i}"><c:v>{x}</c:v></c:pt>' for i, x in enumerate(numbers) if x is not None)
    return (f'<c:ser><c:cat><c:strLit><c:ptCount val="{len(labels)}"/>{points}</c:strLit></c:cat>'
            f'<c:val><c:numLit><c:ptCount val="{len(numbers)}"/>{values}</c:numLit></c:val></c:ser>')


def pptx(path, body, chart_path="ppt/slides/charts/chart7.xml", chart_type="lineChart"):
    # Parts are deliberately relocated: OOXML permits part locations through
    # content types/relationships; a hard-coded folder can silently inspect none.
    types = (f'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
             f'<Override PartName="/{chart_path}" ContentType="application/vnd.openxmlformats-officedocument.drawingml.chart+xml"/>'
             '</Types>')
    chart = (f'<c:chartSpace xmlns:c="{C}"><c:chart><c:plotArea><c:{chart_type}>'
             f'{body}<c:axId val="1"/><c:axId val="2"/></c:{chart_type}></c:plotArea></c:chart></c:chartSpace>')
    with ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", types)
        z.writestr(chart_path, chart)


def main():
    checks = []
    with tempfile.TemporaryDirectory(prefix="office-handoff-controls-") as tmp:
        p = Path(tmp)
        # Missing observations keep their original category positions.
        pptx(p/"aligned.pptx", series(["A", "B", "C"], [1, None, None])+series(["A", "B", "C"], [2, 3, 4]))
        r = checker.inspect(p/"aligned.pptx")
        assert r["structural_assertions_passed"] and len(r["charts"]) == 1
        checks.append("full shared category domain accepts real numeric blanks")
        # The observed failure: shorter first series loses later month labels.
        pptx(p/"short.pptx", series(["A", "B"], [1, 2])+series(["A", "B", "C"], [2, 3, 4]))
        r = checker.inspect(p/"short.pptx")
        assert not r["structural_assertions_passed"] and "unequal" in r["issues"][0]["error"]
        checks.append("relocated chart with shortened first category domain is rejected")
        # Scatter x-coordinates need not be padded/aligned categorically.
        scatter = '<c:ser><c:xVal><c:numLit/></c:xVal><c:yVal><c:numLit/></c:yVal></c:ser>'
        pptx(p/"scatter.pptx", scatter, "ppt/charts/chart1.xml", "scatterChart")
        r = checker.inspect(p/"scatter.pptx")
        assert r["structural_assertions_passed"] and r["charts"][0]["unverified"]
        checks.append("coordinate series retains separate unverified coordinate scope")
        for error, expected in [(True, False), (False, True)]:
            name = p/("error.xlsx" if error else "blank.xlsx")
            cell = '<c r="A1" t="e"><f>1/0</f><v>#DIV/0!</v></c>' if error else '<c r="A1" t="str"><f>IF(1,"",1)</f><v></v></c>'
            with ZipFile(name, "w") as z:
                z.writestr("xl/worksheets/sheet1.xml", f'<worksheet xmlns="{S}"><sheetData><row r="1">{cell}</row></sheetData></worksheet>')
            r = checker.inspect(name)
            assert r["structural_assertions_passed"] is expected
            if not error:
                assert r["sheets"][0]["empty_formula_caches"] == ["A1"]
        checks.append("cached spreadsheet error fails; intentional blank cache remains unresolved")
        with ZipFile(p/"relocated.xlsx", "w") as z:
            z.writestr("[Content_Types].xml", '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Override PartName="/data/tab.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>')
            z.writestr("data/tab.xml", f'<worksheet xmlns="{S}"><sheetData><row r="1"><c r="A1" t="e"><v>#REF!</v></c></row></sheetData></worksheet>')
        r = checker.inspect(p/"relocated.xlsx")
        assert not r["structural_assertions_passed"] and len(r["sheets"]) == 1
        checks.append("relocated worksheet errors are discovered via content types")
        (p/"bad.pptx").write_bytes(b"not a zip")
        assert not checker.inspect(p/"bad.pptx")["structural_assertions_passed"]
        checks.append("malformed package reports failure")
    print("Passed " + str(len(checks)) + " Office parser controls: " + "; ".join(checks))


if __name__ == "__main__":
    main()

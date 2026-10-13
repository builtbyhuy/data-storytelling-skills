"""Inspect native Office structure; this does not grade facts, taste or fidelity.

Uses only the Python standard library. Render the saved files in their native
application and check source calculations and notes separately.
"""
import argparse
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile

NS = {
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
}
ERRORS = {"#REF!", "#VALUE!", "#DIV/0!", "#NAME?", "#N/A", "#NUM!", "#SPILL!", "#CALC!", "#NULL!"}


def category_domain(cat):
    """Return ordered cache positions, preserving absent category labels."""
    if cat.find("c:multiLvlStrRef", NS) is not None:
        return None, "multi-level categories require separate review"
    cache = next((cat.find(tag, NS) for tag in ("c:strRef/c:strCache", "c:numRef/c:numCache", "c:strLit", "c:numLit")
                  if cat.find(tag, NS) is not None), None)
    if cache is None:
        return None, "no cached category domain; inspect native linked data"
    points = {}
    for point in cache.findall("c:pt", NS):
        index = int(point.attrib["idx"])
        if index in points:
            return None, "duplicate category-cache position"
        points[index] = point.findtext("c:v", default="", namespaces=NS)
    declared = cache.find("c:ptCount", NS)
    count = int(declared.attrib["val"]) if declared is not None else max(points, default=-1) + 1
    if any(i < 0 or i >= count for i in points):
        return None, "category-cache position outside declared domain"
    return [points.get(i) for i in range(count)], None


def content_parts(z, suffix, fallback=()):
    if "[Content_Types].xml" not in z.namelist():
        return list(fallback)
    node = ET.fromstring(z.read("[Content_Types].xml"))
    return sorted(x.attrib["PartName"].lstrip("/") for x in node
                  if x.attrib.get("ContentType", "").endswith(suffix))


def inspect_pptx(z, result):
    names = z.namelist()
    slides = content_parts(z, "presentationml.slide+xml")
    notes = content_parts(z, "presentationml.notesSlide+xml")
    charts = content_parts(z, "drawingml.chart+xml")
    result["slides"] = len(slides)
    result["native_tables"] = 0
    result["pictures"] = 0
    for name in slides:
        node = ET.fromstring(z.read(name))
        result["native_tables"] += len(node.findall(".//a:tbl", NS))
        result["pictures"] += sum(x.tag.endswith("}pic") for x in node.iter())
    result["embedded_workbooks"] = sum(n.startswith("ppt/embeddings/") and n.endswith(".xlsx") for n in names)
    result["speaker_notes"] = []
    for name in notes:
        node = ET.fromstring(z.read(name))
        result["speaker_notes"].append({"part": name, "text": "\n".join(x.text or "" for x in node.findall(".//a:t", NS))})
    result["charts"] = []
    for name in charts:
        node = ET.fromstring(z.read(name))
        chart = {"part": name, "category_groups": [], "numeric_position_profiles": [], "unverified": []}
        plot = node.find("c:chart/c:plotArea", NS)
        if plot is None:
            result["issues"].append({"part": name, "error": "missing plot area"})
            continue
        # Coordinate/scatter series keep actual x/y positions. Only category
        # series sharing a plot/axis pair must have the same ordered domain.
        groups = {}
        for plot_type in plot:
            axes = tuple(x.attrib.get("val") for x in plot_type.findall("c:axId", NS))
            for series in plot_type.findall("c:ser", NS):
                cat = series.find("c:cat", NS)
                if cat is None:
                    chart["unverified"].append("coordinate series or category domain absent")
                    continue
                domain, reason = category_domain(cat)
                if reason:
                    if reason.startswith("duplicate") or "outside declared" in reason:
                        result["issues"].append({"part": name, "error": reason})
                    else:
                        chart["unverified"].append(reason)
                    continue
                groups.setdefault(axes, []).append(domain)
                val = series.find("c:val", NS)
                cache = None if val is None else next((val.find(tag, NS) for tag in ("c:numRef/c:numCache", "c:numLit") if val.find(tag, NS) is not None), None)
                if cache is None:
                    chart["unverified"].append("no numeric cache; verify value/category binding from linked source")
                    continue
                indices = [int(pt.attrib["idx"]) for pt in cache.findall("c:pt", NS)]
                declared = cache.find("c:ptCount", NS)
                span = int(declared.attrib["val"]) if declared is not None else max(indices, default=-1)+1
                chart["numeric_position_profiles"].append({"declared_span": span, "category_count": len(domain), "present_indices": indices, "omitted_category_positions": [i for i in range(len(domain)) if i not in indices]})
                if len(set(indices)) != len(indices) or any(i < 0 or i >= span or i >= len(domain) for i in indices):
                    result["issues"].append({"part": name, "error": "duplicate or out-of-domain numeric-cache position"})
                if span != len(domain):
                    chart["unverified"].append("numeric-cache extent differs from categories; confirm intended missing positions against source, not only cache indices")
        for axes, domains in groups.items():
            entry = {"axis_ids": list(axes), "domains": domains}
            chart["category_groups"].append(entry)
            if any(x != domains[0] for x in domains[1:]):
                result["issues"].append({"part": name, "axis_ids": list(axes), "error": "unequal ordered category domains across shared-position series"})
            if any(v is None or v == "" for d in domains for v in d):
                result["issues"].append({"part": name, "axis_ids": list(axes), "error": "missing category label in cached domain; confirm intentional label suppression in native render"})
        result["charts"].append(chart)


def inspect_xlsx(z, result):
    strings = []
    shared = content_parts(z, "spreadsheetml.sharedStrings+xml", ["xl/sharedStrings.xml"] if "xl/sharedStrings.xml" in z.namelist() else [])
    if shared:
        strings = ["".join(x.text or "" for x in item.findall(".//s:t", NS))
                   for item in ET.fromstring(z.read(shared[0])).findall("s:si", NS)]
    result["sheets"] = []
    worksheets = content_parts(z, "spreadsheetml.worksheet+xml", sorted(n for n in z.namelist() if n.startswith("xl/worksheets/sheet") and n.endswith(".xml")))
    if not worksheets:
        result["issues"].append({"error": "no worksheet parts inspected"})
    for name in worksheets:
        node = ET.fromstring(z.read(name))
        sheet = {"part": name, "formulas": 0, "empty_formula_caches": []}
        for cell in node.findall(".//s:c", NS):
            value = cell.findtext("s:v", namespaces=NS)
            if cell.attrib.get("t") == "s" and value is not None:
                value = strings[int(value)]
            if cell.find("s:f", NS) is not None:
                sheet["formulas"] += 1
                if value is None or value == "":
                    sheet["empty_formula_caches"].append(cell.attrib.get("r"))
            if cell.attrib.get("t") == "e" or value in ERRORS:
                result["issues"].append({"part": name, "cell": cell.attrib.get("r"), "error": value or "cached error cell"})
        result["sheets"].append(sheet)
    result["cache_limit"] = "Empty formula caches can be intentional blank results or uncalculated cells; native recalculation and source meaning distinguish them."


def inspect(path):
    result = {"file": str(path), "issues": [], "scope": "structural only; source facts, note truth, edit/save behavior and rendered fidelity are separate checks"}
    try:
        with ZipFile(path) as z:
            if path.suffix.lower() == ".pptx":
                inspect_pptx(z, result)
            elif path.suffix.lower() == ".xlsx":
                inspect_xlsx(z, result)
            else:
                result["issues"].append({"error": "supported inputs are .pptx and .xlsx"})
    except (OSError, BadZipFile, ET.ParseError, ValueError, KeyError, IndexError) as exc:
        result["issues"].append({"error": f"{type(exc).__name__}: {exc}"})
    result["structural_assertions_passed"] = not result["issues"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    reports = [inspect(path) for path in args.files]
    passed = all(r["structural_assertions_passed"] for r in reports)
    payload = {"all_structural_assertions_passed": passed, "reports": reports}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"all_structural_assertions_passed": passed, "report": str(args.report), "issues": sum(len(r["issues"]) for r in reports)}))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

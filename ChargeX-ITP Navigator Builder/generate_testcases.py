import os
import re
import json
import pandas as pd
import pdfkit
from PyPDF2 import PdfMerger


def parse_test_conditions(text):
    if not isinstance(text, str):
        return {}

    parent_keys = [
        "Authentication Type/s:", "HLC Protocol/s:", "Involved System/s:", "Certificate/s (PKI):",
        "EVSE HLC Priority:", "EV HLC Priority:", "Plug or Authenticate first:", "EV Initial SoC:",
        "EV SoC Charge Limit:", "Stop Method/s:", "Session Initialization Stop State/s:", "EV State/s:",
        "Temperature:", "Vehicle Conditioning:", "Pause Method/s:", "Resume Method/s:", "OCPP Protocol/s:",
        "EV HMI charge scheduling values:", "EVSE charge scheduling values:", "OCPP Curtailment Command:",
        "State Transition:", "Test Reference:", "Fault Method/s:", "EV ServiceID/s:", "EV Charge Parameters:",
        "EVSE Charge Parameters:", "EV Bidirectional Control:", "EVSE Bidirectional Control:"
    ]
    certificate_sub_keys = [
        "Valid Certificate/s:", "Invalid Certificate/s:", "Reason/s for Certificate/s Invalidity:"
    ]
    all_keys = parent_keys + certificate_sub_keys
    pattern = r'(' + '|'.join(re.escape(key) for key in all_keys) + r')'
    splits = re.split(pattern, text)
    conditions = {}
    current_parent, current_key = None, None

    for part in map(str.strip, splits):
        if not part:
            continue
        if part in parent_keys:
            current_parent = part.rstrip(':')
            conditions[current_parent] = {}
            current_key = None
        elif part in certificate_sub_keys:
            if current_parent == "Certificate/s (PKI)":
                current_key = part.rstrip(':')
                conditions[current_parent][current_key] = ''
        elif current_parent:
            if current_key:
                conditions[current_parent][current_key] += (' ' + part).strip()
            else:
                if isinstance(conditions[current_parent], dict) and not conditions[current_parent]:
                    conditions[current_parent] = part
                else:
                    conditions[current_parent] += ' ' + part
    return conditions



def create_html_table(row_data, index):
    def wrap(val):
        return str(val) if pd.notna(val) else ""

    def tr(content_list, style=""):
        style_attr = f" style='{style}'" if style else ""
        return f"<tr{style_attr}>" + "".join(content_list) + "</tr>"

    def td(content, colspan=1, rowspan=1, is_label=False, style=""):
        class_attr = " class='label'" if is_label else ""
        cs = f" colspan='{colspan}'" if colspan > 1 else ""
        rs = f" rowspan='{rowspan}'" if rowspan > 1 else ""
        style_attr = f" style='{style}'" if style else ""
        return f"<td{class_attr}{cs}{rs}{style_attr}>{content}</td>"

    def format_steps(text):
        if not isinstance(text, str):
            return ""
        parts = re.findall(r'\d+\.\s.*?(?=\s\d+\.|$)', text, re.DOTALL)
        return "<br/>".join(part.strip() for part in parts)

    def format_multiline_or_link(key, val):
        if not isinstance(val, str):
            return val
        multiline_keys = [
            "State Transition", "Fault Method/s", "OCPP Curtailment Command",
            "EVSE charge scheduling values", "Pause Method/s", "Resume Method/s", 
            "HLC Protocol/s", "OCPP Protocol/s", "Reason/s for Certificate/s Invalidity",
            "EV ServiceID/s", "EV Charge Parameters", "EVSE Charge Parameters", 
            "EV Bidirectional Control", "EVSE Bidirectional Control", "Stop Method/s", 
            "Purpose", "Observed Metrics", "EVSE HLC Priority", "EV HLC Priority", 
            "Session Initialization Stop State/s", "EV State/s", "EV SoC Charge Limit", 
            "Temperature", "EV Initial SoC", "Authentication Type/s"
        ]
        if key in multiline_keys:
            return val.replace('\n', '<br/>')
        if key == "Test Reference":
            url = val.strip()
            if not re.match(r'^https?://', url):
                url = 'http://' + url
            return f'<a href="{url}" target="_blank">{val}</a>'
        return val

    html = """<html><head><style>
        body { font-family: Arial; font-size: 16px; padding: 20px; position: relative; }
        table { border: 1px solid #000; border-collapse: collapse; width: 100%; table-layout: auto;}
        td { border: 1px solid #000; padding: 2px 4px; vertical-align: top; word-wrap: break-word; max-width: 200px;}
        td.label { font-weight: bold; background: #f2f2f2; }
        .header-img { position: absolute; top: 20px; right: 20px; }
        .footer { margin-top: 20px; font-size: 14px; }
        </style></head><body>
        <img src="/static/images/chargex.png" alt="ChargeX Logo", 
        style="float: right; width: 25%; margin: 5px;">
        <table>
        <br>
        <br>
        """

    html += tr([td("Test Name", is_label=True, style="background-color: #779394; color: white;"),
                td(row_data[('Test Name', 'Test Name')], is_label=True, colspan=4, 
                   style="background-color: #779394; color: white;")])

    html += tr([td("Test Identifier", is_label=True), td(row_data[('Nr', 'Nr')], colspan=4)])
    html += tr([td("Test Type", is_label=True), td(row_data[('Test Type', 'Test Type')], colspan=4)])
    html += tr([td("Test Category", is_label=True), td(row_data[('Test Category', 'Test Category')], colspan=4)])
    html += tr([td("Test Purpose", is_label=True), td(row_data[('Purpose', 'Purpose')], colspan=4)])
    html += tr([td("Observed Metrics", is_label=True), td(row_data[('Test Results', 'Observed Metrics')], colspan=4)])
    html += tr([td("Intended MRECs/Errors", is_label=True), td(row_data[('Test Results', 'Intended MRECs')], colspan=4)])
    html += tr([td("Other Possible MRECs", is_label=True), td(row_data[('Test Results', 'Other Possible MRECs')], colspan=4)])

    parsed_conditions = parse_test_conditions(row_data.get(('Test Conditions', 'Test Conditions'), ''))
    if parsed_conditions:
        total_rows = sum(len(v) if isinstance(v, dict) else 1 for v in parsed_conditions.values())
        first = True
        for key, val in parsed_conditions.items():
            if isinstance(val, dict):
                sub_items = list(val.items())
                if first:
                    html += tr([td("Test Conditions", is_label=True, rowspan=total_rows),
                                td(key, is_label=True, rowspan=len(sub_items)),
                                td(sub_items[0][0], is_label=True),
                                td(format_multiline_or_link(sub_items[0][0], sub_items[0][1]), colspan=2)])
                    for sk, sv in sub_items[1:]:
                        html += tr([td(sk, is_label=True), td(format_multiline_or_link(sk, sv), colspan=2)])
                    first = False
                else:
                    html += tr([td(key, is_label=True, rowspan=len(sub_items)),
                                td(sub_items[0][0], is_label=True),
                                td(format_multiline_or_link(sub_items[0][0], sub_items[0][1]), colspan=2)])
                    for sk, sv in sub_items[1:]:
                        html += tr([td(sk, is_label=True), td(format_multiline_or_link(sk, sv), colspan=2)])
            else:
                if first:
                    html += tr([td("Test Conditions", is_label=True, rowspan=total_rows),
                                td(key, is_label=True),
                                td(format_multiline_or_link(key, val), colspan=3)])
                    first = False
                else:
                    html += tr([td(key, is_label=True), td(format_multiline_or_link(key, val), colspan=3)])

    html += tr([td("Steps", is_label=True), td(format_steps(row_data[('Steps', 'Steps')]), colspan=4)])

    pass_text = row_data.get(('Pass Criteria', 'Pass Criteria'), '')
    rows = ""
    if pass_text:
        for s in re.split(r'(?<=[.!?])\s+', str(pass_text).strip()):
            if s:
                rows += f"""<tr style="border:none;"><td style="border:none;">• {s}</td>
                            <td style="border:none;width:10%;text-align:right;">
                            <input type="checkbox" /></td></tr>"""
    inner_table = f"""<table style="width:100%;border:none;">{rows}</table>"""
    html += tr([td("Pass Criteria (Check box if met)", is_label=True), td(inner_table, colspan=4)])

    html += tr([td("Comments", is_label=True), td("<br/><br/><br/><br/><br/>", colspan=4)])

    html += "</table>"

    html += """
    <div class="footer">
        <br>
        <br>
        Interoperability Test Plan: An initiative by
        <a href="https://inl.gov/chargex/" target="_blank">ChargeX</a> consortium,
        Contact Person: Sam Thruston, Argonne National Laboratory (ANL),
        <a href="mailto:sthurston@anl.gov">sthurston@anl.gov</a>
    </div>
    """

    html += "</body></html>"

    return html



def build_tree_structure(df):
    tree = []
    for idx, (_, row) in enumerate(df.iterrows()):
        cat = row[("Test Category", "Test Category")]
        typ = row[("Test Type", "Test Type")]
        name = row[("Test Name", "Test Name")]
        filename = f"TestCase_{idx+1}.html"

        # Find or create category node
        cat_node = next((c for c in tree if c["text"] == cat), None)
        if not cat_node:
            cat_node = {
                "text": cat,
                "icon": "fa fa-folder",
                "children": []
            }
            tree.append(cat_node)

        # Find or create type node
        type_node = next((t for t in cat_node["children"] if t["text"] == typ), None)
        if not type_node:
            type_node = {
                "text": typ,
                "icon": "fa fa-folder",
                "children": []
            }
            cat_node["children"].append(type_node)

        # Add leaf node with star icon
        type_node["children"].append({
            "text": name or "Test name not available",
            "li_attr": {"data-filename": filename},
            "icon": "fa fa-flag"  # flag icon instead of file
        })

    return tree


def process_excel_to_html_json(excel_path, html_out_folder="static/testcases", json_out_path="tree_data.json"):
    df = pd.read_excel(excel_path, sheet_name="Detailed Test Cases", skiprows=1, header=[0, 1])
    os.makedirs(html_out_folder, exist_ok=True)
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdf_files = []

    for idx, (_, row) in enumerate(df.iterrows()):
        html = create_html_table(row, idx)
        html_file = os.path.join(html_out_folder, f"TestCase_{idx+1}.html")
        pdf_file = os.path.join(html_out_folder, f"TestCase_{idx+1}.pdf")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html)
        pdfkit.from_file(html_file, pdf_file, options={'page-size': 'Letter','encoding': 'UTF-8',
                                                       'enable-local-file-access': None,'zoom': '0.85', 
                                                       'margin-top': '5mm','margin-bottom': '5mm',
                                                       'margin-left': '10mm','margin-right': '10mm'}, 
                                                       configuration=config)
        pdf_files.append(pdf_file)

    merger = PdfMerger()
    for f in pdf_files:
        merger.append(f)
    merged_path = os.path.join(html_out_folder, "ITP_Version2.pdf")
    merger.write(merged_path)
    merger.close()

    with open(json_out_path, "w", encoding="utf-8") as f:
        json.dump(build_tree_structure(df), f, indent=2)

    print(f"Generated HTML, PDFs, merged PDF at {merged_path}, and JSON tree.")


if __name__ == "__main__":
    process_excel_to_html_json("Interoperability Test Plan Version 2.xlsx", html_out_folder="static/testcases", json_out_path="tree_data.json")

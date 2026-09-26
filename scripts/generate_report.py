from pathlib import Path
import re
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs' / 'respuestas-examen-final.md'
OUTPUT = ROOT / 'Informe_Examen_Final_Automatizacion_Pruebas.docx'

BLUE = RGBColor(31, 78, 121)
DARK = RGBColor(31, 31, 31)


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd')
        tc_pr.append(shd)
    shd.set(qn('w:fill'), fill)


def set_cell_text(cell, text, bold=False, color=None):
    cell.text = ''
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(text.strip())
    run.bold = bold
    run.font.name = 'Arial'
    run.font.size = Pt(10)
    if color:
        run.font.color.rgb = color
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def set_run_font(run, size=12, bold=False, italic=False, color=DARK, name='Arial'):
    run.font.name = name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run('Página ')
    set_run_font(run, 9, color=RGBColor(100, 100, 100))
    fld_char1 = OxmlElement('w:fldChar')
    fld_char1.set(qn('w:fldCharType'), 'begin')
    instr_text = OxmlElement('w:instrText')
    instr_text.set(qn('xml:space'), 'preserve')
    instr_text.text = 'PAGE'
    fld_char2 = OxmlElement('w:fldChar')
    fld_char2.set(qn('w:fldCharType'), 'end')
    run._r.append(fld_char1)
    run._r.append(instr_text)
    run._r.append(fld_char2)


def add_rich_paragraph(doc, text, style=None):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)
    # Simple bold support for **text**.
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if not part:
            continue
        bold = part.startswith('**') and part.endswith('**')
        content = part[2:-2] if bold else part
        run = p.add_run(content)
        set_run_font(run, 12, bold=bold)
    return p


def add_code_block(doc, lines):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    cell = table.cell(0, 0)
    set_cell_shading(cell, 'F2F2F2')
    cell.text = ''
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    for i, line in enumerate(lines):
        run = p.add_run(line)
        set_run_font(run, 9, name='Courier New', color=RGBColor(50, 50, 50))
        if i < len(lines) - 1:
            run.add_break()
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_markdown_table(doc, rows):
    if len(rows) < 2:
        return
    data = []
    for row in rows:
        cells = [c.strip() for c in row.strip().strip('|').split('|')]
        if all(re.fullmatch(r':?-{3,}:?', c.replace(' ', '')) for c in cells):
            continue
        data.append(cells)
    if not data:
        return
    cols = max(len(r) for r in data)
    table = doc.add_table(rows=len(data), cols=cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    for i, row in enumerate(data):
        for j in range(cols):
            value = row[j] if j < len(row) else ''
            set_cell_text(table.cell(i, j), value, bold=(i == 0), color=RGBColor(255, 255, 255) if i == 0 else DARK)
            if i == 0:
                set_cell_shading(table.cell(i, j), '1F4E79')
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def build_document():
    document = Document()
    section = document.sections[0]
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)

    normal = document.styles['Normal']
    normal.font.name = 'Arial'
    normal._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(6)

    for style_name, size in [('Heading 1', 16), ('Heading 2', 14), ('Heading 3', 12)]:
        style = document.styles[style_name]
        style.font.name = 'Arial'
        style._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = BLUE
        style.paragraph_format.space_before = Pt(10)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.line_spacing = 1.15

    footer = section.footer
    add_page_number(footer.paragraphs[0])

    # Cover page.
    p = document.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(80)
    run = p.add_run('AUTOMATIZACIÓN DE PRUEBAS')
    set_run_font(run, 20, bold=True, color=BLUE)
    p = document.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Examen Final')
    set_run_font(run, 18, bold=True, color=DARK)
    p = document.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(40)
    run = p.add_run('Proyecto Maven, Integración Continua y Deployment Pipeline')
    set_run_font(run, 13, color=DARK)
    p = document.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(100)
    run = p.add_run('Estudiante: [Completar nombre y apellido]\nAsignatura: Automatización de Pruebas\nFecha: [Completar fecha]')
    set_run_font(run, 12, color=DARK)
    document.add_page_break()

    lines = SOURCE.read_text(encoding='utf-8').splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith('# '):
            # The cover already contains the title; keep it as a body heading only once.
            p = document.add_paragraph(style='Heading 1')
            p.add_run(line[2:].strip())
            i += 1
            continue
        if line.startswith('## '):
            p = document.add_paragraph(style='Heading 1')
            p.add_run(line[3:].strip())
            i += 1
            continue
        if line.startswith('### '):
            p = document.add_paragraph(style='Heading 2')
            p.add_run(line[4:].strip())
            i += 1
            continue
        if line.startswith('```'):
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i])
                i += 1
            add_code_block(document, code)
            i += 1
            continue
        if line.startswith('|'):
            table_rows = []
            while i < len(lines) and lines[i].startswith('|'):
                table_rows.append(lines[i])
                i += 1
            add_markdown_table(document, table_rows)
            continue
        if line.startswith('- '):
            p = document.add_paragraph(style='List Bullet')
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(line[2:].strip())
            set_run_font(run, 12)
            i += 1
            continue
        if re.match(r'^\d+\. ', line):
            p = document.add_paragraph(style='List Number')
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(re.sub(r'^\d+\. ', '', line).strip())
            set_run_font(run, 12)
            i += 1
            continue
        add_rich_paragraph(document, line.strip())
        i += 1

    document.save(OUTPUT)
    print(OUTPUT)


if __name__ == '__main__':
    build_document()

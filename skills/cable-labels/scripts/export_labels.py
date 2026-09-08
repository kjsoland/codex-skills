"""Export alternating cable-end labels from a standard ICD Cabling sheet."""
import argparse
import csv
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font


def export(source, output, icd, skip_unused=False):
    source, output = Path(source), Path(output)
    if output.suffix.lower() != '.xlsx':
        raise ValueError('Output must have an .xlsx extension')
    if source.resolve() in (output.resolve(), output.with_suffix('.csv').resolve()):
        raise ValueError('Output must not overwrite source')
    book = openpyxl.load_workbook(source, data_only=True)
    sheet = book['Cabling']
    header = [str(c.value).strip() if c.value is not None else '' for c in sheet[1]]
    required = ['Designator', 'From Location', 'From Component', 'From Connection',
                'To Location', 'To Component', 'To Connection']
    for name in required:
        if name == 'Designator' and name not in header:
            continue
        if header.count(name) != 1:
            raise ValueError(f'Expected exactly one column: {name}')
    indices = [header.index(name) if name in header else None for name in required]
    labels = []
    excluded = []
    for number, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), 2):
        if all(v is None or str(v).strip() == '' for v in row):
            continue
        values = [row[i] if i is not None else None for i in indices]
        if skip_unused and all(str(v).strip().upper() == 'NONE' for v in [values[0], *values[4:7]]):
            excluded.append(number)
            continue
        if any(v is None or str(v).strip().upper() in {'', 'NONE', 'TBD'} for v in values[1:]):
            raise ValueError(f'Incomplete cable fields on source row {number}')
        values = [str(v).strip() if v is not None else "" for v in values]
        for side in ['FROM SIDE', 'TO SIDE']:
            designator = f' {values[0]}' if values[0] else ''
            labels.append(f'{side}{designator}    ICD: {icd}\n'
                          + 'FROM: ' + ' / '.join(values[1:4]) + '\n'
                          + 'TO: ' + ' / '.join(values[4:7]))
    if not labels:
        raise ValueError('No cables found')
    result = openpyxl.Workbook()
    target = result.active
    target.title = 'Labels'
    for label in labels:
        target.append([label])
        cell = target.cell(target.max_row, 1)
        cell.data_type = 's'
        cell.font = Font(name='Arial', size=11)
        cell.alignment = Alignment(vertical='center', wrap_text=True)
        target.row_dimensions[target.max_row].height = 54
    target.column_dimensions['A'].width = 78
    target.sheet_view.showGridLines = False
    target.print_area = f'A1:A{len(labels)}'
    result.properties.description = f'Source: {source.name}; Cabling order; From Side then To Side.'
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output)
    csv_path = output.with_suffix('.csv')
    with csv_path.open('w', newline='', encoding='utf-8-sig') as handle:
        csv.writer(handle).writerows([label] for label in labels)
    check = openpyxl.load_workbook(output, data_only=True).active
    assert check.max_column == 1 and check.max_row == len(labels)
    assert list(check.values) == [(label,) for label in labels]
    with csv_path.open(newline='', encoding='utf-8-sig') as handle:
        assert list(csv.reader(handle)) == [[label] for label in labels]
    print(f'Excluded unused source rows: {excluded}')
    print(f'Validated {len(labels) // 2} cables, {len(labels)} labels.\n{output}\n{csv_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source')
    parser.add_argument('output')
    parser.add_argument('--icd', required=True, help='Governing ICD acronym from the routing procedure')
    parser.add_argument('--skip-unused', action='store_true', help='Exclude rows with literal NONE designator and all three To fields NONE')
    args = parser.parse_args()
    export(args.source, args.output, args.icd, args.skip_unused)

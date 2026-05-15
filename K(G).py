import openpyxl
from logging_config import setup_logger
from parser import column_headers, get_column_by_header, get_sheet
from utils import valid_file_name
import statistics

from constants import SQUARE_M2

logger = setup_logger(__name__)

all_results: list = []

sheetlist = valid_file_name()
for filename in sheetlist:
    sheet = get_sheet(filename)
    headers_to_find = ['Qiv', 'Tin', 'Tout']
    column_numbers = {}
    for header in headers_to_find:
        column_numbers[header] = get_column_by_header(
            sheet, column_headers[header]
        )

    logger.debug(f'Номера колонок {column_numbers}')

    header_idx = {
        'Qiv_idx': column_numbers['Qiv'] - 1,
        'Tin_idx': column_numbers['Tin'] - 1,
        'Tout_idx': column_numbers['Tout'] - 1,
    }

    logger.debug(header_idx)

    Qiv_Tin_Tout_values = []
    for row in sheet.iter_rows(values_only=True):
        Qiv = row[header_idx['Qiv_idx']]  # Берем нужный элемент кортежа
        Tin = row[header_idx['Tin_idx']]
        Tout = row[header_idx['Tout_idx']]
        Qiv_Tin_Tout_values.append({
            'Qiv': Qiv,
            'Tin': Tin,
            'Tout': Tout
        })

    Qiv_all_values = [
        record['Qiv']
        for record in Qiv_Tin_Tout_values
        if record['Qiv'] is not None
    ]
    Tin_all_values = [
        record['Tin']
        for record in Qiv_Tin_Tout_values
        if record['Tin'] is not None
    ]
    Tout_all_values = [
        record['Tout']
        for record in Qiv_Tin_Tout_values
        if record['Tout'] is not None
    ]

    Tin_median = statistics.median(
        x for x in Tin_all_values if isinstance(x, float)
    )
    Tout_median = statistics.median(
        x for x in Tout_all_values if isinstance(x, float)
    )
    Tin_mean = statistics.mean(
        x for x in Tin_all_values if isinstance(x, float)
    )
    Tout_mean = statistics.mean(
        x for x in Tout_all_values if isinstance(x, float)
    )

    Qiv_unique_values = sorted(
        set(x for x in Qiv_all_values if isinstance(x, float))
    )
    logger.info(
        f'Уникальные значения Qiv для файла {filename}: \n'
        f'{sorted(set(Qiv_unique_values))} \n'
    )
    logger.info(
    f'Медиана значений Tin для файла {filename} = {round(Tin_median, 2)}\n'
    f'Медиана значений Tout для файла {filename} = {round(Tout_median, 2)}\n'
    )
    K_value = []
    delta_t = abs(Tout_median - Tin_median)
    for value in Qiv_unique_values:
        if delta_t == 0:
            continue
        K = value / (SQUARE_M2 * delta_t)
        K_value.append(round(K, 2))
        K_unique__values = sorted(set(K_value))
    logger.info(
        f'Уникальные значения K для файла {filename}: {K_unique__values}\n'
        f'{"-"*80}'
    )
    all_results.append({
        'filename': filename,
        'Qiv': Qiv_unique_values,
        'K': K_unique__values,
        'Tin_median': Tin_median,
        'Tout_median': Tout_median,
        'delta_t': delta_t
    })
    
print(all_results)

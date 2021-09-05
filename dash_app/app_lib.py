import dash
import datetime
import pandas as pd
from pathlib import Path

colors={
    'text_heading_H2': '#005ABB',
    'background_heading_h4': '#F3F3F3',
    'white': '#FFFFFF',
    'blue': '#005ABB',
    'table_header_grey': '#F3F3F3'
}

project_folder = Path(__file__).parent.parent
model_folder = project_folder / 'models'


raw_data = pd.read_pickle(project_folder / 'data/processed/all_data.pckl')
all_options = raw_data[
    [
        'WM_OWNR',
        'WM_UWNR',
        'WM_PROFILOW',
        'WM_OWDUAU',
        'start_date_phase',
        'phase'
    ]
].dropna().drop_duplicates()

results = raw_data[
    [
        'phase',
        'start_date_phase',
        'end_date_phase',
        'duration_in_spec',
        'duration_in_spec_in_percent',
        'thickness_min_in_spec',
        'thickness_max_in_spec',
        'WK_UW1TEMP_SOLL',
        'WK_UW2TEMP_SOLL',
        'WK_OW1TEMP_SOLL',
        'WK_OW2TEMP_SOLL',
        'WM_ARTGESCH',
        'WM_ARTHOE',
        'WM_ARTLAE',
        'WM_OWGESCH',
        'WM_UWGESCH',
        'WM_OWWI',
        'WM_UWWI',
        'WM_POHOE',
        'WM_POLAE',
        'WM_ROLAE',
        'WM_ROGESCH',
        'WM_HPLI',
        'WM_HPRE'
    ]
].dropna().drop_duplicates()

results = results.round({'thickness_min_in_spec': 2,
                         'thickness_max_in_spec': 2,
                         'WK_UW1TEMP_SOLL': 2,
                         'WK_UW2TEMP_SOLL': 2,
                         'WK_OW1TEMP_SOLL': 2,
                         'WK_OW2TEMP_SOLL': 2,
                         'WM_ARTGESCH': 2,
                         'WM_ARTHOE': 2,
                         'WM_ARTLAE': 2,
                         'WM_OWGESCH': 2,
                         'WM_UWGESCH': 2,
                         'WM_OWWI': 2,
                         'WM_UWWI': 2,
                         'WM_POHOE': 2,
                         'WM_POLAE': 2,
                         'WM_ROLAE': 2,
                         'WM_ROGESCH': 2,
                         'WM_HPLI': 2,
                         'WM_HPRE': 2
                         })

epoch = datetime.datetime.utcfromtimestamp(0)


def get_marks_from_start_end(start, end):
    """Returns dict with one item per start of month (stating year and month only),
    plus one item for start and end day (stating year, month, and day).
    """
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    month_starts = pd.date_range(start, end, freq='MS').tolist()
    # month_starts = [Timestamp('2020-02-01 00:00:00', freq='MS'), ...]
    month_starts_dict = {ts_to_unix_time_sec(ts): str(ts.strftime('%Y-%m')) for ts in month_starts}
    # month_start_dict = {1580515200.0: '2020-02', ...}
    start_end_dict = {ts_to_unix_time_sec(ts): str(ts.strftime('%Y-%m-%d')) for ts in [start, end]}
    # start_end_dict = {1579046400.0: '2020-01-15', 1600950060.0: '2020-09-24'}
    return {**month_starts_dict, **start_end_dict}


def ts_to_unix_time_sec(dt):
    return int((dt - epoch).total_seconds())


def unix_time_sec_to_ts(s):
    return epoch + s * pd.Timedelta('1s')

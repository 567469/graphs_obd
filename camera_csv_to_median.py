import pandas as pd
import re
from datetime import datetime, timedelta

from variables import PFAD_ZUR_DEC_CSV


def datetime_to_ms(date_str):
    # Entfernen der Zeitzone
    date_str = re.sub(r'(\+|\-)\d{2}:\d{2}$', '', date_str)

    if '.' in date_str:
        # Wenn Millisekunden vorhanden sind, extrahiere sie
        milliseconds_part = date_str.split('.')[-1]
        ms_length = len(milliseconds_part)

        # Entfernen der Millisekunden aus date_str, um den String mithilfe von datetime zu verarbeiten
        date_without_ms = date_str.rsplit('.', 1)[0]
        dt_obj = datetime.strptime(date_without_ms, '%Y-%m-%d %H:%M:%S')

        # Umwandeln in Millisekunden
        total_ms = int(dt_obj.timestamp() * 1000)

        # Die Millisekunden wieder hinzufügen
        total_ms += int(milliseconds_part) // (10 ** (ms_length - 3))
    else:
        # Wenn keine Millisekunden vorhanden sind, wandle das Datum direkt um
        dt_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        total_ms = int(dt_obj.timestamp() * 1000)

    return total_ms

def ms_to_datetime(ms):
    return datetime.fromtimestamp(ms / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
def time_to_ms(time_str):
    min, sec, ms = map(int, time_str.split(':'))
    return (min * 60 + sec) * 1000 + ms

def ms_to_time(ms):
    min = ms // 60000
    sec = (ms % 60000) // 1000
    ms = ms % 1000
    return f"{min}:{sec}:{ms}"

def aggregate_data_with_correction(filepath):
    df = pd.read_csv(filepath, dtype={'Float Number': 'str'})

    # Datenkorrektur
    def correct_float(val):
        if '.' not in val:
            if len(val) == 1:
                return val + '.0'
            elif len(val) == 2:
                return val[0] + '.' + val[1]
        return val

    df['Float Number'] = df['Float Number'].apply(correct_float).astype(float)

    # Zeitumwandlung und Aggregation
    df['Time (ms)'] = df['Time (min:sec:ms)'].apply(time_to_ms)
    df['Interval'] = df['Time (ms)'] // 200
    aggregated_df = df.groupby('Interval')['Float Number'].median().reset_index()
    aggregated_df['New Time'] = aggregated_df['Interval'] * 200
    aggregated_df['New Time'] = aggregated_df['New Time'].apply(ms_to_time)

    output_name = filepath.split('.csv')[0] + '_Median.csv'
    aggregated_df[['New Time', 'Float Number']].to_csv(output_name, index=False)

def aggregate_data_without_correction(filepath):
    df = pd.read_csv(filepath, sep=';')

    # Zeitumwandlung und Aggregation
    df['Time (ms)'] = df[df.columns[0]].apply(datetime_to_ms)
    df['Interval'] = df['Time (ms)'] // 200
    aggregated_df = df.groupby('Interval').agg({
        df.columns[2]: 'median',  # Assuming 3rd column needs median
        df.columns[4]: 'median'   # Assuming 4th column needs median
    }).reset_index()
    aggregated_df['Time'] = aggregated_df['Interval'] * 200
    aggregated_df['Time'] = aggregated_df['Time'].apply(ms_to_datetime)

    # Ändern Sie hier die Spaltennamen
    aggregated_df = aggregated_df[['Time', df.columns[2], df.columns[4]]]
    aggregated_df.columns = ['Time', 'DataByte_2', 'DataByte_4']

    output_name = filepath.split('.csv')[0] + '_Median.csv'
    aggregated_df.to_csv(output_name, index=False)



# Implementation
# aggregate_data_with_correction(PFAD_ZUR_DEC_CSV)
aggregate_data_without_correction(PFAD_ZUR_DEC_CSV)

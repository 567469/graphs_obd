import os
import pandas as pd
import matplotlib.pyplot as plt

from variables import AUSGABE_PFAD_GRAPH2, EINGABE_FILE2

# Hier standen echte CAN-Bus ids anstatt XXX_n diese wurden für die Veroeffentlichung entfernt
allowed_combinations = [
    ("XXX_1", "DataByte_3"),
    ("XXX_2", "DataByte_6"),
    ("XXX_3", "DataByte_3"),
    ("XXX_4", "DataByte_6"),
    ("XXX_5", "DataByte_5"),
    ("XXX_6", "DataByte_3"),
    ("XXX_7", "DataByte_5"),
    ("XXX_8", "DataByte_3"),
    ("XXX_9", "DataByte_1"),
    ("XXX_10", "DataByte_3"),
    ("XXX_11", "DataByte_5"),
    ("XXX_12", "DataByte_4"),
    ("XXX_13", "DataByte_4"),
    ("XXX_14", "DataByte_3"),
    ("XXX_15", "DataByte_6"),
]

def hex_to_decimal(hex_string):
    return int(hex_string, 16)

# Anpassung der split_data_bytes Funktion für 4 Hex-Ziffern
def split_data_bytes(data_bytes):
    return [hex_to_decimal(data_bytes[i:i + 4]) for i in range(0, len(data_bytes), 4)]

def plot_data():
    print('Start: CSV-Datei einlesen')
    df = pd.read_csv(EINGABE_FILE2, delimiter=';')
    print('Ende: CSV-Datei einlesen')

    print('Start: Datum umwandeln')
    df['TimestampEpoch'] = pd.to_datetime(df['TimestampEpoch'], unit='s', utc=True).dt.tz_convert('Europe/Berlin')
    print('Ende: Datum umwandeln')

    print('Start: DataBytes umwandeln')
    for i in range(1, 5):  # Von 1 bis 4, da es nur vier DataBytes gibt
        df[f'DataByte_{i}'] = df['DataBytes'].apply(
            lambda x: split_data_bytes(x)[i - 1] if isinstance(x, str) and len(x) == 16 else None)
    print('Ende: DataBytes umwandeln')

    print('Start: unique IDs zusammenstellen')
    ids_df = pd.DataFrame({'HexKey': df['ID'].unique()})
    print('Ende: unique IDs zusammenstellen')

    # df['Time'] = df['TimestampEpoch'].dt.time
    # start_time = pd.to_datetime("10:55").time()
    # end_time = pd.to_datetime("11:08").time()
    # df = df[(df['Time'] >= start_time) & (df['Time'] <= end_time)]

    print('Start: Graphen erstellen')
    for nr, desired_key in enumerate(ids_df['HexKey']):

        print(f"Graph {nr} von {len(ids_df['HexKey'])}")

        filtered_data = df[df['ID'] == desired_key]
        filtered_data = filtered_data.iloc[::100, :]

        if not filtered_data.empty:
            # X-Werte sind der TimestampEpoch
            x = filtered_data['TimestampEpoch']

            # Für jedes DataByte eine separate Figur und einen Plot erstellen
            for i in range(1, 5):  # Von 1 bis 4
                # if (desired_key, f'DataByte_{i}') in allowed_combinations:
                y = filtered_data[f'DataByte_{i}']

                if y.nunique() > 1:
                    plt.figure(figsize=(21, 9))  # Erstellt eine neue Figur für dieses DataByte

                    plt.plot(x, y, label=f'DataByte_{i}')

                    fig = plt.gcf()
                    if fig.axes:
                        plt.legend(loc='upper left')  # Legende hinzufügen
                        plt.title(f"Plot für ID {desired_key} - {f'DataByte_{i}'}")

                        filename = os.path.join(AUSGABE_PFAD_GRAPH2, f"plot_{desired_key}_{f'DataByte_{i}'}.png")
                        plt.savefig(filename)

                        csv_filename = os.path.join(AUSGABE_PFAD_GRAPH2, f"data_{desired_key}_{f'DataByte_{i}'}.csv")
                        filtered_data.to_csv(csv_filename, index=False)

                    plt.close()
        else:
            print(f"No data found for HexKey {desired_key}")
    print('Ende: Graphen erstellen')


plot_data()

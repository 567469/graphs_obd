import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

from variables import EINGABE_FILE, AUSGABE_PFAD_GRAPH


def smooth_data_savgol(series, window_length, poly_order):
    return savgol_filter(series, window_length, poly_order)

def resample_grouped_data(group):
    return group.resample('30S').mean()


def convert_hex_to_decimal(hex_val):
    return int(hex_val, 16)


def split_and_convert_to_decimal(data):
    # Splittet den DataBytes-String in jeweils zwei Zeichen
    split_data = [data[i:i + 2] for i in range(0, len(data), 2)]

    # Wandelt die einzelnen Hexadezimal-Werte in Dezimal um
    decimal_data = [convert_hex_to_decimal(x) for x in split_data]
    return decimal_data


def plot_graph_smooth(df, id, position):
    # Filtert die Daten nach ID und Position im DataBytes-Feld
    filtered_data = df[df["ID"] == id]
    timestamps = filtered_data["TimestampEpoch"]
    values = filtered_data[str(position)]

    # Überprüft, ob alle Werte gleich sind
    if all(val == values.iloc[0] for val in values):
        return

    # Glättung der Daten mit Savitzky-Golay Filter
    # Die Werte für window_length und poly_order können je nach Ihren Daten angepasst werden.
    # window_length muss ungerade sein und poly_order muss kleiner als window_length sein.
    smoothed_values = smooth_data_savgol(values, window_length=9, poly_order=2)

    # Plottet die Daten
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, smoothed_values, label=f'Position: {position}')
    plt.title(f'Graph for ID: {id} at Position: {position}')
    plt.xlabel('TimestampEpoch')
    plt.ylabel('Value')
    plt.legend()

    # Speichert den Graphen
    if not os.path.exists(AUSGABE_PFAD_GRAPH):
        os.mkdir(AUSGABE_PFAD_GRAPH)
    plt.savefig(AUSGABE_PFAD_GRAPH + f"\\ID_{id}_Pos_{position}.png")
    plt.close()


def plot_graph(df, id, position):
    # Filtert die Daten nach ID und Position im DataBytes-Feld
    filtered_data = df[df["ID"] == id]
    timestamps = filtered_data["TimestampEpoch"]
    values = filtered_data[str(position)]

    # Überprüft, ob alle Werte gleich sind
    if all(val == values.iloc[0] for val in values):
        return

    # Plottet die Daten
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, values, label=f'Position: {position}')
    plt.title(f'Graph for ID: {id} at Position: {position}')
    plt.xlabel('TimestampEpoch')
    plt.ylabel('Value')
    plt.legend()

    # Speichert den Graphen
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    plt.savefig(output_folder + f"\\ID_{id}_Pos_{position}.png")
    plt.close()


# Liest die CSV-Datei
df = pd.read_csv(EINGABE_FILE, delimiter=";")

# Wandelt den DataBytes-Wert in eine Liste von Dezimalzahlen um
df["DataBytes"] = df["DataBytes"].apply(split_and_convert_to_decimal)

# Fügt für jede Position in DataBytes eine neue Spalte hinzu
for i in range(8):
    df[str(i)] = df["DataBytes"].apply(lambda x: x[i] if i < len(x) else None)

# Entfernt die DataBytes-Spalte, da sie nicht mehr benötigt wird
df = df.drop(columns=["DataBytes"])
df['TimestampEpoch'] = pd.to_datetime(df['TimestampEpoch'], unit='s', utc=True).dt.tz_convert('Europe/Berlin')

# Setzt den TimestampEpoch als Index
df.set_index('TimestampEpoch', inplace=True)

# Gruppiert nach ID und wendet resample auf jede Gruppe an
df_resampled = df.groupby('ID').apply(resample_grouped_data)

# Entfernt die zusätzliche ID-Ebene im Index, die durch groupby erstellt wurde
df_resampled = df_resampled.reset_index()

# Plottet die Graphen für jede Kombination aus ID und Position in DataBytes
unique_ids = df["ID"].unique()
for id in unique_ids:
    for position in range(8):
        plot_graph_smooth(df_resampled, id, position)

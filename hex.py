import pandas as pd

from variables import EINGABE_FILE, CAN_ID, PFAD_ZU_HEX_FILE, PFAD_ZU_DEC_FILE


def hex_to_dec(hex_str):
    return str(int(hex_str, 16))


def csv_to_text_and_csv_files():
    # CSV-Datei mit pandas einlesen; Semikolons als Trennzeichen verwenden
    df = pd.read_csv(EINGABE_FILE, sep=";")

    # Konvertiere das Feld 'TimestampEpoch'
    df['TimestampEpoch'] = pd.to_datetime(df['TimestampEpoch'], unit='s', utc=True).dt.tz_convert('Europe/Berlin')

    # Zeilen filtern, bei denen die Spalte "ID" dem geforderten Text entspricht
    filtered_df = df[df["ID"] == CAN_ID]

    # Überprüfen ob es gefilterte Daten gibt
    if not filtered_df.empty:
        # Textdatei erstellen
        formatted_data_for_text = [' '.join([str(ts), ' '.join([data[i:i + 2] for i in range(0, len(data), 2)])]) for
                                   ts, data in zip(filtered_df['TimestampEpoch'], filtered_df['DataBytes'])]
        with open(PFAD_ZU_HEX_FILE, 'w') as f:
            f.write('\n'.join(formatted_data_for_text))

        # CSV-Datei erstellen mit hexadezimalen Werten in dezimale umgewandelt
        formatted_data_for_csv = [';'.join([str(ts)] + [hex_to_dec(data[i:i + 2]) for i in range(0, len(data), 2)]) for
                                  ts, data in zip(filtered_df['TimestampEpoch'], filtered_df['DataBytes'])]
        with open(PFAD_ZU_DEC_FILE, 'w') as f:
            for line in formatted_data_for_csv:
                f.write(line + '\n')
    else:
        print(f"Keine Daten gefunden für ID: {CAN_ID}")

csv_to_text_and_csv_files()

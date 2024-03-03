import cv2
import pytesseract
import re
import csv

from variables import ORDNER_NAME_VIDEO, ORDNER_NAME_CSV

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.'
pattern = r"^(?:\d{1,2}\.\d|\d{1,2})$"

# Öffne das Video
cap = cv2.VideoCapture(ORDNER_NAME_VIDEO)
fps = int(cap.get(cv2.CAP_PROP_FPS))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

with open(ORDNER_NAME_CSV, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Time (min:sec:ms)", "Float Number"])

    for frame_num in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        # Binarisierung (optional, kann die Erkennung verbessern)
        _, binary_frame = cv2.threshold(frame, 128, 255, cv2.THRESH_BINARY)

        # Erlaubt nur Zahlen und den Punkt
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.'

        # Wenn Sie den ROI kennen, schneiden Sie das Bild entsprechend zu:
        # x, y sind die obere linke Ecke und w, h sind die Breite und Höhe der ROI.
        # roi = binary_frame[y:y+h, x:x+w]

        # OCR auf dem gesamten Frame oder dem ROI
        extracted_text = pytesseract.image_to_string(binary_frame, config=custom_config)  # oder roi statt binary_frame

        # Entferne unnötige Zeichen und Whitespace
        extracted_text = extracted_text.strip()

        if re.match(pattern, extracted_text):
            # Zeitstempel berechnen
            time_in_ms = (frame_num * 1000) // fps
            minutes = time_in_ms // 60000
            seconds = (time_in_ms % 60000) // 1000
            milliseconds = time_in_ms % 1000

            timestamp = f"{minutes}:{seconds}:{milliseconds}"
            csv_writer.writerow([timestamp, extracted_text])
            print(timestamp)

cap.release()
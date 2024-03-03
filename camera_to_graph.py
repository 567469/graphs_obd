import cv2
import pytesseract
import pandas as pd
from moviepy.editor import VideoFileClip

from variables import PFAD_ZUR_VIDEO_CSV, VIDEO_PATH

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

df = pd.DataFrame(columns=['Zahlen'])
cap = cv2.VideoCapture(VIDEO_PATH)

def format_seconds_to_timestamp(seconds):
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return "{:02d}:{:02d}:{:02d}.{:03d}Z".format(hours, minutes, int(seconds), milliseconds)

def convert_to_float(text):
    # Ersetze Kommas durch Punkte
    text = text.replace(',', '.')
    try:
        return float(text)
    except ValueError:
        return None

clip = VideoFileClip(VIDEO_PATH)
framerate = clip.fps  # Dies gibt die Framerate des Videos zurück
clip.close()
frame_duration = 1.0 / framerate
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    current_time_seconds = frame_duration * frame_count
    timestamp = format_seconds_to_timestamp(current_time_seconds)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresholded = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # ROI für Uhrzeit
    #roi_time = gray[423:423+134, 59:59+288]
    # time_text = pytesseract.image_to_string(roi_time).strip()

    # ROI für Float-Zahl
    roi_number = gray[319:319+391, 593:593+831]
    number_text = pytesseract.image_to_string(roi_number, config='--psm 6').strip()

    # Konvertiere den Text zu einer float-Zahl
    number = convert_to_float(number_text)

    if number is not None and number < 100:
        new_row = pd.DataFrame({'Frame': [frame_count], 'Uhrzeit': [timestamp], 'Zahlen': [number]})
        df = pd.concat([df, new_row], ignore_index=True)
        print(len(df))

cap.release()
cv2.destroyAllWindows()

# Daten in CSV-Datei speichern
df.to_csv(PFAD_ZUR_VIDEO_CSV, index=False)

# Optional: Daten aus CSV-Datei lesen
# df2 = pd.read_csv(data_path)
#
# # Plot des DataFrames
# plt.figure(figsize=(21, 9))
# df2.plot(kind='line', y='Zahlen', title='Erkannte Zahlen aus dem Video', grid=True)
# plt.ylabel('Wert')
# plt.xlabel('Frame Index')
# plt.show()


# def files():
#     try:
#         print('deleting Files')
#         os.remove(image_path)
#     except OSError:
#         pass
#
#     if not os.path.exists(image_path):
#         print('creating Folder')
#         os.makedirs(image_path)
#
#     print('loading Video')
#     src_vid = cv2.VideoCapture(video_path)
#     print('loading Video completed')
#     return src_vid
#
#
# def process(src_vid):
#     index = 0
#     while src_vid.isOpened():
#         ret, frame = src_vid.read()
#         if not ret:
#             break
#
#         name = image_path + 'frame' + str(index) + '.png'
#         if index % 100 == 0:
#             print('Extracting frames...' + name)
#             cv2.imwrite(name, frame)
#         index = index + 1
#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break
#
#     src_vid.release()
#     cv2.destroyAllWindows()
#
#
# def get_text():
#     for i in os.listdir(image_path):
#         # print(str(i))
#         opened_image = Image.open(image_path + i)
#         text = pytesseract.image_to_string(opened_image)
#         print(text)
#
#
# # vid = files()
# # process(vid)
# get_text()

Dieses Repository ist Teil der Bachelorarbeit von Simon J. Heilmeier (Matr.Nr.: 567469) mit dem Titel:

# Prototypische Entwicklung einer Smartphone-Anwendung zur Verbrauchserkennung elektrifizierter Fahrzeuge

Bei der Implementierung der fogenden Scripte wurde ChatGPT4 [^1] verwendet um im Entwicklungsprozess zu unterstützen.

Inhaltsverzeichnis:

- [Skript_CSVDatein.R](https://github.com/567469/graphs_obd/blob/master/Skript_CSVDatein.R)  --> Script zum optischen Vergleich anhand von Graphen, von den gemittelten CAN- und Sensordaten
- [camera_csv_to_median.py](https://github.com/567469/graphs_obd/blob/master/camera_csv_to_median.py)  --> Berechnet aus einer CSV-Datei den Median in einem angegebenen Intervall 
- [camera_to_graph.py](https://github.com/567469/graphs_obd/blob/master/camera_to_graph.py)  --> Erste Variante der Textextraktion aus einem Video
- [camera_to_graph_new.py](https://github.com/567469/graphs_obd/blob/master/camera_to_graph_new.py)  --> Zweite Variante der Textextraktion aus einem Video
- [hex.py](https://github.com/567469/graphs_obd/blob/master/hex.py)  --> Script zur besseren Darstellung der HEX_CAN-Daten in dezimaler Darstellung
- [obd_to_graph.py](https://github.com/567469/graphs_obd/blob/master/obd_to_graph.py)  --> Erstellung der Graphen aus umgewandelter CSV-Datei, die die CAN-Daten enthält
- [obd_to_graph_2Byte.py](https://github.com/567469/graphs_obd/blob/master/obd_to_graph_2Byte.py)  --> Erstellung der Graphen aus umgewandelter CSV-Datei, die die CAN-Daten enthält, mit Filter für relevante CAN-IDs.

Zur Ausführung benötigte Files: (*Können für die Begutachtung freigegeben werden* [Simon J. Heilmeier](mailto:567469@fom-net.de?subject=[GitHub]%20Daten-Freigabe))

- aufgenommene Videos & erstellte CSV-Datein
  - (*enthält private Fahrt-Daten, die nicht für die Veröffentlichung bestimmt sind*) 
- ... .MF4 (Datein des CAN-Bus-Loggers)
  - (*enthält proprietäre Daten, die nicht für die Veröffentlichung bestimmt sind*)


[^1]: https://chat.openai.com/


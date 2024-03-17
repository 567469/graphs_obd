library(ggplot2)
library(dplyr)

# Angeben des Ordnernamens
ordnername <- "C:/..."
startTimeStamp<- "2023-09-30 00:13:08"

# Daten laden
# ------------------------------------------------------------------------------
# Pfad zu den Dateien basierend auf dem Ordnernamen erstellen
pfad_erste_datei <- file.path(ordnername, "XXX_dec_Median.csv")
pfad_zweite_datei <- file.path(ordnername, "daten_median.csv")

# Einlesen der CSV-Dateien
erste_datei <- read.csv(pfad_erste_datei, header=TRUE, sep=",", stringsAsFactors=FALSE)
zweite_datei <- read.csv(pfad_zweite_datei, header=TRUE, sep=",", stringsAsFactors=FALSE)

#erste_datei$DataByte_2 <- erste_datei$DataByte_2 / 9.1 + 7.9
erste_datei$DataByte_2 <- erste_datei$DataByte_2 / 2.5
#erste_datei$DataByte_4 <- erste_datei$DataByte_4 / 1.5

erste_datei$Combined <- erste_datei$DataByte_2 + erste_datei$DataByte_4

# Sicherstellen, dass die 'Time' Spalte als Zeichenkette behandelt wird
zweite_datei$Time <- as.character(zweite_datei$Time)

# Konvertieren der 'Time' Spalte aus zweite_datei in eine Zeitdifferenz
zeit_parts <- strsplit(zweite_datei$Time, ":")
zeit_in_sekunden <- sapply(zeit_parts, function(parts) {
  min <- as.numeric(parts[1])
  sek <- as.numeric(parts[2])
  ms <- as.numeric(parts[3]) / 1000
  return(min*60 + sek + ms)
})

# Addieren der Zeitdifferenz zu einem Startdatum und einer Startzeit
start_datum_zeit <- as.POSIXct(startTimeStamp, format="%Y-%m-%d %H:%M:%S", tz="UTC")
start_milliseconds <- 123 / 1000
start_datum_zeit <- start_datum_zeit + start_milliseconds

zweite_datei$DateTime <- start_datum_zeit + zeit_in_sekunden

# Konvertiere die 'Time' Spalte aus erste_datei in POSIXct
erste_datei$Time <- as.POSIXct(erste_datei$Time, format="%Y-%m-%d %H:%M:%OS", tz="UTC")

# Konvertiere die 'DateTime' Spalte aus zweite_datei in POSIXct
zweite_datei$DateTime <- as.POSIXct(zweite_datei$DateTime, format="%Y-%m-%d %H:%M:%OS3", tz="UTC")
# ------------------------------------------------------------------------------

# Daten für ggplot vorbereiten
# ------------------------------------------------------------------------------
# Für die erste Datei
data1 <- data.frame(Time = erste_datei$Time,
                    Value = erste_datei$DataByte_2,
                    Source = 'erste_datei',
                    Type = 'DataByte_2')

data2 <- data.frame(Time = erste_datei$Time,
                    Value = erste_datei$DataByte_4,
                    Source = 'erste_datei',
                    Type = 'DataByte_4')

# Für die zweite Datei
data3 <- data.frame(Time = zweite_datei$DateTime,
                    Value = zweite_datei$Number,
                    Source = 'zweite_datei',
                    Type = 'Number')

data_combined <- data.frame(Time = erste_datei$Time,
                            Value = erste_datei$Combined,
                            Source = 'erste_datei',
                            Type = 'Combined')

# Kombinieren Sie alle Daten
#all_data <- rbind(data1, data3)
all_data <- rbind(data1, data3)

# Darstellung als Linien-Graph
gg <- ggplot(all_data, aes(x=Time, y=Value, group=Source)) + 
  geom_line(aes(linetype = Source, color = Source, size = Source)) +
  labs(x="Zeit", y="kWh/100 km") +
  theme_minimal() +
  theme(
    legend.position = "top",
    legend.title = element_text(size=14),       # Größe des Legendentitels
    legend.text = element_text(size=12),        # Größe des Legendentextes
    axis.title = element_text(size=14),         # Größe der Achsentitel
    axis.text.x = element_text(size=10),        # Größe des Textes der x-Achse
    axis.text.y = element_text(size=10)         # Größe des Textes der y-Achse
  ) +
  scale_color_manual(values=c("#E69F00", "#56B4E9"), 
                     name="Quelle", 
                     labels=c("CAN-Daten", "Aufnahme-Daten")) +
  scale_linetype_manual(values=c("solid", "dashed"), 
                        name="Quelle", 
                        labels=c("CAN-Daten", "Aufnahme-Daten")) +
  scale_size_manual(values=c(1.01, 0.75),                        
                    name="Quelle", 
                    labels=c("CAN-Daten", "Aufnahme-Daten"))
# ------------------------------------------------------------------------------

ggsave(filename = "C:/.../meinGGplotDiagramm.jpeg", plot = gg, width = 1920/96, height = 1080/96, dpi = 96)

print(gg)

mittelwert_data1 <- mean(data1$Value, na.rm = TRUE)
mittelwert_data2 <- mean(data2$Value, na.rm = TRUE)
mittelwert_data_combined <- mean(data_combined$Value, na.rm = TRUE)

print(mittelwert_data1)
print(mittelwert_data2)
print(mittelwert_data_combined)



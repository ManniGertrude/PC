## Dieses Repository beinhaltet Auswertungen von drei verschiedenen Versuchen bezüglich der Löslichkeit von Festkörpern. 

### Daten-Ordner
**Im Ordner "Daten" sind die Daten für 5 Semester des "Mirkoskop" Versuchs, sowie Datensätze des Wintersemesters 2024/25 der beiden anderen Versuche "Wasser" und "Ideal".**
- Genauere Aufschlüsselung ist in der ReadMe.md Datei im Daten-Ordner zu finden.
- Ebenso ist ein weiterer Ordner enthalten, der eine LaTeX-Tabellen-Aufbereitung der Daten in pdf-Form beinhaltet.

### PNG-Ordner
**Im Ordner "PNG" sind die Diagramme für 5 Semester des "Mirkoskop" Versuchs, sowie des Wintersemesters 2024/25 des Versuchs "Wasser".**
- Genauere Aufschlüsselung ist in der ReadMe.md Datei im PNG-Ordner zu finden.

### Lösungen.py
Die Python Datei *Lösungen.py* erstellt die Dateien im *PNG/WS2425 Wasser* Ordner aus den Daten aus *Daten/Wasser_WS_24-25.csv* und gibt die errechnete ideale Löslichkeit sowie Lösungsenthalpie und Mischungsenthalpie ins Terminal aus. Dies geschieht in der Funktion *Auswertung*

Ebenfalls werden die Werte aus *Daten/Ideal_WS_24-25.csv* mit der Funktion *Ideal* ausgewertet und ebenfalls ins Terminal ausgegeben.

Ob alle Gruppen mit *AlleAbfragen* oder nur bestimmte Gruppen mit *EineAbfrage* bzw. *EineGruppe* ausgewertet werden sollen, kann individuell eingestellt werden. *EineAbfrage* wertet nur die wässrige Lösung eines Stoffes einer Gruppe aus, während *EineGruppe* beide wässrige Lösungen sowie die ideale mit *Ideal* analysiert.

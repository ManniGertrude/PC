Im Ordner "Daten" sind die Daten für 5 Semester des "Mirkoskop" Versuchs, sowie Datensätze des Wintersemesters 2024/25 der beiden anderen Versuche "Wasser" und "Ideal", sowie ein Ordner "DatenPDF".


DatenPDF ist ein Ordner, indem u.a. DatenPDF.py, DatenPDFtab.tex DatenPDF.tex zu finden sind. 
- Die .py Datei konvertiert die Messdaten des übergeordneten Ordners in eine LaTeX Schreibweise und speichert Diese in DatenPDFtab.tex.
- In DatenPDF.tex wird diese DatenPDFtab.tex nun in ein reguläres LaTeX Umfeld per \include eingefügt, was DatenPDF.pdf erstellt.
- Alle weiteren Dateien werden von LaTeX bei der PDF-Erstellung erzeugt und sind nicht weiter relevant.


Die "Mikroskop" Daten beinhalten Temperaturwerte für bestimmte Zusammensetzungen für die untere und obere Schmelztemperatur des Systems Benzamid - Acetanilid, bzw. für das WS24/25 Acetanilid - Benzil. 
- E290 bedeutet beispielsweise die Eutektikums-Temperatur (untere Schmelztemperatur) bei einer Zusammensetzung mit einem Stoffmengenanteil von 29.0% Acetanilid oder im WS24/25 29.0% Benzil.
- L290 ist dann die Liquidus-Temperatur (obere Schmelztemperatur) der gleichen Zusammensetzung.
- Die Gruppenbezeichnung bezieht sich auf die Gruppen, die den Versuch durchgeführt haben und der Rest des Datei-Namens beschreibt der Zeitraum der Messreihen.


Ideal_WS_24-25.csv beinhaltet die Werte, die bei der Vermessung einer vermeindlich idealen Lösung von Benzoesäure in 65% Ethanol und 35% Ethylacetat von verschiedenen Gruppen erstellt wurden.
- T ist hierbei die Temperatur der Lösung in °C.
- M_Tara und M_brutto sind die Massen in g der genutzten Wägepipette.
- NaOH ist die Menge an 0.5M NaOH in mL, die gegentritiert werden musste bis zum Umschlagpunkt. Genutzt wurden wenige Tropfen verdünntes Phenolphthalein.


Wasser_WS_24-25.csv beinhaltet die Werte, die bei der Vermessung einer vermeindlich ideal verdünnten Lösung von entweder Benzoesäure oder Salicylsäure in deionisiertem Wasser. 
- T(X_Y) bzw. V(X_Y) beschreibt dabei Temperatur T in °C der Lösung bei Entnahme und gegentritiertes Volumen V von 0.1M NaOH in mL der Gruppe X mit Stoff Y (S für Salicylsäure, B für Benzoesäure).
- Jede Gruppe hat dabei bei verschiedenen Temperaturen 6 Messwerte genommen.

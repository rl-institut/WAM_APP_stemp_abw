.. _energy_system_label:

Energiesystem
=============

Die Berechnungen dieses StEmp-Tools umfassen u.a. die Erzeugung, den Bedarf und
die Speicherung von elektrischer und thermischer Energie über ein Kalenderjahr.
Was auf den ersten Blick wie eine simple Bilanzierung von Energiemengen anmuten
könnte, ist in Wirklichkeit ein Energiesystemmodell, das mit Hilfe einer
linearen Optimierung gelöst wird.

Für die Optimierung wird das vom RLI mitentwickelte
`Open Energy System Modelling Framework (oemof) <https://oemof.readthedocs.io/en/stable/index.html>`_
eingesetzt. oemof ist ein freies, offenes und gut dokumentiertes Framework für
die Modellierung und Optimierung von Energieversorgungssystemen.

Die Eingangsparameter für das Modell sind einerseits vorberechnete Daten wie
beispielsweise Zeitreihen zur Einspeisung oder Heizwärebedarf und andererseits
die durch den/die BenutzerIn einstellbaren Größen wie z.B. installierte
Windleistung. Die Ergebnisse werden im Anschluss an die Optimierung aufbereitet
und im Tool dargestellt.

Struktur und Vereinfachungen
----------------------------

Das Energiesystemmodell wird über Komponenten definiert (bspw. Erzeuger und
Verbraucher), die an Busse angeschlossen werden an welchen ein Austausch
stattfindet. Aus diesem Modell wird ein lineares Optimierungsproblem erstellt,
das durch einen Solver gelöst wird.

Aus verschiedenen Gründen sind Vereinfachungen notwendig, um ein sinnvolles
Gleichgewicht aus Genauigkeit und Rechenzeit herzustellen.

:Zeitraum:
    Die Optimierung erstreckt sich über den Zeitraum von 1 Kalenderjahr in
    1h-Schritten.

:Perfect Foresight:
    Aus den gegebenen Randbedingungen wird ein Gesamtproblem erstellt, der
    Zustand aller Komponenten des Energiesystems wie z.B. Erzeuger ist zu
    jedem Zeitpunkt bekannt (im Gegensatz zu bspw. Rolling-Horizon-Verfahren)

:Modelltopologie:
    Die antreibenden Modelldaten selbst liegen gemeindescharf vor, werden
    zugunsten der Rechenzeit jedoch zusammengefasst und an einen zentralen
    elektrischen Bus angeschlossen. So werden z.B. die Einspeisezeitreihen der
    Windenergieanlagen aller 20 Gemeinden in einer einzigen Komponente
    aggregiert und mit diesem Bus verbunden. Im Ergebnis besteht das Modell
    aus einem Einspeiser pro Technologie (Wind, FF-PV, Dach-PV, ...) und einem
    Verbraucher pro Sektor (Haushalte, GHD u. Landwirtschaft, Industrie). Für
    die Ergebnisdarstellung in der Karte findet eine Desaggregation statt.

Mehr über die Integration des Energiesystems in das Tool erfahren sie unter
:ref:`developer_label`.

.. _energy_system_label:

Energiesystem
=============

Die Berechnungen dieses StEmp-Tools umfassen u.a. die Erzeugung, den Bedarf und
die Speicherung von elektrischer und thermischer Energie über ein Kalenderjahr.
Was auf den ersten Blick wie eine simple Bilanzierung von Energiemengen anmuten
könnte, ist in Wirklichkeit ein Energiesystemmodell, das mit Hilfe einer
linearen Optimierung gelöst wird.

Die Eingangsparameter für das Modell sind einerseits vorberechnete Daten wie
beispielsweise Zeitreihen zur Einspeisung oder Heizwärebedarf und andererseits
die durch den/die BenutzerIn einstellbaren Größen wie z.B. installierte
Windleistung. Die Ergebnisse werden im Anschluss an die Optimierung aufbereitet
und im Tool dargestellt.

Features in aller Kürze
-----------------------

- Lineare Optimierung
- Zeitraum 1 Kalenderjahr
- Zeitintervall: 1 Stunde
- usw.

Struktur
--------

Für die Optimierung wird das vom RLI mitentwickelte
`Open Energy System Modelling Framework (oemof) <https://oemof.readthedocs.io/en/stable/index.html>`_
eingesetzt. oemof ist ein freies, offenes und gut dokumentiertes Framework für
die Modellierung und Optimierung von Energieversorgungssystemen.

Mehr über die Schnittstelle des Tool zum erfahren sie unter :ref:`developer_label`.

<INSERT ENERGY MODEL GRAPH HERE>

Vereinfachungen
---------------

Aus verschiedenen Gründen sind Vereinfachungen notwendig, um ein sinnvolles
Gleichgewicht aus Genauigkeit und Rechenzeit herzustellen. Methodische
Vereinfachungen finden Sie unter :ref:`scenarios_label`.

:Perfect Foresight:
    Aus den gegebenen Randbedingungen wird ein Gesamtproblem erstellt, der
    Zustand aller Komponenten des Energiesystems wie z.B. Erzeuger ist zu
    jedem Zeitpunkt bekannt (im Gegensatz zu bspw. zu
    Rolling-Horizon-Verfahren)

:add more:
    Text

Integration
-----------

Mehr über die Integration des Energiesystems in das Tool erfahren sie unter
:ref:`developer_energy_system_label` (für EntwicklerInnen).



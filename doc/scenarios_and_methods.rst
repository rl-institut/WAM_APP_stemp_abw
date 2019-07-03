.. _scenarios_label:

Szenarien und Methoden
======================

Szenarien
---------

Für das Tool wurden mehrere Szenarien entwickelt, wie in folder Tabelle dargestellt:

+------------+------------+------------+-----------+
|            | Status Quo | Szenario 2 | Szenario 3|
+============+============+============+===========+
| Bezugsjahr | 2016       | column 2   | column 3  |
+------------+------------+------------+-----------+
| Monty      | body row 2 | Cells may span columns.|
+------------+------------+------------+-----------+
| Python     | body row 3 | Cells may  | - Cells   |
+------------+------------+ span rows. | - contain |
| Brian      | body row 4 |            | - blocks. |
+------------+------------+------------+-----------+

Mehr über die Integration der Szenarien in das Tool erfahren sie unter
:ref:`developer_scenarios_label` (für EntwicklerInnen).

Methoden
--------

Energiesystem
.............

Mehr über die Integration des Energiesystems in das Tool erfahren sie unter
:ref:`developer_energy_system_label` (für EntwicklerInnen).

Daten
.....

Hier kommen Details zu der Erstellung der verwendeten :ref:`data_label` rein.

Beispiel: Einspeisezeitreihen

Vereinfachungen
---------------

Modelle, Szenarien und Daten können grundsätzlich in nahezu beliebiger
Komplexität ausgeführt werden. Aus verschiedenen Gründen ist eine Reduktion
der Genauigkeit jedoch notwendig:

- Bei der Bedienung des Tools sollten auftretende Wartezeiten - und folglich
  auch der Rechenaufwand - auf ein Minimum reduziert werden
- Die Verfügbarkeit von (inbesondere offener) Eingangsdaten ist begrenzt
- [ADD MORE]

Die Vereinfachungen umfassen:

- Wärme: Keine Betrachtung des Industriesektors [BEGRÜNDUNG]
- [ADD MORE FROM METHODS DOC]

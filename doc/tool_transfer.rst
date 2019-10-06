.. _tool_transfer_label:

Übertragung des Tools auf andere Regionen
=========================================

Das Tool kann durch seinen offenen Charakter grundsätzlich auf andere Regionen
übertragen werden.

Der aufwändigste Teil ist hierbei die Recherche und Aufbereitung der Daten,
siehe auch :ref:`data_label`.

Es werden **statische Geodaten** (im Tool Flächen -> Statische Flächen)
verwendet, deren Verfügbarkeit je nach Region unterschiedlich ausfällt. Zudem
müssen die Daten oft von von vielen verschiedenen Anbietern (Regionalplanung,
Landesämter, Umweltbehörden, ...) bezogen werden.

Die :ref:`areas_and_potentials_label` werden u.a. durch Verschneidung von
geeigneten Flächen mit Restriktionsflächen erzeugt. Die Aufbereitung und
Verarbeitung der Geodaten (z.B. mit `QGIS <https://www.qgis.org>`_) nimmt
hierbei den meiste Zeit in Anspruch.

Weiterhin werden **Kraftwerksdaten** benötigt, die in vollständiger,
georeferenzierter Form derzeit (Stand Sep. 2019) noch nicht verfügbar sind. Mit
der Einführung des Marktstammdatenregisters
(`MaStR <https://www.marktstammdatenregister.de>`_) ist hier ein wichtiger
Schritt erfolgt, die Georeferenzierung dauert jedoch noch an. Das RLI hat ein
offenes `Tool <https://github.com/OpenEnergyPlatform/open-MaStR>`_ entwickelt,
mit dessen Hilfe der aktuelle Stand des heruntergeladen werden kann. Ein
ständig aktualisierter Datensatz kann auch über die
`Website des RLI <https://reiner-lemoine-institut.de/datenveroeffentlichung-aus-dem-marktstammdatenregister-der-bundesnetzagentur/>`_
heruntergeladen werden.

Aus diesen Daten können unter Verwendung passender Wetterdaten vom Tool
benötigte **Einspeisezeitreihen** für fluktuierende erneuerbare Energieanlagen
generiert werden. Alternativ kann auf geeignete Tools zurückgegriffen werden,
die fertige Zeitreihen generien, z.B.
`open_FRED <https://wam.rl-institut.de/WAM_APP_FRED/>`_ (verwendet u.a.
`windpowerlib <https://github.com/wind-python/windpowerlib>`_ und
`pvlib <https://github.com/pvlib/pvlib-python>`_) oder
`renewables.ninja <https://www.renewables.ninja/>`_.

Erforderliche **Verbrauchsdaten** können zum Beispiel in stark aggregierter
Form von Statistischen Landesämtern oder detaillierter von der
`OpenEnergy Platform <https://openenergy-platform.org/>`_ bezogen werden.
Anhand von Standardlastprofilen können Zeitreihen generiert werden, etwa mit
der `demandlib <https://github.com/oemof/demandlib>`_.

Bei der Erstellung dieser Datensätze und darüber hinaus werden weitere Annahmen
benötigt.

Bei allen verwendeten Daten ist stets die Lizenz zu beachten. Dürfen die Daten
verändert oder veröffentlicht werden? Wenn ja, unter welchen Bedingungen? Wie
müssen abgeleitete Daten lizenziert werden?  Siehe hierzu auch
`1 <https://wiki.openmod-initiative.org/wiki/Choosing_a_license>`_ und
`2 <https://reiner-lemoine-institut.de/beyond-open-source-modeling/>`_.

Ein geeigneter Einstiegspunkt für die Energiesystemmodellierung ist die
`openmod initiative <https://wiki.openmod-initiative.org>`_.

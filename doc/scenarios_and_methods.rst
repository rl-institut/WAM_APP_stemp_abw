.. _scenarios_label:

Szenarien und Methoden
======================

Szenarien
---------

Das Grundszenario ist der Status quo (Stand der Daten: Ende 2017), der als
Ausgangspunkt für Variationen dient. Mögliche Variationen umfassen die
Anpassung der Energieerzeugung (und diese beeinflussende EE-Potenzialflächen)
sowie des Energieverbrauchs.

Es können weitere Szenarien definiert werden, die anschließend im Tool
ausgewählt werden können. Mehr über die Integration der Szenarien erfahren Sie
unter :ref:`developer_scenarios_label` (für EntwicklerInnen).

Methoden
--------

Im Folgenden werden die wichtigsten Methoden skizziert, die für die
Aufbereitung der Rohdaten zu verwendbaren Daten innerhalb des Tools und
Parametrierung des Energiesystems verwendet wurden.

Erzeugung der Tooldaten
.......................

Wenn Sie beabsichtigen neue Eingangsdaten zu erzeugen, können Sie die folgenden
Schritte selbst ausführen oder alternative Daten und Tools verwenden, siehe
Kapitel :ref:`tool_transfer_label`.

Kraftwerksdaten
+++++++++++++++

1. Herunterladen des aktuellen Kraftwerksdatensatzes von
   `Open Power Systems Data (OPSD) <https://open-power-system-data.org/>`_
   (EE und konventionell).
2. Zuordnung der Kraftwerke zu Gemeinden anhand der Koordinaten
3. Aggregation von Leistung und Anzahl nach Technologie und Gemeinde
4. Speichern in Tabelle :class:`stemp_abw.models.MunData`.

Anmerkung: Für die räumliche Zuordnung auf Gemeindeebene ist die Genuigkeit
des OPSD-Datensatzes ausreichend, nicht jedoch für eine exakte
Geopositionierung. Hierfür sollte auf OSM-Daten oder zukünftig auf das
Marktstammdatenregister zurückgegriffen werden, s. :ref:`tool_transfer_label`.

Verbrauchsdaten Strom
+++++++++++++++++++++

1. Herunterladen des Datensatzes zu Lastgebieten (Load Areas) von der
   `OpenEnergy Platform <https://openenergy-platform.org/dataedit/view/demand/ego_dp_loadarea>`_,
   welcher den jährlichen Verbrauch je OSM-Lastgebiet und Sektor enthält
   (`Paper zum Hintergrund <https://journals.aau.dk/index.php/sepm/article/download/1833/1531>`_).
2. Herunterladen des Datensatzes zu industriellen Großverbrauchern (Large scale
   consumer) von der
   `OpenEnergy Platform <https://openenergy-platform.org/dataedit/view/model_draft/ego_demand_hv_largescaleconsumer>`_,
   welcher den jährlichen Verbrauch je OSM-Lastgebiet und Sektor enthält.
3. Zuordnung der Load Areas und Large scale consumer zu Gemeinden anhand der
   Koordinaten
4. Aggregation des Verbrauchs nach Sektor und Gemeinde
5. Speichern in Tabelle :class:`stemp_abw.models.MunData`.

Verbrauchsdaten Wärme
+++++++++++++++++++++

Die Wärmebedarfe von Haushalten wurden mit Hilfe folgender Daten gemeindescharf
bestimmt:

- Wohngebäudebestand (Alter, Größe, Wohneinheiten, Leerstand etc.) nach
  `Zensus 2011 <https://ergebnisse.zensus2011.de/>`_
- Einwohner nach
  `Regionalstatistik <https://www.regionalstatistik.de/genesis/online/>`_
- Wohngebäudetypologie nach
  `IWU <http://www.building-typology.eu/downloads/public/docs/brochure/DE_TABULA_TypologyBrochure_IWU.pdf>`_
- Temperaturen nach
  `DWD <https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/>`_

Die Wärmebedarfe für Gewerbe, Handel, Dienstleistungen und Landwirtschaft
wurden mit Hilfe folgender Daten gemeindescharf bestimmt:

- Bevölkerung und Erwerbstätigkeit nach
  `STALA <https://statistik.sachsen-anhalt.de/fileadmin/Bibliothek/Landesaemter/StaLa/startseite/Themen/Erwerbstaetigkeit/Berichte/6A606_j_2016.pdf>`_
- Energieverbrauch des Sektors GHD nach
  `BMWi <https://www.bmwi.de/Redaktion/DE/Publikationen/Studien/sondererhebung-zur-nutzung-erneuerbarer-energien-im-gdh-sektor-2011-2013.pdf?__blob=publicationFile&v=6>`_
- Arbeitsmarktstatistiken der
  `Bundesagentur für Arbeit <https://statistik.arbeitsagentur.de>`_
- Temperaturen nach
  `DWD <https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/>`_

Die Ergebnisse wurden in der Tabelle :class:`stemp_abw.models.MunData` abgelegt.

Einspeisezeitreihen
+++++++++++++++++++

1. Wetterdaten herunterladen und aufbereiten (hier
   `coastdat2 <http://dx.doi.org/10.1594/WDCC/coastDat-2_COSMO-CLM>`_).
   Verwendetes Wetterjahr: 2013 (in Region ABW ca. 100 % Globalstrahlung nach
   `DWD <https://www.dwd.de/DE/leistungen/solarenergie/lstrahlungskarten_ab.html>`_
   und 100 % Windenergieertrag nach
   `IEE <http://publica.fraunhofer.de/dokumente/N-283735.html>`_ im Vergleich
   zum langjährigen Mittel)
2. Zuordnung der Wetterzellen zu Gemeinden
3. Kennlinien von betrachteten Anlagentypen auswählen: Hier entsprechend der
   Marktanteile in Deutschland nach
   `IEE <http://windmonitor.iee.fraunhofer.de/opencms/export/sites/windmonitor/img/Windmonitor-2017/WERD_2017_180523_Web_96ppi.pdf>`_
   (2017): 63 % Enercon (E-82 mit 85 m und 98 m Nabenhöhe und E-115 mit 122 m
   Nabenhöhe) und 37 % Vestas (V90 mit 80 m und 100 m Nabenhöhe und V112 mit
   119 m Nabenhöhe). Für Zukunftsszenarien Enercon E-141 mit 159 m Nabenhöhe.
4. Erzeugung von normierten Zeitreihen (stündlich) pro Technologie und Gemeinde
   für den Status quo und Zukunftsszenerien (nur Wind)
5. Speichern in Tabelle :class:`stemp_abw.models.FeedinTs`.

Dieser Prozess wurde mit Hilfe von `reegis <https://github.com/reegis/reegis>`_
durchgeführt. Die normierten Zeitreihen werden anhand der EE-Kapazitäten (s.
EE-Kraftwerksdaten oben) im Tool ad hoc auf absolute Zeitreihen umgerechnet.

Verbrauchszeitreihen
++++++++++++++++++++

1. Voraussetzung: Verbrauchsdaten (s.o.)
2. Erzeugung von absoluten Verbrauchszeitreihen (stündlich) mit Hilfe von
   BDEW-Standardlastprofilen, hierbei wurden die Typen H0 für Haushalte, G0 für
   GHD und L0 für Landwirtschaft verwendet. Für industrielle Verbraucher wurde
   ein Stufenlastprofil angenommen.
3. Speichern in Tabelle :class:`stemp_abw.models.DemandTs`.

Schritt 2 wurde mit Hilfe der `demandlib <https://github.com/oemof/demandlib>`_
durchgeführt.

Flächen und Potenziale
......................

Details zur Ermittlung der Potenzialflächen für erneuerbare Energieanlagen
finden sie im Bereich :ref:`areas_and_potentials_label`.

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
   (Stand EE: Ende 2017, Stand konventionelle Kraftwerke: Ende 2018).
2. Zuordnung der Kraftwerke zu Gemeinden anhand der Koordinaten
3. Aggregation von Leistung und Anzahl nach Technologie und Gemeinde

Datentabelle Ergebnisse: :class:`stemp_abw.models.MunData`

Anmerkung: Für die räumliche Zuordnung auf Gemeindeebene ist die Genuigkeit
des OPSD-Datensatzes ausreichend, nicht jedoch für eine exakte
Geopositionierung. Hierfür sollte auf OSM-Daten oder zukünftig auf das
Marktstammdatenregister zurückgegriffen werden, s. :ref:`tool_transfer_label`.

Verbrauchsdaten Strom
+++++++++++++++++++++

1. Herunterladen des
   `Datensatzes zu Lastgebieten (Load Areas) <https://openenergy-platform.org/dataedit/view/demand/ego_dp_loadarea>`_,
   von der OpenEnergy Platform, welcher den jährlichen Verbrauch je
   OSM-Lastgebiet und Sektor enthält
   (`Paper zum Hintergrund <https://journals.aau.dk/index.php/sepm/article/download/1833/1531>`_).
2. Herunterladen des
   `Datensatzes zu industriellen Großverbrauchern (Large scale consumer) <https://openenergy-platform.org/dataedit/view/model_draft/ego_demand_hv_largescaleconsumer>`_,
   von der OpenEnergy Platform, welcher den jährlichen Verbrauch für große
   Industriegebiete enthält.
3. Zuordnung der Load Areas und Large scale consumer zu Gemeinden anhand der
   Koordinaten
4. Aggregation des Verbrauchs nach Sektor und Gemeinde

Die Datensätze in 1 und 2 wurden im Projekt open_eGo erstellt (Abschlussbericht
`hier <https://www.uni-flensburg.de/fileadmin/content/abteilungen/industrial/dokumente/downloads/veroeffentlichungen/forschungsergebnisse/20190426endbericht-openego-fkz0325881-final.pdf>`_
abrufbar).

Datentabelle Ergebnisse: :class:`stemp_abw.models.MunData`

Verbrauchsdaten Wärme
+++++++++++++++++++++

Die Wärmebedarfe von Haushalten wurden mit Hilfe folgender Daten und Studien
gemeindescharf bestimmt:

- Wohngebäudebestand (Alter, Größe, Wohneinheiten, Leerstand etc.) nach
  `Zensus 2011 <https://ergebnisse.zensus2011.de/>`_
- Einwohner nach
  `Regionalstatistik <https://www.regionalstatistik.de/genesis/online/>`_
- Wohngebäudetypologie nach
  `IWU <http://www.building-typology.eu/downloads/public/docs/brochure/DE_TABULA_TypologyBrochure_IWU.pdf>`_
- Temperaturen nach `DWD1`_

Die gemeindescharfen Wärmebedarfe für Gewerbe, Handel, Dienstleistungen und
Landwirtschaft basieren auf folgenden Studien und Daten:

- Bevölkerung und Erwerbstätigkeit nach
  `STALA1 <https://statistik.sachsen-anhalt.de/fileadmin/Bibliothek/Landesaemter/StaLa/startseite/Themen/Erwerbstaetigkeit/Berichte/6A606_j_2016.pdf>`_
- Energieverbrauch des Sektors GHD nach
  `BMWi <https://www.bmwi.de/Redaktion/DE/Publikationen/Studien/sondererhebung-zur-nutzung-erneuerbarer-energien-im-gdh-sektor-2011-2013.pdf?__blob=publicationFile&v=6>`_
- Arbeitsmarktstatistiken der
  `Bundesagentur für Arbeit <https://statistik.arbeitsagentur.de>`_
- Temperaturen nach `DWD1`_

Datentabelle Ergebnisse: :class:`stemp_abw.models.MunData`

Einspeisezeitreihen
+++++++++++++++++++

Verwendetes Wetterjahr: 2013 (in Region ABW ca. 100 % Globalstrahlung nach
`DWD2 <https://www.dwd.de/DE/leistungen/solarenergie/lstrahlungskarten_ab.html>`_
und 100 % Windenergieertrag nach
`IEE1 <http://publica.fraunhofer.de/dokumente/N-283735.html>`_ im Vergleich zum
langjährigen Mittel)

**Windenergie**

1. Wetterdaten herunterladen und aufbereiten (hier
   `coastdat2 <http://dx.doi.org/10.1594/WDCC/coastDat-2_COSMO-CLM>`_).
2. Zuordnung der Gemeinden zu Zellen des Wettermodells
3. Kennlinien von betrachteten Anlagentypen auswählen: Hier entsprechend der
   Marktanteile in Deutschland nach
   `IEE2 <http://windmonitor.iee.fraunhofer.de/opencms/export/sites/windmonitor/img/Windmonitor-2017/WERD_2017_180523_Web_96ppi.pdf>`_
   (2017):

   - 40 % Enercon (E-82 mit 85 m und 98 m Nabenhöhe und E-115 mit 122 m
     Nabenhöhe) und 24 % Vestas (V90 mit 80 m und 100 m Nabenhöhe und V112 mit
     119 m Nabenhöhe), hochskaliert auf 100 %: Enercon 63 %, Vestas 37 %.
   - Die einzelnen Anlagentypen wurden anhand des Anlagenbestandes
     (Kraftwerksdaten wie oben beschrieben) vereinfacht in 2 Klassen <2,5 MW
     (87 %) und >2,5 MW (13 %) sortiert und die o.g. 6 Typen entsprechend
     gewichtet.
   - Für Zukunftsszenarien: Enercon E-141 mit 159 m Nabenhöhe verwendet

4. Erzeugung von normierten Zeitreihen (stündlich) pro Technologie und Gemeinde
   für a) Status quo und b) Zukunftsszenerien.
5. Erhöhung der Repräsentativität durch Skalierung der Status-quo-Zeitreihen
   auf langjähriges Mittel der Jahresvolllaststunden von Sachsen-Anhalt anhand
   von Erhebungen der
   `AEE1 <https://www.foederal-erneuerbar.de/landesinfo/bundesland/ST/kategorie/wind/auswahl/811-durchschnittliche_ja/#goto_811>`_
   (2011-2015: 1630 h).

Dieser Prozess wurde mit Hilfe von `reegis <https://github.com/reegis/reegis>`_
automatisiert durchgeführt.

**Photovoltaik**

1. Normierte Einspeisezeitreihen herunterladen von
   `renewables.ninja <https://www.renewables.ninja/>`_ (Wetterdatensatz:
   CM-SAF SARAH)
2. Anlagen-Setting:

   - 20 % Systemverluste nach
     `ISE <https://www.ise.fraunhofer.de/content/dam/ise/de/documents/publications/studies/aktuelle-fakten-zur-photovoltaik-in-deutschland.pdf>`_
   - Tilt: 45° (Dach), 35° (Freifläche/Flachdach, optimale Ausrichtung für DE)
   - Azimut: 180°, Berücksichtigung verschiedener Ausrichtungen auf Dächern
     durch nachträgliche Ertragskorrektur mit Minderungsfaktor von 0,85 nach
     `FfE <https://www.ffe.de/download/article/464/Dissertation_Roger_Corradini.pdf>`_.

3. Korrektur der Zeitreihen anhand der mittleren Jahresvolllaststunden nach
   `AEE2 <https://www.foederal-erneuerbar.de/landesinfo/bundesland/ST/kategorie/solar/auswahl/813-durchschnittliche_ja/#goto_813>`_,
   für Sachsen-Anhalt (2011-2015: 998 h), da mit Wetterdatensatz CM-SAF SARAH
   produzierte Einspeisung tendenziell zu niedrig ist
   (`Pfenninger et al. <https://dx.doi.org/10.1016/j.energy.2016.08.060>`_):

   - Aus Kraftwersdaten folgt: Anteil Dachanlagen an Gesamtleistung: 20%,
     Anteil Freiflächenanlagen an Gesamtleistung: 80%
   - Anhand dieser Gewichtung werden die Zeitreihen skaliert, sodass beim
     aktuellen Bestand für alle 20 Gemeinden die mittlere Vollaststundenzahl
     (s.o.) von 998 h erreicht werden.
   - Vernachlässigt: Modul- und Wechselrichterkonfiguration, Flach- und
     Fassadenbauweise, Degradation, Tracking, variabler Airmass-Faktor

4. Erzeugung von normierten Zeitreihen (stündlich) pro Typ (Dach, Freifläche)
   und Gemeinde, die sowohl für den Status quo als auch Zukunftsszenerien
   verwendet werden.

**Laufwasserkraft**

1. Es wird eine konstante Einspeiseleistung über das gesamte Jahr an allen
   Anlagen angenommen.
2. Erzeugung konstante, normierte Zeitreihe mit mittlerer
   Jahresvolllaststundenzahl in Sachsen-Anhalt nach
   `STALA2 <https://statistik.sachsen-anhalt.de/themen/wirtschaftsbereiche/energie/tabellen-energie-und-wasserversorgung/>`_
   (2012-2017: 3833 h).

**Konventionelle Kraftwerke**

Unterteilung in 2 Klassen nach Netto-Stromerzeugungsleistung:

- **>=10 Megawatt:**
  2 Erdgaskraftwerke (106 MW, 40 MW), 1 Braunkohlekraftwerk (49 MW). Es wird
  eine stromgeführte Betriebsweise mit konstanter Einspeiseleistung angenommen
  mit typischen Werten für die Jahresvolllaststunden:

  - Erdgaskraftwerk (Turbine): 1250 h/a
  - Erdgaskraftwerk (GuD): 2900 h/a
  - Braunkohlekraftwerk: 7000 h/a

- **<10 Megawatt:**
  Hierzu zählen 21 Anlagen im Leistungsbereich von 750 kW bis 9,9 MW. Es
  werden eine wärmegeführte Betriebsweise und 5000 Jahresvolllaststunden
  angenommen.

Datentabelle Ergebnisse: :class:`stemp_abw.models.FeedinTs`

Die normierten Zeitreihen werden beim Start des Tools geladen und anhand der
eingestellten EE-Kapazitäten ad hoc auf absolute Zeitreihen skaliert (s.
:func:`stemp_abw.simulation.esys.prepare_feedin_timeseries()`).

Verbrauchszeitreihen Strom
++++++++++++++++++++++++++

1. Voraussetzung: Verbrauchsdaten (s.o.)
2. Erzeugung von absoluten Verbrauchszeitreihen (stündlich) mit Hilfe von
   BDEW-Standardlastprofilen, hierbei wurden die Typen H0 für Haushalte, G0 für
   GHD und L0 für Landwirtschaft verwendet. Für industrielle Verbraucher wurde
   ein Stufenlastprofil angenommen.

Datentabelle Ergebnisse: :class:`stemp_abw.models.DemandTs`

Schritt 2 wurde mit Hilfe der `demandlib <https://github.com/oemof/demandlib>`_
durchgeführt.

Die Zeitreihen werden beim Start des Tools geladen und entsprechend den
Tool-Einstellungen im Bereich Verbrauch skaliert (s.
:func:`stemp_abw.simulation.esys.prepare_demand_timeseries()`).

Flächen und Potenziale
......................

Details zur Ermittlung der Potenzialflächen für erneuerbare Energieanlagen
finden sie im Bereich :ref:`areas_and_potentials_label`.

.. _`DWD1`: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/

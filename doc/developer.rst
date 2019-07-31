.. _developer_label:

Für EntwicklerInnen
===================

Der Quellcode ist auf `GitHub
<https://github.com/rl-institut/WAM_APP_stemp_abw>`_ verfügbar und es existiert
ein Python-Paket auf PyPI <INSERT LINK> (Details zur Installation siehe
:ref:`install_label`).

Technologien
------------

Django-Kosmos
-------------

Diese StEmp-Web-Applikation ist Teil des WAM-Applikationen-Kosmos_ des
Reiner Lemoine Instituts (RLI). Die Bezeichnung WAM steht hierbei für
*Web Applications and Maps* und stellt eine Kategorie von Applikationen dar,
welche am RLI erstellt werden. Dies sind hauptsächlich Web-Applikationen,
die mit Hilfe von Karten arbeiten und oder bei denen im Hintergrund Berechnungen
stattfinden, dessen Ergebnis an die NutzerInnen visuell zurückgegeben wird.
Einige der WAM-Applikationen sind mit dem RLI-eigenen Web-Applikationen-Framework
mit dem Namen WAM_ erstellt worden, andere WAM-Applikationen basieren auf anderen
Frameworks oder sind freie Implementationen ohne Framework-Basis.

Diese StEmp-Web-Applikation des RLI nutzt das Git-Projekt WAM_ als Basis-Projekt.
Das verwendete WAM-Basis-Projekt baut auf dem Django_-Web-Framework auf,
welches Python als Programmiersprache verwendet. Django hat eine gewisse
Lernkurve, deswegen kann es Sinn machen, sich bei Bedarf zuerst mit dem
zugrunde liegenden Web-Framework Django zu beschäftigen, bevor mit der Arbeit
an einer auf Django basierenden WAM-Applikation begonnen wird. Für das Erlernen
des Umgangs mit Django gibt es sehr viel Lernmaterial Dritter, weswegen im
Folgenden in dieser Dokumentation auf einige dieser Anleitungen und
Dokumentationen zum Erlernen von Django verwiesen werden soll. Anschließend
wird im nächsten Abschnitt auf der auf Django basierenden WAM-Projektbasis
eingegangen.

Tutorials und Informationen zu Django:

- Das Django `getting started Tutorial`_
- Tutorial_ einer einfachen Geo-Applikation in Django
- Die offizielle Django-Dokumentation_
- Die Django-Design-Philosophie_

WAM-Kosmos
----------

Wie im vorherigen Abschnitt *Django-Kosmos* bereits kurz angesprochen, verwendet
dieses Projekt das RLI eigene Web-Applikationen-Framework WAM_.
Das WAM-Framework nutzt hierfür Django also Unterbau. Der Django-Unterbau ist
dahingehend umgearbeitet, dass er besonders gut auf die Bedürfnisse für die
Entwicklung von Applikationen am RLI zugeschnitten ist und er sich von Projekt
zu Projekt als Projektbasis wiederverwenden lässt. Im Folgenden soll deshalb
kurz auf das WAM-Framework eingegangen werden.

Das WAM-Framework setzt mehrere zugrundlegende Prinzipien konsequent um:

- die initiale Konfigurationsarbeit für auf der WAM basierende Web-Applikationen
  soll minimiert und wenn möglich automatisiert werden.
- das Zusammenfassen von häufig benötigten Funktionalitäten und die Integration
  dieser Funktionalitäten in die WAM-Projektbasis, für die einfache Verwendung
  von auf der WAM basierenden Web-Applikationen.
- eine gemeinsame Projektbasis in der multiple Applikationen angedockt sind
  minimieren den Wartungsaufwand des Gesamtsystems zur Laufzeit.

Der Grund für die Umsetzung dieser Prinzipien ist die Minimierung von Aufwänden
bei der Erstellung und dem Betrieb von Web-Applikationen, welche am RLI und
Allgemein im Bereich der Erneuerbaren-Energien-Forschung und -Entwicklung
benötigt werden. Durch diese Herangehensweise profitieren bereits die beiden
(stemp_abw_, stemp_mv_) im Rahmen des ENavi-Projektes vom RLI entwickelten
StEmp-Tools, welche beide das WAM_-Framework als Unterbau nutzen.

Für die Sichtbarmachung von Aufbau und Nutzung des WAM-Frameworks gibt es eine
eigenständige WAM-Dokumentation_, welche weiterführende Informationen enthält.

Tool-Struktur
-------------

In den vorherigen Abschnitten wurde die Pfadabhängigkeit dieses Projektes, mit
dem Django-Framework und dem darauf aufbauenden WAM-Framework herausgearbeitet.
An dieser Stelle soll nun auf die eigentliche Struktur dieses Projektes
eingegangen werden. Dies setzt unter anderem Kenntnisse des Django_-Frameworks
und des WAM_-Frameworks voraus. Es kann deshalb Sinn machen, erst nach einer
Einarbeitung in Django und WAM sich diesem Abschnitt verstärkt zu widmen, falls
die Voraussetzungen zum Zeitpunkt des ersten Lesens noch nicht in ausreichender
Tiefe vorhanden sind.

Zuerst soll in diesem Abschnitt kurz daran erinnert werden, dass die WAM als
Projektbasis dient und das auf der WAM aufbauende Applikationen im Ordner der
WAM-Projekbasis zu finden sind. Das bedeutet, dass die WAM-Projektbasis der
Gastgeber (Host) von multiplen WAM-Applikationen sein kann. Somit kann auf jeder
WAM-Instanz ein bis viele WAM-Applikationen laufen. Diese Logik folgt der
Logik von Django, also der Trennung von Projektbasis und Applikationen, welche
auf dieser Projektbasis laufen. Eine WAM-Applikation, kann dabei auf zwei Arten
in eine WAM-Projektbasis integriert werden:

- eine WAM-Applikation wird von Grund auf neu angelegt. Dies erfolgt mit den
  Bordmitteln von Django (Stichwort: :code:`python manage.py startapp appname`).
- eine WAM-Applikation wird von einer bestehenden WAM-Applikation abgeleitet und
  in dem WAM-Projektbasis-Ordner manuell angelegt.

In beiden Fällen muss die neu zu erstellende Applikation konfiguriert und mit
der WAM-Projektbasis verknüpft werden. Weitergehende Infos zur Installation und
Inbetriebnahme einer neuen WAM-Applikation finden sich in der
WAM-Dokumentation_. In dieser Dokumentation soll deswegen vielmehr auf die
konkrete Struktur dieses Projektes eingegangen werden, um EntwicklerInnen an die
konkrete Codebasis heranzuführen. Die Strukturbetrachtung findet hierbei aus
verschiedenen Blickwinkeln statt, um die Komplexität des Projektes besser
durchdringen zu können.

In einer ersten groben Betrachtung widmet sich dieses Dokument im Folgenden der
Ordnerstruktur des Projektes::

    .
    ├── config
    ├── dataio
    ├── doc
    ├── migrations
    ├── results
    ├── simulation
    ├── static
    ├── templates
    ├── views
    └── visualizations

Im Rootordner "." finden sich die für Django typischen Dateien, darunter sind
aber auch einige Dateien, welche projektspezifischer Natur sind. Unter den
projektspezifischen Dateien sind queries.py (welches Hilfsfunktionen
für wiederkehrende Prozesse enthält) und sessions.py (in der User-Sessions
gehandhabt werden) hervorzuheben.

Bei den Ordnern (Modulen) verhält es sich ähnlich. Einige sind typisch für Django
(doc, migrations, static, templates, views), andere spezifisch für dieses Projekt
(config, dataio, results, simulation, visualizations). Im Folgenden soll
ausschließlich auf die projektspezifischen Module kurz eingegangen werden:

- `config:` Konfigurationsmodul, in dem Layer-, Label- und Kartenparameter definiert werden.

- `dataio:` Modul, in dem das Laden von statischen Daten gehandhabt wird.

- `results:` Modul, in dem die Resultate der Simulation behandelt werden.

- `simulation:` Modul, in dem die Simulation mit der Energiesystemmodellierungsframework oemof_ realisiert wird.

- `visualizations:` In diesem Modul befindet sich der Python-Wrapper für die JS-Chartsbibliothek.

Nach diesem kurzen strukturellen Überblick folgt nun ein funktionaler Überblick
der wichtigsten Komponenten des Projektes. Eine komplette Beschreibung aller
Schnittstellen findet sich im Kapitel API_ dieser Dokumentation.

Zusammenspiel UI und Backend
----------------------------

Infos/Diagramme z.B. zu

- Verbindung UI-Django-oemof..
  POST (fired by :meth:`stemp_abw.views.MapView.post`)
- Datenflüsse
- ???

[HIER GEHIRNSCHMALZ EINFÜGEN]

User Session
------------

- Wofür?
- Cookie (stored data)
- Initialisierung (fired by :meth:`stemp_abw.views.MapView.get`)

.. graphviz::

   digraph {
      "start" -> "set default user scenario" ->
      "init simulation" -> "set aggregation ratios" ->
      "init tracker" -> "end";

      "start" [color=red]
      "set default user scenario" [shape=polygon,sides=4]
      "init simulation" [shape=polygon,sides=4]
      "set aggregation ratios" [shape=polygon,sides=4]
      "init tracker" [shape=polygon,sides=4]
      "end" [color=green]
   }

- Verfall
- Verknüpfte Daten (scenario, data, results, ...)

(use refs to APIdoc)

.. _developer_geo_layers_label:

Geo-Ebenen (Layer)
------------------

Ebenen mit räumlichen Informationen werden an 4 Stellen im Tool verwendet:

1. Regions-Informationen (Panel "Region")
2. Statische Flächen (Panel "Flächen" -> "Statische Flächen")
3. Weißflächen (Panel "Flächen" -> "Variierbare Flächen")
4. Ergebnisse (Panel "Ergebnisse")

TBD:

- Wo liegen Daten in welchem Format und CRS/SRID?
- Wo liegen die Metainformationen & Styles zu den Ebenen?
- Welche Datenstrukturen sind wichtig? (Serial-/GeoJSONLayerView, DetailView)
- Wie werden Ebenen geladen und aktiviert?
- Wie werden die Endpunkte bereitgestellt (urls.py)?
- Wie kann ich einen neuen Layer hinzufügen?

Hinzufügen eines neuen Layers
.............................

Wenn ein neuer Layer hinzugefügt werden soll, dann muss an sechs Stellen Code
hinzugefügt und eine Migration (neues Modell) durchgeführt
werden. Die sechs Stellen sind:

- models.py
- config/labels.cfg
- config/layers_<Panelname>.cfg
- templates/stemp_abw/popups/<Templatename-des-Popups>.html
- views/detail_views.py
- views/serial_views.py

Als Referenz für die Implementation von weiteren Layern, können folgende drei
Commits exemplarisch herangezogen werden:

- `Add layer for reg_mun_gen_count_wind_density_result #38`_
- `Add layer for reg_mun_gen_cap_re_density_result #38`_
- `Add layer for reg_mun_gen_cap_re_result #38`_

Wie sich aus den Commits entnehmen lässt folgt das Hinzufügen von weiteren
Layern einem definierten Ablauf, welcher die Layer automatisch in das
gewählte Panel hinzufügt, ohne das hierfür der HTML-Code des Panels angefasst
werden muss. In den folgenden Abschnitten soll auf die einzelnen Schritte
vertiefend eingegangen werden, indem exemplarisch auf die Erstellung eines Layers
eingegangen wird.

Erstellung eines neuen Modells in `models.py`
.............................................

Die Basis eines jeden neuen Layers ist ein Modell, aus dem der Layer seine Daten speist.
Bei den Modellen handelt es sich um den bekannten `Modellmechanismus aus Django`_.
In diesem Projekt werden mit zwei Arten von Modellen gearbeitet:

- Modelle, welche mit einer Datenbanktabelle (via ORM-Mechanismus) korrespondieren
- Proxymodelle, welche von anderen Modellen erben und nicht direkt mit einer eigenen Datenbanktabelle korrespondieren, sondern mit den Datenbanktabellen der vererbten Modelle

In beiden Modellarten können über den `@property`-Dekorator weitere Eigenschaften
definiert werden. In diesem Projekt ist dies z.B. in den Proxymodellen der Fall,
hier werden neue Werte mit Hilfe der arithmetischen Grundrechenarten aus bestehenden
Werten ermittelt und zurückgegeben.

Im Folgenden zwei Beispiele für das Modell `RegMun`_ und dem davon erbenden
Proxymodell `RegMunDemElEnergy`_:

-  Klassendefinition des `RegMun`-Modells, mit Datenbanktabelle `stemp_abw_regmun`::

    class RegMun(LayerModel):
        name = 'reg_mun'
        ags = models.IntegerField(primary_key=True)
        geom = geomodels.MultiPolygonField(srid=3035)
        geom_centroid = geomodels.PointField(srid=3035, null=True)
        gen = models.CharField(max_length=254)

Jedes Modell hat mindestens zwei definierte Eigenschaften `name` und `geom`.
Mit der Eigenschaft `name` wird der Name definiert, welcher im Konfigurationsmodell
(`config/`) Verwendung findet. Für die Benennung und Verwendung der Datenbanktabelle wiederum
wird der Appname (`stemp_abw`) mit dem Klassennamen (`RegMun`) zu einem eindeutigen
Tabellennamen von Django automatisiert verbunden (`stemp_abw_regmun`). Somit ist
Obacht geboten, denn wir haben an zwei Stellen die Vergabe von Namensräumen für
dasselbe Modell, einmal automatisiert für die Handhabung der Daten und einmal
manuell für die automatisierte Konfiguration und Verwendung des Modells in einem
Layer. Mit der Eigenschaft `geom` wird die Geometrie des Layers mit dem Modell verknüpft.
Alle weiteren Eigenschaften sind optional.

- Klassendefinition des `RegMunGenEnergyRe`-Proxymodells, ohne eigene Datenbanktabelle::

    class RegMunDemElEnergy(RegMun):
        name = 'reg_mun_dem_el_energy'

        class Meta:
            proxy = True

        @property
        def dem_el_energy(self):
            return round((self.mundata.dem_el_energy_hh +
                          self.mundata.dem_el_energy_rca +
                          self.mundata.dem_el_energy_ind) / 1e3)

        @property
        def dem_el_energy_region(self):
            result = MunData.objects.aggregate(Sum('dem_el_energy_hh'))['dem_el_energy_hh__sum'] + \
                     MunData.objects.aggregate(Sum('dem_el_energy_rca'))['dem_el_energy_rca__sum'] + \
                     MunData.objects.aggregate(Sum('dem_el_energy_ind'))['dem_el_energy_ind__sum']
            return round(result / 1e3)

In jedem  Proxymodell wird ein eigener Name (`name`) als Eigenschaft vergeben,
die Geometrie (`geom`) wird in der Regel geerbt. Das Proxymodell wird über
`class Meta` als Proxyklasse gekennzeichnet. Weitere Schritte, für die Kennzeichnung
eines Modells als Proxymodell, sind nicht nötig. An dem Beispiel von `RegMunGenEnergyRe`
lässt sich die bereits erwähnte Verwendung des `@property`-Dekorators exemplarisch
in den Methodendefinitionen von `dem_el_energy` und `dem_el_energy_region` alesen.

Nach der Erstellung eines oder mehrerer Modelle, sollte eine Datenbankmigration
mit `python manage.py makemigrations` und `python manage.py migrate` durchgeführt
werden, falls dies nötig ist. Der Befehl `python manage.py makemigrations` gibt
Aufschluss darüber.

Die Registrierung und automatische Erstellung des Layers in einem Panel
.......................................................................

Dieses Projekt verfügt über die Möglichkeit einen neuen Layer automatisiert
einem bestimmten Panel hinzuzufügen. Dies wird durch die Definition des Layers
in zwei Konfigurationsdateien ermöglicht:

- config/labels.cfg
- config/layers_<Panelname>.cfg

In `config/labels.cfg` wird hierbei das zu verwendende Panel, die Bezeichnung des
Layers im Panel (`title`) und die (Tooltip-)Beschreibung des Layers im Panel
(`text`) definiert. Eine vertiefende  Beschreibung der Datenstruktur und ihrer
Verwendung kann dem Dateikommentar_ in `config/labels.cfg` entnommen werden.

In `config/layers_<Panelname>.cfg` wird der Layer anhand des Modell konfiguriert und
das Aussehen definiert. Im Folgenden eine generelle Übersicht::

    Format:
    [<GROUP_ID>]
        [[<LAYER_ID>]]
             model = <DATA MODEL NAME (property 'name' of model)>
             geom_type = <TYPE OF GEOMETRY (line, point, poly)>
             show = <SHOW LAYER ON STARTUP (0/1)>
             sources = <COMMA-SEPARATED SOURCES ID(s) (PK from database)>, (0 = no source)
             [[[style]]]
                 <CSS STYLE OPTIONS>
             [[[accuracy]]]
                 <ACCURACY OF LAYER DISPLAY -> GEOJSON PARAMS>
             [[[choropleth]]]
                 unit = <LEGEND TITLE>
                 data_column = <MODEL PROPERTY USED AS DATA>
                 color_schema = <COLORBREWER COLOR SCHEMA>
                 min = <MIN VALUE FOR COLOR AND LEGEND (int or float)>
                 max = <MAX VALUE FOR COLOR AND LEGEND (int or float)>
                 step = <STEP SIZE FOR COLOR AND LEGEND (int or float)>
                 reverse = <REVERSE COLOR SCHEMA (true/false)>

Anhand des konkreten Beispiels von `RegMunDemElEnergy in config/layers_region.cfg`_
soll an dieser Stelle exemplarisch auf die Konfiguration eines Layers eingegangen werden,
welcher im Panel `Region` Verwendung findet::

    [layer_grp_demand]
        [[reg_mun_dem_el_energy]]
            model = reg_mun_dem_el_energy
            geom_type = poly
            show = 0
            sources = 0
            [[[style]]]
                fillColor = '#41b6c4'
                weight = 1
                opacity = 1
                color = gray
                fillOpacity = 0.7
            [[[accuracy]]]
                precision = 5
                simplify = 0
            [[[choropleth]]]
                unit = 'GWh'
                data_column = dem_el_energy
                color_schema = YlGnBu
                min = 0
                max = 500
                step = 50
                reverse = false

`[layer_grp_demand]`: jedes Panel besteht aus Layergruppen. Die Bezeichnung und
die Beschreibung einer Layergruppe wird, wie bei den Layern, in `config/labels.cfg`
definiert. Der Layergruppenname wird je Layergruppe nur einmal angegeben.

`[[reg_mun_dem_el_energy]]`: der Name des Layers.

`model = reg_mun_dem_el_energy`: der Modellname (`name`) des Layers aus der Modelldefinition.

`geom_type = poly`: der Geometrietyp des Layers. Es stehen `line`, `point`, `poly` zur Verfügung.

`show = 0`: fragt ab, ob der Layer beim Start der Applikation sichtbar sein soll.
In der Regel wird hier 0 angegeben. Mögliche Werte: 0 oder 1 (false|true).

`sources = 0`: jedem Layer kann auf bestimmte Quellen zu den Daten verweisen,
welche im Gesamten über die URL `<Hostname>/stemp_abw/sources/` im Browser zugänglich sind.
Die Quellen werden im Backend (`<Hostname>/admin/`) angelegt. Es können pro Layer
mehrere Quellen verwendet werden (`1, 2, 3, ... n`). Die Angabe erfolgt kommagetrennt
und entspricht dem Primärschlüssel (PK) der jeweiligen Quelle in der Datenbank.
In unserem Beispiel wird keine Quelle angegeben (deswegen der Wert 0).

`[[[style]]]`: in diesem Abschnitt wird das grundlegende Styling eines Layers
definiert.

`fillColor = '#41b6c4'`: der Parameter `fillColor` definiert die Grundfarbe des
Layers und nimmt als Wert alle Werte entgegen, welche vom CSS `color`-Attribut
entgegen genommen werden können (z.B. Hexadezimalwerte und sprechende Bezeichnungen).

`weight = 1?`: der Parameter `weight` definiert die Randstärke eines Layers.
Ein Wert von 10 steht hierbei beispielsweise für eine Randstärke von 10 Pixeln.
In der Regel steht der Wert bei 1.

`opacity = 1`: der Transparenzwert des Randes eines Layers. Bei dem Wert
handelt es sich um einen Dezimalwert von 0 bis 1. Dieser Wert ist in der Regel 1.

`color = gray`: mit dem Parameter `color` wird die Farbe des Randes definiert.
Dieser Wert ist in der Regel grau (`gray`).

`fillOpacity = 0.7`: der Transparenzwert eines Layers. Bei dem Wert
handelt es sich um einen Dezimalwert von 0 bis 1. Dieser Wert liegt in der Regel
bei 0.7, damit der Layer teildurchsichtig ist.

`[[[accuracy]]]`: in diesem Abschnitt wird die Genauigkeit definiert, mit der
die Geometriedaten eines Layers angezeigt werden sollen.

`precision = 5`: der Parameter `precision` wird als Ganzzahl angegeben und definiert
die Anzahl von Nachkommastellen, welche bei den Geometriewerten eines Layers
berücksichtigt werden sollen. Dieser Wert ist in der Regel 5. Der Parameter
`precision` spiegelt hierbei das Verhalten des Attributes `precision aus der Django GEOS API`_,
welcher in diesem Projekt als Unterbau Verwendung findet.

`simplify = 0`: der Parameter `simplify` definiert inwieweit die Geometrie
eines Layers vereinfacht werden soll. Weil dieser Prozess rechenintensiv
ist wird er in der Regel in diesem Projekt nicht verwendet und deswegen
der Wert auf 0 gesetzt. Der Parameter `simplify` spiegelt hierbei das Verhalten
des Attributes `simplify aus der Django GEOS API`_, welcher in diesem Projekt
als Unterbau Verwendung findet.

`[[[choropleth]]]`: in diesem Abschnitt wird, falls es sich bei dem Layer
um eine `Choroplethkarte`_ handelt, diese definiert. Jede Choroplethkarte
hat zusätzlich noch rechts unten eine Legende, welche eine Farbskala mit ihren
Werten beschreibt.

`unit = 'GWh'`: Einheit, welche in der Legende als Maßeinheit verwendet wird.
Der Wert wird als String angegeben.

`data_column = dem_el_energy`: Der Parameter `data_column` enthält den
`property`-Wert, welcher als Wert in der Choroplethkarte auf Gemeindeebene
Verwendung finden soll. Der `property`-Wert wird zwar im Modell definiert,
aber in `views/serial_views.py` für die Verwendung im Layer explizit ausgewiesen.

`color_schema = YlGnBu`: Der Parameter `color_schema` definiert das Farbschema,
welches in der jeweiligen Choroplethkarte Verwendung findet. Mögliche Werte
richten sich nach den von Cynthia Brewer entwickelten Farbschemata. Mit dem
von Frau Brewer entwickelten Online-Tool `colorbrewer2.org`_ lassen sich die
passenden Farbschemata und ihre Bezeichnungen ermitteln. Um diese Funktionalität
zur Verfügung zu stellen, verwendet dieses Projekt die JavaScript-Farbbibliothek
`Chroma.js`_ als Unterbau.

`min = 0`: der Parameter `min` definiert einen Minimalwert für die Choroplethkarte.
Dieser Minimalwert sollte sich am Minimalwert aller Werte aus `data_column` orientieren.

`max = 500`: der Parameter `max` definiert einen Maximalwert für die Choroplethkarte.
Dieser Maximalwert sollte sich am Maximalwert aller Werte aus `data_column` orientieren.

`step = 50`: der Parameter `step` definiert die Schrittgröße einer Farbabstufung
einer Choropletkarte. Hierbei sollten sinnvolle Werte verwendet werden, welche
mehrfach in das Intervall von Maximalwert minus Minimalwert passen. In unserem
Beispiel hat das Intervall eine Länge von 500, eine Schrittgröße von 50 und somit
zehn Farbabstufungen in der Choroplethkarte.

`reverse = false`: der Parameter `reverse` definiert, ob das verwendet Farbschema
gedreht werden soll. Mögliche Werte sind hierbei `false` (nein) und `true` (ja).
Ein Farbschema das z.B. bei dem Minimalwert blau und beim Maximalwert rot ist, wird
durch den Wert `true` vertauscht, so dass der Minimalwert rot und
der Maximalwert blau ist.

Die Verwendung von angepassten Popup-Fenstern in Layern
.......................................................

In jedem Layer können Popup-Fenster verwendet werden, welche die einzelnen
Elemente eines Layers genauer beschreiben. In diesen Popup-Fenstern können
des Weiteren Charts verwendet werden, welche sich aus den Layerdaten speisen.

Standardmäßig ist ein Standard-Popup definiert, welcher Verwendung findet.
Dieser kann angepasst werden, indem ein eigenes Popup-Template verwendet wird.
Hierbei wird der von Django zur Verfügung gestellte Templatemechanimus_
verwendet, um das Standard-Popup zu erweitern.

Die Templates der Popups befinden sich im Ordner `templates/stemp_abw/popups/`.
Falls für einen neuen Layer ein angepasstes Popup erstellt werden soll, bietet
es sich an, eine bestehendes Popup-Template als Vorlage zu verwenden.

Im Folgenden soll exemplarisch auf das Popup-Template von `RegMunGenEnergyRe`_
eingegangen werden::

    {% extends 'stemp_abw/popups/base_layer_popup.html' %}

    {% block gen %}
      <div class="cell">
        <p>{{ layer.gen }}: {{ layer.gen_energy_re }} GWh</p>
      </div>
      <div>
        Region ABW: {{ layer.gen_energy_re_region }} GWh
      </div>
    {% endblock %}

    {% block vis %}
    <div class="cell" style="height: 252px;">
      {{ chart }}
    </div>
    {% endblock%}

Im ersten Abschnitt "{% extends ..." wird vom Basis-Popup geerbt.

Im Block `gen` werden Angaben zur erzeugten Energie "layer.gen_energy_re" der
Gemeinde "layer.gen" im Verhältnis zum Gesamtgebiet von ABW
"layer.gen_energy_re_region" gemacht.

Im Block `vis` wird ein Chart (`chart`) eingebunden, welcher in der Detailview in
`views/detail_views.py` definiert wird.

Die Erstellung der Detailansicht
................................

Alle Detailansichten finden sich in `views/detail_views.py`. In der Detailansicht
werden Modell und Template verbunden, damit das passende Popup bei einem Klick
auf eine Element in einem bestimmten Layer angezeigt wird.

`Einfache Detailansichten`_ enthalten nur die Werte für das zu verwendende
Modell (`model`) und das zugrunde liegende Template (`template_name`).

`Komplexere Detailansichten`_ enthalten darüber hinaus auch Methoden für die Übergabe
des Django `context`_ (`get_context_data`) und die Erstellung eines Charts (`build_chart`),
welcher mittels `{{ chart }}`-Tag im Template Verwendung findet.

Die Definition der zu serialisierenden Daten
............................................

Die Daten einer jeden Ansicht werden serialisiert und an einem bestimmten Endpunkt
zur Verfügung gestellt, damit von der Applikation via AJAX-Abruf darauf zugegriffen
werden kann.

Im Folgenden soll hierbei exemplarisch auf die `Serialisierungsansicht von RegMunGenEnergyRe`_
eingegangen werden::

    class RegMunGenEnergyReData(GeoJSONLayerView):
        model = models.RegMunGenEnergyRe
        properties = [
            'name',
            'gen',
            'gen_energy_re',
            'gen_energy_re_region'
        ]

Als erstes wird das Modell (`model`) definiert, welches Verwendung finden soll.

In einem zweiten Schritt werden alle `properties` aus dem Modell definiert,
welche serialisiert werden sollen, um an dem Endpunkt zur Verfügung zu stehen.

Bei den Layern der Gemeinden orientieren sich die Endpunkte an den `Amtlichen
Gemeindeschlüsseln`_ (AGS). Die Endpunkte bei der Gemeinde Dessau mit dem
AGS-Wert 15001000 sind somit::

    stemp_abw/popup/reg_mun_gen_energy_re/15001000/
    stemp_abw/popupjs/reg_mun_gen_energy_re/15001000/

Unter `stemp_abw/popup/` finden sich hierbei die menschenlesbaren Daten für das
Popup und unter `stemp_abw/popupjs/` befinden sich Daten, wenn ein Chart in einem Popup
Verwendung findet.


Energiesystem
-------------

- Wo werden die Komponenten definiert?

.. _developer_scenarios_label:

Szenarien
---------

- Wo werden die Szenarien definiert?
- Wie kann ich ein neues Szenario anlegen?

.. _developer_help_texts_label:

Hilfetexte
----------

- Wo liegen die Hilfetexte (Tooltips)?
- Wie werden diese eingebunden?

.. _`Amtlichen Gemeindeschlüsseln`: https://de.wikipedia.org/wiki/Amtlicher_Gemeindeschl%C3%BCssel
.. _`Serialisierungsansicht von RegMunGenEnergyRe`: https://github.com/rl-institut/WAM_APP_stemp_abw/blob/dev/views/serial_views.py#L60-L67
.. _`context`: https://docs.djangoproject.com/en/2.2/ref/templates/api/#rendering-a-context
.. _`Komplexere Detailansichten`: https://github.com/rl-institut/WAM_APP_stemp_abw/blob/dev/views/detail_views.py#L177-L225
.. _`Einfache Detailansichten`: https://github.com/rl-institut/WAM_APP_stemp_abw/blob/dev/views/detail_views.py#L434-L436
.. _`RegMunGenEnergyRe`: https://github.com/rl-institut/WAM_APP_stemp_abw/blob/dev/templates/stemp_abw/popups/gen_energy_re.html
.. _Templatemechanimus: https://docs.djangoproject.com/en/2.2/topics/templates/
.. _`Chroma.js`: https://github.com/gka/chroma.js/
.. _`colorbrewer2.org`: http://colorbrewer2.org
.. _`Choroplethkarte`: https://de.wikipedia.org/wiki/Choroplethenkarte
.. _`simplify aus der Django GEOS API`: https://docs.djangoproject.com/en/2.2/ref/contrib/gis/geos/#django.contrib.gis.geos.GEOSGeometry.simplify
.. _`precision aus der Django GEOS API`: https://docs.djangoproject.com/en/2.2/ref/contrib/gis/geos/#django.contrib.gis.geos.WKTWriter.precision
.. _`RegMunDemElEnergy in config/layers_region.cfg`: https://github.com/rl-institut/WAM_APP_stemp_abw/blob/b5c0a18b79f899e746876f74296c65c906617a00/config/layers_region.cfg#L286-L307
.. _Dateikommentar: https://github.com/rl-institut/WAM_APP_stemp_abw/blob/dev/config/labels.cfg#L1-L34
.. _`RegMunDemElEnergy`: https://github.com/rl-institut/WAM_APP_stemp_abw/blob/dev/models.py#L115-L132
.. _`RegMun`: https://github.com/rl-institut/WAM_APP_stemp_abw/blob/b5c0a18b79f899e746876f74296c65c906617a00/models.py#L42-L47
.. _`Add layer for reg_mun_gen_cap_re_result #38`: https://github.com/rl-institut/WAM_APP_stemp_abw/commit/720f2e7e69d942d0b4344da8c086b72aa7ec2621
.. _`Add layer for reg_mun_gen_cap_re_density_result #38`: https://github.com/rl-institut/WAM_APP_stemp_abw/commit/b9331809f1e66594c46ce1d4ac544bceb7a6ac60
.. _`Add layer for reg_mun_gen_count_wind_density_result #38`: https://github.com/rl-institut/WAM_APP_stemp_abw/commit/41c70311fcbc1ad2f6db59e1c34a62bdcea5d5f0
.. _API: https://stemp-abw.readthedocs.io/en/dev/api.html
.. _Django: https://www.djangoproject.com/
.. _Django-Design-Philosophie: https://docs.djangoproject.com/en/2.2/misc/design-philosophies/
.. _Django-Dokumentation: https://docs.djangoproject.com/en/2.2/
.. _getting started Tutorial: https://www.djangoproject.com/start/
.. _`Modellmechanismus aus Django`: https://docs.djangoproject.com/en/2.2/topics/db/models/
.. _oemof: https://github.com/oemof/oemof
.. _stemp_abw: https://github.com/rl-institut/WAM_APP_stemp_abw
.. _stemp_mv: https://github.com/rl-institut/WAM_APP_stemp_mv
.. _Tutorial: https://realpython.com/location-based-app-with-geodjango-tutorial/
.. _WAM: https://github.com/rl-institut/WAM
.. _WAM-Applikationen-Kosmos: https://wam.rl-institut.de/
.. _WAM-Dokumentation: https://wam.readthedocs.io/en/latest/

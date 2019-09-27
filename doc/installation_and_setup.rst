.. _install_label:

Installation
============

Voraussetzungen
---------------

- Python Version >=3.6
- `WAM <https://github.com/rl-institut/WAM>`_ (Installation in der folgenden Anleitung enthalten)
- Git (Linux/Windows) und Git Bash (Windows), falls direkt vom Quellcode installiert wird

Installation (Quellcode-Weg)
----------------------------

1. Ordner anlegen und in diesen wechseln:

- Linux und Windows (Git Bash):

.. code-block:: bash

    mkdir ~/StEmp-ABW/
    cd ~/StEmp-ABW/

2. GitHub-Repository der `WAM <https://github.com/rl-institut/WAM>`_ klonen und in
den Master-Branch wechseln:

- Linux und Windows (Git Bash):

.. code-block:: bash

    git clone https://github.com/rl-institut/WAM.git WAM
    cd ./WAM/
    git checkout master

3. Einrichtung der WAM.

Entsprechend der `WAM-Dokumentation <https://wam.readthedocs.io/en/latest/getting_started.html>`_ (PostgreSQL,
PostGIS, Celery, Umgebungsvariablen, benötigte Pakete etc.). Danach an dieser Stelle weiter.

Anmerkung: In der `WAM-Dokumentation <https://wam.readthedocs.io/en/latest/getting_started.html>`_ wird u. a. beschrieben,
wie Sie via Conda eine virtuelle Umgebung erstellen und diese aktivieren. In den nächsten Schritten gehen wir davon aus,
dass diese aktiviert ist.

4. GitHub-Repository des StEmp-Tools in das WAM-Verzeichnis klonen und in den
Master-Branch wechseln:

- Linux und Windows (Git Bash):

.. code-block:: bash

    git clone https://github.com/rl-institut/WAM_APP_stemp_abw.git stemp_abw
    cd ./stemp_abw/
    git checkout master

Anmerkung: falls noch nicht getan, im der Umgebungsvariable ``WAM_APPS`` den Applikationennamen ``stemp_abw`` eintragen - vgl. mit `WAM-Dokumentation
<https://wam.readthedocs.io/en/latest/getting_started.html>`_.

5. Datenbankeinrichtung

- Linux und Windows (Git Bash):

Anmerkung: Falls nicht bereits geschehen ins WAM-Stammverzeichnis wechseln, in dem sich die Datei `manage.py` befindet.

.. code-block:: bash

    python manage.py makemigrations
    python manage.py migrate

.. _install_data_label:

6. Datenmigration

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3376167.svg
   :target: https://doi.org/10.5281/zenodo.3376167

Die benötigten Daten liegen auf `Zenodo <https://doi.org/10.5281/zenodo.3376167>`_
und können mit dem bereitgestellten Skript ``get_fixtures_stemp_abw.py`` über
`Django fixtures <https://docs.djangoproject.com/en/2.2/howto/initial-data/>`_
installiert werden.

- Linux und Windows (Git Bash):

.. code-block:: bash

    python manage.py get_fixtures_stemp_abw
    python manage.py loaddata stemp-abw_data_<VERSION>.json

Anmerkung: Falls der Downloadvorgang (``get_fixtures_stemp_abw``) fehlschlägt, dann einfach den Datensatz von
`Zenodo <https://doi.org/10.5281/zenodo.3376167>`_ herunterladen, entpacken und die resultierende JSON-Datei
in das Fixtureverzeichnis (``stemp_abw/fixtures``) kopieren.

Anmerkung: Der Ladevorgang der JSON-Daten (``loaddata``) kann bis zu 15 Minuten dauern.

7. Django-Server starten

- Linux und Windows (Git Bash):

.. code-block:: bash

    ./manage.py runserver 8888

Per Browser kann nun auf das Tool zugegriffen werden: http://127.0.0.1:8888/

.. _install_data_label:

.. note::
    Kompatibilität: Die Versionsnummern des verwendeten Tools und der Daten
    müssen übereinstimmen.

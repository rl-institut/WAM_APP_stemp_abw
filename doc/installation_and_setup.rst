.. _install_label:

Installation
============

Voraussetzungen
---------------

- Python Version >=3.6
- `WAM <https://github.com/rl-institut/WAM>`_ (Installation in der folgenden Anleitung enthalten)

Installation (Quellcode)
------------------------

Das StEmp-ABW-Tool kann lokal aus dem Quellcode installiert werden. Dies setzt
voraus, dass git vorhanden ist.

Ordner anlegen (hier im Benutzerverzeichnis) und in diesen wechseln:

.. code-block:: bash

    mkdir ~/StEmp-ABW/
    cd ~/StEmp-ABW/

Wir empfehlen die vorherige Einrichtung einer virtuellen Umgebung (`virtual
environment <https://virtualenv.pypa.io>`_):

.. warning:: VENV kann raus, da Conda mit der WAM installiert wird

.. code-block:: bash

    virtualenv stemp_abw_venv

Virtual environment aktivieren:

.. code-block:: bash

    source ./stemp_abw_venv/bin/activate

GitHub-Repository der `WAM <https://github.com/rl-institut/WAM>`_ klonen und in
den master-Branch wechseln:

.. code-block:: bash

    git clone https://github.com/rl-institut/WAM.git WAM
    cd ./WAM/
    git checkout master

Einrichtung der WAM entsprechend der `WAM-Doku
<https://wam.readthedocs.io/en/latest/getting_started.html>`_ (PostgreSQL,
PostGIS, Celery, Umgebungsvariablen, benötigte Pakete etc.).

GitHub-Repository des StEmp-Tools in das WAM-Verzeichnis klonen und in den
master-Branch wechseln:

.. code-block:: bash

    git clone https://github.com/rl-institut/WAM_APP_stemp_abw.git stemp_abw
    cd ./stemp_abw/
    git checkout master

Datenpaket installieren, siehe :ref:`install_data_label`.

Django-Server starten

.. code-block:: bash

    ./manage.py runserver 8888

Per Browser kann nun auf das Tool zugegriffen werden: http://127.0.0.1:8888/

.. _install_data_label:

Daten bereitstellen
-------------------

Die benötigten Daten liegen bei `Zenodo <https://zenodo.org/record/3376168>`_
und können mit dem bereitgestellten Skript <XXX> über `Django fixtures
<https://docs.djangoproject.com/en/2.2/howto/initial-data/>`_ installiert
werden:

.. warning:: TBD

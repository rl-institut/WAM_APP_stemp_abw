.. _install_label:

Installation
============

.. warning:: Update nach `Packaging-Entscheidung der WAM <https://github.com/rl-institut/WAM/issues/50>`_

Das Tool kann bei Bedarf auch lokal eingerichtet werden.

Voraussetzungen
---------------

- Python Version >=3.6
- WAM

Installation (Python-Paket)
---------------------------

StEmp-ABW ist als Python-Paket auf PyPI <INSERT LINK> verfügbar und kann über
das Paketverwaltungsprogrammvon von Python (pip) installiert werden. Wir
empfehlen die vorherige Einrichtung einer virtuellen Umgebung (`virtual
environment <https://virtualenv.pypa.io>`_):

Virtual environment einrichten (empfohlen):

.. code-block:: bash

    virtualenv stemp_abw_env

Virtual environment aktivieren und StEmp-Tool installieren:

.. code-block:: bash

    source /pfad/zur/venv/bin/activate
    pip3 install <NAME>


Installation (Quellcode)
------------------------

Die Installation setzt voraus, dass git vorhanden ist.

GitHub-Repository (s.o.) klonen:

.. code-block:: bash

    git clone https://github.com/rl-institut/WAM_APP_stemp_abw.git stemp_abw

Virtual environment aktivieren (Installation s.o.) und StEmp-Tool installieren:

.. code-block:: bash

    source /pfad/zur/venv/bin/activate
    pip3 install -e ./stemp_abw/

Daten bereitstellen
-------------------

Noch zu klären auf welchem Weg.. (import DB dump, the "djangonic" way, ...)

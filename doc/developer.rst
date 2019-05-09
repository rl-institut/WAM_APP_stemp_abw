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
Reiner-Lemoine-Instituts (RLI). Die Bezeichnung WAM steht hierbei für
*Web Applications and Maps* und stellt eine Kategorie von Applikationen dar,
welche am RLI erstellt werden. Dies sind hauptsächlich Web-Applikationen,
die mit Hilfe von Karten arbeiten und oder bei denen im Hintergrund Berechnungen
stattfinden, dessen Ergebnis an die NutzerInnen visuell zurückgegeben wird.
Einige der WAM-Applikationen sind mit dem RLI-eigenen Web-Applikationen-Framework
mit dem Namen WAM_ erstellt worden, andere WAM-Applikationen basieren auf anderen
Frameworks oder sind freie Implementationen ohne Framework-Basis.

Diese StEmp-Web-Applikation des RLI nutzt das Git-Projekt WAM_ als Basis-Projekt.
Das verwendete WAM-Basis-Projekt baut auf dem Django-Web-Framework auf,
welches Python als Programmiersprache verwendet. Django hat eine gewisse
Lernkurve, deswegen kann es Sinn machen, sich bei Bedarf zuerst mit dem
zugrunde liegenden Web-Framework Django zu beschäftigen, bevor mit der Arbeit
an einer auf Django basierenden WAM-Applikation begonnen wird. Für das Erlernen
des Umgangs mit Django gibt es sehr viel Lernmaterial Dritter, weswegen im
Folgenden in dieser Dokumentation auf einige dieser Anleitungen und
Dokumentationen zum Erlernen von Django verwiesen werden soll. Anschließend
wird im nächsten Abschnitt auf der auf Django basierenden WAM_-Projektbasis
eingegangen.

Tutorials und Informationen zu Django:

- Das Django `getting started Tutorial`_

- Tutorial_ einer einfachen Geo-Applikation in Django

- Die offizielle Django-Dokumentation_

- Die Django-Design-Philosophie_

Tool-Struktur
-------------

Infos/Diagramme z.B. zu

- Verbindung UI-Django-oemof..
- Datenflüsse
- ???

.. _Django-Design-Philosophie: https://docs.djangoproject.com/en/2.2/misc/design-philosophies/
.. _Django-Dokumentation: https://docs.djangoproject.com/en/2.2/
.. _getting started Tutorial: https://www.djangoproject.com/start/
.. _Tutorial: https://realpython.com/location-based-app-with-geodjango-tutorial/
.. _WAM-Applikationen-Kosmos: https://wam.rl-institut.de/
.. _WAM: https://github.com/rl-institut/WAM

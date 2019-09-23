# Wind Turbines and Repowering <img src="../../static/stemp_abw/img/energy_icons/Stromerzeuger_Windenergieanlage.svg" alt="WEA" width="35">

You can select a type of extension scenario here:

1. **Variable extension:** You are free to choose your extension. Other areas
   can be selected in addition to the priority areas (VG/EG). The maximum
   potential depends on the available surfaces which can be adjusted in the
   **Areas** category.

2. **No Repowering:** No repowering will be carried out (only present wind
   plants, average full load hours for the entire region: 1630).

3. **1:1-Repowering (locally):** Local repowering of all currently active old
   plants by a new plant, both within and outside priority areas (VR/EG) for
   wind energy. 

4. **Full utilization VR/EG:** A maximum number of new turbines will be
   installed in all current priority areas (VR/EG) for wind energy (you can
   find them in **Areas -> Static Areas**). All turbines outside these areas
   will be disassembled. 

## Model plant

For the simplification an Enercon E-141 (4.2 MW) with a hub height of 159 m is
used as the new plant in **scenarios 2-4** (on average 2500 full load hours in
the entire region).

**Note:** Due to the higher efficiency of new plants,
_a higher energy production can be achieved with the same installed capacity_.
If you have activated repowering or free extension, this will always lead to a
higher energy prodction even without additional capacity.

## Framework

- The year of construction of existing wind turbines will be neglected, i.e. in
  **scenarios 2-4** no successive extensions or the like are taken into
  account.
- The wind plant arrangement is not optimized. A general area requirement of 20
  hectares per plant is assumed (based on assumptions from
  <a href="https://mlv.sachsen-anhalt.de/fileadmin/Bibliothek/Politik_und_Verwaltung/MLV/MLV/Service/Publikationen/Abschlussbericht_der_interministeriellen_Arbeitsgruppe__Repowering__zur_Modernisierung_von_Windenergieanlagen_in_Sachsen-Anhalt.pdf" target="_blank">ImAG 2018</a>, 
  <a href="https://www.umweltbundesamt.de/sites/default/files/medien/378/publikationen/potenzial_der_windenergie.pdf" target="_blank">UBA 2013</a>,
  <a href="https://www.bmwi.de/Redaktion/DE/Downloads/B/berichtsmodul-2-modelle-und-modellverbund.pdf" target="_blank">BMWi 2017</a>).

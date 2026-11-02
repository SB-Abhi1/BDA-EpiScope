# Third-party sources and notices

- D3.js 7.9.0: Mike Bostock / Observable, ISC license. https://github.com/d3/d3/blob/v7.9.0/LICENSE ; bundled minified distribution in `dashboard/vendor/`. The ISC license allows use, copying, modification and distribution with its copyright and permission notice.
- geoBoundaries Bangladesh ADM2: underlying BBS / OCHA ROAP boundaries; CC BY 3.0 IGO, as declared in the cached metadata. https://www.geoboundaries.org/api/current/gbOpen/BGD/ADM2/ . Simplified geometry is used for the browser; representative coordinates are vertex-mean locations, not guaranteed area-weighted centroids.
- Open-Meteo historical reanalysis: https://open-meteo.com/en/docs/historical-weather-api ; attribute Open-Meteo and applicable underlying reanalysis providers; CC BY 4.0 for API data. Noncommercial API access limits/terms apply. Sixty-four location requests are cached and limited to two concurrent requests with retries.
- BBS-2022-labelled district totals: https://www.arcgisbd.com/server/rest/services/ADB005/CRIIPS/MapServer/355 . This is a secondary GIS distribution, not a claim that the project downloaded the official district census tables. Verify original source and redistribution terms before external publication; attribution is not a substitute for permission.
- US Census Bureau population estimates/projections: https://www2.census.gov/programs-surveys/international-programs/tables/time-series/pepfar/bangladesh.xlsx . Public federal population estimates, based on 2011 census. District 2022 age/sex shares are calibrated to GIS totals; they are estimates, not observed 2022 district census age-sex counts.
- Apache Spark: Apache License 2.0. https://spark.apache.org/ . Installed by dependency manager, not vendored.
- SciPy/NumPy/pandas/PyArrow/Matplotlib/ReportLab: their installed package licenses apply. Python dependencies are not redistributed in the source archive.

Independent project code is provided under MIT (see LICENSE). Public source datasets retain their original terms. No proprietary official endorsement is implied.

- Tinos fonts: Copyright 2026 The Tinos Project Authors / Google Fonts, SIL Open Font License 1.1; original license bundled in docs/fonts/Tinos_LICENSE.txt. DejaVu Sans: Bitstream Vera / DejaVu license, bundled copyright in docs/fonts/DejaVu_LICENSE.txt. Fonts are embedded in PDFs to preserve typography across viewers.

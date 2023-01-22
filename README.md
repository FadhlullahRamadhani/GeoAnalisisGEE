### APLIKASI ANALISIS GEOSPASIAL REGRESI MULTI SKALA / Aplikasi AGRMS 1.0 ###

Aplikasi ini bertujuan untuk mengolah data raster dan vektor data geospasial untuk mendapatkan regresi untuk hubungan terhadap sebuah parameter yang independent.

Dalam aplikasi ini menggunakan data-data yang bersumber dari data open-source, peta rupa bumi Indonesia, dan peta wilayah administrasi dari BPS. Adapun data-data raster input adalah:

1.	Kedalaman lapisan pembatas akar/ Root restricting layer depth (depth_to_root_rest_layer,  mm) 
2.	Fraksi (fractp ): Estimasi fraksi evapotranspirasi sebenarnya dari presipitasi per piksel/ Estimated actual evapotranspiration fraction of precipitation per pixel 
(Actual Evapotranspiration / Precipitation). It is the mean fraction of precipitation that actually evapotranspires at the pixel level. 
3.	Kandungan Air Tersedia Tanaman/ Plant Available Water Content (pawc),  PAWC is a fraction from 0 to 1. 
4.	Presipitasi/ Precipitation (precip, mm) 
5.	Rata-rata Evapotranspirasi Referensi Tahunan (eto, mm). Evapotranspirasi acuan tahunan rata-rata (Eto). Eto , adalah energi (dinyatakan sebagai kedalaman air, misalnya mm) yang disediakan oleh matahari (dan terkadang angin) untuk menguapkan air.
6.	Rata-rata evapotranspirasi aktual per piksel pada subDAS/ AET_mn (mm): Mean actual evapotranspiration per pixel on the subwatershed. 
7.	Raster data ketinggian digital/ Digital Elevation Meter (DEM)
8. Data keluaran dari aplikasi INVEST yaitu data hasil air/ ESTIMATED WATER YIELD.
9. Data vektor batas kecamatan

Fitur yang ada di aplikasi ini:
1. Otomatisasi input raster untuk dimasukkan ke input Analisis Geospasial Regresi Multi skala.
2. Peta dalam bentuk grafik otomatis disimpan dalam bentuk PNG.
3. Tampilan keluaran peta per kecamatan dalam ditampilkan secara otomatis menggunakan Google Earth Engine.

Cara Instalasi
A. Instalasi Anaconda dan paket pendukung.
1. Instalasi Anaconda dari https://www.anaconda.com/
2. Instalasi Visual Code dari https://code.visualstudio.com/
3. Copy master repository ini dan ekstract.
4. Buat Enviroment Anaconda dengan nama "mgwr38-GEEMAP"
5. instalasi paket pendukung di perintah pip. pip install -r requirements.txt
6. Jika ada masalah mengenai GEEMAP, silahkan membaca https://geemap.org/.
7. Jika ada masalah mengenai MGWR, silahkan membaca https://mgwr.readthedocs.io/en/latest/.
8. Untuk menghasilkan data keluaran dari aplikasi INVEST, silahkan membaca https://invest-userguide.readthedocs.io/en/latest/annual_water_yield.html.
9. Untuk contoh Daerah Aliran Sungai Citarum, bisa membaca dan mensitasi: Spatial-Temporal Changes in Water Supply and Demand in the Citarum Watershed, West Java, Indonesia Using a Geospatial Approach. https://www.mdpi.com/2071-1050/15/1/562 

Cara Penggunaan
1. Aktifkan akun Google Earth Engine di peramban chrome.
2. Buka file mgwr_raster.py versi terakhir.
3. Jalankan satu-satu sesuai arahan di halaman jupyter.
4. Jika ada masalah, silahkan kontak pembangun aplikasi ini. 

#### SELAMAT MENCOBA ####
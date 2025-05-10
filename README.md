# README
This repository contains data, code and figures for our paper: 
> Jianxuan Hong, and Shengqian Chen. Network Analysis of Jade Artifacts in Liangzhu: Exploring the Relationships Between Liangzhu Ancient City, Fuquanshan, and Sidun

# Environment Setup
```bash
pip3 install -r requirements.txt
```

# File Structure  
* 📂 `supplementary_materials` contains all data included in the paper<br>
  * 📄 `all_jade_artifacts.xlsx` contains presence/absence data of jade artifact types by site and phase in the Liangzhu culture. It forms the basis of Section 3.1, "The Network of Shared Jade Traditions in Liangzhu Society."
  * 📄 `all_smc.xlsx` provides the simple matching coefficients for all site pairs across the four phases of the Liangzhu culture, based on the presence/absence data of all jade artifact types from `all_jade_artifacts.xlsx`. Combined with spatial information from site_coordinate.xlsx, it was used to generate the network figure `all_network.png`.
  * 📄 `all_measurement.xlsx` presents the characteristic indicators of the Network of Shared Jade Traditions, derived from `all_smc.xlsx`, and corresponds to Table 1 in the manuscript.
  * 📄 `special_jade_artifacts.xlsx` contains binary presence/absence matrices of specific expected jade artifact types for each site across the four phases of the Liangzhu culture. It serves as the foundational dataset for Section 3.2 "The Network of Power and Status Represented by Jade Artifacts."
  * 📄 `special_smd.xlsx` includes simple matching distances between sites based on specific jade artifact types, calculated from `special_jade_artifacts.xlsx`.
  * 📄 `special_coordinate_and_total.xlsx` records the geographic coordinates of sites with special jade artifacts, along with the number of special artifacts per site and phase. Together with `special_smd.xlsx`, it was used to generate `special_network.png`. The artifact counts in this file contribute to Table 2 in the manuscript.
  * 📄 `weighted_degrees.xlsx` records the weighted simple matching distances of each site, derived from `special_smd.xlsx`. The top 5 sites per phase contribute to Table 2 in the manuscript.
  * 📄 `cong.xlsx` contains binary presence/absence matrices capturing 31 features of jade cong at each site and phase where jade cong are present. This file serves as the foundational dataset for Section 3.3, "The Network of Jade Cong."
  * 📄 `cong_smc.xlsx` contains the simple matching coefficients for each site&phase where jade cong are present, calculated based on the data in `cong.xlsx`.This file corresponds to Table 3 in the manuscript.
  * 📄 `cong_smc_processed.xlsx` is based on `cong_smc.xlsx`, with an additional sheet indicating the cultural phase of each site&phase. This was added to enable color differentiation by cultural phase in the network visualization.It was used to generate `special_network.png`.


* 📂 `code` includes scripts for generating figures and tables.The order of code execution reflects the sequence of analysis conducted in this study.<br> 
  * 📄 `1_all_smc.py` fits the data from `all_jade_artifacts.xlsx` and outputs `all_smc.xlsx`<br>
  * 📄 `2_all_network.py` fits the data from `all_smc.xlsx` and `site_coordinate.xlsx`, and outputs `all_network.png`<br>
  * 📄 `3_all_measurement.py` fits the data from `all_smc.xlsx` and outputs `all_measurement.xlsx`<br>
  * 📄 `4_special_smd.py` fits the data from `special_jade_artifacts.xlsx` and outputs `special_smd.xlsx`<br>
  * 📄 `5_special_network.py` fits the data from `special_smd.xlsx` and `special_coordinate_and_total.xlsx`, and outputs `special_network.png`<br>
  * 📄 `6_top5.py` fits the data from `special_smd.xlsx` and outputs `weighted_degrees.xlsx`<br>
  * 📄 `7_cong_smc.py` fits the data from `cong.xlsx` and outputs `cong_smc.xlsx`<br>
  * 📄 `8_cong_network.py` fits the data from `cong_smc_processed.xlsx` and outputs `cong_network.png`<br>

* 📂 `figures` contains all figures included in the paper<br>
  * 📄 `all_network.png` was generated based on `all_smc.xlsx` and `site_coordinate.xlsx`, and is presented as Fig.3 in the manuscript.
  * 📄 `special_network.png` was generated based on `special_smd.xlsx` and `special_coordinate_and_total.xlsx`, and is presented as Fig.4 in the manuscript.
  * 📄 `cong_network.png` was generated based on `cong_smc.xlsx`, and is presented as Fig.5 in the manuscript.
 


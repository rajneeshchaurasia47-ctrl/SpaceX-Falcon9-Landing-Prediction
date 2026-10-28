# Attributed historical reference data (not original live collection)

These files are **published third-party historical snapshots** added to support the data-provenance comparison in the final presentation. They are **not proof that this repository successfully executed SpaceX API requests or Wikipedia scraping**.

| Local reference | Published original | Purpose |
|---|---|---|
| `dataset_part_1_api_derived_mirror.csv` | [adgsenpai/IBM-DataScience-SpaceX-Capstone](https://github.com/adgsenpai/IBM-DataScience-SpaceX-Capstone/blob/main/dataset_part_1.csv) | Examine API-derived historical schema; 90 rows, 17 columns |
| `spacex_web_scraped_mirror.csv` | [Roderic19/IBM-Applied-Data-Science-Capstone](https://github.com/Roderic19/IBM-Applied-Data-Science-Capstone/blob/main/spacex_web_scraped.csv) | Examine historical Wikipedia-style launch-table schema |
| `Spacex_SQL_101_mirror.csv` | [chuksoo/IBM-Data-Science-Capstone-SpaceX](https://github.com/chuksoo/IBM-Data-Science-Capstone-SpaceX/blob/main/Spacex.csv) | 101-row historical SQL exercise source |

The primary executed model and visualization results use the **separate** `dataset_part_2.csv` (90 labelled records, `Class` outcome). The teaching SQL table has different columns and 101 records; values from the two datasets must not be combined as though they share the same row universe.

Official lab references:
- [IBM archived API JSON](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json)
- [Wikipedia historical launch list](https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922)
- [IBM SQL lab CSV](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv)

Connection failures during original collection attempts are documented in the project scripts; no successful direct API / HTML collection is claimed.

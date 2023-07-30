# Description
Command line Python program to extract army rules and unit cards from 10th edition Warhammer 40k indexes to create army list specific pdfs with reduced file size. Requires Python.

# Instructions
- Download an army index https://www.warhammer-community.com/warhammer-40000-downloads/#indexes-faqs-and-errata  
- Install [Python](https://wiki.python.org/moin/BeginnersGuide/Download)
- Install py40kie using pip:  
  ```
  pip install -U py40kie
  ```
- Run py40kie using command line:  
  ```
  py40kie [-h] [-i EXTRA_INDEXES [EXTRA_INDEXES ...]] [-o OUTPUT_PDF] [-b] [-a] [-d] [-s] [-e] [-w] [-na] [-nd]
               [-ns] [-ne] [-nw] [-r RULE_PAGES [RULE_PAGES ...]] [-v]
               index_pdf pages [pages ...]
  ```
  ### Examples  
  ```
  py40kie "Tyranids Index.pdf" 9 21 25 27 -o "my army list"  
  ```
  ```
  py40kie "Tyranids Index.pdf" "hive tyrant" "tyranid warriors with ranged bio-weapons" 25 "hOrMaGaUnTs" -o "./my lists/my army list"
  ```
  ```
  py40kie "Space Wolves Index.pdf" 7 1-23 "Blood Claws" 1-53 "terminator squad" "2-culexus assassin" 2-7 3-1 -o "Best Army List Ever.pdf" -i "Space Marines Index.pdf" "Agents of Imperium Index.pdf" "Imperial Armour Astartes.pdf"
  ```
  
  # Arguments
  #### Postional arguments
    - The "index.pdf" file to extract cards from  
    - Space separated list of cards to extract. Can be page numbers or **exact** unit titles. Army rules, detachment rules, stratagems, enhancements and unit wargear are included automatically  
  #### Optional arguments:  
    - -o: The file to save the extracted pdf to. Folder path can be included
    - -i: Optional space separated list of additional pdfs to extract allied units from other Indexes/Imperial Armour/Legends ("1-10" to extract the card on page 10 from the first additional pdf). Also use this to extract the Adeptus Astartes army rule when using Space Marines
    - -b: Optional flag for boarding actions (extracts the army rules page but not the detachment or stratagem pages)  
    - -na: Optional flag to disable extracting the army rules page  
    - -nd: Optional flag to disable extracting the detachment rules page  
    - -ns: Optional flag to disable extracting the stratagem pages  
    - -ne: Optional flag to disable extracting the enhancements page  
    - -nw: Optional flag to disable extracting wargear pages  
    - -r: Optional argument to specify army rules and stratagem pages (space separated numbers). Use this if the army rules and stratagems are not successfully extracted from the index  
    - -v: Optional flag to override page extraction. Will extract only the page numbers specified from the main index  

# Contributions  
## Future features  
Any suggested features would be appreciated  
 - [x] Allied units from other Indexes/Imperial Armour/Legends  
 - [x] Extract Adeptus Astartes army rule page for Space Marine lists  
 - [x] Create runnable command from [Google Sheet army builder lists](https://www.reddit.com/r/WarhammerCompetitive/comments/14br6rw/10e_40k_list_builder_spreadsheets/)  
       Copy the cells in the yellow box from here to your own sheet: https://docs.google.com/spreadsheets/d/1A1lDqmL0f_iH9OIUQWL_v83_leyhm3t0rhyC20UfrPA  
 - [ ] Extract extra rule pages. e.g. Deathwatch Armoury  
 - [ ] Handle exceptions gracefully  
 - [ ] Webapp version?...  


## Issues  
py40kie was not tested on all indexes. If there is any problem extracting cards please submit an issue https://github.com/Dragons-Ire/40k-index-pdf-extractor/issues/new

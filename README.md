# Description
Command line Python program to extract army rules and unit cards from 10th edition Warhammer 40k indexes to create army list specific pdfs with reduced file size. Requires Python and pypdf.

# Getting Started
## Prerequisites
- [Python](https://wiki.python.org/moin/BeginnersGuide/Download)


## Instructions
- Install Python
- Download an army index https://www.warhammer-community.com/warhammer-40000-downloads/#indexes-faqs-and-errata  
- Install py40kie using pip:
  ```
  pip install py40kie
  ```
- Run 40k_index_pdf_extractor.py using command line
    - First argument: The index.pdf file to extract cards from  
    - Second argument: Space separated list of cards to extract. Can be page numbers or **exact** unit titles. Army rules, strategems and wargear are included automatically  
    - -o: The file to save the extracted pdf to. Folder path can be included  
    - -a: Optional argument to specify army rules and strategem pages (space separated numbers). Use this if the army rules and strategems are not contained in the first 4 pages of the index  
    - -v: Optional flag to override page extraction. Will extract only the page numbers specified  

## Example usages
python py40kie.py "tyranids index.pdf" 9 21 25 27 -o "my army list"  
python py40kie.py "tyranids index.pdf" "hive tyrant" "tyranid warriors with ranged bio-weapons" 25 "hormagaunts" -o ".\my lists\my army list"

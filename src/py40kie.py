import argparse
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def parse_args():
    parser = argparse.ArgumentParser(prog='py40kie',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Example usages:\n'
                                                 '%(prog)s "tyranids index.pdf" 9 21 25 27 -o "my army list"'
                                                 '\n%(prog)s "tyranids index.pdf" "hive tyrant" '
                                                 '"tyranid warriors with ranged bio-weapons" 25 "hOrMaGaUnTs" '
                                                 '-o "./my lists/my army list"'
                                                 '\n%(prog)s "Space Wolves Index.pdf" 7 1-23 "Blood Claws"'
                                                 '1-53 "terminator squad" "2-culexus assassin" 2-7 3-1 -o '
                                                 '"Best Army List Ever.pdf" -i "Space Marines Index.pdf" '
                                                 '"Agents of Imperium Index.pdf" "Imperial Amour Astartes.pdf"')
    # Positional arguments
    parser.add_argument('index_pdf', type=str,
                        help='index pdf file to extract cards from')

    parser.add_argument('pages', nargs='+',
                        help='space separated page numbers or exact unit titles of cards to extract '
                             '(army rules and wargear included automatically)')

    # Optional arguments                
    parser.add_argument('-i', dest='extra_indexes', nargs='+', default=None,
                        help='space separated list of additional pdfs to extract allied units from other Indexes/Imperial Armour/Legends ("1-10" to extract the card on page 10 from the first additional pdf). Also use this to extract the Adeptus Astartes army rule when using Space Marines')
    
    parser.add_argument('-o', dest='output_pdf', default="my army list", type=str,
                        help='file to save the extracted cards to - '
                             'can be in a folder (default: "%(default)s")')
    
    parser.add_argument('-b', dest='boarding_actions', action='store_true',
                        help='flag for boarding actions (no enhancement, stratagems or detachment pages)')

    parser.add_argument('-a', dest='army_rules', action='store_true',
                        help='flag to extract army rules (on by default)')
    
    parser.add_argument('-d', dest='detachment_rules', action='store_true',
                        help='flag to extract detachment rules (on by default)')
    
    parser.add_argument('-s', dest='stratagems', action='store_true',
                        help='flag to extract stratagem pages (on by default)')
    
    parser.add_argument('-e', dest='enhancements', action='store_true',
                        help='flag to extract enhancements (on by default)')
    
    parser.add_argument('-w', dest='wargear', action='store_true',
                        help='flag to extract wargear (on by default)')
    
    # Deactivation arguments
    parser.add_argument('-na', dest='army_rules', action='store_false',
                        help='flag to not extract army rules')
    
    parser.add_argument('-nd', dest='detachment_rules', action='store_false',
                        help='flag to not extract detachment rules')
    
    parser.add_argument('-ns', dest='stratagems', action='store_false',
                        help='flag to not extract stratagem pages')
    
    parser.add_argument('-ne', dest='enhancements', action='store_false',
                        help='flag to not extract enhancements')
    
    parser.add_argument('-nw', dest='wargear', action='store_false',
                        help='flag to not extract wargear')
    
    parser.set_defaults(army_rules=True)
    parser.set_defaults(detachment_rules=True)
    parser.set_defaults(stratagems=True)
    parser.set_defaults(enhancements=True)
    parser.set_defaults(wargear=True)

    # Overwrite arguments
    parser.add_argument('-r', '--rule_pages', default=None, type=int, nargs='+',
                        help='override army rule pages - use this if the army rules and stratagems are not successfully extracted from the index')
    
    parser.add_argument('-v', dest='override_pages', action='store_true',
                        help='flag to override functionality - only page numbers specified will be extracted and only from the main index')
    
    return parser.parse_args()


def main(index_pdf, pages, output_file_name="my army list", army_rules=True, detachment_rules=True, stratagems=True, enhancements=True, wargear=True, boarding_actions=False, rule_pages=None, override_pages=False):
    if boarding_actions:
        detachment_rules = False
        stratagems = False
        enhancements = False
    # reader_pages = page_extractor(index_pdf=index_pdf, pages=pages, army_rules=army_rules, detachment_rules=detachment_rules, stratagems=stratagems, enhancements=enhancements, wargear=wargear, extra_indexes=extra_indexes, rules_pages=rules_pages, override_pages=override_pages)
    if isinstance(index_pdf, list):
        readers = []
        for index in index_pdf:
            readers.append(PdfReader(index))
    else:
        readers = [PdfReader(index_pdf)]
    
    writer = PdfWriter()
    reader_pages = []
    if override_pages:
        # only extract the specified page numbers
        for page in pages:
            if page.isdigit():
                writer.add_page(readers[0].pages[int(page) - 1])
    else:
        if rule_pages:
            # override extracting army rule pages
            for page in rule_pages:
                writer.add_page(readers[0].pages[int(page) - 1])
        else:
            # extract the army rule pages
            if army_rules or detachment_rules or stratagems or enhancements:
                if ("adeptus astartes" in readers[0].pages[0].extract_text().lower() or "deathwatch" in readers[0].pages[0].extract_text().lower()) and not readers[0].pages[0].extract_text().split('\n')[0].lower() == "adeptus astartes":
                    found_army_rule_page = False
                    if len(readers) > 1:
                        for i in range(1, len(readers)):
                            if readers[i].pages[0].extract_text().split('\n')[0].lower() == "adeptus astartes":
                                found_army_rule_page = True
                                writer.add_page(readers[i].pages[0])
                                break
                    if not found_army_rule_page:
                        print("No Adeptus Astartes army rules found. Please add the Adeptus Astartes index with the extra indexes flag")
                for i in range(6):
                    text = readers[0].pages[i].extract_text().split('\n')
                    if len(text) == 1:
                        continue
                    for j in range(len(text)):
                        if army_rules and (text[j].lower() == "army rule" or text[j].lower() == "army rules"):
                            writer.add_page(readers[0].pages[i])
                            break
                        if detachment_rules and (text[j].lower() == "detachment rule" or text[j].lower() == "detachment rules"):
                            writer.add_page(readers[0].pages[i])
                            break
                        if stratagems and text[j].lower() == "stratagems":
                            writer.add_page(readers[0].pages[i])
                        if enhancements and text[j].lower() == "enhancements":
                            writer.add_page(readers[0].pages[i])
                            break
        
        for page in pages:
            reader_index = 0
            if not page.isdigit():
                if len(page) > 2:
                    if page[1] == "-":
                        if page[0].isdigit():
                            reader_index = int(page[0])
                            if reader_index > len(readers)-1:
                                continue
                            page = page[2:]
            if page.isdigit():
                # extract the specified page numbers and the following page (their wargear)
                # todo add a check that the page number given isn't a wargear page
                # if int(page)-1 >= len(readers[reader_index].pages)-1:
                    # continue
                writer.add_page(readers[reader_index].pages[int(page) - 1])
                if wargear:
                    writer.add_page(readers[reader_index].pages[int(page)])
            else:
                # extract the specified pages by unit title (must be exact match)
                # not tested thoroughly so may miss some things
                # additionally this functionality may break in future if pypdf changes or index.pdf is reformatted
                # if it doesn't work - use page numbers
                if reader_index == 0:
                    found_page = False
                    for reader in readers:
                        for i in range(len(reader.pages)):
                            text = reader.pages[i].extract_text()
                            if text.split('\n')[0].lower() == page.lower():
                                found_page = True
                                writer.add_page(reader.pages[i])
                                if wargear:
                                    writer.add_page(reader.pages[i + 1])
                                break
                        if found_page:
                            break
                else:
                    for i in range(len(readers[reader_index].pages)):
                        text = readers[reader_index].pages[i].extract_text()
                        if text.split('\n')[0].lower() == page.lower():
                            found_page = True
                            writer.add_page(readers[reader_index].pages[i])
                            if wargear:
                                writer.add_page(readers[reader_index].pages[i + 1])
                            break
    
    output_path = Path(output_file_name).with_suffix('.pdf')
        
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with output_path.open("wb") as f:
        writer.write(f)

def console_entry():
    args = parse_args()
    if args.extra_indexes:
        args.index_pdf = [args.index_pdf]
        for index in args.extra_indexes:
            args.index_pdf.append(index)
    main(index_pdf=args.index_pdf,
         pages=args.pages,
         output_file_name=args.output_pdf,
         army_rules=args.army_rules,
         detachment_rules=args.detachment_rules,
         stratagems=args.stratagems,
         enhancements=args.enhancements,
         wargear=args.wargear,
         boarding_actions=args.boarding_actions,
         rule_pages=args.rule_pages,
         override_pages=args.override_pages)

if __name__ == "__main__":
    console_entry()

import argparse
from pypdf import PdfReader, PdfWriter

def parse_args():
    parser = argparse.ArgumentParser(prog='40k_index_pdf_extractor',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Example usages:\n'
                                                 'python %(prog)s.py "tyranids index.pdf" 9 21 25 27 -o "my army list"'
                                                 '\npython %(prog)s.py "tyranids index.pdf" "hive tyrant" '
                                                 '"tyranid warriors with ranged bio-weapons" 25 "hormagaunts" '
                                                 '-o ".\my lists\my army list"')
    # Positional arguments
    parser.add_argument('index_pdf', type=str,
                        help='index pdf file to extract cards from')

    parser.add_argument('pages', nargs='+',
                        help='page numbers(or exact unit titles) of cards to extract '
                             '(army rules and wargear included automatically')

    # Optional arguments
    parser.add_argument('-o', dest='output_pdf', default="my army list", type=str,
                        help='file to save the extracted cards to - '
                             'can be in a folder if it already exists (default: "%(default)s")')

    parser.add_argument('-a', '--army_rules_pages', default=[1, 2, 3, 4], type=int, nargs='+',
                        help='overwrite army rule pages - use if the army rules are not on pages 1,2,3,4 '
                             '(default: 1 2 3 4)')

    parser.add_argument('-v', dest='overwrite_pages', action='store_true',
                        help='flag to overwrite functionality - only page numbers specified will be extracted')
    return parser.parse_args()

def main(index_pdf, pages, output_file_name="my army list", army_rules_pages=[1, 2, 3, 4], overwrite_pages=False):
    reader = PdfReader(index_pdf)
    reader_pages = []
    if overwrite_pages:
        # only extract the specified page numbers
        for page in pages:
            if page.isdigit():
                reader_pages.append(int(page) - 1)
    else:
        # extract the army rules pages
        for page in army_rules_pages:
            if not int(page) - 1 in reader_pages:
                reader_pages.append(int(page) - 1)

        for page in pages:
            if page.isdigit():
                # extract the specified page numbers and following page (their wargear)
                if not int(page) - 1 in reader_pages:
                    reader_pages.append(int(page) - 1)
                if not int(page) in reader_pages:
                    reader_pages.append(int(page))
            else:
                # extract the specified pages by unit title (must be exact match)
                # not tested thoroughly so may miss some things
                # additionally this functionality may break in future if pypdf changes or index.pdf is reformatted
                # if it doesn't work - use page numbers
                i = 0
                for i in range(len(reader.pages)):
                    text = reader.pages[i].extract_text()
                    if text.split('\n')[0].lower() == page.lower():
                        if not i in reader_pages:
                            reader_pages.append(i)
                        if not i + 1 in reader_pages:
                            reader_pages.append(i + 1)
                        break

    writer = PdfWriter()

    for page in reader_pages:
        writer.add_page(reader.pages[page])

    if output_file_name[-4:] == ".pdf":
        output_file_name = output_file_name[:-4]

    with open(f"{output_file_name}.pdf", "wb") as fp:
        writer.write(fp)

if __name__ == "__main__":
    args = parse_args()
    main(index_pdf=args.index_pdf,
         pages=args.pages,
         output_file_name=args.output_pdf,
         army_rules_pages=args.army_rules_pages,
         overwrite_pages=args.overwrite_pages)

import sys
import os
import pypdf


def usage(name):
    print(f"{name} pdf pages [out_dir]")
    print("pages: A comma separated list of pages to split at, e.g. (23,45,..).")
    print(
        "  By default a split page will be included in the FIRST PDF. Suffix the page number with `!` to include it in both."
    )


def parse_split(component):
    double_include = False
    if component.endswith("!"):
        double_include = True
        component = component[:-1]

    # People will give page numbers as 1-based, but PyPDF takes them as zero-based indexes.
    # Correct for that here.
    page_num = int(component, base=10) - 1

    return (double_include, page_num)


def parse_page_splits(pages):
    splits = []

    if "," not in pages:
        # We assume this is one large component.
        splits.append(parse_split(pages))
        return splits

    # Otherwise, split on commas and parse.
    components = pages.split(",")
    for c in components:
        splits.append(parse_split(c))

    return splits


def get_segments(splits, num_pages):
    segments = []

    start_page = 0

    for double_include, page in splits:
        if page >= num_pages:
            raise ValueError(
                f"Split {page} must be less than total pages {num_pages + 1}"
            )

        segments.append((start_page, page))
        if double_include:
            start_page = page
        else:
            start_page = page + 1

    # Remember to add on the final segment
    segments.append((start_page, num_pages - 1))

    return segments


def write_segments(segments, out_path, out_filename, in_pdf):
    out_number = 1
    for start, end in segments:
        out_pdf = pypdf.PdfWriter()
        for p in range(start, end + 1):
            out_pdf.add_page(in_pdf.pages[p])
        out_pdf.write(os.path.join(out_path, f"{out_filename}_{out_number}.pdf"))
        out_number += 1


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"{len(sys.argv) - 1} arguments found, 1 expected.")
        usage(sys.argv[0])
        sys.exit(1)

    pages = sys.argv[3]
    try:
        splits = parse_page_splits(pages)
    except ValueError as e:
        print(f"{pages} was not a valid page specification.")
        sys.exit(1)

    in_path = sys.argv[1]
    in_pdf = pypdf.PdfReader(in_path)

    try:
        segments = get_segments(splits, len(in_pdf.pages))
    except ValueError as e:
        print(e)
        sys.exit(1)

    out_path = sys.argv[2]
    out_filename = os.path.splitext(os.path.basename(in_path))[0]
    write_segments(segments, out_path, out_filename, in_pdf)

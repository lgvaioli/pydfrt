import argparse

parser = argparse.ArgumentParser(description="A Python PDF rotator. Positive degrees (DEG) mean "
        "clockwise rotation; negative degrees mean counter-clockwise rotation.")
parser.add_argument("file", help="input filename")
parser.add_argument("-fo", "--fileout", metavar="NAME", help="output filename")
group = parser.add_mutually_exclusive_group()
group.add_argument("-p", "--page", metavar="N", help="single page to be rotated", type=int)
group.add_argument("-pp", "--pagerange", metavar="N", help="range of pages to be rotated", nargs=2, type=int)
parser.add_argument("-e", "--even", metavar="DEG", help="rotate even pages", type=int)
parser.add_argument("-o", "--odd", metavar="DEG", help="rotate odd pages", type=int)
parser.add_argument("-a","--all", metavar="DEG", help="rotate all pages", type=int)
args = parser.parse_args()

print("file: " + args.file)

if args.fileout:
    print("args.fileout: " + args.fileout)

if args.page:
    print("args.page: " + str(args.page))

if args.pagerange:
    if args.pagerange[0]:
        print("args.pagerange[0]: " + str(args.pagerange[0]))

    if args.pagerange[1]:
        print("args.pagerange[1]: " + str(args.pagerange[1]))

if args.even:
    print("args.even: " + str(args.even))

if args.odd:
    print("args.odd: " + str(args.odd))

if args.all:
    print("args.all: " + str(args.all))
    

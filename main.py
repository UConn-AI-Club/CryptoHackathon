from manager.args import readArguments

from process.loadData import loadData
from visualize.visualizeTendency import visualizeTendency

def main():
    args = readArguments()

    data = loadData(args.csv_type, delimiter=args.set_delimiter, offset=args.set_offset)

    if args.visualize_tendencies:
        visualizeTendency(data)

# Run if run as script
if __name__ == '__main__':
    main()

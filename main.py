from manager.args import readArguments

from process.loadData import loadData, loadDataRealtime
from visualize.visualizeTendency import visualizeTendency

def main():
    args = readArguments()

    data = []
    if args.load_data:
        data = loadData(args.csv_type, delimiter=args.set_delimiter, offset=args.set_offset)

    if args.visualize_tendencies:
        visualizeTendency(data)

    if args.realtime_run:
        loadDataRealtime(args.csv_type, delimiter=args.set_delimiter, offset=args.set_offset)

# Run if run as script
if __name__ == '__main__':
    main()

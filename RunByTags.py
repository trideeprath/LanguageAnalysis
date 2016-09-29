import argparse

__Author__ = "Anupam Panwar"

__Date__ = 9 / 29 / 16

import run as run

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('TAG', action='store', help='Tag')
    argparser.add_argument('-q', dest='QUES', default=True, help='Fetch Ques')
    argparser.add_argument('-k', dest='KEYPHRASE', default=False, help='Fetch keyphrase')
    argparser.add_argument('-o', dest='OUTPUT_FILE', default='csv', help='Output file name ')
    args = argparser.parse_args()

    run.main(args.TAG, args.QUES, args.KEYPHRASE, args.OUTPUT_FILE)


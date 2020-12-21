import argparse

from pygd.game import PyGd


def main():
    parser = argparse.ArgumentParser(description="Gravity Defiled")
    parser.add_argument("-l", "--level", type=int, help="Level to load")
    parser.add_argument("-t", "--track", type=int, help="Track to load")
    parser.add_argument(
        "-d", "--debug", default=False, action="store_true", help="Run in debug mode"
    )
    args = vars(parser.parse_args())

    pygd = PyGd(**args)
    pygd.run()


main()

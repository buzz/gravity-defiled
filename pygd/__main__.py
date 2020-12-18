import sys

from pygd.game import PyGd


def main():
    debug_render = False
    try:
        if sys.argv[1] in ("-d", "--debug"):
            debug_render = True
    except IndexError:
        pass

    pygd = PyGd(debug_render=debug_render)
    pygd.run()


main()

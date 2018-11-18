#!/usr/local/bin/python3

import sys
import os
import argparse
import worldinfo


def build_parser():
    """This functions build the parser.
    The parser is build with the building argparse.
    In total 4 arguments are read from the terminal.

    Sites_file >> The df file with world sites_and_pop info.

    Naam_civ_plot >> Name for the  civ plot.

    Naam_civ_pop_plot >> Name for the civ pop plot.

    --debug >> optinal optie for debugging the code.
                This will print the vars and other info.

    All inputs need to be strings. If the parameter is not a string
    the program will stop.

    :return: args: argparser object.
    """

    parser = argparse.ArgumentParser(
        description='Plot df world info.')
    parser.add_argument('Sites_file', metavar='F', type=str,
                        help='df world sites_and_pop file')

    parser.add_argument('Naam_civ_plot', metavar='F_O', type=str,
                        help='Name for civ plot html')

    parser.add_argument('Naam_civ_pop_plot', metavar='F_OO', type=str,
                        help='Name for civ and pop plot html')
    parser.add_argument("--debug", help='Option for debuging')
    args = parser.parse_args()
    return args


def main():
    """The main function.
    First the arparser is requested to check if the input is okay.
    if this is not the case the parser will give a error and show which
    argument is wrong.

    Then the class wordinfo is called to make the plot files.
    when debug is on the parameter True is also givin. otherwise
    only the input.

    At last the plots are made by calling ktImportText in the terminal
    with the givin names and the right files.
    :return: None
    """
    args = build_parser()

    print("++++++++++++++++++++++++++++++++")
    print("+    Staring krona df plots    +")
    print("++++++++++++++++++++++++++++++++")
    if args.debug:
        wordinfo = worldinfo.worldInfoClass(args.Sites_file, True)
    else:
        wordinfo = worldinfo.worldInfoClass(args.Sites_file)

    wordinfo.make_plot_file_normale_civ_pop()
    wordinfo.plot_pop_per_civ()

    os.system("ktImportText -o {}.html  plot_text.txt".format(
        args.Naam_civ_plot))
    os.system("ktImportText -o {}.html  plot_text_pop_civ.txt".format(
        args.Naam_civ_pop_plot))

    print("++++++++++++++++++++++++++++++++")
    print("+    Finished plotting         +")
    print("++++++++++++++++++++++++++++++++")


main()

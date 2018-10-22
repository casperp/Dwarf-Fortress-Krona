#!/usr/local/bin/python3

import sys
import os
import argparse
import worldinfo


def build_parser():
    """snele manier om args te parsen van de terminal
    nu alleen world info file en kijken of het wel een string is

    :return:
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
    args = build_parser()

    print("++++++++++++++++++++++++++++++++")
    print("+    Staring krona df plots    +")
    print("++++++++++++++++++++++++++++++++")
    if args.debug:
        wordinfo = worldinfo.worldInfoClass(args.Sites_file,True)
    else:
        wordinfo = worldinfo.worldInfoClass(args.Sites_file)
    # wordinfo =worldinfo. worldInfoClass('../region2-00125-01-01-world_sites_and_pops.txt')
    wordinfo.make_plot_file_normale_civ_pop()
    wordinfo.plot_pop_per_civ()

    os.system("ktImportText -o {}.html  plot_text.txt".format(args.Naam_civ_plot))
    os.system("ktImportText -o {}.html  plot_text_pop_civ.txt".format(args.Naam_civ_pop_plot))

    print("++++++++++++++++++++++++++++++++")
    print("+    Finished plotting         +")
    print("++++++++++++++++++++++++++++++++")

main()



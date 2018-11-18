import os
import fnmatch
import re
import datetime


class worldInfoClass:
    def __init__(self, file_sideload=None, debug=False):
        """This is the init for the worldinfoclass
        Fist the parameters are set and check if an file is givin
        if no file is given fnmatch is used to search for and df file.
        than that file is used.

        :param file_sideload: input file. If no file is given the class
         will search for a df file.
        :param debug: True or False, enables future debug options.


        """
        self.debug = debug
        self.pops = []
        self.popsize = {}
        self.sites = {}
        self.__file_content = []

        if file_sideload is None:
            for file in os.listdir('.'):
                if fnmatch.fnmatch(file, '*and_pops.txt'):
                    self.__file = file
        else:
            self.__file = file_sideload
        self.__count_pop()
        self.__site_info()

    def __count_pop(self):
        """This function reads the population size for every cite.

        First the file is opend and split on sites.
        Than for every site the population is counted and
         added to a list and dictionary.

        :return: None
        """
        with open(self.__file, 'r', encoding='latin_1') as info:
            file_lines = info.read().splitlines()
            pop_info = file_lines[0:file_lines.index("Sites")]
            self.__file_content = file_lines
            del file_lines
        for population in pop_info[2::]:
            if population != '' and population.strip('\t').split()[0] != \
                    "Total:":
                self.pops.append(population.strip('\t').split(' ')[0])
                self.popsize[population.strip('\t').split(' ')[0]] = \
                    population.strip('\t').split(' ')[1]

    def __site_info(self):
        """
        Here is the site info procesed.
        Fist the metadata is collected than the name en the type of site.
        the info is set in the site dict.

        :return:  None
        """

        sites = []
        site_list = self.__file_content[
                    self.__file_content.index(
                        "Sites") + 1:self.__file_content.index(
                        "Outdoor Animal Populations (Including Undead)")]  # alle tekst met sites
        site_lists = re.split('[0-9]+: ', ''.join(
            site_list))  # een site per line nu
        site_num = 0
        for i in site_lists[1::]:
            site_meta, line_skipe, pop_owner = self.__meta_site_info(i)
            pop_dict = {}
            sites.append(str(site_num) + '\t' + i)
            site_num += 1
            name = "".join(i.split('\t')[0].split(',')[1])
            type = i.split('\t')[0].split(',')[2]

            pop = i.split('\t')[1 + line_skipe::]
            for i in pop:
                pop_dict["".join(i.split(' ')[1:])] = i.split(' ')[0]
            self.sites[name.replace('"', '')] = [pop_owner, type,
                                                 site_meta, pop_dict]
            del site_meta

    def __meta_site_info(self, list):
        """
        This function gets the lineskip. The skip skips the tag
        with info like admin owner en parent.
         This info is added to and site meta dict

        :param list: list with lines per site (list)
        :return: site_meta:  metadata from the site (dict)
        , line_skipe: amount of lines to skip (int)
        , pop_owner: population owner (str)
        """
        site_meta = {}
        line_skipe = 0
        pop_owner = "None"
        for line in list.split("\t"):
            line_skipe, pop_owner = self.__check_meta_stuff(line,
                                                            line_skipe,
                                                            pop_owner,
                                                            site_meta)

        for nobels in ['administrator', 'law_giver', 'Owner', 'Parent',
                       'lord', 'lady']:
            if not nobels in site_meta:
                site_meta[nobels] = 'none'

        return site_meta, line_skipe, pop_owner

    def __check_meta_stuff(self, line, line_skipe, pop_owner,
                           site_meta):
        """ Check if the metadata exist. and add count to lineskip
        add owner info.

        :param line:  list with lines per site (list)
        :param line_skipe: amount of lines to skip (int)
        :param pop_owner: population owner (str)
        :param site_meta:  metadata from the site (dict)

        :return: line_skipe: amount of lines to skip (int)
                  pop_owner: population owner (str)
        """

        if 'Owner:' in line:
            site_meta['Owner'] = line.split(":")[1].split(',')[0]
            pop_owner = line.split(":")[1].split(',')[1].strip()
            line_skipe += 1
        if 'Parent Civ:' in line:
            site_meta['Parent'] = line.split(":")[1].split(',')[0]
            pop_owner = line.split(":")[1].split(',')[1].strip()
            line_skipe += 1
        if 'law-giver:' in line:
            site_meta['law_giver'] = line.split(":")[1].split(',')[
                0]
            pop_owner = line.split(":")[1].split(',')[1].strip()
            line_skipe += 1
        if 'lord' in line:
            site_meta['lord'] = line.split(":")[1].split(',')[0]
            line_skipe += 1
        if 'lady' in line:
            site_meta['lady'] = line.split(":")[1].split(',')[0]
            line_skipe += 1
        if 'administrator' in line:
            site_meta['administrator'] = line.split(":")[1].split(',')[
                0]
            line_skipe += 1
        return line_skipe, pop_owner

    def make_plot_file_normale_civ_pop(self, fileout='plot_text.txt'):
        """
        This function makes the file for the default plot
          The file data structure is : count  pop, civ,owner,name

        :param fileout: output file for the plot info. (str)
        :return: None
        """
        lines_info = []
        for key, items in self.popsize.items():
            pop_size = 0
            for name, info in self.sites.items():
                if info[0].lower() == items.lower():
                    try:
                        lines_info.append(''.join(i + '\t' for i in [
                            info[3][items.lower()], items,
                            info[2]['Parent'], info[2]["Owner"],
                            name.replace('"', '')]) + '\n')
                        pop_size += int(info[3][items.lower()])
                    except:
                        lines_info.append(''.join(str(i) + '\t' for i in
                                                  [0, items,
                                                   info[2]['Parent'],
                                                   info[2]["Owner"],
                                                   name.replace('"',
                                                                '')]) + '\n')
            lines_info.append(
                str(int(key) - pop_size) + '\t' + items + '\n')
        with open(fileout, 'w') as file:
            file.writelines(lines_info)
        if self.debug:
            with open(str(datetime.date.today()) + fileout,
                      'w') as file:
                file.writelines(lines_info)

    def plot_pop_per_civ(self, fileout='plot_text_pop_civ.txt'):
        """
         This function makes the file for the plot per civ
          The file data structure is : count civ,site,organise

        :param fileout: output file for the plot info. (str)
        :return: None
        """
        lines_info = []
        for name, info in self.sites.items():
            if len(info[3]) > 3:
                try:
                    for pop, size in info[3].items():
                        lines_info.append("".join(i + "\t" for i in
                                                  [size,
                                                   info[2]['Parent'],
                                                   name, pop]) + '\n')
                except:
                    for pop, size in info[3].items():
                        lines_info.append("".join(i + "\t" for i in
                                                  [size,
                                                   info[2]['Parent'],
                                                   name, pop]) + '\n')
        with open(fileout, 'w') as file:
            file.writelines(lines_info)
        if self.debug:
            with open(str(datetime.date.today()) + fileout,
                      'w') as file:
                file.writelines(lines_info)


if __name__ == '__main__':
    tester = worldInfoClass(
        "example/region3-01051-02-16-world_sites_and_pops.txt")

    tester.make_plot_file_normale_civ_pop()
    tester.plot_pop_per_civ()

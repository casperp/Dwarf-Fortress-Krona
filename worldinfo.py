import os
import fnmatch
import re
import datetime

class worldInfoClass:
    def __init__(self, file_sideload=None,debug=False):
        """

        :param file_sideload:
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
        """ haald de pop size uit het bestand en plaats het
                in een dicte een een lijst met civs

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
        """ript site info van de txt. haald meta er uit hierna
        de naam en de typer of site. door meta info word de line skip pepaald voor pop info.
        ierna word pop geteld en in de site dict gezet.

        :return:
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
        """haal de meta info er uit site info en parents ect.
        als er een neiwe tag is gewoon toevoegen en dan een check er bij
        lineskipt haald deze info dan uit pop info.

        :param list:
        :return:
        """
        site_meta = {}
        line_skipe = 0
        pop_owner = "None"
        for line in list.split("\t"):
            line_skipe, pop_owner = self.__check_meta_stuff(line,
                                                            line_skipe,
                                                            pop_owner,
                                                            site_meta)


        for nobels in ['administrator','law_giver','Owner','Parent','lord','lady']:
            if not nobels in site_meta:
                site_meta[nobels] = 'none'
        #
        #
        # if not "law_giver" in site_meta:
        #     site_meta['law_giver'] = 'None'
        # if not "Owner" in site_meta:
        #     site_meta['Owner'] = "None"
        # if not "Parent" in site_meta:
        #     site_meta['Parent'] = 'None'
        # if not "lord" in site_meta:
        #     site_meta['lord'] = 'None'
        # if not "lady" in site_meta:
        #     site_meta['lady'] = 'None'
        return site_meta, line_skipe, pop_owner

    def __check_meta_stuff(self, line, line_skipe, pop_owner,
                           site_meta):


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
            site_meta['administrator'] = line.split(":")[1].split(',')[0]
            line_skipe += 1
        return line_skipe, pop_owner

    def make_plot_file_normale_civ_pop(self, fileout='plot_text.txt'):
        """werkt dus neit aanraken.
                hier word de ino gemaakt voor een normale pop plot.
                bestaat uit : aantal, pop, civ,owner,naam"""
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
            with open(str(datetime.date.today())+fileout, 'w') as file:
                file.writelines(lines_info)

    def plot_pop_per_civ(self, fileout='plot_text_pop_civ.txt'):
        """Hier word de andere plot gemaakt. niet gericht op soort sit maar

         text structuur: civ,site,organisme.

         :param fileout:
         :return:
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
            with open(str(datetime.date.today())+fileout, 'w') as file:
                file.writelines(lines_info)

if __name__ == '__main__':
    tester = worldInfoClass(
        "example/region3-01051-02-16-world_sites_and_pops.txt")

    tester.make_plot_file_normale_civ_pop()
    tester.plot_pop_per_civ()



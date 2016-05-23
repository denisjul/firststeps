# -*- coding: utf-8 -*-

""" contains classes """


class Article:
    """ Object containing all the paramaeters
    concerning a law article"""

    def __init__(self):
        # /!\ A remodifier avec la définition
        # des bons types de champs dans le cadre de Django!!! /!\
        self.name = ""
        self.contents = []

    def __repr__(self):
        txt = "=" * 70 + "\n"
        txt += self.name + "\n"
        txt += "=" * 70 + "\n"
        for i in range(len(self.contents)):
            if isinstance(self.contents[i], Tableau):
                txt += self.contents[i].represent + "\n\n"
            else:
                txt += self.contents[i] + "\n\n"
        return txt


class Titre:
    """ containers of Articles or other containers"""

    def __init__(self, rank, name):
        self.rank = rank
        self.name = name
        self.contents = []

    def __repr__(self):
        txt = "*" * 70 + "\n"
        txt += self.name + "\n"
        txt += "RANK: " + str(self.rank) + "\n"
        txt += "*" * 70 + "\n\n\n"
        return txt

    def in_contents(self):
        """ maid for the __repr__ function.
        recusivity must by improved/finished"""
        txt = ""
        if len(self.contents) != 0:
            for i in range(len(self.contents)):
                txt += self.contents[i].__repr__()
                if isinstance(self.contents[i], Article) is not True:
                    txt += self.in_contents(self.contents[i])
        return txt


class Code_de_lois:
    """ A Law code """

    def __init__(self):
        self.name = ""
        self.contents = []

    def __repr__(self):
        txt = "-" * 70 + "\n"
        txt = "-" * 70 + "\n"
        txt += "||" + self.name + "||\n"
        txt = "-" * 70 + "\n"
        txt += "-" * 70 + "\n\n\n"
        txt += self.in_contents()
        return txt

    def in_contents(self):
        """ maid for the __repr__ function. must be completed to
        have recurcivity with contents attribute from Titre class"""
        txt = ""
        if len(self.contents) != 0:
            for i in range(len(self.contents)):
                txt += self.contents[i].__repr__()
                if isinstance(self.contents[i], Article) is not True:
                    txt += self.in_contents(self.contents[i])
        return txt


class Tableau():
    """ Class maid to recover tables from a legifrance page """

    def __init__(self, html):
        self.html = html
        self.tab = self._html_to_tab()
        self.represent = self._get_represent()

    def _html_to_tab(self):
        """ tranform the html source code to a Tableau object"""
        nb_lines = self.html.count('</tr>')
        nb_columns = self.html.count('</th>')
        self.html = self.html.replace('<p>', '')
        self.html = self.html.replace('</p>', '')
        self.html = self.html.replace('<br/>', '')
        self.html = self.html.replace('<tr>', '')
        self.html = self.html.replace('</tr>', '')
        self.html = self.html.replace('<tbody>', '')
        self.html = self.html.replace('</tbody>', '')
        tab = []
        i = 0
        for x in range(nb_lines):
            tab.append([])
            for y in range(nb_columns):
                if x == 0:
                    start = '<th'
                    end = '</th>'
                else:
                    start = '<td'
                    end = '</td>'
                data, i = self._get_something(start,
                                              end, i, code_source=self.html)
                data = data.replace("\n", "")
                tab[x].append(data)
        return tab

    def _get_something(self, start, end, i, code_source=""):
        """ Recover the text between 'start' and 'end' (as str),
        'start' & 'end' excluded"""
        length_start = len(start)
        length_end = len(end)
        buf_start = ""
        buf_end = ""
        text = ""
        flag = True
        while flag:
            i += 1
            buf_start += code_source[i]
            if len(buf_start) >= length_start:
                if buf_start == start:
                    buf = code_source[i]
                    while buf != ">":
                        i += 1
                        buf = code_source[i]
                    while flag:
                        i += 1
                        buf_end += code_source[i]
                        text += code_source[i]
                        if len(buf_end) >= length_end:
                            if buf_end == end:
                                text = text.replace(end, '')
                                flag = False
                            buf_end = buf_end[1: len(end)]
                buf_start = buf_start[1: len(start)]
        return text, i

    def _get_represent(self):
        """ the represent attibute is only made to simplify
        the __repr__ function. _get_represent is maid to set it"""
        nb_columns = len(self.tab[0])
        nb_lines = len(self.tab)
        text = ""
        for x in range(nb_columns):
            text += "-" * 80 + "\n"
            for y in range(nb_lines):
                if y == 0:
                    text += self.tab[y][x] + ": "
                else:
                    text += str(y) + ") " + self.tab[y][x] + "   "
            text += "\n" + "-" * 80 + "\n"
        return text

    def __repr__(self):
        """ display only the column heads """
        return self.represent

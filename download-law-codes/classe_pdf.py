# -*- coding: utf-8 -*-

""" contains classes """

from html_to_ascii_table import Table


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
            if isinstance(self.contents[i], Table):
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

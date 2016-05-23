# -*- coding:utf-8 -*-

# #############################################################################
# ################################   Notes   ##################################
# #############################################################################
"""
1. run the script
2. acces to the codes by listofcodes: for the 'x'th code:
    listofcodes[x][0] or listofcodes[x][2].name: code's title
    listofcodes[x][1]: ref legifrance
    listofcodes[x][2]: the code

*listofcodes[x][2].contents[] will return the main titles of the codes
*listofcodes[x][2].contents[0].contents[] will return the rank 2 titles or
the Articles contained in the first main title of the code
*etc.
"""
# #############################################################################


from classe_pdf import Code_de_lois, Article, Titre, Tableau
import ssl
import urllib.error
import urllib.request
import urllib.parse

# Pour dl en PDF
"""
def dlcodeLEGITEXT(code_LEGITEXT, file_name):  # Pour dl en PDF
    url = "https://www.legifrance.gouv.fr/download_code_pdf.do?cidTexte="\
        + "LEGITEXT" + code_LEGITEXT + "&dlType=pdf"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(url, context=ctx) as u, \
            open(file_name, 'wb') as f:
        f.write(u.read())
"""

# Programme utile


def get_code_data(code_LEGITEXT):  # 2
    """ Recover the data (titles and articles) from a specified code
    (param code LEGITEXT corresponding on Legifrance) """
    url = "https://www.legifrance.gouv.fr/affichCode.do?cidTexte="\
        + "LEGITEXT" + code_LEGITEXT
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    a = urllib.request.urlopen(url, context=ctx)
    code_source = a.read().decode("utf-8")
    code = Code_de_lois()
    buf_15 = ""
    list_title_open = []
    for i in range(len(code_source)):
        buf_15 += code_source[i]
        if len(buf_15) == 15:
            # --------- Code title recovering ---------------
            if buf_15 == 'd="titreTexte">':
                code.name, i = get_title_code(code_source, i)
                code.name = code.name.replace("\r", "")
                code.name = code.name.replace("\t", "")
            # ------- paragraph title recovering ------------
            if buf_15 == '<span class="TM':
                title, i = get_title(code_source, i)
                if title.rank == 1:
                    code.contents.append(title)
                    list_title_open.clear()
                else:
                    for x in range(len(list_title_open) - 1, 0, -1):
                        if list_title_open[x].rank >= title.rank:
                            list_title_open.remove(list_title_open[x])
                    list_title_open[-1].contents.append(title)
                list_title_open.append(title)
            # -- Articles contained in the last paragraph Title recovering --
            if buf_15 == '="codeLienArt">':
                link, i = get_link_articles(code_source, i)
                list_title_open[len(list_title_open) - 1].contents = \
                    get_articles(link)
            buf_15 = buf_15[1:15]
    return code


def get_articles(link):
    """ detect, select and copy all articles from a Legifrance page """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    b = urllib.request.urlopen(link, context=ctx)
    cs_article = b.read().decode("utf-8")
    contents = []
    new_article = Article()
    buf = ""
    for j in range(len(cs_article)):
        buf += cs_article[j]
        if len(buf) >= 21:
            if buf == '<div class="article">':
                new_article.name, j = get_something(cs_article,
                                                    '<div class="titreArt">',
                                                    '<a',
                                                    j)
                text, j = get_something(cs_article,
                                        'class="corpsArt">',
                                        '</div>',
                                        j)
                new_article.contents = recover_article(text)
                contents.append(new_article)
                new_article = Article()
            buf = buf[1:21]
    return contents


def get_something(code_source, start, end, i):
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


def recover_article(text):
    """recover the entire article (text & table parts)"""
    text = text.replace('<center>', "")
    text = text.replace('</center>', "")
    if text[0:5] == '<br/>':
        text = text[5:len(text) - 1]
    article = []
    i = 0
    buf_get_table = text[0:7]
    art_part = ""
    while i < len(text):
        if buf_get_table == "<table ":
            article.append(clean_article_text(art_part))
            art_part = ""
            i += 7
        elif buf_get_table == "/table>":
            i += 7
            tab = Tableau(art_part)
            article.append(tab)
            art_part = ""
        art_part += text[i]
        i += 1
        buf_get_table = text[i:i + 7]
    article.append(clean_article_text(art_part))
    return article


def clean_article_text(text):
    """ remove all html to keep the text """
    text = text.replace('<p>', '')
    text = text.replace('</p>', '')
    text = text.replace('<p/>', '')
    text = text.replace('</a>', '')
    text = text.replace('<br/>', '\n')
    text = remove_piece_of_text(text, '<a', '">')
    return text


def remove_piece_of_text(text, start, end):
    """remove the text between 'start' and 'end' str,
        'start' & 'end' encluded"""
    length_start = len(start)
    length_end = len(end)
    buf = ""
    new_text = ""
    flag = True
    i = 0
    for i in range(len(text)):
        buf += text[i]
        if flag:
            new_text += text[i]
        if len(buf) == length_start:
            if buf == start:
                new_text = new_text[0:len(new_text) - length_start]
                flag = False
        if len(buf) == length_end:
            if buf == end:
                flag = True
            buf = buf[1:2]
    return new_text


def get_link_articles(code_source, i):  # 2.c
    i += 11
    buf = ""
    link = ""
    flag = True
    while flag:
        i += 1
        link += code_source[i]
        buf += code_source[i]
        if len(buf) >= 2:
            if buf == '">':
                flag = False
            buf = buf[1:2]
    link = link.replace('">', '')
    link = link.replace('&amp;', '&')
    link = "https://www.legifrance.gouv.fr/" + link
    return link, i


def get_title(code_source, i):  # 2.b
    """ record a title from a chapter, book, part, etc.
    from a law code, with his rank
    (ex:a book rank> a part rank> a chapter rank...)"""
    i += 1
    rank = int(code_source[i])
    i += 32
    buf = ""
    titre = ""
    flag = True
    while flag:
        i += 1
        titre += code_source[i]
        buf += code_source[i]
        if len(buf) >= 2:
            if buf == '</':
                flag = False
            buf = buf[1:2]
    titre = titre.replace('</', '')
    NewTitle = Titre(rank, titre)
    return NewTitle, i


def get_title_code(code_source, i):  # 2.a
    """ Recover the title of a law code"""
    buf = ""
    titre = ""
    flag = True
    while flag:
        i += 1
        titre += code_source[i]
        buf += code_source[i]
        if len(buf) >= 5:
            if buf == '<span':
                flag = False
            buf = buf[1:5]
    titre = titre.replace('\n', '')
    titre = titre.replace('<br/>', '')
    titre = titre.replace('<span', '')
    i += 1
    return titre, i


def get_LEGITEXT_ref(code_source, i):  # 1.1
    """ recover a Legifrance law code reference with his title
    return a tuple with """
    code_ref = ""
    title = ""
    for j in range(12):
        code_ref += code_source[i]
        i += 1
    i += 9
    while code_source[i] != '"':
        title += code_source[i]
        i += 1
    title = title.replace("&#39;", "'")
    return [title, code_ref, ""], i


def Get_codes_ref():  # 1
    """ recover all the legifrance law code reference"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = "https://www.legifrance.gouv.fr/initRechCodeArticle.do"
    a = urllib.request.urlopen(url, context=ctx)
    code_source = a.read().decode("utf-8")
    list_of_codes = []
    buf_23 = ""
    for i in range(len(code_source)):
        buf_23 += code_source[i]
        if len(buf_23) == 23:
            if buf_23 == '<option value="LEGITEXT':
                i += 1
                ref_legitext, i = get_LEGITEXT_ref(code_source, i)
                if ref_legitext not in list_of_codes:
                    list_of_codes.append(ref_legitext)
            buf_23 = buf_23[1:len(buf_23)]
    return list_of_codes


listofcodes = Get_codes_ref()
for x in range(len(listofcodes)):
    listofcodes[x][2] = get_code_data(listofcodes[x][1])

"""
Test instructions:

code = get_code_data("000006075116")

link = 'https://www.legifrance.gouv.fr/affichCode.do;jsessionid=A9AC8977D52FB09BD905F2970370E00D.tpdila10v_3?idSectionTA=LEGISCTA000006132295&cidTexte=LEGITEXT000006075116&dateTexte=20160516'
page_contents = get_articles(link)
"""

import matplotlib.pyplot as plt
import statistics as st

def get_id(manga_dict):
    try:
        id = manga_dict["id"]
    except:
        print('Error al intentar obtener el id del manga')
        id = ""
    return id

def get_title(manga_dict):
    try:
        title = list(manga_dict["attributes"]["title"].values())[0]
    except:
        print('Error al intentar obtener el título del manga')
        title = ""
    return title

def get_altTitles(manga_dict):
    try:
        altTitles = manga_dict["attributes"]["altTitles"]
    except:
        print('Error al intentar obtener los títulos alternos del manga')
        altTitles = ""
    return altTitles

def get_description(manga_dict):
    try:
        for lang in ["en", "es-la", "ja", "fr", "ko"]:
            desc = manga_dict["attributes"]["description"].get(lang, "")
            if desc:
                break
        if not desc:
            desc = list(manga_dict["attributes"]["description"].values())[0]
    except:
        print('Error al intentar obtener la descripción del manga')
        desc = ""
    return desc

def get_contentRating(manga_dict):
    try:
        contentRating = manga_dict["attributes"]["contentRating"]
    except:
        print('Error al intentar obtener la clasificación del contenido del manga')
        contentRating = ""
    return contentRating

def get_tags(manga_dict):
    try:
        tags_dict = manga_dict["attributes"]["tags"]
        tags_list = list()
        for tag in tags_dict:
            tags_list.append(tag["attributes"]["name"]["en"])

    except:
        print('Error al intentar obtener las etiquetas del manga')
        tags_list = ""
    return tags_list

def get_stat_comms(manga_stat_dict):
    msd = manga_stat_dict
    manga_id = list(msd["statistics"].keys())[0]
    try: 
        comments = msd["statistics"][manga_id]["comments"]["repliesCount"]

    except:
        #print('Error al intentar obtener los comentarios')
        comments = 0
    return comments

def get_stat_ratings(manga_stat_dict):
    msd = manga_stat_dict
    manga_id = list(msd["statistics"].keys())[0]
    try: 
        ratings = msd["statistics"][manga_id]["rating"]

    except:
        print('Error al intentar obtener las estadísticas')
        ratings = None
    return ratings

def get_stat_follows(manga_stat_dict):
    msd = manga_stat_dict
    manga_id = list(msd["statistics"].keys())[0]
    try: 
        follows = msd["statistics"][manga_id]["follows"]

    except:
        print('Error al intentar obtener los seguidores')
        follows = ""
    return follows

def get_stat_dist(manga_stat_dict):
    msd = manga_stat_dict
    try:
        dist = get_stat_ratings(msd)["distribution"]
    
    except:
        print('Error al intentar obtener la distribución de la puntuación')
        dist = None
    return dist

def p(func):
    def dec(*args, **kwargs):
        s = func(*args, **kwargs)
        print(s)
        print()
        return s
    return dec

@p
def plot_dist(manga_dict, manga_stat_dist):
    manga_dist = get_stat_dist(manga_stat_dist)
    fig, ax = plt.subplots()
    ax.bar(
        manga_dist.keys(), 
        manga_dist.values(), 
        1, edgecolor='k')
    ax.set_title(f'Puntuaciones de {get_title(manga_dict)}')
    ax.set_xlabel('Puntuación')
    ax.set_ylabel('Recuento')
    ax.grid(axis='y')
    fig.show()

    values = []
    for score, count in manga_dist.items():
        values += [int(score)] * count

    s  = 'Estadísticas' + '\n'
    s += f'{"Media":>20}: {st.mean(values):.2f}\n'
    s += f'{"Media armónica":>20}: {st.harmonic_mean(values):.2f}\n'
    s += f'{"Media geométrica":>20}: {st.geometric_mean(values):.2f}\n'
    s += f'{"Desviación estándar":>20}: {st.stdev(values):.2f}\n'
    s += f'{"Varianza":>20}: {st.variance(values):.2f}\n'
    return s

@p
def print_id(manga_dict):
    s = f'ID: {get_id(manga_dict)}'
    return s

@p
def print_title(manga_dict):
    s = f'Título: {get_title(manga_dict)}'
    return s

@p
def print_altTitles(manga_dict):
    s = 'Títulos alternos:\n'
    for altTitle in get_altTitles(manga_dict):
        lang, title = list(altTitle.items())[0]
        s += f'{lang}: {title}\n'
    return s

@p
def print_description(manga_dict):
    s  = 'Descripción:\n'
    s += get_description(manga_dict) + '\n'
    return s

@p
def print_contentRating(manga_dict):
    s = f'Clasificación de contenido: {get_contentRating(manga_dict)}'
    return s

@p
def print_tags(manga_dict):
    s  = f'Etiquetas:\n{get_tags(manga_dict)}'
    return s

@p
def print_comms(_, manga_stat_dict):
    s = f'Comentarios: {get_stat_comms(manga_stat_dict)}'
    return s

@p
def print_follows(_, manga_stat_dict):
    s = f'Seguidores: {get_stat_follows(manga_stat_dict)}'
    return s

attr_dict = {
        0: print_title,
        1: print_id,
        #2: print_title,
        2: print_altTitles,
        3: print_description,
        4: print_contentRating,
        5: print_tags,
    }
stat_dict = {
        6: print_comms,
        7: plot_dist,
        8: print_follows,
}
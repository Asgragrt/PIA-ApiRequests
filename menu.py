import api_requests as ar
import re
import manga_data as md
import file_handler as fh

def search():
    while True:
        print('Sugerencias de búsqueda:')
        print(*[
            '-Solo Leveling',
            '-That Time I Got Reincarnated as a Slime', 
            '-One-Punch Man',
            '-Chainsaw Man',
            '-Berserk',
            '-Frieren: Beyond Journey\'s End',
            '-Moon-led Journey Across Another World',
            '~-'*50,
            ], sep="\n")
        title = input('Ingrese el título que está buscando: ')

        data = ar.api_search(title)

        if not data:
            print('No se encontró ningún manga con ese nombre.')
            val = input('Si desea volver a intentar, presione 1: ')
            if val != '1':
                return None
        else:
            break
    return data

def val_idx(l, ub, lb = 0):
    manga_idx = list()
    for i in l:
        j = int(i)
        if lb < j <= ub:
            if j not in manga_idx:
                manga_idx.append(j)
        else:
            print(f'Se ignorará el valor {i} ya que está fuera de límites')
    return manga_idx

def select(data, s):
    op = s == 'los mangas'
    print('Si desea repetir la búsqueda, escriba "r"\n'*op, end='')
    while True:
        in_read = input(f'Ingrese los números de {s} de interés separados por caracter no numérico: ')
        if in_read == 'r' and op:
            return None
        
        idxs = re.findall(r'\b\d+\b', in_read)
        if idxs := val_idx(idxs, len(data)):
            break
    return idxs

def search_n_select():
    selection = None
    while not selection:
        if not (data := search()):
            return None
        
        print()
        print('Resultados de la búsqueda:')
        for index, manga in enumerate(data, 1):
            print(f'{index} - {md.get_title(manga)}')

        selection = select(data, 'los mangas')

    return [data[i - 1] for i in selection]

def info(manga):
    info = [
        'ID',
        'Títulos alternos',
        'Descripción',
        'Clasificación del contenido',
        'Etiquetas',
        'Cantidad de comentarios',
        'Distribución de la puntuación',
        'Cantidad de seguidores'
    ]
    print('~-'*50)
    print(f'Datos que se pueden obtener de {"~"*3 + " "*3}{md.get_title(manga)}{" "*3 + "~"*3}: ')
    for i, option in enumerate(info, 1):
        print(f'{i} - {option}')

    selected = [0] + select(info, 'los datos')
    info = ['Título'] + info

    manga_info = dict()

    if attrs := ( set(selected) & set( md.attr_dict.keys() ) ):
        for attr in attrs:
            manga_info[info[attr]] = md.attr_dict[attr](manga)

    if stats := ( set(selected) & set( md.stat_dict.keys() ) ):
        manga_stat = ar.api_stats(manga)
        for stat_idx in stats:
            manga_info[info[stat_idx]] = md.stat_dict[stat_idx](manga, manga_stat)

    op = input('¿Desea guardar los datos en un archivo? 1-Si: ')
    if op != '1':
        return None
    
    fh.open_save(manga_info)

def file_read():
    if not ( wb := fh.open()):
        print('No se puede realizar la lectura')
        return None
    
    print(f'Hay {len(wb.get_sheet_names())} consultas almacenadas')
    for sn in wb.get_sheet_names():
        print('~-'*50)
        print('De esta consulta se encuentran los siguientes datos:\n')
        ws = wb.get_sheet_by_name(sn)
        data = fh.read_sheet(ws)

        for elem in select(data[1:], 'los datos'):
            print(data[elem][1])

        op = input('Si desea eliminar esta consulta presione 1: ')
        rs = False
        if op == '1':
            rs = fh.del_sheet(wb,ws)
    if not rs:
        fh.save(wb)
    print()
    print('~-'*50)

def search_info():
    if not (selected_mangas := search_n_select()):
        return None
    for manga in selected_mangas:
        if manga:
            info(manga)
    print()
    print('~-'*50)

def menu():
    while True:
        options = [
            'Para realizar una búsqueda',
            'Para revisar las consultas anteriores',
            'Para salir',
        ]

        print(f'{"~"*3 + " "*3}Menú{" "*3 + "~"*3}\nPresione:')
        for i, option in enumerate(options, 1):
            print(f'{i} - {option}')

        while True:
            op = input('Selección: ')
            try:
                if int(op) not in range(1, len(options) + 1):
                    print('Opción no válida')
                else:
                    break
            except:
                print('Opción no válida')
        
        print('~-'*50)
        if op == '1':
            search_info()
        elif op == '2':
            file_read()
        else:
            print('Gracias por usar el servicio de consulta!')
            break
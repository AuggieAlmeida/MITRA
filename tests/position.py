# Variáveis Globais
x1 = y1 = 0  # Armazenam a posição inicial de x e y

print('''Botão Esquerdo: 'place' Clique na posição inicial e arraste até a posição final
Botão Direitro:   'geometry' Mostra as medidas para o posicionamento da janela "geometry"
''')


def start_place(arg):
    global x1, y1
    x1 = arg.x
    y1 = arg.y


def end_place(arg, root):
    global x1, y1
    print(f'Coordinates! .place(width={arg.x - x1}, height={arg.y - y1}, x={x1}, y={y1})')
    root.clipboard_clear()
    root.clipboard_append(f'.place(width={arg.x - x1}, height={arg.y - y1}, x={x1}, y={y1})')


def para_geometry(root):
    print(f'Coordinates! .geometry("{root.geometry()}")')
    root.clipboard_clear()
    root.clipboard_append(f'.geometry("{root.geometry()}")')


# FIM DA FUNÇÃO
def position():
    return None

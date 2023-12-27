from clientDraw import Create_Draw

def process_data(coordenada, caracter_nuevo):
    # Abre el archivo en modo lectura
    with open('draw.txt', 'r') as file:
        lines = file.readlines()
    caracter_nuevo='◾' if caracter_nuevo==1 else '◽'
    # Modifica el caracter en la coordenada especificada
    y, x = coordenada
    if 0 <= y < len(lines) and 0 <= x < len(lines[y]):
        nueva_linea = lines[y][:x] + caracter_nuevo + lines[y][x+1:]
        lines[y] = nueva_linea

    # Escribe los cambios de vuelta al archivo
    with open('draw.txt', 'w') as file:
        file.writelines(lines)

for data in Create_Draw().split():
    data=data.split(',')
    coordinates=(int(data[1]),int(data[0]))
    process_data(coordinates,int(data[2]))
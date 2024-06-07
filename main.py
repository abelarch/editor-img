import PySimpleGUI as sg
import cv2, imutils, os
from PIL import Image

sg.theme('DarkTeal9')

 # ------ Menu Definition ------ #
menu_def = [['&Archivo', ['&Abrir', '&Salir']],
            ['&Edición', ['&Traslacion', '&Rotacion', 'T&amaño', ['Sin Proporcion', 'Proporcional'], '&Espejado', ['Horizontal', 'Vertical', 'Ambos'], 'Re&corte'], ],
            ['&Help', '&About...'], ]

#ancho y alto para el frame de la imagen cargada
ancho = 500
alto = 450

# Imagen cargada
imagen_cargada = None

# Imagen modificada
imagen_mod = None

def win_main():
    layout = [  [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
                [sg.Frame('Imagen', 
                        [[sg.Image(key='img', size=(ancho, alto))] 
                        ]
                )],
                [sg.Button('Original'), sg.Button('Guardar'), sg.Button('Deshacer'), sg.Button('Detalles'), sg.Button('Limpiar'), sg.Button('Salir')],
            ]
    return sg.Window('Editor de Fotos', layout, finalize=True)

#Crea ventana Traslación
def win_translation():
    layout = [ [sg.T('Traslación en X'), sg.InputText("0", key="-TRANSLATE-X-", size=(5, 1))],
            [sg.T('Traslación en Y'), sg.InputText("0", key="-TRANSLATE-Y-", size=(5, 1))],
            [sg.Button('Aceptar', key='-TRANSLATE-')],
    
    ]
    return sg.Window('Traslación', layout, finalize=True)

#Crea ventana Rotación
def win_rotate():
    layout = [ [sg.T('Rotación', size=(10,1)), sg.InputText("0", key="-ROTATE-ANG-", size=(5, 1))],
            [sg.Button('Aceptar', key='-ROTATE-')],
    
    ]
    return sg.Window('Rotación', layout, finalize=True)

#Crea ventana Redimensión NP
def win_resize_not_prop():
    layout = [ [sg.Text("Altura:", size=(10, 1)), sg.InputText("0", key="-NEW-ALTO-", size=(5, 1))],
            [sg.Text("Anchura:", size=(10, 1)), sg.InputText("0", key="-NEW-ANCHO-", size=(5, 1))],
            [sg.Button('Aceptar', key='-RESIZE-')],
    ]
    return sg.Window('Cambiar Tamaño', layout, finalize=True)

#Crea la ventana redimension proporcional
def win_resize_prop():
    layout = [ [sg.Text("Altura:", size=(10, 1)), sg.InputText("0", key="-NEW-ALTO-P", size=(5, 1))],
            [sg.Text("Anchura:", size=(10, 1)), sg.InputText("0", key="-NEW-ANCHO-P", size=(5, 1))],
            [sg.Button('Aceptar', key='-RESIZE-P-')],
    ]
    return sg.Window('Cambiar Tamaño', layout, finalize=True)

#Crea la ventana recorte
def win_crop():
    layout = [ [sg.Text("Inicio Y:", size=(10, 1)), sg.InputText("0", key="START-Y", size=(5, 1))],
            [sg.Text("Fin Y:", size=(10, 1)), sg.InputText("0", key="END-Y", size=(5, 1))],
            [sg.Text("Inicio X:", size=(10, 1)), sg.InputText("0", key="START-X", size=(5, 1))],
            [sg.Text("Fin X:", size=(10, 1)), sg.InputText("0", key="END-X", size=(5, 1))],
            [sg.Button('Aceptar', key='-CROP-')],
    ]
    return sg.Window('Recortar', layout, finalize=True)

# Función para redimensionar la imagen
def resize_image(image_path, size):
    img = Image.open(image_path)
    img = img.resize(size, Image.LANCZOS)
    return img

# Función para convertir la imagen a formato que PySimpleGUI pueda mostrar
def convert_to_bytes(image, format='PNG'):
    from io import BytesIO
    bio = BytesIO()
    image.save(bio, format=format)
    return bio.getvalue()


window1, window2 , window3, window4, window5, window6= win_main(), None, None, None, None, None

# Pila para mantener el historial de estados de la imagen
history = []

# Loop para porcesar los "events" y obener los "values" de los imputs
while True:
    window, event, values = sg.read_all_windows()
    if event in (sg.WIN_CLOSED, 'Salir'): # if user closes window or clicks cancel
        window.close()
        if window == window2:       # if closing win 2, mark as closed
            window2 = None
        elif window == window3: # if closing win 3, mark as closed
            window3 = None
        elif window == window4: # if closing win 4, mark as closed
            window4 = None
        elif window == window5: # if closing win 5, mark as closed
            window5 = None
        elif window == window6: # if closing win 6, mark as closed
            window6 = None
        elif window == window1:     # if closing win 1, exit program
            break

    elif event == 'Abrir':
        ruta_archivo = sg.popup_get_file('file to open', no_window=True, file_types=(("Archivos JPEG", "*.jpg"), ("Archivos PNG", "*.png")))
        imagen_cargada = cv2.imread(ruta_archivo) #Lee la imagen de la ruta
        history.append(imagen_cargada)
        imagen_mod = imagen_cargada.copy()  # Copia la imagen original
        resized_image = resize_image(ruta_archivo, (ancho, alto))  # Redimensiona a píxeles
        image_bytes = convert_to_bytes(resized_image) #Convierte a bytes
        window['img'].update(data=image_bytes) #Actualiza la ventana con la imagen

    elif event == 'Original':
        if imagen_cargada is not None:
            cv2.imshow('Original', imagen_cargada)
        else: sg.popup('Error. No se ha encontrado ningún archivo', title='Error')
    
    if event == "Deshacer":
        if len(history) > 1:
            # Eliminar el último estado (cambio actual)
            history.pop()
            # Obtener el estado anterior
            previous_image = history[-1]
            # Actualizar la imagen en la ventana
            cv2.imshow('Resultado', previous_image)

    elif event == 'Traslacion':
        win_translation()
    elif event == "-TRANSLATE-":
        if imagen_cargada is not None:
            x = int(values["-TRANSLATE-X-"])
            y = int(values["-TRANSLATE-Y-"])
            imagen_mod = imutils.translate(imagen_cargada, x, y)
            cv2.imshow('Resultado', imagen_mod)
            #Guarda la modificacion en la lista
            history.append(imagen_mod)

    elif event == "Rotacion":
        win_rotate()
    elif event == "-ROTATE-":
        if imagen_cargada is not None:
            # ángulo de rotación
            angulo = int(values["-ROTATE-ANG-"])
            # Centro de la imagen
            (h, w) = imagen_cargada.shape[:2]
            centro = (w // 2, h // 2)
            
            # Matriz de rotación
            M = cv2.getRotationMatrix2D(centro, angulo, 1.0)
            
            # Aplicar la rotación
            imagen_mod = cv2.warpAffine(imagen_cargada, M, (w, h)) 
            cv2.imshow('Resultado', imagen_mod)
            history.append(imagen_mod)
        
    elif event == "Sin Proporcion":
        win_resize_not_prop()
    #Sin proporcion
    elif event == "-RESIZE-":
        if imagen_cargada is not None:
            new_alto = int(values["-NEW-ALTO-"])
            new_ancho = int(values["-NEW-ANCHO-"])
            if new_alto and new_ancho:
                imagen_mod = cv2.resize(imagen_cargada, (new_ancho, new_alto), interpolation= cv2.INTER_AREA)
                cv2.imshow('Resultado', imagen_mod)
                history.append(imagen_mod)
            else: sg.popup("Por favor, ingrese valores válidos...", title="Error")
    
    elif event == "Proporcional":
        win_resize_prop()
    #Manteniendo proporción    
    elif event == "-RESIZE-P-":
        if imagen_cargada is not None:
            height = int(values["-NEW-ALTO-P"])
            width = int(values["-NEW-ANCHO-P"])
            # Extraemos las dimensiones originales.
            (original_height, original_width) = imagen_cargada.shape[:2]
            # Si el nuevo ancho es vacío (*width*), calcularemos la relación de aspecto con base a la nueva altura (*height*)
            if height and not width:
                # Proporción para mantener la relación de aspecto con base a la nueva altura.
                ratio = height / float(original_height)
                # Nueva anchura
                width = int(original_width * ratio)
            else: 
                # Proporción para mantener la relación de aspecto con base a la nueva anchura.
                ratio = width / float(original_width)
                # Nueva altura
                height = int(original_height * ratio)
            new_size = (width, height)
            imagen_mod = cv2.resize(imagen_cargada, new_size, interpolation= cv2.INTER_AREA)
            cv2.imshow('Resultado', imagen_mod)
            history.append(imagen_mod)
    
    #Espejado
    elif event == 'Horizontal':
        if imagen_cargada is not None:
            imagen_mod = cv2.flip(imagen_cargada, 1)
            cv2.imshow("Resultado", imagen_mod)
            history.append(imagen_mod)

    elif event == 'Vertical':
        if imagen_cargada is not None:
            imagen_mod = cv2.flip(imagen_cargada, 0)
            cv2.imshow("Resultado", imagen_mod)
            history.append(imagen_mod)

    elif event == 'Ambos':
        if imagen_cargada is not None:
            imagen_mod = cv2.flip(imagen_cargada, -1)
            cv2.imshow("Resultado", imagen_mod)
            history.append(imagen_mod)
    
    #Recorte
    elif event == 'Recorte':
        win_crop()
    elif event == '-CROP-':
        start_y = int(values["START-Y"])
        end_y = int(values["END-Y"])
        start_x = int(values["START-X"])
        end_x = int(values["END-X"])
        if imagen_cargada is not None:
            if end_y > start_y and end_x > start_x:
                imagen_mod = imagen_cargada[start_y:end_y , start_x:end_x]
                cv2.imshow("Resultado", imagen_mod)
                history.append(imagen_mod)
            else: sg.popup("Por favor, ingrese valores válidos...", title="Error") 
    
    #Guardado
    elif event == 'Guardar':
        if imagen_mod is not None:
            file_name = sg.popup_get_file("Guardar como", save_as=True, file_types=(("Archivos PNG", "*.png"), ("Archivos JPEG", "*.jpg")), no_window=True)
            if file_name:
                # Guardar la imagen
                cv2.imwrite(file_name, history[-1])
                sg.popup("Imagen guardada con éxito.")

    elif event == 'Limpiar':
        imagen_cargada = None
        imagen_mod = None
        window['img'].update(data='', size=(ancho, alto))
        cv2.destroyAllWindows()

    elif event == 'Detalles':
        if imagen_cargada is not None:
            alto_px = imagen_cargada.shape[0]
            ancho_px = imagen_cargada.shape[1]
            canales = imagen_cargada.shape[2]
            size_file = os.path.getsize(ruta_archivo)  
            size_kb = size_file // 1024 
            sg.popup('Detalles de la Imagen:', 'Alto: '+str(alto_px)+'px', 'Ancho: '+str(ancho_px)+'px',
                     'Canales: '+str(canales), 'Tamaño: '+str(size_kb)+'Kb', grab_anywhere=True)
    
    elif event == 'About...':
            window.disappear()
            sg.popup('About this program', 'Version 1.0',
                     'PySimpleGUI Version', sg.version,  grab_anywhere=True)
            window.reappear()

cv2.destroyAllWindows()
window.close()
# -*- coding: utf-8 -*-
"""
PIV: Flujo óptico

@author: Daniel Santiago
"""

# Importar librerías


# Crear objeto de cámara, asignado a un video


# Adquirir un primer frame de la cámara


# Convertir primer frame a escala de grises. Este será el frame pasado


# Generar una matriz HSV con las dimensiones del frame
# Asignar a la capa S, un valor de 255

# Loop de análisis de video

    # Obtener sgt frame del video
    
    # Convertir frame a escala de grises
    
    # Función de flujo óptico dense
    
    # Obtener magnitud y fase de la salida del paso anterior
    
    # Ubicar la fase en la capa H, y la magnitud en la capa V
    
    # Pasar de HSV a BGR
    
    # Mostrar resultado
    
    # Actualizar valor del frame pasado
    

# Finalizar
















    
# %%
import numpy as np
import cv2

cap = cv2.VideoCapture(r'C:\Users\Lepi\Downloads\Video(1).mp4')

_, frame = cap.read()

old_gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

hsv = np.zeros_like(frame)

hsv[..., 1] = 255

while(True):
    ok, frame = cap.read()
    if not ok:
        print("[INFO] Se ha alcanzado el límite del archivo")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    flow = cv2.calcOpticalFlowFarneback(old_gray_frame, 
                                       gray_frame, 
                                       None, 
                                       0.5, 3, 15, 3, 5, 1.2, 0)
    
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    
    hsv[..., 0] = ang*180/np.pi/2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
                   
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    cv2.imshow('Ventana', bgr)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'):
        cv2.imwrite('opticalfb.png', frame)
        cv2.imwrite('opticalhsv.png', bgr)
    old_gray_frame = gray_frame

cv2.destroyAllWindows()
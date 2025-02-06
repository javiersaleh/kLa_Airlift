import cv2

# Defining video path and the ranges of saving frames
video_path = "C:/Users/javie/OneDrive/Documentos/Tracking bubbles/Nuevos Videos/col28_fl05/IMG_1773.mov"
start_frame=500
end_frame=600

# Charging the video
video=cv2.VideoCapture(video_path)

# Obtaining video info
fps=int(video.get(cv2.CAP_PROP_FPS))
total_frames=int(video.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width=int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height=int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Establecer el cursor en el primer frame que se desea guardar
video.set(cv2.CAP_PROP_POS_FRAMES,start_frame)

# Recorrer los frames y guardarlos en formato de imagen
for i in range(start_frame,end_frame):
    ret,frame=video.read()
    if ret:
        cv2.imwrite("C:/Users/javie/OneDrive/Escritorio/prueba extraccion frames//frames/frame{}.png".format(i),frame)
    else:
        break

# Liberar el objeto de video
video.release()
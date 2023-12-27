import tkinter as tk
import math

def Create_Draw():
    
    entrada=[[0 for k in range(50)] for j in range(50)]
    def condicion(x,y):
        return x>=0 and x<50 and y>=0 and y<50
    def transform(a):
        return int(math.floor(a/10))
    
    def start_draw(event):
        global last_x,last_y
        last_x,last_y=event.x,event.y
        tx,ty=transform(event.x),transform(event.y)
        if(condicion(tx,ty)):
            entrada[tx][ty]=1
    def draw(event):
        global last_x,last_y
        canvas.create_line((last_x,last_y,event.x,event.y),fill='black',width=20)
        last_x,last_y=event.x,event.y
        tx,ty=transform(event.x),transform(event.y)
        if(condicion(tx,ty)):
            entrada[tx][ty]=1
    def delete():
        canvas.delete('all')
        for i in range(50):
            for j in range(50):
                entrada[i][j]=0
    def send():
        ventana.destroy()
    
    ventana = tk.Tk()
    canvas = tk.Canvas(ventana,width=500,height=500,bg='white')
    canvas.pack(padx=10,pady=10)
    canvas.bind('<Button-1>',start_draw)
    canvas.bind('<B1-Motion>',draw)
    boton_send=tk.Button(ventana,text='Send',command=send)
    boton_send.pack(padx=10,pady=10)
    boton_delete=tk.Button(ventana,text='Delete',command=delete)
    boton_delete.pack(padx=10,pady=10)
    last_x,last_y=None,None
    ventana.mainloop()
    STREntry=""
    for i in range(0,50):
        for j in range(0,50):
            STREntry+=f"{i},{j},{entrada[i][j]} "
    return STREntry
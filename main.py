import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import os
import functions

def browse_path_func():
    path = tkinter.filedialog.askdirectory()
    if path == '':
        return
    if os.path.isdir(path+'/bin'):
        game_dir_label.config(text=path)
        config['game_path'] = path
        functions.json_save(config, 'config.json')
        if not os.path.isdir(path+'/mod_manager'):
            os.mkdir(path+'/mod_manager')
    else:
        tk.messagebox.showerror('Error', 'This is not minecraft directory!')

window = tk.Tk()
window.title('Minecraft Mod Manager')
window.geometry('600x500')

background = tk.Canvas(window, width=600, height=500, bg='#297bff')
background.pack()

config_preset = {
    'game_path': None
}

if not os.path.isfile('config.json'):
    open('config.json', 'w').close()
    functions.json_save(config_preset, 'config.json')

config = functions.json_load('config.json')

game_dir_label = tk.Label(window, bd=3, width=60, text=config['game_path'])
game_dir_label.place(rely=0.925, relx=0.05)
game_dir_button = tk.Button(window, text='Browse', command=browse_path_func)
game_dir_button.place(rely=0.925, relx=0.85)

window.mainloop()
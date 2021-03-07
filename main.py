import tkinter as tk
import os, functions, tkinter.messagebox, tkinter.filedialog, shutil

class Mod():
    def __init__(path, name, version):
        self.path = path
        self.name = name
        self.verison = version
        self.loaded = False

    def version():
        return self.version
    
    def path():
        return self.path

    def name():
        return self.name

    def load():
        self.loaded = True
    
    def unload():
        self.loaded = False

    def is_loaded():
        return self.loaded

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
        if not os.path.isdir(path+'/mods'):
            os.mkdir(path+'/mods')  

    else:
        tk.messagebox.showerror('Error', 'This is not minecraft directory!')

def version_selection_menu():

    def create_new_version():

        def confirm_new_version():
            version_name = entry_box.get()
            if '/' in version_name:
                tk.messagebox.showerror('Invalid version name', 'Version name can not have any "/" in it!')
                return
            if os.path.isdir(config['game_path']+f'/mod_manager/{version_name}'):
                tk.messagebox.showerror('Invalid version name', 'Version with selected name already exist!')
                return

            os.mkdir(config['game_path']+f'/mod_manager/{version_name}')
            os.mkdir(config['game_path']+f'/mod_manager/{version_name}/mods')
            os.mkdir(config['game_path']+f'/mod_manager/{version_name}/profiles')
            version_list.delete('0', 'end')
            
            for version in os.listdir(config['game_path']+'/mod_manager'):
                version_list.insert(0, version)

            entry_box.place_forget()
            confirm_button.place_forget()

        entry_box = tk.Entry(select_menu)
        entry_box.place(rely=0.875, relx=0.1)
        confirm_button = tk.Button(select_menu, text='Confirm', command=confirm_new_version)
        confirm_button.place(rely=0.865, relx=0.42)

    def delete_version():
        selection = version_list.get('active')
        if selection == '':
            return

        msgbox = tk.messagebox.askquestion('Are you sure?', 'This action will delete version and all profiles and mods corelated with it.', icon='warning')
        if msgbox == 'yes':
            shutil.rmtree(config['game_path']+f'/mod_manager/{selection}')
            
            version_list.delete('0', 'end')
            
            for version in os.listdir(config['game_path']+'/mod_manager'):
                version_list.insert(0, version)
        else:
            return

    def select_version():
        selection = version_list.get('active')
        version_label.config(text=selection)
        config['selected_version'] = selection
        functions.json_save(config, 'config.json')
        select_menu.destroy()

    if config['game_path'] == 'Select game path':
        tk.messagebox.showerror('Error', 'Select the game folder first!')
        return

    select_menu = tk.Toplevel(window)
    select_menu.title('Version selection')   
    select_menu.resizable(width=False, height=False)
    select_menu.geometry('400x250')
    
    new_version_button = tk.Button(select_menu, text='New', height=2, width=10, command=create_new_version)
    new_version_button.place(rely=0.15, relx=0.7)
    del_version_button = tk.Button(select_menu, text='Delete', height=2, width=10, command=delete_version)
    del_version_button.place(rely=0.35, relx=0.7)
    select_version_button = tk.Button(select_menu, text='Select', height=2, width=10, command=select_version)
    select_version_button.place(rely=0.55, relx=0.7)

    version_list = tk.Listbox(select_menu, height=12, width=30, justify='center')
    version_list.place(rely=0.05, relx=0.1)

    for version in os.listdir(config['game_path']+'/mod_manager'):
        version_list.insert(0, version)

def add_mods():
    version_name = version_label.cget('text')
    if version_name == 'Version - None':
        tk.messagebox.showerror('Error', 'Select version first!')
        return

    mod_paths = tkinter.filedialog.askopenfilenames()
    not_mod_notification = False
    for path in mod_paths:
        if path[-3:] != 'jar':
            not_mod_notification = True
            continue
        shutil.copy(path, config['game_path']+f'/mod_manager/{version_name}/mods')
    
    if not_mod_notification:
        tk.messagebox.showerror('Not a mod', 'Some of the files were not .jar files. They were skipped')

def del_mods():

    def mod_del_confirm():
        for mod, status in var.items():
            if status.get() == 1:
                os.remove(config['game_path']+f'/mod_manager/{version_name}/mods/{mod}')
        tk.messagebox.showinfo('Done', 'Selected mods has been removed.')
        mod_del_menu.destroy()

    version_name = version_label.cget('text')
    if version_name == 'Version - None':
        tk.messagebox.showerror('Error', 'Select version first!')
        return
    
    mod_del_menu = tk.Toplevel(window)
    mod_del_menu.title('delete mods')   

    var = dict()
    for i, mod in enumerate(os.listdir(config['game_path']+f'/mod_manager/{version_name}/mods')):
        var[mod] = tk.IntVar()
        chk = tk.Checkbutton(mod_del_menu, text=mod, variable=var[mod])
        chk.place(y=i*25)
    
    mod_del_confirm_button = tk.Button(mod_del_menu, text='Confirm', width=7, command=mod_del_confirm)
    mod_del_confirm_button.place(y=(i+1)*25)

window = tk.Tk()
window.title('Minecraft Mod Manager')
window.resizable(width=False, height=False)
window.geometry('600x500')

config_preset = {
    'game_path': 'Select game path',
    'selected_version': 'Version - None'
}

if not os.path.isfile('config.json'):
    open('config.json', 'w').close()
    functions.json_save(config_preset, 'config.json')

config = functions.json_load('config.json')

game_dir_label = tk.Label(window, bd=3, width=60, bg='white', text=config['game_path'])
game_dir_label.place(rely=0.925, relx=0.05)
game_dir_button = tk.Button(window, text='Browse', width=16, command=browse_path_func)
game_dir_button.place(rely=0.924, relx=0.775)

version_label = tk.Label(window, bd=3, width=40, bg='white', text=config['selected_version'])
version_label.place(rely=0.025, relx=0.05)
version_button = tk.Button(window, text='Select', width=7, command=version_selection_menu)
version_button.place(rely=0.024, relx=0.54)

add_mods_button = tk.Button(window, text='Add mods', command=add_mods)
add_mods_button.place(rely=0.024, relx=0.68, width=80)
del_mods_button = tk.Button(window, text='Delete mods', command=del_mods)
del_mods_button.place(rely=0.024, relx=0.82, width=80)

window.mainloop()
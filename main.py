import tkinter as tk
import os, tkinter.messagebox, tkinter.filedialog, shutil, json
from typing import Text

background_color = '#212121'
button_color = '#2e2e2e'
font_color = '#ffffff'

config_preset = {
    'game_path': 'Select game path'
}

def read(file_path, binary = False):
    file_path = os.path.join(f'{os.path.dirname(os.path.abspath(__file__))}', file_path)
    if binary:
        with open(file_path, 'rb') as f:
            data = f.read()
    else:
        with open(file_path) as f:
            data = f.read()
    return data

def write(file_path, data, binary = False):
    file_path = os.path.join(f'{os.path.dirname(os.path.abspath(__file__))}', file_path)
    if binary:
        with open(file_path, 'wb') as f:
            f.write(data)
    else:
        with open(file_path, 'w') as f:
            f.write(data)

def dict_add(data, place, content, update = True):
    copy = data
    if len(place) == 0:
        data.update(content)
    else:
        for i in place:
            copy = copy[i]
        if update:
            copy.update(content)
        else:
            copy = content
    return data

def dict_rem(data, place):
    copy = data
    if len(place) == 1:
        del data[place[0]]
    else:
        for i in place[:-1]:
            copy = copy[i]
        del copy[place[-1]]

def json_load(path):
    return json.loads(read(path))

def json_save(data, path):
    write(path, json.dumps(data, indent=4, sort_keys=True))

if not os.path.isfile('config.json'):
    open('config.json', 'w').close()
    json_save(config_preset, 'config.json')

config = json_load('config.json')

import os, json

class MainWindow():
    
    def __init__(self, root):

        self.root = root

        #game dir label and button 
        self.game_dir_label = create_label(self.root, bd=3, width=57,
            text=config['game_path'], y=461, x=30)
        self.game_dir_button = create_button(self.root, text='Browse', width=16,
            y=460, x=450).configure(command=self.browse_path_func)
        
        #version label and button
        self.version_label = create_label(self.root, bd=3, width=40,
            text='Version - None', y=31, x=30)
        self.version_button = create_button(self.root, text='Select', width=7,
            y=30, x=330).configure(command=self.version_selection_menu)
        
        #add and delete mods buttons
        self.add_mods_button = create_button(self.root, width=10, text='Add mods',
            y=30, x=410).configure(command=self.add_mods)
        self.del_mods_button = create_button(self.root, width=10, text='Delete mods',
            y=30, x=495).configure(command=self.del_mods)

        #creating frame for listbox with available mods
        self.available_mods_frame = tk.Frame(self.root)
        self.available_mods_frame.place(y=100, x=30)

        #label of listbox
        self.available_mods_label = tk.Label(self.available_mods_frame, bg=button_color, fg=font_color, text='Mods for selected verison')
        self.available_mods_label.grid(column=0, row=0, columnspan=2, sticky='w'+'e')
        
        #creating listbox with available mods
        self.available_mods = tk.Listbox(self.available_mods_frame, bg=button_color, fg=font_color, height=19, width=30)
        self.available_mods.grid(column=0, row=1)

        #creating scrollbars for listbox
        self.available_scrolly = tk.Scrollbar(self.available_mods_frame, orient='vertical')
        self.available_scrolly.configure(command=self.available_mods.yview)
        self.available_scrolly.grid(column=1, row=1, sticky='w'+'n'+'s')
        self.available_scrollx = tk.Scrollbar(self.available_mods_frame, orient='horizontal')
        self.available_scrollx.configure(command=self.available_mods.xview)
        self.available_scrollx.grid(sticky='n'+'e'+'w')
        self.available_mods.configure(xscrollcommand=self.available_scrollx.set, yscrollcommand=self.available_scrolly.set)
        
        #creating frame for listbox with loaded mods
        self.loaded_mods_frame = tk.Frame(self.root)
        self.loaded_mods_frame.place(y=100, x=235)

        #label of listbox
        self.available_mods_label = tk.Label(self.loaded_mods_frame, bg=button_color, fg=font_color, text='Mods in game folder')
        self.available_mods_label.grid(column=0, row=0, columnspan=2, sticky='w'+'e')

        #creating listbox with loaded mods
        self.loaded_mods = tk.Listbox(self.loaded_mods_frame, bg=button_color, fg=font_color, height=19, width=30)
        self.loaded_mods.grid(column=0, row=1)

        #creating scrollbars for listbox
        self.loaded_scrolly = tk.Scrollbar(self.loaded_mods_frame, orient='vertical')
        self.loaded_scrolly.configure(command=self.loaded_mods.yview)
        self.loaded_scrolly.grid(column=1, row=1, sticky='w'+'n'+'s')
        self.loaded_scrollx = tk.Scrollbar(self.loaded_mods_frame, orient='horizontal')
        self.loaded_scrollx.configure(command=self.loaded_mods.xview)
        self.loaded_scrollx.grid(sticky='n'+'e'+'w')
        self.loaded_mods.configure(xscrollcommand=self.loaded_scrollx.set, yscrollcommand=self.loaded_scrolly.set)
        
        #load/unload button
        self.load_button = create_button(self.root, text='>>', width=6, y=70, x=165)
        self.load_button.configure(command=self.load_mods)
        self.unload_button = create_button(self.root, text='<<', width=6, y=70, x=250)
        self.unload_button.configure(command=self.unload_mods)

        #creating frame for listbox with profiles
        self.profiles_frame = tk.Frame(self.root)
        self.profiles_frame.place(y=225, x=455)

        #select profiles button
        self.profiles_button = create_button(self.root, text='Profiles', width=15, y=105, x=462.5)
        self.profiles_button.configure(command=self.profiles_menu)
        self.profiles_listbox = tk.Listbox(self.profiles_frame, bg=button_color, fg=font_color, height=10, width=18)
        self.profiles_listbox.grid(column=0, row=1)

        #load list and profiles buttons
        self.load_profiles_list_button = create_button(self.root, text='load list', width=15, y=135, x=462.5)
        self.load_profiles_list_button.configure(command=self.load_profiles)
        self.load_selected_profile_button = create_button(self.root, text='load profile', width=15, y=195, x=462.5)
        self.load_selected_profile_button.configure(command=self.load_selected_profile)
        self.unload_selected_profile_button = create_button(self.root, text='unload profile', width=15, y=165, x=462.5)
        self.unload_selected_profile_button.configure(command=self.unload_selected_profile)

        #profile label
        self.profile_label = create_label(self.root, bd=3, width=20,
            text='No profile selected', y=410, x=445)

        #profile list scroll bars
        self.profiles_listbox_scrolly = tk.Scrollbar(self.profiles_frame, orient='vertical')
        self.profiles_listbox_scrolly.configure(command=self.profiles_listbox.yview)
        self.profiles_listbox_scrolly.grid(column=1, row=1, sticky='w'+'n'+'s')
        self.profiles_listbox_scrollx = tk.Scrollbar(self.profiles_frame, orient='horizontal')
        self.profiles_listbox_scrollx.configure(command=self.profiles_listbox.xview)
        self.profiles_listbox_scrollx.grid(sticky='n'+'e'+'w')
        self.profiles_listbox.configure(xscrollcommand=self.available_scrollx.set, yscrollcommand=self.available_scrolly.set)

    def check_version(self):
        version_name = self.version_label.cget('text')
        if version_name == 'Version - None': 
            tk.messagebox.showerror('Error', 'Select version first!')
        else:
            return version_name

    def browse_path_func(self):
        path = tkinter.filedialog.askdirectory()
        if path == '':
            return

        if os.path.isdir(path+'/bin'):
            self.game_dir_label.configure(text=path)
            config['game_path'] = path
            json_save(config, 'config.json')
            if not os.path.isdir(path+'/mod_manager'):
                os.mkdir(path+'/mod_manager')
            if not os.path.isdir(path+'/mods'):
                os.mkdir(path+'/mods')  

        else:
            tk.messagebox.showerror('Error', 'This is not minecraft directory!')

    def version_selection_menu(self):
        select_menu = tk.Toplevel(self.root)
        select_menu.title('Version selection')   
        select_menu.resizable(width=False, height=False)
        select_menu.geometry('400x250')
        select_menu.configure(background=background_color)

        VersionSelectionMenu(select_menu)

    def add_mods(self):
        version_name = self.check_version()
        if not version_name: return

        mod_paths = tkinter.filedialog.askopenfilenames()
        not_mod_notification = False
        for path in mod_paths:
            if path[-3:] != 'jar':
                not_mod_notification = True
                continue
            profile_name = self.profile_label.cget("text")
            if profile_name == 'No profile selected': shutil.copy(path, config['game_path']+ f'/mod_manager/{version_name}/mods')
            else: shutil.copy(path, config['game_path']+ f'/mod_manager/{version_name}/profiles/{profile_name}/mods')
        
        if not_mod_notification:
            tk.messagebox.showerror('Not a mod', 'Some of the files were not .jar files. They were skipped')
        self.load_mods_to_labels()
        
    def del_mods(self):
        version_name = self.check_version()
        if not version_name: return

        mod_del_menu = tk.Toplevel(self.root)
        mod_del_menu.title('delete mods') 
        mod_del_menu.configure(background=background_color)  
        ModDeletionMenu(mod_del_menu)

    def load_mods_to_labels(self):
        version_name = self.check_version()
        if not version_name: return
        
        self.available_mods.delete(0, 'end')
        profile_name = self.profile_label.cget('text')
        if profile_name == 'No profile selected':
            for mod in os.listdir(config['game_path']+f'/mod_manager/{version_name}/mods'):
                self.available_mods.insert('end', mod)
        else:
            for mod in os.listdir(config['game_path']+f'/mod_manager/{version_name}/profiles/{profile_name}/mods'):
                self.available_mods.insert('end', mod)

        self.loaded_mods.delete(0, 'end')
        for mod in os.listdir(config['game_path']+'/mods'):
            self.loaded_mods.insert('end', mod)

    def load_mods(self):
        version_name = self.check_version()
        if not version_name: return

        selection = self.available_mods.get('active')
        profile_name = self.profile_label.cget('text')
        if profile_name == 'No profile selected':
            if not os.path.isfile(config['game_path']+f'/mod_manager/{version_name}/mods/{selection}'):
                tk.messagebox.showerror('Error', 'No such file')
                return
        else:
            if not os.path.isfile(config['game_path']+f'/mod_manager/{version_name}/profiles/{profile_name}/mods/{selection}'):
                tk.messagebox.showerror('Error', 'No such file')
                return
        
        profile_name = self.profile_label.cget("text")
        if profile_name == 'No profile selected':
            shutil.move(config['game_path']+f'/mod_manager/{version_name}/mods/{selection}', config['game_path'] + f'/mods/{selection}')
        else:
            shutil.copy(config['game_path']+f'/mod_manager/{version_name}/profiles/{profile_name}/mods/{selection}', config['game_path'] + f'/mods/{selection}')
        self.load_mods_to_labels()

    def unload_mods(self):
        version_name = self.check_version()
        if not version_name: return

        selection = self.loaded_mods.get('active')
        if not os.path.isfile(config['game_path']+f'/mods/{selection}'):
            tk.messagebox.showerror('Error', 'No such file')
            return
        
        profile_name = self.profile_label.cget('text')
        if profile_name == 'No profile selected':
            shutil.move(config['game_path']+f'/mods/{selection}', config['game_path']+f'/mod_manager/{version_name}/mods/{selection}')
        else:
            shutil.move(config['game_path']+f'/mods/{selection}', config['game_path']+f'/mod_manager/{version_name}/profiles/{profile_name}/mods/{selection}')
        
        self.load_mods_to_labels()

    def load_profiles(self):
        version_name = self.check_version()
        if not version_name: return
        
        self.profiles_listbox.delete(0, 'end')
        for profile in os.listdir(config['game_path']+f'/mod_manager/{version_name}/profiles'):
            self.profiles_listbox.insert('end', profile)

    def profiles_menu(self):
        version_name = self.check_version()
        if not version_name: return

        if not os.path.isdir(config['game_path'] + f'/mod_manager/{version_name}/profiles'):
            os.mkdir(config['game_path'] + f'/mod_manager/{version_name}/profiles')

        profile_select_menu = tk.Toplevel(self.root)
        profile_select_menu.title('Profile selection')   
        profile_select_menu.resizable(width=False, height=False)
        profile_select_menu.geometry('400x250')
        profile_select_menu.configure(background=background_color)

        ProfileSelectionMenu(profile_select_menu)

    def load_selected_profile(self):
        profile_name = self.profiles_listbox.get('active')
        if profile_name == '': 
            tk.messagebox.showerror('Error', 'Select profile first!')
        else:
            self.profile_label.config(text=profile_name)
            self.load_mods_to_labels()

    def unload_selected_profile(self):
        self.profile_label.config(text='No profile selected')
        self.load_mods_to_labels()


class VersionSelectionMenu():
   
    def __init__(self, root):

        if config['game_path'] == 'Select game path':
            tk.messagebox.showerror('Error', 'Select the game folder first!')
            return

        self.root = root

        #creating frame for listbox with versions
        self.versions_frame = tk.Frame(self.root)
        self.versions_frame.place(y=15, x=40)

        #creating listbox with versions
        self.versions = tk.Listbox(self.versions_frame, bg=button_color, fg=font_color, height=11, width=27)
        self.versions.grid(column=0, row=1)

        #creating scrollbars for listbox
        self.versions_scrolly = tk.Scrollbar(self.versions_frame, orient='vertical')
        self.versions_scrolly.configure(command=self.versions.yview)
        self.versions_scrolly.grid(column=1, row=1, sticky='w'+'n'+'s')
        self.versions_scrollx = tk.Scrollbar(self.versions_frame, orient='horizontal')
        self.versions_scrollx.configure(command=self.versions.xview)
        self.versions_scrollx.grid(sticky='n'+'e'+'w')
        self.versions.configure(xscrollcommand=self.versions_scrollx.set, yscrollcommand=self.versions_scrolly.set)

        self.new_version_button = create_button(self.root, text='New', height=2, width=10,
            y=40, x=275).configure(command=self.create_new_version)
        self.del_version_button = create_button(self.root, text='Delete', height=2, width=10,
            y=90, x=275).configure(command=self.delete_version)
        self.select_version_button = create_button(self.root, text='Select', height=2, width=10,
            y=140, x=275).configure(command=self.select_version)

        for version in os.listdir(config['game_path']+'/mod_manager'):
            self.versions.insert(0, version)

        self.root.protocol('WM_DELETE_WINDOW', self.user_close)

    def create_new_version(self):
        self.entry_box = tk.Entry(self.root, bg=button_color, fg=font_color)
        self.entry_box.place(rely=0.875, relx=0.1)
        self.confirm_button = tk.Button(self.root, text='Confirm', bg=button_color, fg=font_color, command=self.confirm_new_version)
        self.confirm_button.place(rely=0.865, relx=0.42)

    def confirm_new_version(self):
        version_name = self.entry_box.get()
        if '/' in version_name:
            tk.messagebox.showerror('Invalid version name', 'Version name can not have any "/" in it!')
            return
        if os.path.isdir(config['game_path']+f'/mod_manager/{version_name}'):
            tk.messagebox.showerror('Invalid version name', 'Version with selected name already exist!')
            return

        os.mkdir(config['game_path']+f'/mod_manager/{version_name}')
        os.mkdir(config['game_path']+f'/mod_manager/{version_name}/mods')
        os.mkdir(config['game_path']+f'/mod_manager/{version_name}/profiles')
        self.versions.delete('0', 'end')

        for version in os.listdir(config['game_path']+'/mod_manager'):
            self.versions.insert(0, version)

        self.entry_box.place_forget()
        self.confirm_button.place_forget()

    def delete_version(self):
        selection = self.versions.get('active')
        if selection == '':
            return

        msgbox = tk.messagebox.askquestion('Are you sure?',
            'This action will delete version and all profiles and mods corelated with it.',
            icon='warning')

        if msgbox == 'yes':
            shutil.rmtree(config['game_path']+f'/mod_manager/{selection}')

            self.versions.delete('0', 'end')

            for version in os.listdir(config['game_path']+'/mod_manager'):
                self.versions.insert(0, version)
        else:
            return

    def select_version(self):
        selection = self.versions.get('active')
        McModManager.version_label.config(text=selection)
        McModManager.available_mods.delete(0, 'end')
        McModManager.profiles_listbox.delete(0, 'end')
        McModManager.load_profiles()
        McModManager.load_mods_to_labels()
        self.root.destroy()

    def user_close(self):
        McModManager.version_label.config(text='Version - None')
        McModManager.available_mods.delete(0, 'end')
        McModManager.profiles_listbox.delete(0, 'end')
        self.root.destroy()


class ModDeletionMenu():
   
    def __init__(self, root):
        
        def create_checkbuttons(part_of_the_path):
            for mod in os.listdir(config['game_path'] + f'/mod_manager/{part_of_the_path}/mods'):
                self.var[mod] = tk.IntVar()
                chk = tk.Checkbutton(self.root, text=mod, bg=button_color, fg=font_color, selectcolor="#000000",
                    activebackground=button_color, activeforeground=font_color, variable=self.var[mod])
                chk.grid(padx=2, pady=2, sticky='W')

        self.root = root
        self.version_name = McModManager.version_label.cget('text')
        self.profile_name = McModManager.profile_label.cget("text")
        self.var = dict()

        tk.Label(self.root, width=35, bg=button_color, fg=font_color, text=f'Available mods for {self.version_name}:').grid(padx=2, pady=2)

        if len(os.listdir(config['game_path']+f'/mod_manager/{self.version_name}/mods')) == 0:
            self.no_mods = tk.Label(self.root, bg=button_color, fg=font_color, text='No mods for selected version')
            self.no_mods.grid(padx=5, pady=5)
        else:

            if self.profile_name == 'No profile selected':
                create_checkbuttons(self.version_name)
            else:
                create_checkbuttons(self.version_name + '/profiles/' + self.profile_name)
        
        self.mod_del_confirm_button = tk.Button(self.root, text='Confirm', width=7, bg=button_color, fg=font_color, command=self.mod_del_confirm)
        self.mod_del_confirm_button.grid(pady=5)

    def mod_del_confirm(self):
        for mod, status in self.var.items():
            if status.get() == 1:
                profile_name = McModManager.profile_label.cget('text')
                if profile_name == 'No profile selected':
                    os.remove(config['game_path']+f'/mod_manager/{self.version_name}/mods/{mod}')
                else:
                    os.remove(config['game_path']+f'/mod_manager/{self.version_name}/profiles/{profile_name}/mods/{mod}')

        if len(os.listdir(config['game_path']+f'/mod_manager/{self.version_name}/mods')) != 0:
            tk.messagebox.showinfo('Done', 'Selected mods has been removed.')
        McModManager.load_mods_to_labels()
        self.root.destroy()


class ProfileSelectionMenu():
    
    def __init__(self, root):

        if config['game_path'] == 'Select game path':
            tk.messagebox.showerror('Error', 'Select the game folder first!')
            return

        self.root = root
        
        #creating frame for listbox with profiles
        self.profiles_frame = tk.Frame(self.root)
        self.profiles_frame.place(y=15, x=40)

        #creating listbox with profiles
        self.profiles = tk.Listbox(self.profiles_frame, bg=button_color, fg=font_color, height=11, width=27)
        self.profiles.grid(column=0, row=1)

        #creating scrollbars for listbox
        self.profiles_scrolly = tk.Scrollbar(self.profiles_frame, orient='vertical')
        self.profiles_scrolly.configure(command=self.profiles.yview)
        self.profiles_scrolly.grid(column=1, row=1, sticky='w'+'n'+'s')
        self.profiles_scrollx = tk.Scrollbar(self.profiles_frame, orient='horizontal')
        self.profiles_scrollx.configure(command=self.profiles.xview)
        self.profiles_scrollx.grid(sticky='n'+'e'+'w')
        self.profiles.configure(xscrollcommand=self.profiles_scrollx.set, yscrollcommand=self.profiles_scrolly.set)

        self.new_profile_button = create_button(self.root, text='New', height=2, width=10,
            y=40, x=275).configure(command=self.create_new_profile)
        self.del_profile_button = create_button(self.root, text='Delete', height=2, width=10,
            y=90, x=275).configure(command=self.delete_profile)

        version_name = McModManager.version_label.cget('text')
        for profile in os.listdir(config['game_path'] + f'/mod_manager/{version_name}/profiles'):
            self.profiles.insert(0, profile)

        self.root.protocol('WM_DELETE_WINDOW', self.user_close)

    def create_new_profile(self):
        self.entry_box = tk.Entry(self.root, bg=button_color, fg=font_color)
        self.entry_box.place(rely=0.875, relx=0.1)
        self.confirm_button = tk.Button(self.root, text='Confirm', bg=button_color, fg=font_color, command=self.confirm_new_profile)
        self.confirm_button.place(rely=0.865, relx=0.42)

    def confirm_new_profile(self):
        profile_name = self.entry_box.get()
        if '/' in profile_name:
            tk.messagebox.showerror('Invalid profile name', 'Profile name can not have any "/" in it!')
            return
        version_name = McModManager.version_label.cget('text')
        if os.path.isdir(config['game_path']+f'/mod_manager/{version_name}/profiles/{profile_name}'):
            tk.messagebox.showerror('Invalid profile name', 'Profile with selected name already exist!')
            return

        os.mkdir(config['game_path']+f'/mod_manager/{version_name}/profiles/{profile_name}')
        os.mkdir(config['game_path']+f'/mod_manager/{version_name}/profiles/{profile_name}/mods')
        self.profiles.delete('0', 'end')

        for profile in os.listdir(config['game_path'] + f'/mod_manager/{version_name}/profiles'):
            self.profiles.insert(0, profile)

        self.entry_box.place_forget()
        self.confirm_button.place_forget()
        McModManager.load_profiles()

    def delete_profile(self):
        selection = self.profiles.get('active')
        if selection == '':
            return

        msgbox = tk.messagebox.askquestion('Are you sure?',
            'This action will delete profile and all mods corelated with it.',
            icon='warning')

        if msgbox == 'yes':
            version_name = McModManager.version_label.cget('text')
            shutil.rmtree(config['game_path']+f'/mod_manager/{version_name}/profiles/{selection}')

            self.profiles.delete('0', 'end')

            for profile in os.listdir(config['game_path'] + f'/mod_manager/{version_name}/profiles'):
                self.profiles.insert(0, profile)
            McModManager.profile_label.config(text='No profile selected')
            McModManager.load_profiles()
            McModManager.load_mods_to_labels()
        else:
            return

    def user_close(self):
        McModManager.load_profiles()
        self.root.destroy()


def create_label(window, bd=None, width=None, height=None, bg=button_color, fg=font_color, text=None, y=0, x=0):
    label = tk.Label(window, bd=bd, width=width, height=height, bg=bg, fg=fg, text=text)
    label.place(x=x, y=y)
    return label

def create_button(window, bd=None, width=None, height=None, bg=button_color, fg=font_color, text=None, y=0, x=0):
    button = tk.Button(window, bd=bd, width=width, height=height, bg=bg, fg=fg, text=text)
    button.place(x=x, y=y)
    return button

def create_listbox(window, height=None, width=None, bg=button_color, fg=font_color, justify=None, x=0, y=0):
    listbox = tk.Listbox(window, height=height, bg=bg, fg=fg, width=width, justify=justify)
    listbox.place(x=x, y=y)
    return listbox

root = tk.Tk()
root.title('Minecraft Mod Manager')
root.resizable(width=False, height=False)
root.geometry('600x500')
root.configure(background=background_color)

McModManager = MainWindow(root)
root.mainloop()
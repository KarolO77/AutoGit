
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

from os import path
import git.exc
from github import Github
from github import GithubException
import git

#statics
green = "#154529"

class App():
    def __init__(self):
        # Main Window
        self.display = tk.Tk()
        self.display.title("GitManager")
        self.display.configure(background=green)
        self.display.geometry(f"{700}x{500}")

        # Menus
        self.menu_create = None
        self.menu_push = None

        # Buttons
        self.button = tk.Button(
            self.display,
            text="CreateNewRepo",
            width=16, 
            height=2,
            borderwidth=4,
            relief="raised",
            command= lambda: self.repo_buttons_clicked(0)
            )
        self.button.place(
            relx=0.4,
            rely=0.1,
            anchor="center"
        )

        self.button2 = tk.Button(
            self.display,
            text="PushToRepo",
            width=16, 
            height=2,
            borderwidth=4,
            relief="raised",
            command= lambda: self.repo_buttons_clicked(1)
            )
        self.button2.place(
            relx=0.6,
            rely=0.1,
            anchor="center"
        )

    def repo_buttons_clicked(self, bttn):

        if self.button["relief"] == "raised" and not bttn:
            self.menu_create = MenuCreate(self.display)
            self.clear_menu_widgets(self.menu_push)
            self.button["relief"] = "sunken"
            self.button2["relief"] = "raised"

        elif self.button2["relief"] == "raised" and bttn:
            self.menu_push = MenuPush(self.display)
            self.clear_menu_widgets(self.menu_create)
            self.button["relief"] = "raised"
            self.button2["relief"] = "sunken"
    
    """ def reset_menu_data(self, menu):
        if menu and menu == self.menu_push:
            menu.destination_repo = None
            menu.selected_files.clear()
            menu.selected_dirs.clear()
            menu.commit_message = ""
        elif menu and menu == self.menu_create:
            menu.destination_repo = None """

    def clear_menu_widgets(self, menu):
        if menu == None:
            return

        for widget in menu.__dict__:
            try:
                getattr(menu,widget).place_forget()
            except AttributeError:
                pass
    
    def run(self):
        self.display.mainloop()

class MenuPush():
    def __init__(self, display):
        self.display = display

        # Selected things to push
        self.repo_destination = None
        self.selected_things = set()

        # Token
        self.token_label = tk.Label(
            self.display,
            text="Github Token:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
        )
        self.token_label.place(
            relx=0.13,
            rely=0.26,
            anchor="center"
        )

        self.token_entry = tk.Entry(
            self.display,
            width=72
        )
        self.token_entry.place(
            relx=0.55,
            rely=0.26,
            anchor="center"
        )

        # "Your Repository" 
        self.info_lbl = tk.Label(
            self.display,
            text="Your Repository:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
            )
        self.info_lbl.place(
            relx=0.13,
            rely=0.38,
            anchor="center"
        )

        self.dest_repo_bttn = tk.Button(
            self.display,
            text="Click to select destination repository",
            width=61,
            height=2,
            command=self.select_repository
        )
        self.dest_repo_bttn.place(
            relx=0.55,
            rely=0.38,
            anchor="center"
        )

        # Options to push
        self.push_option_var = tk.BooleanVar()
        self.directory_option_bttn = tk.Radiobutton(
            self.display, 
            width=12,
            height=1,
            value=False, # 0
            variable=self.push_option_var,
            text="Directory",
            command=lambda: self.set_push_option("directory")
        )
        self.directory_option_bttn.place(
            relx=0.13,
            rely=0.49,
            anchor="center"
        )

        self.file_option_bttn = tk.Radiobutton(
            self.display, 
            width=12,
            height=1,
            value=True, # 1
            variable=self.push_option_var,
            text="Files",
            command=lambda: self.set_push_option("file")
        )
        self.file_option_bttn.place(
            relx=0.13,
            rely=0.57,
            anchor="center"
        )

        # Add to push
        self.select_pushed_bttn = tk.Button(
            self.display,
            text="ADD+",
            width=6,
            height=2,
            command=self.select_directory
        )
        self.select_pushed_bttn.place(
            relx=0.28,
            rely=0.53,
            anchor="center"
        )

        self.select_pushed_lbl = tk.Label(
            self.display,
            text="Directory: ",
            width=50,
            height=3
        )
        self.select_pushed_lbl.place(
            relx=0.6,
            rely=0.53,
            anchor="center"
        )

        # Commit Label
        self.commit_label = tk.Label(
            self.display,
            text="Commit message:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
        )
        self.commit_label.place(
            relx=0.13,
            rely=0.68,
            anchor="center"
        )

        self.commit_entry = tk.Entry(
            self.display,
            width=72
        )
        self.commit_entry.place(
            relx=0.55,
            rely=0.68,
            anchor="center"
        )

        # Last Commit
        self.last_commit_lbl = tk.Label(
            self.display,
            text="Last Commit: ",
            width=50,
            height=1,
            borderwidth=0,
            background=green
        )
        self.last_commit_lbl.place(
            relx=0.5,
            rely=0.72,
            anchor="center"
        )

        # Push Button
        self.push_all_bttn = tk.Button(
            self.display,
            text="Push",
            width=10,
            height=2,
            borderwidth=0,
            command=self.push_all
        )
        self.push_all_bttn.place(
            relx=0.35,
            rely=0.85,
            anchor="center"
        )

        # Remove Last Add Button
        self.undo_added_bttn = tk.Button(
            self.display,
            text="Rem Last Add",
            width=12,
            height=2,
            borderwidth=0,
            command=self.remove_last_added
        )
        self.undo_added_bttn.place(
            relx=0.5,
            rely=0.85,
            anchor="center"
        )
        
        # Reset Added Button
        self.reset_added_bttn = tk.Button(
            self.display,
            text="Reset added",
            width=10,
            height=2,
            borderwidth=0,
            command=self.remove_all_added
        )
        self.reset_added_bttn.place(
            relx=0.65,
            rely=0.85,
            anchor="center"
        )

    # select
    def select_repository(self):
        # check user token
        self.user_token = self.token_entry.get()
        if self.user_token == "":
            messagebox.showerror(message="You need to enter your user token")
            return
        
        # select repository
        try:
            repository = askdirectory(title='Select repository')

            self.git_repo = git.Repo(repository)
            self.repo_destination = repository

            self.dest_repo_bttn["text"] = f"Current Repo: {repository}"

            last_commit = self.get_last_commit(repository)
            self.last_commit_lbl["text"] = f"Last Commit: {last_commit}"

        except git.exc.InvalidGitRepositoryError:
            messagebox.showerror(message="The directory is not a valid git repository.")

    def select_directory(self):
        if self.repo_destination == None:
            messagebox.showerror(message="No repository has been selected")
            return
        
        # select directory
        directory = askdirectory(title='Select directory')
        if directory == "":
            messagebox.showerror(message="No directory has been selected")
            return     
        elif self.repo_destination not in directory:
            messagebox.showerror(message="Directory not found in repository")
            return
        
        directory = path.basename(directory)
        self.selected_things.add(directory)
        self.select_pushed_lbl["text"] += directory

    def select_file(self):
        if self.repo_destination == None:
            messagebox.showerror(message="No repository has been selected")
            return
        
        # add file
        file = askopenfilename(title='Add file')
        if file == "":
            messagebox.showerror(message="No file has been selected")
            return
        elif self.repo_destination not in file:
            messagebox.showerror(message="File not found in repository")
            return

        file = path.basename(file)
        self.selected_things.add(file)
        self.select_pushed_lbl["text"] += f"{file}, "
    
    # remove
    def remove_last_added(self):
        last_thing = self.select_pushed_lbl["text"].split(",")[-2][1:]
        d = len(self.select_pushed_lbl["text"]) - len(last_thing) - 3
        self.select_pushed_lbl["text"] = self.select_pushed_lbl["text"][:d]
        self.selected_things.remove(last_thing)

    def remove_all_added(self):
        self.selected_things.clear()

        if self.push_option_var.get():
            self.set_push_option("file")
        else:
            self.set_push_option("directory")
    
    # funcs
    def set_push_option(self, option):
        self.selected_things.clear()
        if option == "directory":
            self.select_pushed_lbl["text"] = "Directory: "
            self.select_pushed_bttn["command"] = self.select_directory
        elif option == "file":
            self.select_pushed_lbl["text"] = "Files: "
            self.select_pushed_bttn["command"] = self.select_file

    def get_last_commit(self, dir_path):
        try:
            g = Github(self.user_token)
            user = g.get_user()
            repo = path.basename(dir_path)
            repo = user.get_repo(repo)
            commits = repo.get_commits()
            return commits[0].commit.message
        except GithubException:
            pass
    
    # PUSH ALL
    def push_all(self):
        try:
            # Add selected files/directory
            for thing in self.selected_things:
                self.git_repo.git.add(thing)

            # Commit message
            commit = self.commit_entry.get()
            self.git_repo.git.commit(m=commit)

            # Push all to User's Github
            origin = self.git_repo.remote(name='origin')
            origin.push()

            # Succes Label
            self.last_commit_lbl.place_forget()
            succes_label = tk.Label(
                self.display,
                width=50,
                height=2,
                text="Successfuly pushed to Your Github repository",
                background="green"
            )
            succes_label.place(
                relx=0.5,
                rely=0.76,
                anchor="center"
            )
        except git.exc.GitCommandError as e:
            messagebox.showerror(message=f"Error occurred when: {e}")
    
class MenuCreate():
    def __init__(self, display):
        self.display = display
        self.repo_destination = None

        # Token
        self.token_lbl = tk.Label(
            self.display,
            text="Github Token:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
        )
        self.token_lbl.place(
            relx=0.13,
            rely=0.26,
            anchor="center"
        )

        self.token_entry = tk.Entry(
            self.display,
            width=72
        )
        self.token_entry.place(
            relx=0.55,
            rely=0.26,
            anchor="center"
        )
      
        # "Your Repository"
        self.info = tk.Label(
            self.display,
            text="Repository place:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
            )
        self.info.place(
            relx=0.13,
            rely=0.38,
            anchor="center"
        )

        self.dest_repo_bttn = tk.Button(
            self.display,
            text="Click to select destination repository",
            width=61,
            height=2,
            command=self.select_repository
        )
        self.dest_repo_bttn.place(
            relx=0.55,
            rely=0.38,
            anchor="center"
        )

        # Name
        self.repo_name = tk.Label(
            self.display,
            text="Repository name:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
        )
        self.repo_name.place(
            relx=0.13,
            rely=0.5,
            anchor="center"
        )

        self.repo_name_entry = tk.Entry(
            self.display,
            width=72
        )
        self.repo_name_entry.place(
            relx=0.55,
            rely=0.5,
            anchor="center"
        )

        # Description
        self.repo_description = tk.Label(
            self.display,
            text="Description:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
        )
        self.repo_description.place(
            relx=0.13,
            rely=0.62,
            anchor="center"
        )

        self.repo_description_entry = tk.Text(
            self.display,
            width=54,
            height=2
        )
        self.repo_description_entry.place(
            relx=0.55,
            rely=0.62,
            anchor="center"
        )
        
        # Status
        self.private_status = tk.BooleanVar()
        self.repo_status = tk.Label(
            self.display,
            text="Status:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
        )
        self.repo_status.place(
            relx=0.13,
            rely=0.74,
            anchor="center"
        )

        self.repo_status_pub = tk.Radiobutton(
            self.display,
            width=8,
            height=1,
            value=False,
            variable=self.private_status,
            text="Public"
        )
        self.repo_status_pub.place(
            relx=0.4,
            rely=0.74,
            anchor="center"
        )

        self.repo_status_priv = tk.Radiobutton(
            self.display,
            width=8,
            height=1,
            value=True,
            variable=self.private_status,
            text="Private"
        )
        self.repo_status_priv.place(
            relx=0.6,
            rely=0.74,
            anchor="center"
        )

        # "Create" Button
        self.create_repo_bttn = tk.Button(
            self.display,
            text="Create",
            width=30,
            height=2,
            borderwidth=0,
            command=self.create_repository
        )
        self.create_repo_bttn.place(
            relx=0.5,
            rely=0.88,
            anchor="center"
        )
    
    def select_repository(self):
        # check github token
        self.user_token = self.token_entry.get()
        if self.user_token == "":
            messagebox.showerror(message="You need to enter your user token")
            return

        # select repository
        try:
            repository = askdirectory(title='Select repository')

            self.git_repo = git.Repo.init(repository)
            self.repo_destination = repository
            self.dest_repo_bttn["text"] = f"Current Repo: {repository}"

        except git.exc.InvalidGitRepositoryError:
            messagebox.showerror(message="The directory is not a valid git repository.")
        except git.exc.GitCommandError as e:
            messagebox.showerror(message=f"Error occurred when: {e}")

    def create_repository(self):  
        try:
            repo_name = self.repo_name_entry.get()
            repo_description = self.repo_description_entry.get()
            repo_status = self.private_status.get()
        
            # create in Github
            g = Github(self.user_token)
            user = g.get_user()
            user.create_repo(
                repo_name,
                allow_rebase_merge=True,
                auto_init=False,
                description=repo_description,
                has_issues=True,
                has_projects=False,
                has_wiki=False,
                private=repo_status,
            )

            url = f"https://github.com/{user.login}/{repo_name}.git"
            self.git_repo.git.commit(m="Initial commit")
            self.git_repo.git.branch('-M', 'main')
            self.git_repo.create_remote("origin", url)
            origin = self.git_repo.remote(name="origin")
            origin.push()

        except git.exc.GitCommandError as e:
            messagebox.showerror(message=f"Error occurred when: {e}")
        except GithubException as e:
            messagebox.showerror(message=f"Error occurred when: {e}")


# Run the program
if __name__ == "__main__":
    main = App()
    main.run()
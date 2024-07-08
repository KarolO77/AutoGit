
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import messagebox
import tkinter as tk

import webbrowser
from os import path
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
        self.new_repo_choice_bttn = tk.Button(
            self.display,
            text="CreateNewRepo",
            width=16, 
            height=2,
            borderwidth=4,
            relief="raised",
            command= lambda: self.repo_buttons_clicked(0)
            )
        self.new_repo_choice_bttn.place(
            relx=0.4,
            rely=0.1,
            anchor="center"
        )

        self.push_repo_choice_bttn = tk.Button(
            self.display,
            text="PushToRepo",
            width=16, 
            height=2,
            borderwidth=4,
            relief="raised",
            command= lambda: self.repo_buttons_clicked(1)
            )
        self.push_repo_choice_bttn.place(
            relx=0.6,
            rely=0.1,
            anchor="center"
        )

    def repo_buttons_clicked(self, bttn):

        if self.new_repo_choice_bttn["relief"] == "raised" and not bttn:
            self.menu_create = MenuCreate(self.display)
            self.clear_menu_widgets(self.menu_push)
            self.new_repo_choice_bttn["relief"] = "sunken"
            self.push_repo_choice_bttn["relief"] = "raised"

        elif self.push_repo_choice_bttn["relief"] == "raised" and bttn:
            self.menu_push = MenuPush(self.display)
            self.clear_menu_widgets(self.menu_create)
            self.new_repo_choice_bttn["relief"] = "raised"
            self.push_repo_choice_bttn["relief"] = "sunken"
    
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
            width=59
        )
        self.token_entry.place(
            relx=0.496,
            rely=0.26,
            anchor="center"
        )
        self.set_token()

        self.token_save_bttn = tk.Button(
            self.display,
            text="Save",
            width=8,
            height=2,
            command=self.save_token
        )
        self.token_save_bttn.place(
            relx=0.816,
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
        self.push_lbl_dir_text = "Direcotry: "
        self.directory_option_bttn = tk.Radiobutton(
            self.display, 
            width=12,
            height=1,
            value=False, # 0
            variable=self.push_option_var,
            text=self.push_lbl_dir_text,
            command=lambda: self.set_push_option("directory")
        )
        self.directory_option_bttn.place(
            relx=0.13,
            rely=0.49,
            anchor="center"
        )

        self.push_lbl_file_text = "Files: "
        self.file_option_bttn = tk.Radiobutton(
            self.display, 
            width=12,
            height=1,
            value=True, # 1
            variable=self.push_option_var,
            text=self.push_lbl_file_text,
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
        # check user token and login
        if not self.login_by_token():
            return
        
        # select repository
        try:
            repository = askdirectory(title='Select repository')
            if repository == "":
                return

            self.git_repo = git.Repo(repository)
            self.repo_destination = repository
            self.dest_repo_bttn["text"] = f"Current Repo: {repository}"

            last_commit = self.get_last_commit()
            self.last_commit_lbl["text"] = f"Last Commit: {last_commit}"

        except git.exc.InvalidGitRepositoryError:
            messagebox.showerror(message="The directory is not a valid git repository.")
        except git.exc.GitCommandError as e:
            messagebox.showerror(message=f"Error occurred when: {e}")

    def select_directory(self):
        if self.repo_destination == None:
            messagebox.showerror(message="No repository has been selected")
            return
        
        # select directory
        directory = askdirectory(title='Select directory')
        if directory == "":
            return     
        elif self.repo_destination not in directory:
            messagebox.showerror(message="Directory not found in repository")
            return
        elif directory in self.selected_things:
            return
        
        directory = path.basename(directory)
        if directory not in self.selected_things:
            self.selected_things.add(directory)
            self.select_pushed_lbl["text"] += f"{directory}, "
            self.push_lbl_dir_text = self.select_pushed_lbl["text"]

    def select_file(self):
        if self.repo_destination == None:
            messagebox.showerror(message="No repository has been selected")
            return
        
        # add file
        file = askopenfilename(title='Add file')
        if file == "":
            return
        elif self.repo_destination not in file:
            messagebox.showerror(message="File not found in repository")
            return
        elif file in self.selected_things:
            return

        file = path.basename(file)
        if file not in self.selected_things:
            self.selected_things.add(file)
            self.select_pushed_lbl["text"] += f"{file}, "
            self.push_lbl_file_text = self.select_pushed_lbl["text"]
    
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
    
    # token
    def set_token(self):
        with open("credentials.txt", 'r') as file:
            content = file.read()
            if content:
                self.token_entry.delete(0,tk.END)
                self.token_entry.insert(0,content)

    def save_token(self):
        token = self.token_entry.get()
        if token == "":
            messagebox.showwarning(message="Token is empty")
            return
        
        with open("credentials.txt", "w") as file:
            file.write(token)

    def login_by_token(self):
        self.user_token = self.token_entry.get()
        if self.user_token == "":
            messagebox.showerror(message="You need to enter your user token")
            return False

        try:
            self.g = Github(self.user_token)
            self.g_user = self.g.get_user()
        except GithubException as e:
            messagebox.showerror(message=f"Error occurred when: {e}")
            return False
        
        return True

    # funcs
    def set_push_option(self, option):
        if option == "directory": # False var
            self.select_pushed_lbl["text"] = self.push_lbl_dir_text
            self.select_pushed_bttn["command"] = self.select_directory
        elif option == "file": # True var
            self.select_pushed_lbl["text"] = self.push_lbl_file_text
            self.select_pushed_bttn["command"] = self.select_file

    def get_last_commit(self):
        try:
            repo = path.basename(self.repo_destination)
            repo = self.g_user.get_repo(repo)
            commits = repo.get_commits()
            return commits[0].commit.message
        except GithubException:
            return ""
    
    # PUSH ALL
    def add_all(self):
        if not self.push_option_var:
            # add directories/whole directory
            if list(self.selected_things)[0] == path.basename(self.repo_destination):
                self.git_repo.git.add(".")
            else:
                for thing in self.selected_things:
                    self.git_repo.git.add(f"{thing}/")
        else:
            # add files
            for thing in self.selected_things:
                self.git_repo.git.add(thing)

    def push_all(self):
        try:
            # Add selected files/directory
            self.add_all()

            # Commit message
            commit = self.commit_entry.get()
            self.git_repo.git.commit(m=commit)

            # Push all to User's Github
            origin = self.git_repo.remote(name='origin')
            origin.push()

            # Link Label
            self.last_commit_lbl.place_forget()
            user = self.g_user.login
            repo = path.basename(self.repo_destination)
            url = f"https://github.com/{user}/{repo}"

            self.link_label = tk.Button(
                self.display,
                width=50,
                height=2,
                text=url,
                background="green",
                command=lambda: webbrowser.open_new(url)
            )
            self.link_label.place(
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
            width=59
        )
        self.token_entry.place(
            relx=0.496,
            rely=0.26,
            anchor="center"
        )
        self.set_token()

        self.token_save_bttn = tk.Button(
            self.display,
            text="Save",
            width=8,
            height=2,
            command=self.save_token
        )
        self.token_save_bttn.place(
            relx=0.816,
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
    
    # token
    def set_token(self):
        with open("credentials.txt", 'r') as file:
            content = file.read()
            if content:
                self.token_entry.delete(0,tk.END)
                self.token_entry.insert(0,content)

    def save_token(self):
        token = self.token_entry.get()
        if token == "":
            messagebox.showwarning(message="Token is empty")
            return
        
        with open("credentials.txt", "a+") as file:
            file.write(token)

    # repository
    def select_repository(self):
        # check github token
        self.user_token = self.token_entry.get()
        if self.user_token == "":
            messagebox.showerror(message="You need to enter your user token")
            return

        # select repository
        try:
            repository = askdirectory(title='Select repository')
            if repository == "":
                messagebox.showwarning(message="No repository has been selected")
                return  

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
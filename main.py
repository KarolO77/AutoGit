
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import messagebox
import tkinter as tk

from os import path
import git.exc
from github import Github
from github import GithubException
import git

from credentials import github_token
#statics
green = "#154529"

class Main():
    def __init__(self):
        # Main Window
        self.display = tk.Tk()
        self.display.title("GitManager")
        self.display.configure(background=green)
        self.display.geometry(f"{700}x{400}")

        # Widgets lists
        self.dir_widgets = []
        self.fil_widgets = []

        # Selected things to push
        self.destination_repo = None
        self.selected_files = []
        self.selected_dirs = []
    
    # repository buttons
    def repo_buttons(self):
        
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
        # upload widgets
        for widget in self.display.winfo_children():
            if widget != self.button and widget != self.button2:
                widget.place_forget()

        # newRepo clicked
        if self.button["relief"] == "raised" and not bttn:
            self.create_repo_menu()
            self.button["relief"] = "sunken"
            self.button2["relief"] = "raised"
        # existingRepo clicked
        elif self.button2["relief"] == "raised" and bttn:
            self.push_repo_menu()
            self.button["relief"] = "raised"
            self.button2["relief"] = "sunken"

    # Select directory/files to push
    def push_repo_menu(self):
        # "To push"
        info = tk.Label(
            self.display,
            text="To push:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
            )
        info.place(
            relx=0.13,
            rely=0.26,
            anchor="center"
        )

        # "Your Repository" Button
        self.dest_repo_button = tk.Button(
            self.display,
            text="Click to select destination repository",
            width=60,
            height=2,
            command=lambda: self.select_dir(0)
        )
        self.dest_repo_button.place(
            relx=0.55,
            rely=0.26,
            anchor="center"
        )

        # Push Whole Directory
        self.push_option = tk.BooleanVar()
        directory_option = tk.Radiobutton(
            self.display, 
            width=8,
            height=1,
            value=False, # 0
            variable=self.push_option,
            text="Directory",
            command=self.push_directory_option
        )
        directory_option.place(
            relx=0.13,
            rely=0.38,
            anchor="center"
        )

        # Push Some Files
        file_option = tk.Radiobutton(
            self.display, 
            width=8,
            height=1,
            value=True, # 1
            variable=self.push_option,
            text="Files",
            command=self.push_files_option
        )
        file_option.place(
            relx=0.13,
            rely=0.48,
            anchor="center"
        )

        # Commit Label
        commit_label = tk.Label(
            self.display,
            text="Commit -m:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
        )
        commit_label.place(
            relx=0.13,
            rely=0.6,
            anchor="center"
        )

        # Commit Message Entry
        self.commit_entry = tk.Entry(
            self.display,
            width=55
        )
        self.commit_entry.place(
            relx=0.5,
            rely=0.6,
            anchor="center"
        )

        # Commit Add Message
        commit_add_button = tk.Button(
            self.display,
            text="+",
            width=5,
            height=2,
            borderwidth=0,
            command=self.save_commit_message
        )
        commit_add_button.place(
            relx=0.8,
            rely=0.6,
            anchor="center"
        )

        # Last Commit
        self.last_commit_label = tk.Label(
            self.display,
            text="Last Commit: ",
            width=50,
            height=1,
            borderwidth=0,
            background=green
        )
        self.last_commit_label.place(
            relx=0.5,
            rely=0.65,
            anchor="center"
        )

        # Push Button
        push_button = tk.Button(
            self.display,
            text="Push",
            width=10,
            height=2,
            borderwidth=0,
            command=self.push_all
        )
        push_button.place(
            relx=0.4,
            rely=0.85,
            anchor="center"
        )

        # Reset Git Button
        reset_git_button = tk.Button(
            self.display,
            text="Reset Git",
            width=10,
            height=2,
            borderwidth=0,
            command=lambda: print("Reset Git")
        )
        reset_git_button.place(
            relx=0.6,
            rely=0.85,
            anchor="center"
        )

    def push_directory_option(self):
        # hide "push_files_option" widgets
        for widget in self.fil_widgets:
            widget.place_forget()

        # "ADD+" directory button
        self.select_dir_button = tk.Button(
            self.display,
            text="ADD+",
            width=6,
            height=2,
            command=lambda: self.select_dir(1)
        )
        self.select_dir_button.place(
            relx=0.28,
            rely=0.43,
            anchor="center"
        )
        self.dir_widgets.append(self.select_dir_button)

        # show selected directory
        self.selected_dir_label = tk.Label(
            self.display,
            text="Directory: ",
            width=50,
            height=2
        )
        self.selected_dir_label.place(
            relx=0.6,
            rely=0.43,
            anchor="center"
        )
        self.dir_widgets.append(self.selected_dir_label)

    def push_files_option(self):
        # hide "push_directory_option" widgets
        for widget in self.dir_widgets:
            widget.place_forget()

        # ADD+ file button
        self.add_file_button = tk.Button(
            self.display,
            text="ADD+",
            width=6,
            height=2,
            command=self.select_file
        )
        self.add_file_button.place(
            relx=0.28,
            rely=0.43,
            anchor="center"
        )

        # added files info
        self.added_files_label = tk.Label(
            self.display,
            text="Files: ",
            width=50,
            height=2
        )
        self.added_files_label.place(            
            relx=0.6,
            rely=0.43,
            anchor="center"
        )
        
    def save_commit_message(self):
        self.commit_message = self.commit_entry.get()

    # Select ___ funcs
    def select_dir(self, type=None):
        try:
            dir_path = askdirectory(title='Select directory')
            if dir_path == "":
                messagebox.showwarning(message="You must select some directory")
                return

            if type:
                self.selected_dirs.append(dir_path)
                self.selected_dir_label["text"] += dir_path
            if not type:
                self.destination_repo = dir_path
                self.dest_repo_button["text"] = f"Current Repo: {dir_path}"
                try:
                    last_commit = self.get_last_commit(dir_path)
                    self.last_commit_label["text"] = f"Last Commit: {last_commit}"
                except:
                    pass

        except git.exc.InvalidGitRepositoryError:
            print("The directory is not a valid git repository.")

    def select_file(self):
        try:
            file = askopenfilename(title='Add file')
            if file == "":
                messagebox.showwarning(message="You must select some file")
                return

            file = path.basename(file)
            self.selected_files.append(file)
            self.added_files_label["text"] += f"{file}, "
        
        except git.exc.InvalidGitRepositoryError:
            print("The directory is not a valid git repository.")
    
    def get_last_commit(self, dir_path):
        try:
            g = Github(github_token)
            user = g.get_user()
            repo = path.basename(dir_path)
            repo = user.get_repo(repo)
            commits = repo.get_commits()
            return commits[0].commit.message
        except GithubException:
            pass
    
    def push_all(self):
        try:
            # Set Destination Repository
            repo = git.Repo(self.destination_repo)

            # Add Everything
            for file in self.selected_files:
                repo.git.add(file)

            for folder in self.selected_dirs:
                repo.git.add(folder)

            # Commit message
            repo.git.commit(m=self.commit_message)

            # Push all to User's Github
            origin = repo.remote(name='origin')
            origin.push()

            # Succes Label
            succes_label = tk.Label(
                self.display,
                width=50,
                height=2,
                text="Successfuly pushed to Your Github repository",
                background="green"
            )
            succes_label.place(
                relx=0.5,
                rely=0.75,
                anchor="center"
            )
        
        except git.exc.InvalidGitRepositoryError:
            messagebox.showerror(message="The directory is a valid git repository.")
        except git.exc.GitCommandError as e:
            messagebox.showerror(message=f"Error occurred when: {e}")
    
    # Create new Github repository
    def create_repo_menu(self):

        # "Your Repository"
        self.dest_repo_button = tk.Button(
            self.display,
            text="Click to select destination repository",
            width=60,
            height=2,
            command=lambda: self.select_dir(0)
        )
        self.dest_repo_button.place(
            relx=0.55,
            rely=0.26,
            anchor="center"
        )

        info = tk.Label(
            self.display,
            text="Repository place:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
            )
        info.place(
            relx=0.13,
            rely=0.26,
            anchor="center"
        )

        # Token
        token_label = tk.Label(
            self.display,
            text="Github Token:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
        )
        token_label.place(
            relx=0.13,
            rely=0.38,
            anchor="center"
        )

        self.token_entry = tk.Entry(
            self.display,
            width=55
        )
        self.token_entry.place(
            relx=0.5,
            rely=0.38,
            anchor="center"
        )
      
        # Name
        repo_name = tk.Label(
            self.display,
            text="Repo name",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
        )
        repo_name.place(
            relx=0.13,
            rely=0.5,
            anchor="center"
        )

        self.repo_name_entry = tk.Entry(
            self.display,
            width=55
        )
        self.repo_name_entry.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Description
        repo_description = tk.Label(
            self.display,
            text="Description:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
        )
        repo_description.place(
            relx=0.13,
            rely=0.62,
            anchor="center"
        )

        self.repo_description_entry = tk.Entry(
            self.display,
            width=55
        )
        self.repo_description_entry.place(
            relx=0.5,
            rely=0.62,
            anchor="center"
        )

        # Status
        self.private_status = tk.BooleanVar()
        repo_status = tk.Label(
            self.display,
            text="Status:",
            width=18,
            height=2,
            borderwidth=0,
            background="green"
        )
        repo_status.place(
            relx=0.13,
            rely=0.74,
            anchor="center"
        )

        repo_status_pub = tk.Radiobutton(
            self.display,
            width=8,
            height=1,
            value=False,
            variable=self.private_status,
            text="Public"
        )
        repo_status_pub.place(
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
        create_repo_button = tk.Button(
            self.display,
            text="Create",
            width=30,
            height=2,
            borderwidth=0,
            command=self.create_repository
        )
        create_repo_button.place(
            relx=0.5,
            rely=0.88,
            anchor="center"
        )

    def create_repository(self):  
        try:
            # Get Github User
            #github_token = self.token_entry.get()
            #github_username = self.username_entry.get()

            repo_name = self.repo_name_entry.get()
            repo_description = self.repo_description_entry.get()
            status = self.private_status.get()
        
            # initialize in git
            repo = git.Repo.init(self.destination_repo)

            # create in Github
            g = Github(github_token)
            user = g.get_user()
            user.create_repo(
                repo_name,
                allow_rebase_merge=True,
                auto_init=False,
                description=repo_description,
                has_issues=True,
                has_projects=False,
                has_wiki=False,
                private=status,
            )

            url = f"https://github.com/KarolO77/{repo_name}.git"
            repo.git.commit(m="Initial commit")
            repo.git.branch('-M', 'main')
            repo.create_remote("origin", url)
            origin = repo.remote(name="origin")
            origin.push()

        except git.exc.GitCommandError as e:
            messagebox.showerror(message=f"Error occurred when: {e}")
        except GithubException as e:
            messagebox.showerror(message=f"Error occurred when: {e}")

    # run
    def run(self):
        self.repo_buttons()
        self.display.mainloop()


# Run the application
if __name__ == "__main__":
    main = Main()
    main.run()
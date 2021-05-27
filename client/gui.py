import tkinter as tk
import tkinter.messagebox as messagebox
from openapi_client.api.default_api import DefaultApi
from openapi_client.api_client import ApiClient
from openapi_client.configuration import Configuration
import openapi_client.models as models
import time
from datetime import datetime
import threading


class ChatGUI:
    def __init__(self, api: DefaultApi):
        self.root = tk.Tk()
        self.root.title("Chat")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.is_running = True

        self.chats = []
        self.user = None
        self.users = dict()
        self.show_login()

        self.greet_label = tk.Label(self.root)
        self.greet_label.grid(column=1, row=1)

        self.info_label = tk.Label(self.root, text='Double-click user to start')
        self.info_label.grid(column=1, row=5, rowspan=3)

        self.logout_button = tk.Button(self.root, text="Log Out", command=self.show_login)
        self.logout_button.grid(column=1, row=8, sticky=tk.EW)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.on_closing, width=20)
        self.exit_button.grid(column=1, row=9, sticky=tk.EW)

        self.users_frame = tk.Frame(self.root)
        self.users_label = tk.Label(self.users_frame, text='List of users')
        self.users_label.pack()
        scroll = tk.Scrollbar(self.users_frame)
        self.users_list = tk.Listbox(self.users_frame, yscrollcommand=scroll.set)
        self.users_list.bind('<Double-Button>', self.open_chat)
        self.users_list.pack(side=tk.LEFT)
        scroll.config(command=self.users_list.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.users_frame.grid(column=0, row=0, rowspan=10)

        self.users_activity_thread = threading.Thread(target=self.update_users_list, daemon=True,
                                                      args=(lambda: self.is_running,))

        self.users_activity_thread.start()

        self.root.mainloop()

    def show_login(self):
        self.root.withdraw()

        for i in range(len(self.chats)):
            self.chats[i].destroy()

        if self.user:
            self.try_change_status(False)
        self.user = None

        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        login_window.geometry("+%d+%d" % (x + 100, y + 200))

        label_login = tk.Label(login_window, text="Login:")
        entry_login = tk.Entry(login_window)
        label_password = tk.Label(login_window, text="Password:")
        entry_password = tk.Entry(login_window, show='*')

        login_window.bind('<Return>',
                          lambda event: self.try_login(entry_login.get(), entry_password.get(), login_window))

        button_login = tk.Button(login_window, text="Login",
                                 command=lambda: self.try_login(entry_login.get(), entry_password.get(), login_window))
        button_register = tk.Button(login_window, text="Register",
                                    command=lambda: self.try_register(entry_login.get(), entry_password.get(),
                                                                      login_window))

        label_login.grid(column=0, row=0)
        entry_login.grid(column=1, row=0)
        button_login.grid(column=2, row=0, sticky=tk.EW)
        label_password.grid(column=0, row=1)
        entry_password.grid(column=1, row=1)
        button_register.grid(column=2, row=1, sticky=tk.EW)

    def update_users_list(self, loop: bool):
        users: list(models.User) = None
        try:
            users = api.read_users_users_get()
        except:
            messagebox.showerror("Error", "Failed to obtain list of users!")

        self.users_list.delete(0, 'end')
        self.users.clear()
        for i in range(len(users)):
            if users[i].login != 'admin':
                self.users_list.insert(i, f"{'(+)' if users[i].is_active else '(-)'} {users[i].login}")
                self.users[users[i].login] = users[i].id
        self.users_list.insert(0, '(+) general')
        self.users['general'] = 0

        time.sleep(5)
        if (self.is_running):
            self.update_users_list(self.is_running)

    def open_chat(self, *args):
        receiver_login = self.users_list.get(self.users_list.curselection()[0])[4:]
        receiver_id = self.users[receiver_login]
        chat = self.ChatWindow(self.user.login, self.user.id, receiver_login, receiver_id)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        chat.geometry("+%d+%d" % (x + 100, y + 200))

        self.chats.append(chat)

    def try_login(self, login, password, login_window=None):
        res = None
        loggedIn = False
        try:
            users = api.read_users_users_get()

            for i in users:
                if i.login == login and i.is_active:
                    loggedIn = True

            if not loggedIn:
                res = api.login_user_users_login_post(models.UserCreate(login, password))
            else:
                messagebox.showerror("Login error", "User with given login is already logged in!")
        except:
            messagebox.showerror("Login error", "User with this password does not exists!")

        if res and not loggedIn:
            self.user = res
            self.try_change_status(True)
            self.greet_label.config(text=f"Welcome, {self.user.login}!")
            self.root.deiconify()
            login_window.destroy()

    def try_register(self, login, password, login_window):
        res = None
        try:
            res = api.create_user_users_post(models.UserCreate(login, password))
        except:
            messagebox.showerror("Register error", "User with this name already exists!")

        if res:
            self.user = res
            self.try_change_status(True)
            self.root.deiconify()
            login_window.destroy()

    def try_change_status(self, status):
        res = None
        res = api.update_user_status_users_status_put(models.User(self.user.login, self.user.id, status))

    def on_closing(self):
        res = messagebox.askyesno("Exit", "Do you really want to Exit?")
        if res:
            if self.user:
                self.try_change_status(False)
            self.is_running = False
            self.root.destroy()

    class ChatWindow(tk.Toplevel):
        def __init__(self, my_login, my_id, receiver_login, receiver_id, *args, **kwargs):
            tk.Toplevel.__init__(self, *args, **kwargs)
            self.my_id = my_id
            self.my_login = my_login
            self.receiver_id = receiver_id
            self.receiver_login = receiver_login
            self.messages: [models.Message] = []
            self.is_running = True
            self.last_update = datetime.fromtimestamp(0)

            self.title(f"Chat with {self.receiver_login}")
            self.protocol("WM_DELETE_WINDOW", self.on_closing)

            self.chat_frame = tk.Frame(self)
            self.chat_frame.grid()
            self.scroll = tk.Scrollbar(self.chat_frame)
            self.chat_text = tk.Text(self.chat_frame, yscrollcommand=self.scroll.set)
            self.chat_text.pack(side=tk.LEFT)
            self.scroll.config(command=self.chat_text.yview)
            self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

            self.update_messages_loop = threading.Thread(target=self.update_messages, daemon=True,
                                                         args=(lambda: self.is_running,))
            self.update_messages_loop.start()

            self.message_entry = tk.Entry(self)
            self.message_entry.bind('<Return>', lambda event: self.send_message())
            self.message_entry.grid(sticky=tk.EW)

            self.send_button = tk.Button(self, text='Send', command=self.send_message)
            self.send_button.grid(sticky=tk.EW)

        def update_messages(self, loop: bool):
            temp_time = datetime.now()
            try:
                self.messages = api. \
                    read_messages_to_user_from_date_message_receiver_id_sender_id_from_date_get(
                    self.my_id,
                    self.receiver_id,
                    self.last_update.strftime('%Y-%m-%dT%H:%M:%S.%f'))
            except:
                self.messages = []

            if len(self.messages) > 0:
                users: list(models.User) = None
                try:
                    users = api.read_users_users_get()
                except:
                    messagebox.showerror("Error", "Failed to obtain list of users!")

                self.chat_text.config(state='normal')
                for i in range(len(self.messages)):
                    # header = self.my_login if self.messages[i].from_usr == self.my_id else self.receiver_login
                    header = users[self.messages[i].from_usr - 1].login
                    line = f"'{header}' said at {self.messages[i].date.strftime('%H:%M:%S, %m/%d/%y')}\n" \
                           f"{self.messages[i].msg_content}\n\n"
                    self.chat_text.insert('end', line)
                    self.chat_text.see(tk.END)
                self.chat_text.config(state='disabled')

            self.last_update = temp_time
            time.sleep(2.5)
            if self.is_running:
                self.update_messages(self.is_running)

        def send_message(self):
            resp = None
            msg_content = self.message_entry.get()

            if msg_content:
                msg = models.MessageCreate(msg_content, self.my_id)

                if self.my_login != 'admin' and msg_content.startswith('/'):
                    msg_content = 'Commands can be only executed by admin!'
                    msg = models.MessageCreate(msg_content, self.my_id)
                elif self.my_login == 'admin' and msg_content.startswith('/'):
                    if msg_content.startswith('/kick'):
                        kick_user = msg_content[6:]
                        print(kick_user)
                    elif msg_content.startswith('/ban'):
                        ban_user = msg_content[5:]
                        print(ban_user)
                else:
                    resp = api.create_message_from_user_message_receiver_id_post(self.receiver_id, msg)

            self.message_entry.delete(0, 'end')

        def on_closing(self):
            self.is_running = False
            self.destroy()


if __name__ == "__main__":
    config = Configuration()
    config.host = "http://127.0.0.1:8000"
    api = DefaultApi(ApiClient(config))

    gui = ChatGUI(api)

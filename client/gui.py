import tkinter as tk
import tkinter.messagebox as messagebox

from openapi_client.api.default_api import DefaultApi
from openapi_client.api_client import ApiClient
from openapi_client.configuration import Configuration
import openapi_client.models as models
from datetime import datetime
import threading
import websockets
import websocket


class ChatGUI:
    def __init__(self, api: DefaultApi):
        """
        creating the main user panel with a list of active users and a panel for logging out and exiting
        :param api:
        """
        self.root = tk.Tk()
        self.root.title("Chat")
        self.root.resizable(width=False, height=False)
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

        self.root.mainloop()

    def show_login(self):
        """
        creating a login panel
        :return:
        """
        self.root.withdraw()
        self.webSoc_thread = threading.Thread(target=self.websockets_connect, daemon=True)

        for i in range(len(self.chats)):
            self.chats[i].destroy()

        if self.user:
            self.try_change_status(False)
        self.user = None

        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.resizable(width=False, height=False)
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

    def update_users_list(self):
        """
        updating the list of active users
        :return:
        """
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

    def open_chat(self, *args):
        """
        opening a chat with the other person
        :param args:
        :return:
        """
        receiver_login = self.users_list.get(self.users_list.curselection()[0])[4:]
        receiver_id = self.users[receiver_login]
        chat = self.ChatWindow(self.user.login, self.user.id, receiver_login, receiver_id)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        chat.geometry("+%d+%d" % (x + 100, y + 200))

        self.chats.append(chat)

    def try_login(self, login, password, login_window=None):
        """
        user login attempt
        :param login: login of the user who wants to log in
        :param password: password of the user who wants to log in
        :param login_window: window for which the method was called
        :return:
        """
        res = None
        loggedIn = ban_state = False
        try:
            users = api.read_users_users_get()

            for user in users:
                if user.login == login:
                    ban_state = user.is_banned
                    if user.is_active:
                        loggedIn = True

            if ban_state:
                messagebox.showerror("Login error", "You are banned from this server!")
            elif not loggedIn:
                res = api.login_user_users_login_post(models.UserCreate(login, password))
            else:
                messagebox.showerror("Login error", "User with given login is already logged in!")
        except:
            messagebox.showerror("Login error", "User with this password does not exists!")
        if res and not loggedIn and not ban_state:
            self.login_successful(res, login_window)

    def try_register(self, login, password, login_window):
        """
        user register attempt
        :param login: login of the user who wants to register
        :param password: password of the user who wants to register
        :param login_window: window for which the method was called
        :return:
        """
        res = None
        try:
            res = api.create_user_users_post(models.UserCreate(login, password))
        except:
            messagebox.showerror("Register error", "User with this name already exists!")

        if res:
            self.login_successful(res, login_window)

    def login_successful(self, res, login_window):
        """
        perform login for the user
        :param res: user who logs in
        :param login_window: window for which the method was called
        :return:
        """
        self.user = res
        self.try_change_status(True)
        self.greet_label.config(text=f"Welcome, {self.user.login}!")
        self.root.deiconify()
        login_window.destroy()
        self.update_users_list()
        self.webSoc_thread.start()

    def try_change_status(self, status):
        """
        change user status (is_active)
        :param status: new user status
        :return:
        """
        res = None
        res = api.update_user_status_users_status_put(models.User(self.user.login, self.user.id, status, False))

    def on_closing(self):
        """
        exit the application / close the window
        :return:
        """
        res = messagebox.askyesno("Exit", "Do you really want to Exit?")
        if res:
            if self.user:
                self.try_change_status(False)
            self.is_running = False
            self.root.destroy()

    def websockets_connect(self):
        """
        connect to chat
        :return:
        """
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(f"ws://127.0.0.1:8000/ws/{self.user.id}",
                                         on_message=self.on_message)
        self.ws.run_forever()

    def on_message(self, x, message):
        """
        receiving control commands from the server
        :param x:
        :param message: message send from server
        :return:
        """
        active_chats = []
        for chat in self.chats:
            if not chat.is_running:
                chat.destroy()
                chat.update()
            else:
                active_chats.append(chat)
        self.chats = active_chats
        if message == "offline":
            self.ws.close()
        elif message == "status":
            self.update_users_list()
        elif message == "update_mess":
            for chat in self.chats:
                chat.update_messages()
        elif message == "kick":
            res = messagebox.showinfo("KICK FROM SERVER", "You were kicked out of the server")
            if res:
                self.try_change_status(False)
            self.close()
        elif message == "ban":
            res = messagebox.showinfo("KICK FROM SERVER", "You were kicked out of the server")
            if res:
                self.try_change_status(False)
            self.close()

    def close(self):
        """
        close the connection and destroy main user panel
        :return:
        """
        self.ws.close()
        self.is_running = False
        self.root.destroy()

    class ChatWindow(tk.Toplevel):
        def __init__(self, my_login, my_id, receiver_login, receiver_id, *args, **kwargs):
            """

            :param my_login: login of the current user
            :param my_id: id of the current user
            :param receiver_login: login of the user with which the current user is writing
            :param receiver_id: id of the user with which the current user is writing
            :param args:
            :param kwargs:
            """
            tk.Toplevel.__init__(self, *args, **kwargs)
            self.my_id = my_id
            self.my_login = my_login
            self.receiver_id = receiver_id
            self.receiver_login = receiver_login
            self.messages: [models.Message] = []
            self.is_running = True
            self.last_update = datetime.fromtimestamp(0)

            self.title(f"Chat with {self.receiver_login}")
            self.resizable(width=False, height=False)
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
            # self.update_messages()

        def update_messages(self, test=True):
            """
            updating messages
            :return:
            """
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
                    header = users[self.messages[i].from_usr - 1].login
                    header = 'You' if header == self.my_login else header
                    line = f"'{header}' said at {self.messages[i].date.strftime('%H:%M:%S, %m/%d/%y')}\n" \
                           f"{self.messages[i].msg_content}\n\n"
                    self.chat_text.insert('end', line)
                    self.chat_text.see(tk.END)
                self.chat_text.config(state='disabled')

            self.last_update = temp_time

        def send_message(self):
            """
            sending messages to other client
            :return:
            """
            resp = None
            msg_content = self.message_entry.get()

            if msg_content:
                msg = models.MessageCreate(msg_content, self.my_id)
                is_kicked = True

                if self.my_login != 'admin' and msg_content.startswith('/'):
                    msg_content = 'Commands can be only executed by admin!'
                    msg = models.MessageCreate(msg_content, self.my_id)
                elif self.my_login == 'admin' and msg_content.startswith('/'):
                    if msg_content.startswith('/kick'):
                        kick_user = msg_content[6:]
                        kick_user_id = self.kick_from_server(kick_user)
                        if kick_user_id is None:
                            messagebox.showwarning("ERROR", "User with given nickname doesn't exists!")
                            is_kicked = False
                        else:
                            res = api.kick_user_user_kick_get(kick_user_id)
                    elif msg_content.startswith('/ban'):
                        ban_user = msg_content[5:]
                        ban_user_id = self.kick_from_server(ban_user)
                        if ban_user_id is None:
                            messagebox.showwarning("ERROR", "User with given nickname doesn't exists!")
                            is_kicked = False
                        else:
                            res = api.ban_user_user_ban_put(models.UserBan(ban_user_id, True))
                    elif msg_content.startswith('/unban'):
                        unban_user = msg_content[7:]
                        try:
                            users = api.read_users_users_get()
                            unban_user_id = None
                            for user in users:
                                if user.login == unban_user:
                                    unban_user_id = user.id
                            res = api.ban_user_user_ban_put(models.UserBan(unban_user_id, False))
                        except:
                            messagebox.showerror("Error", "Failed to obtain list of users!")

                if is_kicked:
                    res = api.create_message_from_user_message_receiver_id_post(self.receiver_id, msg)

            self.message_entry.delete(0, 'end')

        def kick_from_server(self, kick_user):
            """
            kick user from the server
            :param kick_user: user to be kicked
            :return:
            """
            try:
                users = api.read_users_users_get()
                kick_user_id = None
                for user in users:
                    if user.login == kick_user:
                        kick_user_id = user.id
                print(kick_user_id)
            except:
                messagebox.showerror("Error", "Failed to obtain list of users!")

            return kick_user_id

        def on_closing(self):
            """
            close chat with other user
            :return:
            """
            self.is_running = False
            self.destroy()


if __name__ == "__main__":
    config = Configuration()
    config.host = "http://127.0.0.1:8000"
    api = DefaultApi(ApiClient(config))

    gui = ChatGUI(api)

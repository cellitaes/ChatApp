import tkinter as tk
import tkinter.messagebox as messagebox

from fastapi import websockets
from terminado import websocket

from openapi_client.api.default_api import DefaultApi
from openapi_client.api_client import ApiClient
from openapi_client.configuration import Configuration
import openapi_client.models as models
from datetime import datetime
import threading



class ChatGUI:
    def __init__(self, api: DefaultApi):
        self.root = tk.Tk()
        self.root.title("ChatUp")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.is_running = True

        self.chats = []
        self.user = None
        self.users = dict()
        self.show_login()

        self.greet_label = tk.Label(self.root)
        self.greet_label.grid(column=1, row=1)

        self.info_label = tk.Label(self.root, text='Double-click user name to start chat')
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

        # self.users_activity_thread = threading.Thread(target=self.update_users_list, daemon=True,
        #                                               args=(lambda: self.is_running,))
        # self.users_activity_thread.start()
        self.root.mainloop()

    def show_login(self):
        self.root.withdraw()
        self.ws_thread = threading.Thread(target=self.websockets_connect, daemon=True)

        for i in range(len(self.chats)):
            self.chats[i].destroy()

        if self.user:
            self.try_change_status(False)
        self.user = None

        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login")
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.login_window.geometry("+%d+%d" % (x + 100, y + 200))

        label_login = tk.Label(self.login_window, text="Login:")
        entry_login = tk.Entry(self.login_window)
        label_password = tk.Label(self.login_window, text="Password:")
        entry_password = tk.Entry(self.login_window, show='*')

        self.login_window.bind('<Return>',
                          lambda event: self.try_login(entry_login.get(), entry_password.get(), self.login_window))

        button_login = tk.Button(self.login_window, text="Login",
                                 command=lambda: self.try_login(entry_login.get(), entry_password.get(), self.login_window))
        button_register = tk.Button(self.login_window, text="Register",
                                    command=lambda: self.try_register(entry_login.get(), entry_password.get(),
                                                                      self.login_window))

        label_login.grid(column=0, row=0)
        entry_login.grid(column=1, row=0)
        button_login.grid(column=2, row=0, sticky=tk.EW)
        label_password.grid(column=0, row=1)
        entry_password.grid(column=1, row=1)
        button_register.grid(column=2, row=1, sticky=tk.EW)

    def update_users_list(self):
        users: list(models.User) = None
        to_sort = []
        try:
            users = api.read_users_users_get()
        except:
            messagebox.showerror("Error", "Failed to obtain list of users!")
        self.users_list.delete(0, 'end')
        self.users.clear()
        for i in range(len(users)):
            self.users[users[i].login] = users[i].id
            try:
                unread = api.unread_messages_to_user_from_message_receiver_id_sender_id_unread_post(self.user.id, users[i].id)
                latest = api.read_messages_to_user_from_latest_message_receiver_id_sender_id_latest_post(self.user.id, users[i].id)
            except:
                unread = 0
                latest = 0
            to_sort.append({"login":users[i].login, "unread": unread, "latest": latest, "active": users[i].is_active})

        to_sort.sort(key=lambda obj: (obj['latest'],obj['active']), reverse=True)
        for usr in to_sort:
            self.users_list.insert(i, f"{'(a)' if usr['active'] else '(n)'} ({usr['unread']}) - {usr['login']}")



    def open_chat(self, *args):
        sep = self.users_list.get(self.users_list.curselection()[0]).find("-")+2
        receiver_login = self.users_list.get(self.users_list.curselection()[0])[sep:]
        receiver_id = self.users[receiver_login]
        chat = self.ChatWindow(self.user.login, self.user.id, receiver_login, receiver_id)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        chat.geometry("+%d+%d" % (x + 100, y + 200))

        self.chats.append(chat)

    def try_login(self, login, password, login_window=None):
        res = None
        try:
            res = api.login_user_users_login_post(models.UserCreate(login, password))
        except:
            messagebox.showerror("Login error", "User with this password does not exists!")

        if res:
            self.succ_log(res)

    def try_register(self, login, password, login_window):
        res = None
        try:
            res = api.create_user_users_post(models.UserCreate(login, password))
        except:
            messagebox.showerror("Register error", "User with this name already exists!")

        if res:
            self.succ_log(res)

    def succ_log(self, res):
        self.user = res
        self.try_change_status(True)
        self.greet_label.config(text=f"Welcome, {self.user.login}!")
        self.root.deiconify()
        self.update_users_list()
        self.login_window.destroy()
        self.ws_thread.start()

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

    def websockets_connect(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(f"ws://127.0.0.1:8000/ws/{self.user.id}",
                                    on_message=self.on_message)
        self.ws.run_forever()

    def on_message(self, message):
        # print(message)
        active_chats = []
        for chat in self.chats:
            if not chat.is_running:
                chat.destroy()
                chat.update()
                print("destroyed")
            else:
                active_chats.append(chat)
            self.chats = active_chats
        if message == "offline":
            self.ws.close()
        elif message == "status":
            self.update_users_list()
        elif message == "new_message":
            for chat in self.chats:
                chat.update_messages()
            self.update_users_list()
        elif message == "read":
            self.update_users_list()
            for chat in self.chats:
                chat.message_read()


    class ChatWindow(tk.Toplevel):
        def __init__(self, my_login, my_id, receiver_login, receiver_id, *args, **kwargs):
            tk.Toplevel.__init__(self, *args, **kwargs)
            self.main_frame = tk.Frame(self)
            self.main_frame.grid(sticky=tk.NSEW)
            self.my_id = my_id
            self.my_login = my_login
            self.receiver_id = receiver_id
            self.receiver_login = receiver_login
            self.messages: [models.Message] = []
            self.is_running = True
            self.last_update = datetime.fromtimestamp(0)
            self.counter = 2
            self.chat_msgs = dict()

            self.title(f"ChatUp with {self.receiver_login}")
            self.protocol("WM_DELETE_WINDOW", self.on_closing)

            container = tk.Frame(self.main_frame)
            self.canvas = tk.Canvas(container)
            self.scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
            self.chat_text = tk.Frame(self.canvas)
            self.chat_text.columnconfigure(0, weight=100)
            self.chat_text.columnconfigure(1, weight=999)
            self.chat_text.columnconfigure(2, weight=999)
            self.chat_text.columnconfigure(3, weight=100)

            self.chat_text.bind(
                "<Configure>",
                lambda e: self.canvas.configure(
                    scrollregion=self.canvas.bbox("all")
                )
            )

            self.canvas.create_window((0, 0), window=self.chat_text, anchor="nw")

            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            container.grid(sticky=tk.NSEW)
            self.canvas.pack(side="left", fill="both", expand=True)
            self.scrollbar.pack(side="right", fill="y")

            self.update_messages()

            self.message_entry = tk.Entry(self.main_frame)
            self.message_entry.bind('<Return>', lambda event: self.send_message())
            self.message_entry.grid(sticky=tk.EW)

            self.send_button = tk.Button(self.main_frame, text='Send', command=self.send_message)
            self.send_button.grid(sticky=tk.EW)
            tk.Label(self.chat_text, width=52,).grid(sticky=tk.E, column=1, columnspan=2, row=self.counter)
            tk.Label(self.chat_text, width=52,).grid(sticky=tk.W, column=0, columnspan=2, row=self.counter)
            self.canvas.yview_moveto('1.0')

        def update_messages(self):
            temp_time = datetime.now()
            try:
                messages = api. \
                    read_messages_to_user_from_date_message_receiver_id_sender_id_from_date_get(
                    self.my_id,
                    self.receiver_id,
                    self.last_update.strftime('%Y-%m-%dT%H:%M:%S.%f'))
            except:
                messages = []

            if len(messages) > 0:
                newly_read = []
                for i in range(len(messages)):
                    if messages[i].from_usr == self.my_id:
                        header = self.my_login
                        color = "AQUAMARINE" if messages[i].is_read else "LIGHTBLUE"
                        column = 0
                        sticky = tk.E
                        if not messages[i].is_read and messages[i].to_usr == self.my_id:
                            newly_read.append(messages[i].id)
                    else:
                        header = self.receiver_login
                        color = "LIGHTGRAY"
                        column = 1
                        sticky = tk.W
                        if not messages[i].is_read:
                            newly_read.append(messages[i].id)

                    line = f"'{header}' said at {messages[i].date.strftime('%H:%M:%S, %m/%d/%y')}\n" \
                           f"{messages[i].msg_content}\n\n"

                    scroll_position = self.scrollbar.get()
                    new_msg = tk.Label(self.chat_text, text=line, background=color, wraplength=300)
                    new_msg.grid(sticky=sticky, column=column, columnspan=2, row=self.counter, pady=(0, 10))
                    self.chat_msgs[messages[i].id]=new_msg
                    self.counter = self.counter + 1
                    
                    if scroll_position[1] > 0.925:
                        self.canvas.yview_moveto('1.0')

                api.update_message_status_message_receiver_id_read_put(self.my_id, newly_read)
            self.last_update = temp_time

        def message_read(self):
            try:
                messages = api.read_messages_to_user_from_message_receiver_id_sender_id_get(self.my_id, self.receiver_id)
            except:
                messages = []

            for message in messages:
                if message.from_usr == self.my_id and message.is_read:
                    try:
                        self.chat_msgs[message.id].configure(background="AQUAMARINE")
                    except:
                        pass

        def send_message(self):
            resp = None
            msg_content = self.message_entry.get()
            if msg_content:
                msg = models.MessageCreate(msg_content, self.my_id)

                resp = api.create_message_from_user_message_receiver_id_post(self.receiver_id, msg)
            self.message_entry.delete(0, 'end')

        def on_closing(self):
            self.is_running = False
            self.destroy()

async def ws_conn(id):
    uri = f"ws://127.0.0.1:8000/ws/{id}"
    async with websockets.connect(uri) as websocket:
        ws = websocket
        while True:
            msg = await websocket.recv()
            print(msg)


if __name__ == "__main__":
    config = Configuration()
    config.host = "http://127.0.0.1:8000"
    api = DefaultApi(ApiClient(config))

    gui = ChatGUI(api)
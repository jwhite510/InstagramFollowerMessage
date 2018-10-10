import imageio
imageio.plugins.ffmpeg.download()
from InstagramAPI import InstagramAPI
import tkinter as tk
from tkinter import ttk
import time
import datetime
import getpass
import sys
from messagefollowers import message_user, get_recent_followers


class AppWindow(tk.Tk):
    def __init__(self, username, password):
        tk.Tk.__init__(self,)
        tk.Tk.wm_title(self, "Instagram Follower Messager")
        self.id = self.after(2000, self.callback)
        self.follow_message = tk.StringVar()
        self.statusvar = tk.StringVar()
        with open('message.txt', 'r') as file:

            message = ''
            for thing in list(file.readlines()):
                message+=thing
            message = message.replace('\n', ' ')

        self.follow_message.set(message)
        self.statusanimnum = 0

        # status
        status_container = tk.LabelFrame(self)
        status_container.grid(row=0, column=0)
        label = tk.Label(status_container, text='Status:')
        label.grid(row=0, column=0)
        label.config(width=5)
        label = tk.Label(status_container, textvar=self.statusvar)
        label.grid(row=0, column=1, columnspan=2)
        label.config(width=5)


        # message displayed
        message_container = tk.LabelFrame(self)
        message_container.grid(row=1, column=0)
        label = tk.Label(message_container, text='{} Follow Message:'.format(username))
        label.grid(row=0, column=0)
        label = tk.Label(message_container, textvar=self.follow_message)
        label.config(width=30, wraplength=150)
        label.grid(row=0, column=1, columnspan=2)


        # recent activity things
        recent_activity_container = tk.LabelFrame(self)
        recent_activity_container.grid(row=2, column=0)
        text_activity = tk.Label(recent_activity_container, text='Recent Activity')
        text_activity.grid(row=0, column=0)
        scrollbar_container = tk.LabelFrame(recent_activity_container)
        scrollbar_container.grid(row=1, column=0)
        # create scrollbar
        scrollbar = tk.Scrollbar(scrollbar_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(scrollbar_container, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listbox.config(width=70)
        scrollbar.config(command=self.listbox.yview)

        # initialize instagram
        self.username = username
        self.password = password

        self.text = self.follow_message.get()

        self.api = InstagramAPI(self.username, self.password)
        self.api.login()

        # get the initial recent followers
        self.dont_message_these_people = get_recent_followers(self.api)
        self.time_started = time.time()


    def callback(self):

        # check if different people are
        recent_followers = get_recent_followers(self.api)

        for recent_follower in recent_followers:

            # check if they are in the list of messaged people
            if recent_follower in self.dont_message_these_people:
                pass

            else:
                # message the person and add them to the dont message list
                message_user(self.api, message=self.text, user=recent_follower)
                datetimestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.listbox.insert(0, datetimestr+"- messaged user: "+recent_follower['username'])
                self.dont_message_these_people.append(recent_follower)


        elapsed = time.time() - self.time_started
        if elapsed > 8 * 60 * 60:
            # every 8 hours reset the dont message list
            self.dont_message_these_people = get_recent_followers(self.api)
            self.time_started = time.time()


        # callback
        self.id = self.after(2000, self.callback)


        # if more than 40 items, remove the oldest
        if self.listbox.size() > 20:
            self.listbox.delete(tk.END)


        # update status bar
        if self.statusanimnum == 0:
            self.statusvar.set('| ')
            self.statusanimnum+=1

        elif self.statusanimnum == 1:
            self.statusvar.set('/ ')
            self.statusanimnum += 1

        elif self.statusanimnum == 2:
            self.statusvar.set('- ')
            self.statusanimnum += 1

        elif self.statusanimnum == 3:
            self.statusvar.set(r'\ ')
            self.statusanimnum = 0



if __name__ == "__main__":

    print('enter instagram login')
    username = input('username:')
    password = getpass.getpass()

    app = AppWindow(username, password)
    app.mainloop()
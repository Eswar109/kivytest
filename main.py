# Import necessary libraries and components
import kivy
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer, MDNavigationDrawerMenu, \
    MDNavigationDrawerHeader
from kivymd.uix.list import OneLineListItem, MDList, ThreeLineIconListItem, TwoLineIconListItem, ThreeLineListItem, \
    TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.popup import Popup
from kivymd.uix.pickers import MDDatePicker
from plyer import filechooser
import mysql.connector
# import helpers
import os
from datetime import datetime
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage

#helpers
screen_helper = '''
ScreenManager:
    LoginScreen:
    SignupScreen:
    ProfileScreen:
    AddTaskScreen:

<LoginScreen>:
    name: 'Login Page'
    MDTextField:
        id: login_username
        hint_text: 'Enter Username'
        helper_text: 'please enter Username'
        helper_text_mode: 'on_focus'
        icon_left: 'account-circle'
        icon_left_color: app.theme_cls.primary_color
        pos_hint: {'center_x' : 0.5, 'center_y' : 0.7}
        size_hint_x: None
        width: 300
    MDTextField:
        id: login_password
        hint_text: 'Enter Password'
        helper_text: 'Enter Password'
        helper_text_mode: 'on_focus'
        icon_left: 'account-lock'
        icon_left_color: app.theme_cls.primary_color
        pos_hint: {'center_x' : 0.5, 'center_y' : 0.6}
        size_hint_x: None
        width: 300
        password: True
    MDRectangleFlatButton:
        text: 'Login'
        pos_hint: {'center_x' : 0.3, 'center_y' : 0.5}
        on_press: root.verify_login()
    MDRectangleFlatButton:
        text: 'SignUp'
        pos_hint: {'center_x' : 0.55, 'center_y' : 0.5}
        on_press: root.manager.current='Signup Page'

<SignupScreen>:
    name: 'Signup Page'
    MDTextField:
        id: signup_username
        hint_text: 'Enter Username'
        helper_text: 'please enter Username'
        helper_text_mode: 'on_focus'
        icon_left: 'account-circle'
        icon_left_color: app.theme_cls.primary_color
        pos_hint: {'center_x' : 0.5, 'center_y' : 0.8}
        size_hint_x: None
        width: 300
    MDTextField:
        id: signup_password
        hint_text: 'Enter Password'
        helper_text: 'Enter Password'
        helper_text_mode: 'on_focus'
        icon_left: 'account-lock'
        icon_left_color: app.theme_cls.primary_color
        pos_hint: {'center_x' : 0.5, 'center_y' : 0.7}
        size_hint_x: None
        width: 300
        password: True
    MDTextField:
        id: signup_fullname
        hint_text: 'Enter Full Name'
        helper_text: 'please enter Full Name'
        helper_text_mode: 'on_focus'
        icon_left: 'account'
        icon_left_color: app.theme_cls.primary_color
        pos_hint: {'center_x' : 0.5, 'center_y' : 0.6}
        size_hint_x: None
        width: 300
    MDTextField:
        id: signup_dob
        hint_text: 'Date Of Birth (YYYY-MM-DD)'
        helper_text: 'Enter DOB '
        helper_text_mode: 'on_focus'
        icon_left: 'calendar'
        icon_left_color: app.theme_cls.primary_color
        pos_hint: {'center_x' : 0.5, 'center_y' : 0.5}
        size_hint_x: None
        width: 300
        readonly: True
        on_focus: if self.focus: root.show_date_picker()
    MDTextField:
        id: signup_email
        hint_text: 'Enter Email'
        helper_text: 'please enter Email'
        helper_text_mode: 'on_focus'
        icon_left: 'email'
        icon_left_color: app.theme_cls.primary_color
        pos_hint: {'center_x' : 0.5, 'center_y' : 0.4}
        size_hint_x: None
        width: 300
    Image:
        id: signup_profile_pic
        source: ''
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        size_hint: (None, None)
        size: (100, 100)
    MDRectangleFlatButton:
        text: 'Choose Profile Pic'
        pos_hint: {'center_x' : 0.5, 'center_y' : 0.2}
        on_press: root.select_file()
    MDRectangleFlatButton:
        text: 'Sign Up'
        pos_hint: {'center_x' : 0.35, 'center_y' : 0.1}
        on_press: root.verify_signup()
    MDRectangleFlatButton:
        text: 'Login'
        pos_hint: {'center_x' : 0.65, 'center_y' : 0.1}
        on_press: root.go_to_login()


<ProfileScreen>:
    name: 'Profile Page'
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDTopAppBar:
                        id: toolbar
                        title: "Hi, User"
                        left_action_items: [['account-circle', lambda x: nav_drawer.set_state('toggle')]]
                        elevation: 10
                    MDBottomNavigation:
                        id: bottom_navigation
                        text_color_active: app.theme_cls.primary_color
                        MDBottomNavigationItem:
                            name: "Ongoing"
                            text: "Ongoing"
                            icon: 'progress-check'
                            on_tab_press: root.switch_tab('Ongoing')
                            BoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "Ongoing Tasks"
                                    font_style: "H5"
                                    halign: 'center'
                                    size_hint_y: None
                                    height: self.texture_size[1]
                                ScrollView:
                                    bar_width: 0
                                    MDList:
                                        id: tasks_layout
                                        padding: dp(10)
                                        spacing: dp(10)
                                        size_hint_y: None
                                        height: self.minimum_height  # Adjust the height dynamically
                                        pos_hint: {'top': 1}
                                        adaptive_height: True
                        MDBottomNavigationItem:
                            name: "Add Task"
                            text: "Add Task"
                            icon: 'plus'
                            on_tab_press: root.manager.current = 'Add Task Page'
                            BoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "Add Task"
                                    font_style: "H5"
                                    halign: 'center'
                                    size_hint_y: None
                                    height: self.texture_size[1]
                        MDBottomNavigationItem:
                            name: "Completed"
                            text: "Completed"
                            icon: 'check-circle'
                            on_tab_press: root.switch_tab('Completed')
                            BoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    text: "Completed Tasks"
                                    font_style: "H5"
                                    halign: 'center'
                                    size_hint_y: None
                                    height: self.texture_size[1]
                                ScrollView:
                                    bar_width: 0
                                    MDList:
                                        id: completed_tasks_layout
                                        padding: dp(10)
                                        spacing: dp(10)
                                        size_hint_y: None
                                        height: self.minimum_height  # Adjust the height dynamically
                                        pos_hint: {'top': 1}
                                        adaptive_height: True
        MDNavigationDrawer:
            id: nav_drawer
            BoxLayout:
                orientation: 'vertical'
                MDNavigationDrawerHeader:
                    text: "User Profile"
                    spacing: "4dp"
                    padding: "12dp"
                Image:
                    id: nav_drawer_image
                    source: ''
                    size_hint: (None, None)
                    size: (200, 200)  # 3:4 ratio
                MDLabel:
                    id: nav_drawer_name
                    text: ''
                    font_style: "Subtitle1"
                    size_hint_y: None
                    height: self.texture_size[1]
                    spacing: "2dp"
                    padding: "6dp"
                MDLabel:
                    id: nav_drawer_dob
                    text: ''
                    font_style: "Subtitle1"
                    size_hint_y: None
                    height: self.texture_size[1]
                    spacing: "2dp"
                    padding: "6dp"
                MDLabel:
                    id: nav_drawer_email
                    text: ''
                    font_style: "Subtitle1"
                    size_hint_y: None
                    height: self.texture_size[1]
                    spacing: "2dp"
                    padding: "6dp"
                ScrollView:
                    MDList:
                        OneLineListItem:
                            text: 'Profile'
                        OneLineListItem:
                            text: 'Logout'
                            on_press:
                                app.root.current = 'Login Page'
                                nav_drawer.set_state('close')
                                app.logout_user()


<AddTaskScreen>:
    name: 'Add Task Page'
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '10dp'
        pos_hint: {'center_x': 0.5}

        MDLabel:
            text: 'Add Task'
            font_style: 'H4'
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]

        MDTextField:
            id: task_name
            hint_text: 'Task Name'
            helper_text: 'Enter the task name'
            helper_text_mode: 'on_focus'
            icon_left: 'account-circle'
            icon_left_color: app.theme_cls.primary_color
            pos_hint: {'center_x' : 0.5, 'center_y' : 0.8}
            size_hint_x: None
            width: 300

        MDTextField:
            id: due_date
            hint_text: 'Due Date (YYYY-MM-DD)'
            helper_text: 'Enter the due date manually or click the calendar icon'
            helper_text_mode: 'on_focus'
            icon_left: 'calendar'
            icon_left_color: app.theme_cls.primary_color
            pos_hint: {'center_x' : 0.5, 'center_y' : 0.8}
            size_hint_x: None
            width: 300
            readonly: True
            on_focus: if self.focus: root.show_date_picker()

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            padding: '50dp'
            spacing: '10dp'

            MDRectangleFlatButton:
                pos_hint: {'center_x' : 0.5, 'center_y' : 0.8}
                text: 'Add Task'
                on_press: root.add_task()

            MDRectangleFlatButton:
                pos_hint: {'center_x' : 0.5, 'center_y' : 0.8}
                text: 'Cancel'
                on_press: root.manager.current = 'Profile Page'
'''


# Establish database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="todoLogin"
)


class LoginScreen(Screen):
    def verify_login(self):
        username = self.ids.login_username.text
        password = self.ids.login_password.text
        cursor = db.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result and result[1] == password:
            self.manager.current = 'Profile Page'
            self.manager.get_screen('Profile Page').setup_profile(result[0])
            self.manager.get_screen('Add Task Page').set_user_id(result[0])
            self.clear_fields()  # Call function to clear fields after successful login
        else:
            self.show_error()

    def show_error(self):
        dialog = MDDialog(
            title="Login Failed",
            text="Invalid username or password.",
            buttons=[
                MDFlatButton(
                    text="Retry",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def clear_fields(self):
        self.ids.login_username.text = ''  # Clear username field
        self.ids.login_password.text = ''  # Clear password field


class SignupScreen(Screen):
    def verify_signup(self):
        username = self.ids.signup_username.text
        password = self.ids.signup_password.text
        fullname = self.ids.signup_fullname.text
        dob = self.ids.signup_dob.text
        email = self.ids.signup_email.text
        profile_pic_path = self.ids.signup_profile_pic.source

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if username == '' or password == '' or fullname == '' or dob == '' or email == '':
            self.show_error("Signup Failed", "All fields must be filled.")
        elif cursor.fetchone():
            self.show_error("Signup Failed", "Username already exists.")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            user_id = cursor.lastrowid

            # Read the profile picture file as binary data
            with open(profile_pic_path, 'rb') as f:
                profile_pic_data = f.read()

            cursor.execute(
                "INSERT INTO user_details (user_id, full_name, dob, email, profile_pic) VALUES (%s, %s, %s, %s, %s)",
                (user_id, fullname, dob, email, profile_pic_data))
            db.commit()
            self.manager.current = 'Login Page'

    def show_error(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="Retry",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def select_file(self):
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        if selection:
            self.ids.signup_profile_pic.source = selection[0]

    def go_to_login(self):
        self.manager.current = 'Login Page'

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_date_selected(self, instance, value, date_range):
        self.ids.signup_dob.text = value.strftime('%Y-%m-%d')

    def on_cancel(self, instance, value):
        date_dialog = MDDatePicker()
        date_dialog.dismiss()


class ProfileScreen(Screen):
    user_id = None
    current_tab = "Ongoing"  # Track the currently selected tab

    def setup_profile(self, user_id):
        self.user_id = user_id
        cursor = db.cursor()
        cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        username = cursor.fetchone()[0]
        cursor.execute("SELECT full_name, dob, email, profile_pic FROM user_details WHERE user_id = %s", (user_id,))
        details = cursor.fetchone()

        self.ids.toolbar.title = f"Hi, {username}"

        # Display user details in the navigation drawer
        if details:
            full_name, dob, email, profile_pic_data = details

            # Decode and save the profile pic temporarily
            profile_pic_path = f'profile_pic_{user_id}.png'
            with open(profile_pic_path, 'wb') as f:
                f.write(profile_pic_data)
            self.ids.nav_drawer_image.source = profile_pic_path

            # Ensure all data is converted to strings
            self.ids.nav_drawer_name.text = f"Name: {str(full_name)}" if full_name else ''
            self.ids.nav_drawer_dob.text = f"DOB: {str(dob)}" if dob else ''
            self.ids.nav_drawer_email.text = f"Email: {str(email)}" if email else ''

        # Load ongoing and completed tasks initially
        self.load_tasks()

    def load_tasks(self):
        self.clear_tasks()
        cursor = db.cursor()

        if self.current_tab == "Ongoing":
            cursor.execute("SELECT task_name, due_date FROM ongoing_tasks WHERE user_id = %s", (self.user_id,))
            tasks = cursor.fetchall()
            tasks_layout = self.ids.tasks_layout

            for task in tasks:
                task_name, due_date = task
                remaining_days = (due_date - datetime.today().date()).days
                if remaining_days <= 0:
                    cursor.execute(
                        "INSERT INTO completed_tasks (user_id, task_name, completed_date) VALUES (%s, %s, %s)",
                        (self.user_id, task_name, due_date))
                    cursor.execute("DELETE FROM ongoing_tasks WHERE user_id = %s AND task_name = %s",
                                   (self.user_id, task_name))
                else:
                    item = ThreeLineIconListItem(text=f"{task_name}",
                                                 secondary_text=f"Due: {due_date}",
                                                 tertiary_text=f"{remaining_days} days left")
                    tasks_layout.add_widget(item)

        elif self.current_tab == "Completed":
            cursor.execute("SELECT task_name, completed_date FROM completed_tasks WHERE user_id = %s", (self.user_id,))
            tasks = cursor.fetchall()
            completed_tasks_layout = self.ids.completed_tasks_layout

            for task in tasks:
                task_name, completed_date = task
                item = TwoLineIconListItem(text=f"{task_name}",
                                           secondary_text=f"Completed: {completed_date}")
                completed_tasks_layout.add_widget(item)

        db.commit()

    def clear_tasks(self):
        tasks_layout = self.ids.tasks_layout
        completed_tasks_layout = self.ids.completed_tasks_layout
        tasks_layout.clear_widgets()
        completed_tasks_layout.clear_widgets()

    def switch_tab(self, tab):
        self.current_tab = tab
        self.load_tasks()


# Custom list item classes for three-line and two-line icons
class ThreeLineIconListItem(ThreeLineListItem):
    pass


class TwoLineIconListItem(TwoLineListItem):
    pass


class AddTaskScreen(Screen):
    user_id = None

    def on_pre_enter(self, *args):
        self.ids.task_name.text = ''
        self.ids.due_date.text = ''

    def set_user_id(self, user_id):
        self.user_id = user_id

    def add_task(self):
        task_name = self.ids.task_name.text
        due_date = self.ids.due_date.text
        cursor = db.cursor()
        cursor.execute("INSERT INTO ongoing_tasks (user_id, task_name, due_date) VALUES (%s, %s, %s)",
                       (self.user_id, task_name, due_date))
        db.commit()

        # After adding the task, navigate back to the ProfileScreen's "Ongoing Tasks" tab
        profile_screen = self.manager.get_screen('Profile Page')
        profile_screen.switch_tab('Ongoing')  # Switches to Ongoing tab
        profile_screen.load_tasks()  # Reloads tasks
        self.manager.current = 'Profile Page'

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_date_selected(self, instance, value, date_range):
        self.ids.due_date.text = value.strftime('%Y-%m-%d')

    def on_cancel(self, instance, value):
        date_dialog = MDDatePicker()
        date_dialog.dismiss()


class TodoListApp(MDApp):
    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen

    def edit_profile(self):
        self.root.get_screen('Profile Page').edit_profile()

    def logout_user(self):
        self.root.get_screen('Login Page')


TodoListApp().run()



# import os
# import json
# import flet as ft

# from emaworld_api import EmaworldApiCleint
# from stox_api import StoxApiClient


# def main(page: ft.Page):
#     page.title = "User Management and Reports"
#     page.scroll = "auto"
#     page.theme_mode = "light"

#     # Callbacks
#     def add_user(e):
#         data_dir = os.path.join(os.path.dirname(__file__), "data")
#         if not os.path.exists(data_dir):
#             os.makedirs(data_dir)

#         users_file = os.path.join(data_dir, "users.json")
#         if not os.path.exists(users_file):
#             with open(users_file, "w") as f:
#                 json.dump([], f)

#         with open(users_file, "r+") as f:
#             data = json.load(f)
#             data.append({"username": username.value, "password": password.value})
#             f.seek(0)
#             json.dump(data, f, indent=4)
#             f.truncate()

#         username.value = ""
#         password.value = ""
#         page.update()

#     def select_user(e):
#         pass

#     def run_task(e, email, password):
#         progress_bar.value = None
#         page.update()

#         ema_client = EmaworldApiCleint(email=email, password=password)
#         stox_client = StoxApiClient(
#             token="32|Ef72nipQ7p1IcLk1sgwnK0J6kgIti4040BXUor9Kc4736f5e",
#             api_client=ema_client,
#         )

#         print("Success" if stox_client.send_oreders().get("success") else "Failed")

#         progress_bar.value = 0.0
#         page.update()

#     def toggle_report(e):
#         # Access the title property of the ListTile's title control
#         report_title = e.control.title.value if e.control.title else "Unknown"

#     # User Management Elements
#     username = ft.TextField(label="Username", expand=True)
#     password = ft.TextField(label="Password", password=True, expand=True)
#     add_user_btn = ft.ElevatedButton("Add User", on_click=add_user)

#     # Dropdown for users
#     users_file = os.path.join(os.path.dirname(__file__), "data", "users.json")
#     with open(users_file) as f:
#         users = json.load(f)

#     user_dropdown = ft.Dropdown(
#         label="Select User",
#         options=[ft.dropdown.Option(user["username"]) for user in users],
#         on_change=select_user,
#     )

#     # Run button and progress bar
#     run_btn = ft.ElevatedButton(
#         "Run",
#         on_click=lambda e: run_task(e, email=username.value, password=password.value),
#     )
#     progress_bar = ft.ProgressBar(width=400, value=0.0)

#     user_management = ft.Column(
#         [
#             ft.Row([username, password], spacing=10),
#             ft.Row([add_user_btn, user_dropdown], alignment="spaceBetween", spacing=10),
#             ft.Divider(),
#             ft.Row([run_btn, progress_bar], spacing=10, alignment="center"),
#         ],
#         spacing=20,
#         alignment="start",
#     )

#     # Reports Elements
#     report_list = ft.Column(
#         [
#             ft.ListTile(
#                 title=ft.Text(f"Report {i+1}"),
#                 subtitle=ft.Text("Click to view details"),
#                 leading=ft.Icon(ft.icons.REPORT),
#                 trailing=ft.Icon(ft.icons.EXPAND_MORE),
#                 on_click=toggle_report,
#             )
#             for i in range(5)  # Example: 5 reports
#         ]
#     )

#     reports = ft.Column(
#         [
#             ft.Text("Reports Section", size=20),
#             report_list,
#         ],
#         spacing=10,
#         alignment="start",
#     )

#     # Tabs
#     tabs = ft.Tabs(
#         selected_index=0,
#         tabs=[
#             ft.Tab(text="User Management", content=user_management),
#             ft.Tab(text="Reports", content=reports),
#         ],
#         expand=True,
#     )

#     # Add tabs to the page
#     page.add(tabs)


# ft.app(target=main)


import os
import json
import flet as ft

from emaworld_api import EmaworldApiCleint
from stox_api import StoxApiClient


class UserManagement:
    def __init__(self, page):
        self.page = page
        self.data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.username = ft.TextField(label="Username", expand=True)
        self.password = ft.TextField(label="Password", password=True, expand=True)
        self.progress_bar = ft.ProgressBar(width=400, value=0.0)
        self.run_btn = ft.ElevatedButton("Run", on_click=self.run_task)
        self.add_user_btn = ft.ElevatedButton("Add User", on_click=self.add_user)
        self.user_dropdown = self.create_user_dropdown()

        self.layout = self.create_layout()

    def ensure_data_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump([], f)

    def load_users(self):
        self.ensure_data_dir()
        with open(self.users_file, "r") as f:
            return json.load(f)

    def save_users(self, users):
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=4)

    def add_user(self, e):
        users = self.load_users()
        users.append({"username": self.username.value, "password": self.password.value})
        self.save_users(users)
        self.username.value = ""
        self.password.value = ""
        self.user_dropdown.options = [
            ft.dropdown.Option(user["username"]) for user in users
        ]
        self.page.update()

    def create_user_dropdown(self):
        users = self.load_users()
        return ft.Dropdown(
            label="Select User",
            options=[ft.dropdown.Option(user["username"]) for user in users],
        )

    async def run_task(self, e):
        self.progress_bar.value = None
        self.page.update()

        selected_user = self.user_dropdown.value
        for user in self.load_users():
            if user["username"] == selected_user:
                ema_client = EmaworldApiCleint(email=user["username"], password=user["password"])
                break
        else:
            raise ValueError(f"User {selected_user} not found in users.json")
        stox_client = StoxApiClient(
            token="32|Ef72nipQ7p1IcLk1sgwnK0J6kgIti4040BXUor9Kc4736f5e",
            api_client=ema_client,
        )

        print("Success" if stox_client.send_oreders().get("success") else "Failed")
        self.progress_bar.value = 0.0
        self.page.update()

    def create_layout(self):
        return ft.Column(
            [
                ft.Row([self.username, self.password], spacing=10),
                ft.Row([self.add_user_btn, self.user_dropdown], alignment="spaceBetween", spacing=10),
                ft.Divider(),
                ft.Row([self.run_btn, self.progress_bar], spacing=10, alignment="center"),
            ],
            spacing=20,
            alignment="start",
        )


class Reports:
    def __init__(self):
        self.layout = self.create_layout()

    def toggle_report(self, e):
        report_title = e.control.title.value if e.control.title else "Unknown"
        print(f"Toggled report: {report_title}")

    def create_layout(self):
        report_list = ft.Column(
            [
                ft.ListTile(
                    title=ft.Text(f"Report {i+1}"),
                    subtitle=ft.Text("Click to view details"),
                    leading=ft.Icon(ft.icons.REPORT),
                    trailing=ft.Icon(ft.icons.EXPAND_MORE),
                    on_click=self.toggle_report,
                )
                for i in range(5)  # Example: 5 reports
            ]
        )
        return ft.Column(
            [
                ft.Text("Reports Section", size=20),
                report_list,
            ],
            spacing=10,
            alignment="start",
        )


class MainApp:
    def __init__(self):
        self.page = None

    def setup_page(self, page):
        self.page = page
        page.title = "User Management and Reports"
        page.scroll = "auto"
        page.theme_mode = "light"

        user_management = UserManagement(page)
        reports = Reports()

        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="User Management", content=user_management.layout),
                ft.Tab(text="Reports", content=reports.layout),
            ],
            expand=True,
        )

        page.add(tabs)


def main(page: ft.Page):
    app = MainApp()
    app.setup_page(page)


ft.app(target=main)

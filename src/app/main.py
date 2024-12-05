import os
import json
import flet as ft

from app.emaworld_api import EmaworldApiCleint
from app.stox_api import StoxApiClient


class StatusScreen:
    def __init__(self, page):
        self.page = page
        self.status_text = ft.Text(value="")
        self.layout = self.create_layout()

    def show_status(self, status):
        self.status_text.value = status
        self.page.update()

    def create_layout(self):
        return ft.Column(
            [
                ft.Text("Status: ", size=20),
                self.status_text,
            ],
            spacing=10,
            alignment="start",
        )


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
        self.status_screen = StatusScreen(page)

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
        sent_oreders = stox_client.send_oreders()
        status = "Success" if sent_oreders.get("success") else "Failed"
        self.status_screen.show_status(f"{status}: {sent_oreders.get('count')} orders sent")
        self.progress_bar.value = 0.0
        self.page.update()

    def create_layout(self):
        return ft.Column(
            [
                ft.Row([self.username, self.password], spacing=10),
                ft.Row([self.add_user_btn, self.user_dropdown], alignment="spaceBetween", spacing=10),
                ft.Divider(),
                ft.Row([self.run_btn, self.progress_bar], spacing=10, alignment="center"),
                self.status_screen.layout,
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


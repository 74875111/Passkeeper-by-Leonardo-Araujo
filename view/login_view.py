import flet as ft
from authenticated import user_actions
from view.register_view import register_view
from view.home_view import home_view
from session_manager import verify_token
from database.models import session, User

def login_view(page: ft.Page):
    page.title = "Login"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    page.window_width = 400
    page.window_height = 400
    page.window_resizable = False
    page.window_center()
    page.window_maximizable = False  # Deshabilitar el botón de maximizar

    def on_login(e):
        email = email_input.value
        password = password_input.value
        message, user, token = user_actions.login(email, password)
        result.value = message
        if user:
            page.client_storage.set("session_token", token)
            page.clean()
            home_view(page, user, login_view)
        page.update()

    def on_register(e):
        page.clean()
        register_view(page)

    email_input = ft.TextField(label="Email", border_color=ft.colors.RED_600, width=250)
    password_input = ft.TextField(label="Password", password=True, border_color=ft.colors.RED_600, width=250)
    result = ft.Text()

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Login", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.RED_600),
                    email_input,
                    password_input,
                    ft.ElevatedButton(text="Login", on_click=on_login, bgcolor=ft.colors.RED_600, color=ft.colors.WHITE, width=150),
                    ft.ElevatedButton(text="Register", on_click=on_register, bgcolor=ft.colors.RED_600, color=ft.colors.WHITE, width=150),
                    result,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            alignment=ft.alignment.center,
        )
    )

    # Verificar si hay un token de sesión almacenado
    token = page.client_storage.get("session_token")
    if token:
        user_id = verify_token(token)
        if user_id:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                page.clean()
                home_view(page, user, login_view)

    page.update()
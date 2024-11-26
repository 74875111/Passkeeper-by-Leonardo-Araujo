import flet as ft
from authenticated import user_actions

def register_view(page: ft.Page):
    page.title = "Register"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE

    def on_register(e):
        email = email_input.value
        password = password_input.value
        message = user_actions.create_user(email, password)
        result.value = message
        if "successfully" in message:
            page.clean()
            from view.login_view import login_view  # Importar aquí para evitar la importación circular
            login_view(page)
        page.update()

    def on_back(e):
        page.clean()
        from view.login_view import login_view  # Importar aquí para evitar la importación circular
        login_view(page)

    email_input = ft.TextField(label="Email", border_color=ft.colors.RED_600, width=250)
    password_input = ft.TextField(label="Password", password=True, border_color=ft.colors.RED_600, width=250)
    result = ft.Text()

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Register", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.RED_600),
                    email_input,
                    password_input,
                    ft.ElevatedButton(text="Register", on_click=on_register, bgcolor=ft.colors.RED_600, color=ft.colors.WHITE, width=150),
                    ft.ElevatedButton(text="Back", on_click=on_back, bgcolor=ft.colors.RED_600, color=ft.colors.WHITE, width=150),
                    result,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            alignment=ft.alignment.center,
        )
    )

    page.update()
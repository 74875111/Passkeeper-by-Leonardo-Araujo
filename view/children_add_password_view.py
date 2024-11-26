import flet as ft
from authenticated import user_actions

def children_add_password_view(page: ft.Page, user):
    def on_add_password(ev):
        service_name = service_name_input.value
        user_email = user_email_input.value
        password = password_input.value

        if not service_name or not user_email or not password:
            result_text.value = "Please fill in all required fields."
            page.update()
            return

        user_actions.create_password(service_name, user_email, password, user.id)
        result_text.value = "Password added successfully!"
        form_container.visible = False
        add_another_button.visible = True
        page.update()

    def add_another(ev):
        service_name_input.value = ""
        user_email_input.value = ""
        password_input.value = ""
        result_text.value = ""
        form_container.visible = True
        add_another_button.visible = False
        page.update()

    service_name_input = ft.TextField(label="Service Name", width=250)
    user_email_input = ft.TextField(label="User/Email", width=250)
    password_input = ft.TextField(label="Password", password=True, width=250)
    result_text = ft.Text()
    add_another_button = ft.ElevatedButton(text="Add Another", on_click=add_another, visible=False)

    form_container = ft.Column(
        [
            service_name_input,
            user_email_input,
            password_input,
            ft.ElevatedButton(text="Add Password", on_click=on_add_password, bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    return ft.Column(
        [
            form_container,
            result_text,
            add_another_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )
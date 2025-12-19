import flet as ft
from database import db

def main(page: ft.Page):
    page.title = "Список покупок"
    page.theme_mode = ft.ThemeMode.LIGHT
    # page.scroll = ft.ScrollMode.AUTO
    # page.padding = 20
    # page.window_width = 500
    # page.window_height = 700
    

    current_filter = "all"
    purchase_list = ft.Column(spacing=10)
    stats_text = ft.Text("Всего: 0 Куплено: 0", size=16)
    
    def create_purchase_row(purchase_id, name, quantity, purchased):
        def delete_clicked(e):
            db.delete_purchase(purchase_id)
            load_purchases()
        
        def toggle_purchased(e):
            db.toggle_purchase(purchase_id)
            load_purchases()
        
        checkbox = ft.Checkbox(value=bool(purchased),on_change=toggle_purchased)
        

        purchase_text = ft.Text(
            f"{name} (x{quantity})",
            color=ft.Colors.GREY_600 if purchased else ft.Colors.BLACK,
            )
        
        delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_color=ft.Colors.RED_400,
            tooltip="Удалить",
            on_click=delete_clicked
        )
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    checkbox,
                    ft.Container(content=purchase_text, expand=True),
                    delete_btn,
                ],
                alignment=ft.MainAxisAlignment.START,
            )
        )
    

    def load_purchases():

        purchase_list.controls.clear()
        
        purchases = db.get_purchases_by_filter(current_filter)
        
        for purchase_id, name, quantity, purchased in purchases:
            purchase_list.controls.append(
                create_purchase_row(purchase_id, name, quantity, purchased)
            )
        
        total, purchased_count = db.get_stats()
        stats_text.value = f"Всего: {total} | Куплено: {purchased_count}"
        
        page.update()
    
    def add_purchase(e):
        name = name_input.value.strip()
        quantity_text = quantity_input.value.strip()
        
        if not name:
            name_input.error_text = "Введите название товара"
            page.update()
            return
        
        if not quantity_text or not quantity_text.isdigit():
            quantity_text = "1"
        
        quantity = int(quantity_text)
        
        db.add_purchase(name, quantity)
        
        name_input.value = ""
        quantity_input.value = ""
        name_input.error_text = None
        
        load_purchases()
    
    def change_filter(e):
        nonlocal current_filter
        current_filter = e.control.data
        load_purchases()
        
        for btn in filter_buttons.controls:
            btn.bgcolor = ft.colors.BLUE if btn.data == current_filter else None
        page.update()
    
    
    name_input = ft.TextField(
        label="Название товара",
        expand=True,
        # autofocus=True,
        on_submit=add_purchase
    )
    
    quantity_input = ft.TextField(label="Количество")
    
    add_button = ft.ElevatedButton(
        text="ДОБАВИТЬ",
        icon=ft.Icons.ADD,
        on_click=add_purchase
        )
    
    input_row = ft.Container(
        content=ft.Row(
            controls=[
                name_input,
                quantity_input,
                add_button,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.only(bottom=20)
    )
    
    filter_buttons = ft.Row(
        controls=[
            ft.ElevatedButton(
                text="Все товары",
                data="all",
                on_click=change_filter,
            ),
            ft.ElevatedButton(
                text="Не купленные",
                data="not_purchased",
                on_click=change_filter
            ),
            ft.ElevatedButton(
                text="Купленные",
                data="purchased",
                on_click=change_filter
            ),
        ],
        spacing=10
    )
    
    list_title = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Список покупок:", size=20, weight=ft.FontWeight.BOLD),
                stats_text,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.only(bottom=10)
    )
    
    list_container = ft.Container(
        content=purchase_list,
        border=ft.border.all(1, ft.Colors.GREY_300),
        bgcolor=ft.Colors.WHITE,
    )
    
    page.add(
        ft.Text("Список покупок", weight=ft.FontWeight.BOLD),
        input_row,
        ft.Text("Фильтры:", weight=ft.FontWeight.BOLD),
        filter_buttons,
        list_title,
        list_container,
        
        )
    
    load_purchases()

if __name__ == "__main__":
    ft.app(target=main)
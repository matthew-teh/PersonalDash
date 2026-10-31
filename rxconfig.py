import reflex as rx
from PersonalDashboard.components.state import DashboardState
config = rx.Config(
    app_name="PersonalDashboard",
    plugins=[
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                accent_color="pink", 
                grayColor="olive",
                panelBackground="solid",
                radius="none",
            )
        ),
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),  
    ],
)



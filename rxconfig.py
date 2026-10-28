import reflex as rx

config = rx.Config(
    app_name="PersonalDashboard",
    plugins=[
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="dark",    
                accent_color="violet",
                radius="full",       
            )
        ),
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ],
)



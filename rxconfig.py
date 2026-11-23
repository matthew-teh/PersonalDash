import reflex as rx
from FlexDashV6.FDstates import Dashboard

config = rx.Config(
    app_name="FlexDashV6",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                scaling="100%",
                appearance=Dashboard.appearance,
                accent_color=Dashboard.colors["name"], # type: ignore
            )
        ),
    ]
)
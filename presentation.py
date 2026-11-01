import config
from views._embed import show


def render():
    show(
        eyebrow="Presentation",
        title="The final presentation.",
        subtitle="The slide deck for the project viva, embedded so you can present straight from the app.",
        file_id=config.PRESENTATION_ID,
        source_url=config.PRESENTATION_URL,
        kind="slides",
        height=720,
    )

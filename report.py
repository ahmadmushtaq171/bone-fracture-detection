import config
from views._embed import show


def render():
    show(
        eyebrow="Project report",
        title="The full written report.",
        subtitle="Introduction, dataset, methodology, results and conclusion, exactly as submitted.",
        file_id=config.REPORT_ID,
        source_url=config.REPORT_URL,
        kind="doc",
        height=880,
    )

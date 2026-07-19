from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from api.home_page import load_home_page_html


def register_home_routes(app: FastAPI) -> None:
    @app.get("/", response_class=HTMLResponse)
    def root():
        return HTMLResponse(
            load_home_page_html(),
            headers={"Cache-Control": "no-store"},
        )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轻量级静态文件服务
用于替代容器内 Nginx，处理静态文件分发和 SPA fallback
"""

import os
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse, RedirectResponse

HTML_DIR = "/app/html"


async def homepage(request):
    """首页：返回 home.html"""
    return FileResponse(os.path.join(HTML_DIR, "home.html"))


async def not_found(request, exc):
    """404 fallback：blog/project 单页路由回退到对应列表页"""
    path = request.url.path

    if path.startswith("/blog/"):
        return FileResponse(os.path.join(HTML_DIR, "blog", "index.html"))

    if path.startswith("/project/"):
        return FileResponse(os.path.join(HTML_DIR, "project", "index.html"))

    if path == "/":
        return RedirectResponse(url="/home.html")

    return FileResponse(os.path.join(HTML_DIR, "404.html"), status_code=404)


routes = [
    Route("/", homepage),
    Mount("/", app=StaticFiles(directory=HTML_DIR, html=True), name="static"),
]

exception_handlers = {
    404: not_found
}

app = Starlette(routes=routes, exception_handlers=exception_handlers)
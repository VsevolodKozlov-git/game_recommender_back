from app.api import service_call
from fastapi import FastAPI


application = FastAPI()

def include_routers(routers: list, prefix: str) -> None:
    for router in routers:
        application.router.include_router(router, prefix=prefix)

root_routers = [service_call.router]
include_routers(root_routers, "")

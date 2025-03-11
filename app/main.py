from app.api import service_call, users, games, questions, surveys
from fastapi import FastAPI


application = FastAPI()

def include_routers(routers: list, prefix: str) -> None:
    for router_info in routers:
        router, tags = router_info
        application.include_router(router, prefix=prefix, tags=tags)

root_routers = [
    (service_call.router, ["Service Calls"]),
    (users.router, ["User Management"]),
    (games.router, ["Game Management"]),
    (surveys.router, ["Survey Management"]),
    (questions.router, ["Question Management"])
]

include_routers(root_routers, "")

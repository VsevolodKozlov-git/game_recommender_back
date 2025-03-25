from app.api import service_call, users, games, questions, surveys, recommender, reactions
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

application = FastAPI()


origins = [
    "*"
]

application.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def include_routers(routers: list, prefix: str) -> None:
    for router_info in routers:
        router, tags = router_info
        application.include_router(router, prefix=prefix, tags=tags)

root_routers = [
    (service_call.router, ["Service Calls"]),
    (users.router, ["User Management"]),
    (games.router, ["Game Management"]),
    (surveys.router, ["Survey Management"]),
    (questions.router, ["Question Management"]),
    (recommender.router, ['Рекомендательная система']),
    (reactions.router, ['Реакции'])
]

include_routers(root_routers, "")

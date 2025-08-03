from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter

from .auth import verify_token
from .schema import schema

app = FastAPI(title="Gateway Service")

# Protect GraphQL endpoint with Keycloak token verification
graphql_app = GraphQLRouter(schema, path="/graphql", dependencies=[Depends(verify_token)])
app.include_router(graphql_app)


@app.get("/health")
async def health():
    return {"status": "ok"}

from fastapi import FastAPI
from database.connection import connect_database
from routes.auth import router as auth_router
from routes.get_users import router as get_user
connect_database()

app=FastAPI(
    title="Tour & Travel Services API",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(get_user)

@app.get("/health")
async def health_check():
    return {"status":"ok" , "mongodb":"Connected ✅"}
    
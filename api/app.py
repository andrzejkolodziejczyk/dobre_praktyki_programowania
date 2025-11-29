from fastapi import FastAPI
import uvicorn
from endpoints import router

app = FastAPI()

# Include the router from endpoints
app.include_router(router)


@app.get('/hello')
def hello():
    return {'hello': 'world'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)

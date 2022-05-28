import uvicorn
from fastapi import FastAPI


app = FastAPI()

from api import *

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

# TODO: add get/post wrappers to the api functions.

import os
from fastapi import FastAPI


app = FastAPI(docs_url=None, redoc_url=None)

FASTAPI_ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

conf = {
    'DefaultReturn': {'code': 200, 'message': 'OK!'}
}
from fastapi import FastAPI


app = FastAPI(docs_url=None, redoc_url=None)

conf = {
    'DefaultReturn': {'code': 200, 'message': 'OK!'}
}
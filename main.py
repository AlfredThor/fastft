from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from app import file
from config.config import app

# 放弃所有表
# Base.metadata.drop_all(engine)
# 创建所有数据模型
# model.Base.metadata.create_all(bind=engine)
# Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)


app.mount("/static", StaticFiles(directory="static"), name="static")    # 加载静态资源位文件
app.include_router(file.router, tags=['file'])     # 文件上传

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8003, reload=True)
import os
from app.file import router
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from config.config import conf, FASTAPI_ROOT_PATH
from fastapi import UploadFile, Form, File, Request, Response
from tool.setting import file_iterator, parse_range_header, encode_filename


templates = Jinja2Templates(directory="templates")
DefaultReturn = conf['DefaultReturn']


@router.get('/', summary='文件列表')
async def file_list(request: Request, page: int = 1, PER_PAGE: int = 10):
    # 检查文件夹是否存在,不存在就创建
    files_path = f'{FASTAPI_ROOT_PATH}/upload/'
    if not os.path.exists(files_path):
        os.makedirs(files_path)

    file_list = os.listdir(files_path)

    result = {'request': request}

    # 如果目录为空，返回一个空页面
    if not file_list:
        result['files'] = []
        result['current_page'] = page
        result['total_pages'] = 0
    else:
        total_files = len(file_list)  # 总文件数
        files = file_list[(page - 1) * PER_PAGE: page * PER_PAGE]  # 根据页码获取文件列表
        total_pages = (total_files + PER_PAGE - 1) // PER_PAGE  # 计算总页数
        result['files'] = files
        result['current_page'] = page
        result['total_pages'] = total_pages

    return templates.TemplateResponse('list.html', result)


@router.post('/upload', summary='接收前端上传的一个分片-通用')
async def upload_part(file: UploadFile = File(...), chunk: str = Form(None), task_id: str = Form(...), chunked: str = Form(...)):  # 接收前端上传的一个分片
    if chunked == 'false':
        contents = await file.read()
        with open(f'{FASTAPI_ROOT_PATH}/upload/{file.filename}', 'wb') as f:
            f.write(contents)

    if chunked == 'true':
        filename = '%s%s' % (task_id, chunk)  # 构造该分片的唯一标识符
        contents = await file.read()  # 异步读取文件
        with open(os.path.join(f'{FASTAPI_ROOT_PATH}/upload/', filename), "wb") as f:
            f.write(contents)


# 三种压缩格式：ZIP、7Z、RAR
@router.get('/success', summary='按序读出分片内容，并写入新文件')
async def upload_success(task_id: str, filename: str):
    chunk = 0
    with open(f'{FASTAPI_ROOT_PATH}/upload/{filename}', 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = f'{FASTAPI_ROOT_PATH}/upload/%s%d' % (task_id, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError as msg:
                break

            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间


@router.get('/download', summary='下载文件-通用')
async def file_download(request: Request, filename: str):
    file_path = os.path.join(f'{FASTAPI_ROOT_PATH}/upload/', filename)

    # 检查文件是否存在
    if not os.path.exists(file_path):
        return Response(status_code=404, content="File not found")

    # 获取文件信息
    file_size = os.path.getsize(file_path)
    file_stat = os.stat(file_path)
    etag = f'"{hex(int(file_stat.st_mtime))}"'
    last_modified = datetime.utcfromtimestamp(file_stat.st_mtime).strftime('%a, %d %b %Y %H:%M:%S GMT')

    # 处理条件请求
    if_none_match = request.headers.get('if-none-match')
    if_modified_since = request.headers.get('if-modified-since')

    if if_none_match and if_none_match == etag:
        return Response(status_code=304)
    if if_modified_since and if_modified_since == last_modified:
        return Response(status_code=304)

    # 处理Range请求
    range_header = request.headers.get('range')
    start = 0
    end = file_size - 1
    status_code = 200

    if range_header:
        start, end = parse_range_header(range_header, file_size)
        status_code = 206  # Partial Content

    # 计算内容长度
    content_length = end - start + 1

    # 创建响应头
    headers = {
        'content-length': str(content_length),
        'accept-ranges': 'bytes',
        'content-type': 'application/octet-stream',
        'etag': etag,
        'last-modified': last_modified,
        'content-disposition': f'attachment; {encode_filename(filename)}'
    }

    if status_code == 206:
        headers['content-range'] = f'bytes {start}-{end}/{file_size}'

    # 返回流式响应
    return StreamingResponse(
        file_iterator(file_path, start, end),
        status_code=status_code,
        headers=headers
    )


@router.delete('/delete/file', summary='刪除文件')
async def delete_file(filename: str):
    file_path = os.path.join(f'{FASTAPI_ROOT_PATH}/upload/', filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {'code': 200, 'message': f'{filename}文件删除成功!'}
    return {'code': 400, 'message': '文件不存在!'}
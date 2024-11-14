import urllib.parse
from typing import BinaryIO, Generator


def parse_range_header(range_header: str, file_size: int) -> tuple[int, int]:
    """解析Range请求头"""
    try:
        range_type, range_values = range_header.split('=')
        if range_type != 'bytes':
            raise ValueError("Only bytes range type is supported")

        start_str, end_str = range_values.split('-')
        start = int(start_str) if start_str else 0
        end = int(end_str) if end_str else file_size - 1

        if start >= file_size or end >= file_size or start > end:
            raise ValueError("Invalid range values")

        return start, end
    except Exception:
        return 0, file_size - 1


async def file_iterator(file_path: str, start: int, end: int, chunk_size: int = 8192) -> Generator[bytes, None, None]:
    """文件流式读取生成器"""
    with open(file_path, 'rb') as file:
        file.seek(start)
        remaining = end - start + 1

        while remaining > 0:
            chunk_size = min(chunk_size, remaining)
            data = file.read(chunk_size)
            if not data:
                break
            remaining -= len(data)
            yield data


def encode_filename(filename: str) -> str:
    """对文件名进行编码，支持中文等非ASCII字符"""
    # 使用RFC 5987编码
    encoded_filename = urllib.parse.quote(filename)
    return f"filename*=UTF-8''{encoded_filename}"
from fastapi import APIRouter, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
import aiofiles
from utils.hash_gen import generate_hash
from subtitle.enums.file_category import FileCategory
from subtitle.services import convert_to_wav
from services.stt import stt
from config import UPLOAD_DIR, SRT_DIR
from services.translation import translation
import os
from .services import generate_srt


router = APIRouter(prefix='/subtitle')

@router.post('/generate/')
async def generate_subtitle(file: UploadFile):
    cat, extension = file.content_type.split('/')
    original_filename = '.'.join(file.filename.split('.')[:-1])
    if cat != FileCategory['Audio'] and cat != FileCategory['Video']:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='file is not video nor audio')

    filename = generate_hash()
    filename_with_ex = f'{filename}.{extension}'
    file_path = os.path.join(UPLOAD_DIR, filename_with_ex)

    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)

    if extension != 'wav':
        filename_with_ex = convert_to_wav(file_path, filename)
    segments = stt.transcribe(os.path.join(UPLOAD_DIR, filename_with_ex))
    srt_path = os.path.join(SRT_DIR, f'{filename}.srt')
    generate_srt(segments, srt_path)
    return FileResponse(
        path=srt_path,
        filename=f'{original_filename}.srt',
        media_type='application/octet-stream'
    )
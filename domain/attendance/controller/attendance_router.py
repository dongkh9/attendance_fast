import asyncio

from fastapi import APIRouter, Request
from starlette.responses import PlainTextResponse

from domain.attendance.dto import attendance_schema
from domain.attendance.service import attendance_service
from database import get_db
from fastapi import Depends
from fastapi.responses import StreamingResponse
from asyncio import Queue, create_task
from typing import List
import time

router = APIRouter(
    prefix="/api/attendance"
)

MAX_CONNECTIONS = 100
event_queue: List[Queue] = []

@router.get("/list/today", response_model=list[attendance_schema.AttendancePlus])
async def today_attendance_list(db  = Depends(get_db)):
    _today_attendance_list = await attendance_service.get_today_attendance_list(db)
    return _today_attendance_list

@router.get("/list/{date_string}")
async def thatday_attendance_list(date_string: str, db  = Depends(get_db)):
    _thatday_attendance_list = await attendance_service.get_thatday_attendance_list(date_string, db)
    return _thatday_attendance_list

@router.post("/")
async def regist_attendance(_attendance_regist: attendance_schema.AttendanceContents,
                         db  = Depends(get_db)):
    new_attendance = await attendance_service.regist_attendance(_attendance_regist,db)
    broadcast_onAddAttendance()
    return new_attendance

@router.post("/nfc")
async def nfc_attendance(taged_info: attendance_schema.TagInfo,
                   db  = Depends(get_db)):
    new_attendacne = await attendance_service.nfc_attendance(taged_info,db)
    broadcast_onAddAttendance()
    return new_attendacne


@router.put("/{id}")
async def attendance_update(id: int,
                      _attendance_update: attendance_schema.AttendanceContents,
                  db  = Depends(get_db)):
    update_attendance = await attendance_service.update_attendance(_attendance_update, id, db)
    return update_attendance

@router.delete("/{id}")
async def attendance_delete(id: int,
                      db  = Depends(get_db)):
    await attendance_service.delete_attendance(id,db)

@router.get("/sse")
async def sse():
    if len(event_queue) >= MAX_CONNECTIONS:
        return PlainTextResponse("Too many clients", status_code=503)
    queue = Queue()
    event_queue.append(queue)

    async def event_generator():
        ping_interval = 30
        last_ping = time.time()

        try:
            while True:
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=1)
                    yield f"data: {data}\n\n"
                except asyncio.TimeoutError:
                    # 매 30초마다 ping
                    if time.time() - last_ping > ping_interval:
                        yield "data: ping\n\n"
                        last_ping = time.time()
        except asyncio.CancelledError:
            pass
        finally:
            event_queue.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

def broadcast_onAddAttendance():
    for queue in event_queue:
        queue.put_nowait("AddAttendance")
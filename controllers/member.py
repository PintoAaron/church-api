import os
from datetime import date
from typing import List

import pandas as pd
from fastapi import (APIRouter, Depends, Form, HTTPException, Security,
                     UploadFile, status)
from fastapi.responses import FileResponse
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core import NotFound, get_db_session
from models import MemberMapper
from schemas import MemberSchemaIn, MemberSchemaOut, MemberSchemaUpdate
from services import IsAuthenticated
from utils import save_file, validate_excel_file

member_router = APIRouter(
    prefix="/api/members",
    tags=["Member"],
)


@member_router.get("", response_model=List[MemberSchemaOut], dependencies=[Security(IsAuthenticated())])
async def get_all(session: Session = Depends(get_db_session)):
    return MemberMapper.get_all(session)


@member_router.get("/{id}", response_model=MemberSchemaOut, dependencies=[Security(IsAuthenticated())])
async def get(id: int, session: Session = Depends(get_db_session)):
    NotFound(session, {MemberMapper: [id]}).__call__()
    return MemberMapper.get_by_id(session, id)


@member_router.post("", response_model=MemberSchemaOut, dependencies=[Security(IsAuthenticated())])
async def post(
        picture: UploadFile | None = None,
        fullname: str = Form(None),
        phone: str = Form(None),
        email: EmailStr = Form(None),
        dob: date = Form(None),
        occupation: str = Form(None),
        emergency_contact_name: str = Form(None),
        emergency_contact_phone: str = Form(None),
        marital_status: str = Form(None),
        address: str = Form(None),
        number_of_children: int = Form(None),
        department_id: int = Form(None),
        session: Session = Depends(get_db_session)
):
    filename = save_file(picture)
    member_data = MemberSchemaIn(
        picture=filename,
        fullname=fullname,
        phone=phone,
        email=email,
        dob=dob,
        occupation=occupation,
        emergency_contact_name=emergency_contact_name,
        emergency_contact_phone=emergency_contact_phone,
        marital_status=marital_status,
        address=address,
        number_of_children=number_of_children,
        department_id=department_id,
    )
    return MemberMapper.create(session=session, data=member_data.model_dump())


@member_router.put("/{id}", response_model=MemberSchemaOut, dependencies=[Security(IsAuthenticated())])
async def update(
        id: int,
        picture: UploadFile | None = None,
        fullname: str = Form(None),
        phone: str = Form(None),
        email: EmailStr = Form(None),
        dob: date = Form(None),
        occupation: str = Form(None),
        emergency_contact_name: str = Form(None),
        emergency_contact_phone: str = Form(None),
        marital_status: str = Form(None),
        address: str = Form(None),
        number_of_children: int = Form(None),
        department_id: int = Form(None),
        session: Session = Depends(get_db_session)
):
    NotFound(session, {MemberMapper: [id]}).__call__()
    filename = save_file(picture)
    member_data = MemberSchemaUpdate(
        id=id,
        picture=filename,
        fullname=fullname,
        phone=phone,
        email=email,
        dob=dob,
        occupation=occupation,
        emergency_contact_name=emergency_contact_name,
        emergency_contact_phone=emergency_contact_phone,
        marital_status=marital_status,
        address=address,
        number_of_children=number_of_children,
        department_id=department_id,
    )
    return MemberMapper.update(session=session, data=member_data.model_dump())


@member_router.get("/image/{filename}")
async def read_image(filename: str):
    file_path = f"assets/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
    return FileResponse(file_path)


@member_router.delete("/{id}", dependencies=[Security(IsAuthenticated())])
async def delete(id: int, session: Session = Depends(get_db_session)):
    NotFound(session, {MemberMapper: [id]}).__call__()
    return MemberMapper.delete(session, id)


@member_router.post("/file/upload", dependencies=[Security(IsAuthenticated())])
async def upload_file(file: UploadFile, department_id: int, session: Session = Depends(get_db_session)):
    val_file = validate_excel_file(file.filename)
    if val_file is False:
        raise HTTPException(status_code=404, detail="Only excel files are allowed")
    df = pd.read_excel(file.file)
    data = df.to_dict(orient='records')
    for member in data:
        member.update({"department_id": department_id})
    return MemberMapper.create_from_file(session=session, data=data)

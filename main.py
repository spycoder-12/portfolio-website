# from fastapi import FastAPI, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from sqlalchemy.orm import Session

# import Models
# import Schemas
# from Database import Base, engine, get_db
# from Emailer import send_contact_notification
# from config import CORS_ORIGINS, UPLOAD_DIR

# # Create database tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title="Photography Portfolio API",
#     version="1.0.0"
# )

# # -----------------------------
# # CORS
# # -----------------------------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=CORS_ORIGINS if CORS_ORIGINS else ["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -----------------------------
# # Static Images
# # -----------------------------
# app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# # -----------------------------
# # Home
# # -----------------------------
# @app.get("/")
# def home():
#     return {
#         "status": "Running",
#         "message": "Photography Portfolio API"
#     }


# # -----------------------------
# # Get Photos
# # -----------------------------
# @app.get("/photos", response_model=list[Schemas.PhotoOut])
# @app.post("/photos/upload")
# def get_photos(db: Session = Depends(get_db)):
#     return (
#         db.query(Models.Photo)
#         .order_by(Models.Photo.sort_order)
#         .all()
#     )


# # -----------------------------
# # Contact Form
# # -----------------------------
# @app.post("/contact")
# def contact(
#     contact: Schemas.ContactCreate,
#     db: Session = Depends(get_db),
# ):

#     # Honeypot check
#     if contact.website:
#         return {"message": "Success"}

#     new_message = Models.ContactMessage(
#         name=contact.name,
#         email=contact.email,
#         message=contact.message,
#         event_date=contact.event_date,
#     )

#     db.add(new_message)
#     db.commit()
#     db.refresh(new_message)

#     try:
#         send_contact_notification(
#             contact.name,
#             contact.email,
#             contact.message,
#             contact.event_date,
#         )
#     except Exception:
#         pass

#     return {
#         "success": True,
#         "message": "Thank you for contacting us!"
#     }


# # -----------------------------
# # Get Messages
# # -----------------------------
# @app.get("/messages", response_model=list[Schemas.ContactOut])
# def get_messages(db: Session =Depends(get_db)):
#     return (
#         db.query(Models.ContactMessage)
#         .order_by(Models.ContactMessage.created_at.desc())
#         .all()
#     )

from fastapi import (
    FastAPI,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

import os
import shutil
import uuid

import Models
import Schemas

from Database import Base, engine, get_db
from Emailer import send_contact_notification
from config import CORS_ORIGINS, UPLOAD_DIR
from Auth import require_admin


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Photography Portfolio API",
    version="1.0.0"
)


# -------------------------
# CORS
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Static uploads folder
# -------------------------

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads"
)



# =========================
# PHOTO APIs
# =========================


# GET ALL PHOTOS
@app.get("/photos", response_model=list[Schemas.PhotoOut])
def get_photos(
    db: Session = Depends(get_db)
):

    return (
        db.query(Models.Photo)
        .order_by(Models.Photo.sort_order)
        .all()
    )



# UPLOAD PHOTO
@app.post("/photos/upload")
def upload_photo(
    category: str = Form(...),
    caption: str = Form(""),
    frame_no: str = Form(""),
    exposure: str = Form(""),
    sort_order: int = Form(0),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed"
        )


    extension = os.path.splitext(image.filename)[1]

    filename = f"{uuid.uuid4().hex}{extension}"


    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )


    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            image.file,
            buffer
        )


    new_photo = Models.Photo(
        category=category,
        caption=caption,
        frame_no=frame_no,
        exposure=exposure,
        image_path=filename,
        sort_order=sort_order
    )


    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)


    return {
        "success": True,
        "message": "Photo uploaded successfully",
        "photo": new_photo
    }



# UPDATE PHOTO
@app.put("/photos/{photo_id}")
def update_photo(
    photo_id: int,
    category: str = Form(None),
    caption: str = Form(None),
    frame_no: str = Form(None),
    exposure: str = Form(None),
    sort_order: int = Form(None),
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):

    photo = (
        db.query(Models.Photo)
        .filter(
            Models.Photo.id == photo_id
        )
        .first()
    )


    if photo is None:
        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )


    if category:
        photo.category = category

    if caption:
        photo.caption = caption

    if frame_no:
        photo.frame_no = frame_no

    if exposure:
        photo.exposure = exposure

    if sort_order is not None:
        photo.sort_order = sort_order


    db.commit()
    db.refresh(photo)


    return {
        "success": True,
        "message": "Photo updated successfully",
        "photo": photo
    }



# DELETE PHOTO
@app.delete("/photos/{photo_id}")
def delete_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):

    photo = (
        db.query(Models.Photo)
        .filter(
            Models.Photo.id == photo_id
        )
        .first()
    )


    if photo is None:
        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )


    file_path = os.path.join(
        UPLOAD_DIR,
        photo.image_path
    )


    if os.path.exists(file_path):
        os.remove(file_path)


    db.delete(photo)
    db.commit()


    return {
        "success": True,
        "message": "Photo deleted successfully"
    }





# =========================
# CONTACT APIs
# =========================


# CREATE CONTACT MESSAGE
@app.post("/contact")
def contact(
    contact: Schemas.ContactCreate,
    db: Session = Depends(get_db)
):

    # Honeypot spam protection
    if contact.website:
        return {
            "message": "Success"
        }


    new_message = Models.ContactMessage(
        name=contact.name,
        email=contact.email,
        message=contact.message,
        event_date=contact.event_date
    )


    db.add(new_message)
    db.commit()
    db.refresh(new_message)


    try:

        send_contact_notification(
            contact.name,
            contact.email,
            contact.message,
            contact.event_date
        )


    except Exception as e:

        print(
            "EMAIL ERROR:",
            e
        )


    return {
        "success": True,
        "message": "Thank you for contacting us!"
    }




# GET ALL CONTACT MESSAGES
@app.get("/contacts")
def get_contacts(
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):

    return (
        db.query(Models.ContactMessage)
        .order_by(
            Models.ContactMessage.id.desc()
        )
        .all()
    )




# DELETE CONTACT MESSAGE
@app.delete("/contact/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    admin: bool = Depends(require_admin)
):

    contact = (
        db.query(Models.ContactMessage)
        .filter(
            Models.ContactMessage.id == contact_id
        )
        .first()
    )


    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact message not found"
        )


    db.delete(contact)
    db.commit()


    return {
        "success": True,
        "message": "Contact deleted successfully"
    }
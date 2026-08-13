from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def documents():

    """Return document API information."""
    return {
        "message": "Documents API"
    }
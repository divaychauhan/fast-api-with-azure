from fastapi import APIRouter,Depends
from models.user import User
from dependencies.auth import get_current_user

router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
async def get_user(current_user: User=Depends(get_current_user)):
    users=User.objects.all()
    return [{
        "id": str(user.id),
        "full_name":user.full_name,
        "email":user.email,
        "phone":user.phone
    }
     for user in users       
    ]
    
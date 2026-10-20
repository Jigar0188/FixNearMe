from fastapi import Depends, FastAPI, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.models import User, ProfessionalProfile, Service
from backend.schema import RegisterRequest, RegisterResponse,LoginRequest, LoginResponse
from backend.auth_utils import hash_password, verify_password
from backend.auth_utils import create_access_token, verify_access_token
from backend.schema import CurrentUserResponse


app = FastAPI()



security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        user_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


@app.get("/")
def home():
    return {"message": "Welcome to the Fixnear application!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}



@app.get("/api/test/users")
def test_read_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id).all()

    return {
        "count": len(users),
        "users": [
            {
                "id": user.id,
                "name": user.name,
                "role": user.role,
            }
            for user in users
        ],
    }

@app.post(
    "/api/auth/register",
    response_model=RegisterResponse,    
    status_code=status.HTTP_201_CREATED,
)
def register(payload: RegisterRequest,db: Session = Depends(get_db)):   #yahaa pe RegisterResponse as an datatype use hai bol skte hain
    email = str(payload.email).strip().lower()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    user = User(
        name=payload.name.strip(),
        email=email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        phone=payload.phone,
    )

    try:
        db.add(user)
        db.flush()

        if payload.role == "professional":
            profile = ProfessionalProfile(user_id=user.id)
            db.add(profile)

        db.commit()
        db.refresh(user)

        return user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The account could not be created because of a data conflict.",
        )
    except Exception:
        db.rollback()
        raise

@app.post("/api/auth/login", response_model=LoginResponse)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):
    email = str(payload.email).strip().lower()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user or not verify_password(
        payload.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )
    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }


@app.get("/api/auth/me", response_model=CurrentUserResponse)
def read_current_user(current_user: User = Depends(get_current_user) ):
    return current_user


@app.get("/api/customer/dashboard")
def customer_dashboard(current_user: User = Depends(read_current_user)):
    
    if current_user.role != "customer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Customers only.")
        
    return {"messege": "Welcome to the customer Dashboard!",
            "user_id": current_user.id,
            "role": current_user.role}


@app.get("/api/services")
def get_services(db: Session = Depends(get_db)):
    services = db.query(Service).order_by(Service.id).all()

    return {
        "count": len(services),
        "services": [
            {
                "id": service.id,
                "name": service.name,
                "description": service.description
            }
            for service in services
        ]
    }




@app.get("/api/professionals")
def get_professionals(
    service_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db)
):
    query = (
        db.query(ProfessionalProfile)
        .join(User, User.id == ProfessionalProfile.user_id)
    )

    if service_id is not None:
        service = db.query(Service).filter(
        Service.id == service_id).first()

    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service with ID {service_id} does not exist."
        )


    professionals = query.order_by(ProfessionalProfile.id).all()

    result = []

    for professional in professionals:
        result.append({
            "professional_id": professional.id,
            "name": professional.user.name,
            "experience_years": professional.experience_years,
            "description": professional.description,
            "service_area": professional.service_area,
            "hourly_rate": professional.hourly_rate,
            "is_available": professional.is_available,
            "services": [
                {
                    "id": service.id,
                    "name": service.name
                }
                for service in professional.services
            ]
        })

    return {
        "count": len(result),
        "professionals": result
    }


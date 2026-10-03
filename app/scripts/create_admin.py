from getpass import getpass

from sqlalchemy import select
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.features.users.models import User
from app.features.roles.models import Role
from app.features.user_roles.models import UserRole
from app.features.users.schemas import UserCreate

def create_admin():
    print("=== Initial Admin Setup ===")

    name = input("Name:").strip()
    email = input("Email: ").strip()

    password = getpass("Password (Hidden): ")
    confirm_password = getpass("Confirm password (Hidden): ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    #Pydantic validation
    user_data = UserCreate(
        name = name,
        email = email,
        password= password,
        role = "ADMIN"
    )

    with SessionLocal() as db:
        try :
            with db.begin():

                #1. Check whether an Admin already exists
                existing_admin = db.execute(
                    select(User)
                    .join(UserRole)
                    .join(Role)
                    .where(
                        Role.name == "ADMIN",
                        User.deleted_at.is_(None)
                    )
                ).scalars().first()
                if existing_admin:
                    raise ValueError(
                        "An active Admin already exists."
                    )

                #2 Check email
                existing_user = db.execute(
                    select(User)
                    .where(User.email== user_data.email)
                ).scalars().first()

                if existing_user:
                    raise ValueError(
                        "A user with this email already exists."
                    )

                #3. Create user
                user = User(
                    name = user_data.name,
                    email= user_data.email,
                    password_hash = hash_password(user_data.password)
                )

                db.add(user)

                #Generate user.id before creating UserRole
                db.flush()

                # 4. Find ADMIN role
                admin_role = db.execute(
                    select(Role)
                    .where(Role.name == "ADMIN")
                ).scalars().one_or_none()

                if admin_role is None:
                    raise ValueError(
                        "ADMIN role does not exist."
                        "Run migrations first."
                    )

                # 5. Assign ADMIN role
                user_role = UserRole(
                    user_id = user.id,
                    role_id = admin_role.id
                )

                db.add(user_role)

            print()
            print("Initial Admin created successfully.")
            print(f"Name : {user.name}")
            print(f"Email : {user.email}")
            print(f"Role : ADMIN")

        except Exception as e:
            print()
            print(f"Failed to create Admin: {e}")

if __name__ == "__main__":
    from app.core import models
    create_admin()
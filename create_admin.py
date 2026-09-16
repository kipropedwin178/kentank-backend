from getpass import getpass

from app.database.session import SessionLocal
from app.services.admin_service import create_admin


def main():
    print("=== Kentank Deliveries - Create Admin ===")

    phone_number = input("Phone number: ").strip()
    email = input("Email address: ").strip()
    password = getpass("Password: ")
    confirm_password = getpass("Confirm password: ")

    if password != confirm_password:
        print("Error: Passwords do not match.")
        return

    if not phone_number:
        print("Error: Phone number is required.")
        return

    if not email:
        print("Error: Email address is required.")
        return

    if not password:
        print("Error: Password is required.")
        return

    db = SessionLocal()

    try:
        admin = create_admin(
            db=db,
            phone_number=phone_number,
            email=email,
            password=password,
        )

        print("\nAdmin created successfully.")
        print(f"Admin ID: {admin.id}")
        print(f"Phone: {admin.phone_number}")
        print(f"Email: {admin.email}")

    except Exception as error:
        db.rollback()
        print(f"\nError creating admin: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
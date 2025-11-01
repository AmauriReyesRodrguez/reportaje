from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import Base


class User(Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(67), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)


    def __init__(self, nombre: str, email: str, password: str):
        self.nombre = nombre

        self.email = email
        self.set_password(password)


    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def name(self) -> str:
        return f"{self.nombre}"

    def update_profile(self, nombre: str, apellido: str, foto_perfil: str = None) -> None:
        self.nombre = nombre
        self.apellido = apellido
        if foto_perfil is not None:
            self.foto_perfil = foto_perfil

    def __repr__(self) -> str:
        return f"<User {self.email} - {self.full_name()}>"

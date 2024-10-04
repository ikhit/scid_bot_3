from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
import sqlalchemy.dialects.postgresql as pgsql_types

from enum import Enum

from core.db import Base


class RoleEnum(str, Enum):
    USER = 'U'
    ADMIN = 'A'
    MANAGER = 'M'


class QuestionEnum(str, Enum):
    GENERAL_QUESTIONS = 'Общие вопросы'
    PROBLEMS_WITH_PRODUCTS = 'Проблемы с продуктами'


class User(Base):
    """БД модель пользователя."""

    tg_id: Mapped[int] = mapped_column(
        pgsql_types.BIGINT,
        nullable=False,
        unique=True
    )

    role: Mapped[RoleEnum] = mapped_column(
        pgsql_types.ENUM(
            RoleEnum,
            name="role_enum",
            create_type=False
        ),
        default=RoleEnum.USER,
    )

    join_date: Mapped[datetime] = mapped_column(
        pgsql_types.TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class ProductCategory(Base):
    """БД модель продуктов и услуг."""

    title: Mapped[str] = mapped_column(
        pgsql_types.VARCHAR(150)
    )

    response: Mapped[str] = mapped_column(
        pgsql_types.TEXT
    )


class CategoryType(Base):
    """БД модель типов категорий."""

    name: Mapped[str] = mapped_column(
        pgsql_types.VARCHAR(150),
        nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey('productcategory.id'),
        index=True
    )

    url: Mapped[str] = mapped_column(
        pgsql_types.VARCHAR(128)
    )

    media: Mapped[str] = mapped_column(
        pgsql_types.VARCHAR(128),
        nullable=True
    )


class InformationAboutCompany(Base):
    """Бд модель информации о компании."""

    name: Mapped[str] = mapped_column(
        pgsql_types.VARCHAR(48),
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        pgsql_types.VARCHAR(128)
    )


class CheckCompanyPortfolio(Base):
    """Бд модель информации о проектах."""

    project_name: Mapped[str] = mapped_column(
        pgsql_types.VARCHAR(48),
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        pgsql_types.VARCHAR(128)
    )


class Info(Base):
    """Бд модель F.A.Q."""

    question_type: Mapped[QuestionEnum] = mapped_column(
        pgsql_types.ENUM(
            QuestionEnum,
            name='question_enum',
            create_type=False
        ),
        nullable=False
    )

    question: Mapped[str] = mapped_column(
        pgsql_types.TEXT,
        unique=True
    )

    answer: Mapped[str] = mapped_column(
        pgsql_types.TEXT,
        nullable=False
    )


class ContactManager(Base):
    """Бд модель заявки к менеджеру."""

    first_name: Mapped[str] = mapped_column(
        pgsql_types.VARCHAR(32),
        nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        pgsql_types.VARCHAR(25),
        nullable=False
    )

    need_support: Mapped[bool] = mapped_column(
        pgsql_types.BOOLEAN,
        default=False,
        nullable=False
    )

    need_contact_with_manager: Mapped[bool] = mapped_column(
        pgsql_types.BOOLEAN,
        default=False,
        nullable=False
    )

    shipping_date: Mapped[datetime] = mapped_column(
        pgsql_types.TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

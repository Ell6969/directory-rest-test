import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import SFilterPagination

logger = logging.getLogger(__name__)


class BaseDAO:
    model = None
    schema_all_fields = None

    @classmethod
    async def find_all(cls, session: AsyncSession, pagination: SFilterPagination = SFilterPagination(), **filter_by):
        """
        Находит и возвращает все записи. С возможным фильтром и пагинацией.
        :param filter_by: Фильтры для поиска записи.
        :return: Список объектов schema_all_fields.
        """
        try:
            query = (
                select(cls.model)
                .filter_by(**filter_by)
                .limit(pagination.page_size)
                .offset((pagination.page - 1) * pagination.page_size)
            )
            result = await session.execute(query)
            instances = result.scalars().all()
            return [cls.schema_all_fields.model_validate(instance) for instance in instances]
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка базы данных при получении записи. {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Неизвестная ошибка при получении записи.{e}")

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        """
        Добавляет запись в таблицу.
        :param data: Словарь с данными для добавления.
        :return: Сам объект schema_all_fields
        """
        try:
            instance = cls.model(**data)

            session.add(instance)
            await session.commit()
            await session.refresh(instance)

            return cls.schema_all_fields.model_validate(instance)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка базы данных при добавлении записи. {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Неизвестная ошибка при добавлении записи.{e}")

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        """
        Находит и возвращает одну запись по фильтру.
        :param filter_by: Фильтры для поиска записи.
        :return: Сам объект schema_all_fields.
        """
        query = select(cls.model).filter_by(**filter_by)

        result = await session.execute(query)

        instance = result.scalars().one_or_none()

        if instance:
            try:
                return cls.schema_all_fields.model_validate(instance)
            except Exception as e:
                raise e

        return None

    @classmethod
    async def find_one_or_create(cls, session: AsyncSession, defaults=None, **filter_by):
        """
        Ищет одну запись по фильтру или создает новую, если не найдена.
        :param defaults: Словарь с данными для создания, если запись не найдена.
        :param filter_by: Фильтры для поиска записи.
        :return: Сам объект schema_all_fields.
        :example: record = await BaseDAO.find_one_or_create(defaults={"name": "Example"}, name="Example")
        """
        defaults = defaults or {}

        try:
            existing_record = await cls.find_one_or_none(session=session, **filter_by)

            if existing_record:
                return cls.schema_all_fields.model_validate(existing_record)

            new_record = await cls.add(session=session, **defaults)
            return new_record

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка базы данных при добавлении записи. {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Неизвестная ошибка при добавлении записи.{e}")

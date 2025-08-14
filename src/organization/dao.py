from fastapi import HTTPException
from geoalchemy2.types import Geography
from sqlalchemy import func, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.building.models import Building
from src.dao.base_dao import BaseDAO
from src.organization.models import Organization, OrganizationActivity
from src.organization.schemas import SOrgAll


class OrgDAO(BaseDAO):
    model = Organization
    schema_all_fields = SOrgAll

    @classmethod
    def _base_query(cls):
        return select(cls.model)

    @classmethod
    def filter_by_activity(cls, query, activity_id: int):
        return query.join(OrganizationActivity, cls.model.id == OrganizationActivity.organization_id).filter(
            OrganizationActivity.activity_id == activity_id
        )

    @classmethod
    def filter_by_radius(cls, query, lat: float, lon: float, radius_m: float):
        point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)

        return query.join(Building, Building.id == cls.model.building_id).filter(
            func.ST_DWithin(Building.geom.cast(Geography), point.cast(Geography), radius_m)
        )

    @classmethod
    def filter_by_bbox(cls, query, bbox: tuple[float, float, float, float]):
        """
        Фильтр организаций по прямоугольной области (bounding box)
        bbox = (min_lon, min_lat, max_lon, max_lat)
        """
        min_lon, min_lat, max_lon, max_lat = bbox
        return query.join(cls.model.building).filter(
            Building.longitude >= min_lon,
            Building.longitude <= max_lon,
            Building.latitude >= min_lat,
            Building.latitude <= max_lat,
        )

    @classmethod
    async def filter_by_activity_name(cls, session: AsyncSession, activity_name: str):
        try:
            sql = text(
                """
                WITH RECURSIVE activity_tree AS (
                    SELECT id
                    FROM activities
                    WHERE name = :activity_name
                    UNION ALL
                    SELECT a.id
                    FROM activities a
                    INNER JOIN activity_tree at ON a.parent_id = at.id
                )
                SELECT o.*
                FROM organizations o
                WHERE EXISTS (
                    SELECT 1
                    FROM organization_activities oa
                    WHERE oa.organization_id = o.id
                      AND oa.activity_id IN (SELECT id FROM activity_tree)
                )
            """
            )

            result = await session.execute(sql, {"activity_name": activity_name})
            orgs = result.mappings().all()
            return [cls.schema_all_fields.model_validate(dict(o)) for o in orgs]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при поиске организаций по виду деятельности. {e}")

    @classmethod
    def filter_by_name(cls, query, org_name: str):
        """
        Фильтр организаций по имени (полное или частичное совпадение)
        """
        return query.filter(cls.model.name.ilike(f"%{org_name}%"))

    @classmethod
    async def find_with_filters(cls, session: AsyncSession, **filters):
        try:
            query = cls._base_query()

            if activity_id := filters.get("activity_id"):
                query = cls.filter_by_activity(query, activity_id)
            elif radius := filters.get("radius"):
                query = cls.filter_by_radius(query, **radius)
            elif bbox := filters.get("bbox"):
                query = cls.filter_by_bbox(query, bbox)
            elif org_name := filters.get("org_name"):
                query = cls.filter_by_name(query, org_name)

            result = await session.execute(query)
            orgs = result.scalars().all()
            return [cls.schema_all_fields.model_validate(o) for o in orgs]
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка базы данных при поиске записи. {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Неизвестная ошибка при поиске записи.{e}")

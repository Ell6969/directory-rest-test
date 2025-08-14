from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import SFilterPagination
from src.organization.dao import OrgDAO
from src.organization.schemas import SGeoBbox, SGeoRadius, SOrgAll


class OrgService:

    def __init__(self, session: AsyncSession, dao: type[OrgDAO] = OrgDAO):
        self.session = session
        self.dao = dao

    async def get_all_org_by_build(
        self, building_id: int, pagination: SFilterPagination = SFilterPagination()
    ) -> List[SOrgAll]:
        """
        Список всех организаций, находящихся в конкретном здании.
        :param building_id: ID здания
        :param pagination: объект пагинации
        :return: список объектов SOrgAll
        """
        orgs = await self.dao.find_all(self.session, pagination=pagination, building_id=building_id)
        return orgs

    async def get_org_by_id(self, org_id: int) -> SOrgAll:
        """
        Получить орг по ИД
        """
        return await self.dao.find_one_or_none(self.session, id=org_id)

    async def get_org_by_act_id(self, activity_id: int) -> SOrgAll:
        """
        Получить орг по ИД деятельности
        """
        return await self.dao.find_with_filters(self.session, activity_id=activity_id)

    async def get_orgs_by_geo_radius(self, geo_filter: SGeoRadius) -> List[SOrgAll]:
        """
        Получить список организаций в радиусе вокруг точки.
        """
        if geo_filter.lat is None or geo_filter.lon is None or geo_filter.radius_m is None:
            raise HTTPException(400, "lat, lon и radius_m обязательны")

        filters = {"radius": {"lat": geo_filter.lat, "lon": geo_filter.lon, "radius_m": geo_filter.radius_m}}
        return await self.dao.find_with_filters(self.session, **filters)

    async def get_orgs_by_geo_bbox(self, geo_filter: SGeoBbox) -> List[SOrgAll]:
        """
        Получить список организаций в пределах прямоугольной области (bbox).
        """
        if not geo_filter.bbox:
            raise HTTPException(400, "bbox обязателен")

        try:
            bbox_values = tuple(map(float, geo_filter.bbox.split(",")))
            if len(bbox_values) != 4:
                raise ValueError("bbox должен содержать 4 числа: min_lon,min_lat,max_lon,max_lat")
        except Exception as e:
            raise HTTPException(400, f"Неверный формат bbox: {e}")

        filters = {"bbox": bbox_values}
        return await self.dao.find_with_filters(self.session, **filters)

    async def get_orgs_by_act_name_tree(self, act_name: str) -> List[SOrgAll]:
        """
        Получить организации по имени вида деятельности (с учетом вложенности)
        """
        return await self.dao.filter_by_activity_name(self.session, act_name)

    async def get_orgs_by_name(self, org_name: str) -> List[SOrgAll]:
        """
        Получить организации по имени
        """
        return await self.dao.find_with_filters(self.session, org_name=org_name)

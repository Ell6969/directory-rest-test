from fastapi import APIRouter, Depends

from src.organization.dep import OrgServiceDEP
from src.organization.schemas import SGeoBbox, SGeoRadius
from src.schemas import SRouterResult, SRouterResultList

router = APIRouter(prefix="/organization", tags=["Организации"])


@router.get("/building/{building_id}")
async def get_all_org_by_building(org_services: OrgServiceDEP, building_id: int) -> SRouterResultList:
    """
    Список всех организаций находящихся в конкретном здании, по ID здания
    """
    return SRouterResultList(results=await org_services.get_all_org_by_build(building_id))


@router.get("/activity/{activity_id}")
async def get_all_org_by_act(org_services: OrgServiceDEP, activity_id: str) -> SRouterResultList:
    """
    Список всех организаций, которые относятся к указанному виду деятельности
    """
    return SRouterResultList(results=await org_services.get_org_by_act_id(int(activity_id)))


@router.get("/activity-name/{act_name}")
async def get_organizations_by_activity_name_tree(org_services: OrgServiceDEP, act_name: str) -> SRouterResultList:
    """
    Получить организации по имени вида деятельности (с учетом вложенности)
    """
    return SRouterResultList(results=await org_services.get_orgs_by_act_name_tree(act_name))


@router.get("/geo/radius")
async def get_org_by_geo_radius(
    org_services: OrgServiceDEP,
    geo_filter: SGeoRadius = Depends(),
):
    """
    Получить список организаций по гео-условиям:
        - Радиус вокруг точки (lat/lon/radius_m)
    """
    return SRouterResultList(results=await org_services.get_orgs_by_geo_radius(geo_filter))


@router.get("/geo/bbox")
async def get_org_by_geo_bbox(
    org_services: OrgServiceDEP,
    geo_filter: SGeoBbox = Depends(),
):
    """
    Получить список организаций по гео-условиям:
        - Прямоугольная область (bbox)
        bbox = str(
            37.6170,  # min_lon
            55.7555,  # min_lat
            37.6180,  # max_lon
            55.7560   # max_lat
        )
    """
    return SRouterResultList(results=await org_services.get_orgs_by_geo_bbox(geo_filter))


@router.get("/search")
async def get_org_by_name(org_services: OrgServiceDEP, name: str) -> SRouterResultList:
    """
    Поиск организаций по имени (полное или частичное совпадение)
    """
    return SRouterResultList(results=await org_services.get_orgs_by_name(name))


@router.get("/{org_id}")
async def get_org_by_id(org_services: OrgServiceDEP, org_id: int) -> SRouterResult:
    """
    Вывод информации об организации по её идентификатору
    """
    return SRouterResult(result=await org_services.get_org_by_id(org_id))

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app import utils

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
async def index(request: Request, year: int | None = None) -> HTMLResponse:
    """
    Return HTMX index page
    """
    data = await utils.get_vessels_from_file(year)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"data": data},
    )


@router.get("/vessels")
async def vessels(request: Request, year: int | None = None) -> HTMLResponse:
    """
    Return JSON with vessels info for desired year for HTMX website
    """
    data = await utils.get_vessels_from_file(year)
    return templates.TemplateResponse(
        request=request,
        name="vessels_table.html",
        context={"data": data},
    )


@router.get("/api/vessels")
async def read_vessel_info(year: int | None = None) -> list[dict]:
    data = await utils.get_vessels_from_file(year)
    summary = utils.generate_summary(data, year)

    return [{"data": data, "summary": summary}]


@router.get("/api/update/check")
async def find_updates(year: int | None = None) -> dict[str, list]:
    data_old = await utils.get_vessels_from_file(year)
    data_new = await utils.get_schedule_json(year)
    report = utils.compare_data(data_old, data_new)
    return report


@router.get("/api/update/confirm", status_code=status.HTTP_204_NO_CONTENT)
def confirm_update(year: int | None = None) -> None:
    """
    Endpoint for confirming updates for schedule.
    Replace new_data_YYYY with data_YYYY.
    """
    utils.replace_old_with_new_file(year)


@router.get("/api/update/notification")
async def update_notification() -> dict:
    """
    Notification about new updates for
    """
    return await utils.update_notification()

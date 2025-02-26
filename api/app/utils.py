#! /usr/bin/python3
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, TypedDict

import httpx
from fastapi import HTTPException

DATA_FILE_PREFIX = "data/data_"
NEW_DATA_PREFIX = "data/new_data_"
REPORT_PREFIX = "data/report_"
DATA_FILE_EXT = ".json"


class Data(TypedDict):
    id: int
    arrival: str
    departure: str
    status: str | None
    port_name: str | None
    vessel_name: str | None
    vessel_passengers: int
    vessel_crew: int
    vessel_length_overall: int | float | None
    vessel_breadth_extreme: int | float | None
    turn_around: bool


def validate_year(year: int | None) -> int:
    """
    Validates user provided year.
    If no year provided by default use current season year
    or next year if season is finished.
    """
    if year is None:
        date = datetime.now()
        year = date.year
        month = date.month
        if month > 9:
            year += 1
    if not isinstance(year, int):
        raise ValueError(f"Variable year is not integer - {year}")
    if year not in range(2025, 2035):
        raise HTTPException(
            status_code=500, detail=f"Unsupported year - {year}."
        )
    return year


async def get_vessels_from_file(year: int | None) -> list[Data]:
    year = validate_year(year)
    data_path = DATA_FILE_PREFIX + str(year) + DATA_FILE_EXT

    file_exists = Path(data_path)
    if not file_exists.is_file():
        await get_schedule_json(year)

    with open(data_path) as f:
        data: list[Data] = json.load(f)
    return data


async def get_schedule_json(year: int | None) -> list[Data]:
    year = validate_year(year)

    port_url = (
        "https://dokk-backend.azurewebsites.net/api/v1/calendar/?start_date="
        + str(year)
        + "-4-01&end_date="
        + str(year)
        + "-11-15&port=3"
    )
    # get data from API
    async with httpx.AsyncClient() as client:
        response = await client.get(port_url, timeout=10)

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Cannot fetch data from API. Try again later",
        )
    data: list[Data] = response.json()

    """
    Check if file for selected year exists.
    If not save as first and finish program.
    Otherwise save data as new data.
    """
    file_exists = Path(DATA_FILE_PREFIX + str(year) + DATA_FILE_EXT)

    if not file_exists.is_file():
        with open(DATA_FILE_PREFIX + str(year) + DATA_FILE_EXT, "w") as f:
            json.dump(data, f)
    else:
        with open(NEW_DATA_PREFIX + str(year) + DATA_FILE_EXT, "w") as f:
            json.dump(data, f)
    return data


def convert_json_to_dict(
    json_data: list[Data],
) -> dict[int, Data]:
    """
    Convert JSON data to list of dicts with cruise ID as key.
    """
    new_dict = {}
    for d in json_data:
        new_dict[d["id"]] = d
    return new_dict


def generate_summary(
    data: list[Data], year: int | None
) -> list[dict[str, Any]]:
    """
    Get dictionary with cruise data and generate report with number of
    passengers and cruises etc.
    """
    validate_year(year)
    data_dict = convert_json_to_dict(data)
    report_may = {"total_pax": 0, "total_crew": 0, "total_vessels": 0}
    report_jun = {"total_pax": 0, "total_crew": 0, "total_vessels": 0}
    report_jul = {"total_pax": 0, "total_crew": 0, "total_vessels": 0}
    report_aug = {"total_pax": 0, "total_crew": 0, "total_vessels": 0}
    report_sep = {"total_pax": 0, "total_crew": 0, "total_vessels": 0}

    for d in data_dict.values():
        # if arrived in May
        if d["arrival"][6] == "5":
            report_may["total_pax"] += d["vessel_passengers"]
            report_may["total_crew"] += d["vessel_crew"]
            report_may["total_vessels"] += 1
        # if arrived in June
        if d["arrival"][6] == "6":
            report_jun["total_pax"] += d["vessel_passengers"]
            report_jun["total_crew"] += d["vessel_crew"]
            report_jun["total_vessels"] += 1
        # if arrived in July
        if d["arrival"][6] == "7":
            report_jul["total_pax"] += d["vessel_passengers"]
            report_jul["total_crew"] += d["vessel_crew"]
            report_jul["total_vessels"] += 1
        # if arrived in August
        if d["arrival"][6] == "8":
            report_aug["total_pax"] += d["vessel_passengers"]
            report_aug["total_crew"] += d["vessel_crew"]
            report_aug["total_vessels"] += 1
        # if arrived in September
        if d["arrival"][6] == "9":
            report_sep["total_pax"] += d["vessel_passengers"]
            report_sep["total_crew"] += d["vessel_crew"]
            report_sep["total_vessels"] += 1

    report_total = {
        "total_pax": report_may["total_pax"]
        + report_jun["total_pax"]
        + report_jul["total_pax"]
        + report_aug["total_pax"]
        + report_sep["total_pax"],
        "total_crew": report_may["total_crew"]
        + report_jun["total_crew"]
        + report_jul["total_crew"]
        + report_aug["total_crew"]
        + report_sep["total_crew"],
        "total_vessels": report_may["total_vessels"]
        + report_jun["total_vessels"]
        + report_jul["total_vessels"]
        + report_aug["total_vessels"]
        + report_sep["total_vessels"],
    }

    return [
        report_may,
        report_jun,
        report_jul,
        report_aug,
        report_sep,
        report_total,
    ]


def compare_data(
    data_old: list[Data], data_new: list[Data]
) -> dict[str, list]:
    """
    Compare data and generate report.
    """

    report: dict = {}
    # convert data to key value pairs to search by ID
    data_old_dict = convert_json_to_dict(data_old)
    data_new_dict = convert_json_to_dict(data_new)

    # Get vessel IDs for old and new data
    old_keys = {d["id"] for d in data_old_dict.values()}
    new_keys = {d["id"] for d in data_new_dict.values()}

    # Get info about new and removed vessels
    added = list(new_keys - old_keys)
    removed = list(old_keys - new_keys)

    if added:
        report["added"] = [data_new_dict[id] for id in added]
    if removed:
        report["removed"] = [data_old_dict[id] for id in removed]

    # Compare all data in dicts in common vessels IDs
    common_vessels = old_keys.intersection(new_keys)

    updated: list[dict[str, dict | Data]] = []
    for el in common_vessels:
        vessel_diff = set(data_new_dict[el].items()) - set(
            data_old_dict[el].items()
        )
        if vessel_diff:
            updated.append(
                {
                    "vessel": data_old_dict[el],
                    "change": {k: v for k, v in vessel_diff},
                }
            )
    if updated:
        report["updated"] = updated
    return report


def replace_old_with_new_file(year: int | None) -> None:
    validate_year(year)

    data_new = NEW_DATA_PREFIX + str(year) + DATA_FILE_EXT
    data_old = DATA_FILE_PREFIX + str(year) + DATA_FILE_EXT

    file_old_path = Path(data_old)
    file_new_path = Path(data_new)
    if not (file_old_path.is_file() and file_new_path.is_file()):
        raise HTTPException(
            status_code=500,
            detail=f"At least one of the files with data for {year} does not exist.",
        )
    os.remove(data_old)
    os.rename(data_new, data_old)


async def update_notification() -> dict:
    year = validate_year(None)
    data_new = NEW_DATA_PREFIX + str(year) + DATA_FILE_EXT
    file_new_path = Path(data_new)
    if not file_new_path.is_file():
        return {}
    fresh_data = await get_schedule_json(year)

    with open(data_new) as f:
        data: list[Data] = json.load(f)

    report = compare_data(data, fresh_data)
    return report

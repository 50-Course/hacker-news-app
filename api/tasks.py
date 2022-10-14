from __future__ import annotations

import asyncio
from typing import Any
from typing import Dict

import aiohttp
from celery import shared_task
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings
from django.db import transaction
from rest_framework import status

from api.lib.collector import HackerNewsCollector
from api.models.models import HNUser
from api.serializers import BaseItemSerializer
from api.serializers import UserSerializer


# from api.lib import runsync

logger = get_task_logger(__name__)


@shared_task
def sync_db():
    logger.info(f"Syncing DB....")

    try:
        asyncio.run(HackerNewsCollector.main())
    except Exception as e:
        logger.exception(e)

    logger.info(f"Sync Finished. Exiting.")


def fetch_changes(retries: int = 3):
    """
    Listens for changes on the HN Endpoint \
    on `/updates.json` and updates the db \
    for item and profile changes.
    """

    BASE_URL = settings.HACKER_NEWSAPI_URI
    """Hacker News v0 Public Endpoint"""

    endpoint = f"{BASE_URL}/updates.json"

    logger.info(f"Making HTTP Rquest call to {endpoint}.")

    with aiohttp.ClientSession as session:
        try:
            resp = yield from session.get(endpoint)
        except Exception as err:
            logger.error(f"An exception occured on {endpoint}: {err}")

        else:
            if resp.status != status.HTTP_200_OK:
                logger.error(f"Error connecting to {endpoint}: {resp.status}")
            else:
                logger.info(f"Updating DB....")
                resp_data = yield from resp.json()
                return resp_data


@crontab(minute=0, hour="*/3")
def update_changes(data: dict[Any, Any]) -> dict:
    # if resp data we want to update the db immidiately
    if data is not None:
        profiles = data.get("profiles")

        items_to_update = data["items"]

        for user in profiles:
            try:
                user_serializer = UserSerializer(data=user)
                if user_serializer.is_valid():
                    users = HNUser.objects.update_or_create(
                        user_serializer.data
                    )
                pass
            except Exception as err:
                logger.info(
                    f"There was an error while updating user profiles"
                    f"Error: {err}"
                )
            return {}

        for item in items_to_update:
            items = HackerNewsCollector.save_to_db(item=item)

    return {"profiles": users, "items": items}

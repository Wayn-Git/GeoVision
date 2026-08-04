"""Google Earth Engine initialization."""

from __future__ import annotations

import json
import logging
import os
from typing import Optional

import ee
from google.oauth2 import service_account

log = logging.getLogger(__name__)


def init_ee(project: Optional[str]) -> None:
    """Initialize Google Earth Engine."""

    kwargs = {"project": project} if project else {}

    service_key = os.getenv("EE_SERVICE_ACCOUNT_KEY")

    if service_key:
        info = json.loads(service_key)

        credentials = service_account.Credentials.from_service_account_info(
            info,
            scopes=["https://www.googleapis.com/auth/earthengine"],
        )

        ee.Initialize(credentials=credentials, **kwargs)
        log.info("Initialized EE using service account.")
        return

    # Local development only
    try:
        ee.Initialize(**kwargs)
        log.info("Initialized EE using local credentials.")
    except ee.EEException:
        log.info("Authenticating Earth Engine...")
        ee.Authenticate()
        ee.Initialize(**kwargs)
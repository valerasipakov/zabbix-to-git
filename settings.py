# tg_bot_dev/settings.py
import logging
import os
from dataclasses import dataclass
from typing import Set
from dotenv import load_dotenv

# Загружаем .env один раз при импорте настроек
load_dotenv()

@dataclass(frozen=True)
class Settings:
    token: str
    acl_ids: Set[int]
    zbx_user: str
    zbx_passwd: str

def _parse_acl(raw_acl: str | None) -> Set[int]:
    acl: Set[int] = set()
    if not raw_acl:
        return acl
    for part in raw_acl.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            acl.add(int(part))
        except ValueError:
            logging.warning("Skip invalid ACL id: %r", part)
    return acl

def get_settings() -> Settings:
    token = os.environ.get("BOT_TOKEN", "")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    acl_ids = _parse_acl(os.environ.get("ACL_IDS"))

    if not acl_ids:
        logging.warning("ACL_IDS is empty — никто не сможет писать боту")

    zbx_user = os.environ.get("ZBX_USER", "")
    zbx_passwd = os.environ.get("ZBX_PASSWD", "")
    if (not zbx_user) or (not zbx_passwd):
        logging.warning("ZBX_USER or ZBX_PASSWD is empty")

    return Settings(
        token=token,
        acl_ids=acl_ids,
        zbx_user=zbx_user,
        zbx_passwd=zbx_passwd,
    )

# Единый экземпляр настроек для всего приложения
settings = get_settings()

from .zabbix_handler import router as zabbix_handler_router
from .admin_handler import router as admin_handler_router
from .navigation import router as navigation_router


__all__ = ["zabbix_handler_router", "admin_handler_router", "navigation_router"]




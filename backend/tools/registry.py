from backend.tools.order_tools import get_order
from backend.tools.return_tools import check_return_eligibility
from backend.tools.shipping_tools import get_shipping_status


TOOLS = [
    get_order,
    get_shipping_status,
    check_return_eligibility,
]

TOOLS_BY_NAME = {
    tool.name: tool
    for tool in TOOLS
}
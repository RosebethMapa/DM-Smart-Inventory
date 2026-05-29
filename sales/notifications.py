import json
import logging
from urllib import request
from urllib.error import HTTPError, URLError

from django.conf import settings
from django.utils import timezone

from .models import Sale

logger = logging.getLogger(__name__)


def _format_money(value):
    return f"PHP {value:,.2f}"


def _order_message(sale):
    created_at = timezone.localtime(sale.created_at).strftime("%b %d, %Y %I:%M %p")
    customer = sale.customer_name or "Walk-in customer"
    lines = [
        "New successful order",
        f"Receipt: #{sale.pk:06d}",
        f"Date: {created_at}",
        f"Status: {sale.get_status_display()}",
        f"Cashier: {sale.cashier.username}",
        f"Customer: {customer}",
        "",
        "Items:",
    ]

    for item in sale.items.all()[:8]:
        lines.append(f"- {item.product.name} x{item.quantity} = {_format_money(item.line_total)}")

    item_count = sale.items.count()
    if item_count > 8:
        lines.append(f"- and {item_count - 8} more item(s)")

    lines.extend(
        [
            "",
            f"Subtotal: {_format_money(sale.subtotal)}",
            f"Discount: {_format_money(sale.discount)}",
            f"Total: {_format_money(sale.total_amount)}",
            f"Payment: {sale.get_payment_method_display()}",
            f"Received: {_format_money(sale.amount_received)}",
            f"Change: {_format_money(sale.change)}",
            f"Balance: {_format_money(sale.balance_due)}",
        ]
    )
    return "\n".join(lines)


def notify_order_success(sale_id):
    if not settings.TELEGRAM_ORDER_NOTIFICATIONS:
        return
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return

    sale = (
        Sale.objects.select_related("cashier")
        .prefetch_related("items__product")
        .get(pk=sale_id)
    )
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": _order_message(sale),
        "disable_web_page_preview": True,
    }
    body = json.dumps(payload).encode("utf-8")
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    telegram_request = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(telegram_request, timeout=8):
            return
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        logger.warning("Telegram order notification failed for sale %s: %s", sale_id, exc)

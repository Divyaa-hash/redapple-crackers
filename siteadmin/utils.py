from django.conf import settings


def send_whatsapp_notification(order):
    """Send WhatsApp notification for new order"""
    try:
        # Get WhatsApp admin number from settings
        whatsapp_number = getattr(settings, 'WHATSAPP_ADMIN_NUMBER', '9345980679')
        
        # Prepare message
        message = f"""
🎉 *NEW ORDER RECEIVED* 🎉

Order Number: {order.order_number}
Customer: {order.shipping_name}
Phone: {order.shipping_phone}
Amount: ₹{order.total_amount}
Status: {order.get_order_status_display().upper()}

Shipping Address:
{order.shipping_address_line1}
{order.shipping_address_line2}
{order.shipping_city}, {order.shipping_state}
{order.shipping_postal_code}

Items:
"""
        for item in order.items.all():
            message += f"- {item.product.name} x {item.quantity} = ₹{item.total_price}\n"
        
        message += f"\nTotal: ₹{order.total_amount}"
        
        # Use WhatsApp API (you'll need to integrate with a service like Twilio, WhatsApp Business API, etc.)
        # This is a placeholder - you'll need to set up actual WhatsApp API integration
        print(f"WhatsApp notification sent to {whatsapp_number}: {message}")
        
        return True
    except Exception as e:
        print(f"Error sending WhatsApp notification: {e}")
        return False
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.core.mail import EmailMessage
from django.conf import settings

def generate_invoice_pdf(order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 24)
    p.drawString(250, 770, "INVOICE")

    p.setFont("Helvetica", 12)
    p.drawString(50, 700, f"Order ID: {order.id}")
    p.drawString(50, 680, f"Date: {order.created_at.strftime('%Y-%m-%d')}")
    p.drawString(50, 660, f"Customer: {order.user.get_full_name()}")
    
    p.drawString(50, 620, "Product")
    p.drawString(300, 620, "Quantity")
    p.drawString(400, 620, "Price")
    p.drawString(500, 620, "Total")
    
    p.line(50, 610, 550, 610)
    
    p.drawString(50, 590, order.product.name)
    p.drawString(300, 590, str(order.quantity))
    p.drawString(400, 590, f"${order.product.price:.2f}")
    p.drawString(500, 590, f"${order.total_price:.2f}")
    
    p.line(50, 570, 550, 570)
    p.drawString(400, 550, "Total:")
    p.drawString(500, 550, f"${order.total_price:.2f}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer

def send_invoice_email(order):
    pdf_buffer = generate_invoice_pdf(order)
    
    subject = f"Invoice for Order #{order.id}"
    message = f"Thank you for your purchase. Please find attached the invoice for your order #{order.id}."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [order.user.email]
    
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach(f"invoice_{order.id}.pdf", pdf_buffer.getvalue(), 'application/pdf')
    email.send()
from flask import Flask, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

app = Flask(__name__)

def create_watermark(text):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.6, 0.6, 0.6)
    c.drawString(50, 50, text)
    c.save()
    packet.seek(0)
    return PdfReader(packet)

def add_watermark(input_pdf_path, output_pdf_path, watermark_text):
    watermark = create_watermark(watermark_text)
    watermark_page = watermark.pages[0]

    pdf_reader = PdfReader(input_pdf_path)
    pdf_writer = PdfWriter()

    for page in pdf_reader.pages:
        page.merge_page(watermark_page)
        pdf_writer.add_page(page)

    with open(output_pdf_path, "wb") as output_file:
        pdf_writer.write(output_file)

@app.route('/generate_watermarked_pdf', methods=['POST'])
def generate_watermarked_pdf():
    data = request.json
    order_number = data.get('order_number')
    email = data.get('email')

    watermark_text = f"Order #{order_number} - Buyer: {email}"

    input_pdf_path = "original_pdf.pdf"
    output_pdf_path = f"watermarked_order_{order_number}.pdf"

    add_watermark(input_pdf_path, output_pdf_path, watermark_text)

    return send_file(output_pdf_path, as_attachment=True)

from flask import Flask, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

# Flask app setup
app = Flask(__name__)

# Function to create a watermark
def create_watermark(text):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.6, 0.6, 0.6)  # Light gray
    c.drawString(50, 50, text)
    c.save()
    packet.seek(0)
    return PdfReader(packet)

# Function to add watermark to PDF
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
    data = request.json  # Expecting JSON with 'order_number' and 'email'
    order_number = data.get('order_number')
    email = data.get('email')

    # Prepare watermark text
    watermark_text = f"Order #{order_number} - Buyer: {email}"

    # Set file paths
    input_pdf_path = "/path/to/your/original_pdf.pdf"  # Update with your PDF file path
    output_pdf_path = f"/tmp/watermarked_order_{order_number}.pdf"

    # Add watermark
    add_watermark(input_pdf_path, output_pdf_path, watermark_text)

    # Send watermarked file
    return send_file(output_pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

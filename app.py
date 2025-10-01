import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import date
from io import BytesIO

# --- PDF Generation Function ---
def create_quotation_pdf(user_name, items_data, output_buffer):
    """Generates the PDF using ReportLab with dynamic data."""
    
    doc = SimpleDocTemplate(output_buffer, pagesize=A4,
                            rightMargin=inch/2, leftMargin=inch/2,
                            topMargin=inch/2, bottomMargin=inch/2)
    styles = getSampleStyleSheet()

    # Define Custom Styles (Same as before)
    header_style = ParagraphStyle('Header', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=18, alignment=1, spaceAfter=0)
    subheader_style = ParagraphStyle('SubHeader', parent=styles['Normal'], fontName='Helvetica', fontSize=10, alignment=0, leading=12, spaceAfter=0)
    address_style = ParagraphStyle('Address', parent=styles['Normal'], fontName='Helvetica', fontSize=8, alignment=0, leading=10, spaceAfter=0)
    quotation_title_style = ParagraphStyle('QuotationTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, alignment=0, spaceAfter=12)
    name_style = ParagraphStyle('NameStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, alignment=0, spaceAfter=12)
    table_header_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, alignment=1, spaceAfter=6, spaceBefore=6)
    table_cell_style = ParagraphStyle('TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=9, alignment=0, spaceAfter=3, spaceBefore=3)
    table_cell_right_style = ParagraphStyle('TableCellRight', parent=styles['Normal'], fontName='Helvetica', fontSize=9, alignment=2, spaceAfter=3, spaceBefore=3)
    total_style = ParagraphStyle('Total', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, alignment=2, spaceAfter=6, spaceBefore=6)
    payment_material_style_bold = ParagraphStyle('PaymentMaterialBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, alignment=0, spaceAfter=3)
    payment_material_style_normal = ParagraphStyle('PaymentMaterialNormal', parent=styles['Normal'], fontName='Helvetica', fontSize=9, alignment=0, spaceAfter=3)

    elements = []

    # --- Header Section (Identical to Image) ---
    logo_and_name_data = [
        [Paragraph('<font color="#8B0000" size="24"><b>SB</b></font>', styles['Normal']),
         Paragraph('Shree Balaji Interiors', header_style)],
        [Paragraph('SHREE BALAJI INTERIORS', subheader_style),
         Paragraph('Modular Kitchen All Types of Wooden Furniture', subheader_style)],
        [Paragraph('Mob.: <font color="blue">9579455022</font>, <font color="blue">7588552035</font>', address_style),
         Paragraph('Fadol Mala, Near Ambad Weight, Ambadgaon, Nashik-422010.', address_style)],
        [Paragraph('Email: <font color="blue">shreebalajiinteriors12@gmail.com</font>', address_style),
         Paragraph('State : Maharashtra', address_style)],
    ]

    logo_and_name_table = Table(logo_and_name_data, colWidths=[1.5*inch, 4.5*inch])
    logo_and_name_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'), ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('SPAN', (0,0), (0,1)),
        ('TEXTCOLOR', (0,0), (0,0), colors.Color(red=0.54, green=0.0, blue=0.0)), 
        ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(logo_and_name_table)
    elements.append(Spacer(1, 0.1 * inch))

    elements.append(Paragraph('<hr width="100%" color="black" noshade size="3"/>', styles['Normal']))
    elements.append(Spacer(1, 0.1 * inch))

    # Quotation and Date Section
    quotation_date_data = [
        [Paragraph('<b>Quotation</b>', quotation_title_style), Paragraph(f'<b>Date:</b> {date.today().strftime("%d-%m-%Y")}', quotation_title_style)]
    ]
    quotation_date_table = Table(quotation_date_data, colWidths=[3*inch, 3*inch])
    quotation_date_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (0,0), 'LEFT'), ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(quotation_date_table)
    elements.append(Spacer(1, 0.1 * inch))

    # Dynamic User Name
    elements.append(Paragraph(f'Name {user_name}', name_style))
    elements.append(Spacer(1, 0.1 * inch))

    # --- Dynamic Items Table ---
    table_data = [
        [
            Paragraph('<b>sr no</b>', table_header_style),
            Paragraph('<b>Description</b>', table_header_style),
            Paragraph('<b>qty / sq.fee</b>', table_header_style),
            Paragraph('<b>rate</b>', table_header_style),
            Paragraph('<b>Amt</b>', table_header_style)
        ],
    ]
    
    total_amount = 0
    for i, item in enumerate(items_data):
        # Calculate Amount and Total
        try:
            amount = item['qty'] * item['rate']
            total_amount += amount
        except (TypeError, ValueError):
            amount = 0 # Handle cases where qty or rate are not numbers

        table_data.append([
            Paragraph(str(i+1), table_cell_style), 
            Paragraph(item['name'], table_cell_style), 
            Paragraph(f"{item['qty']}", table_cell_right_style), 
            Paragraph(f"{item['rate']}", table_cell_right_style), 
            Paragraph(f"{amount:,.2f}", table_cell_right_style)
        ])

    # Total Row
    table_data.append([
        '', '', '', Paragraph('<b>Total</b>', total_style), Paragraph(f'₹ {total_amount:,.2f}', total_style)
    ])

    col_widths = [0.5*inch, 2.5*inch, 1*inch, 1*inch, 1*inch]
    item_table = Table(table_data, colWidths=col_widths)

    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey), ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (0,1), (1,-2), 'LEFT'), ('ALIGN', (2,1), (-1,-2), 'RIGHT'),
        ('RIGHTPADDING', (2,1), (-1,-2), 5), ('LEFTPADDING', (1,1), (1,-2), 5), 
        
        # Style for the Total row
        ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey), ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('ALIGN', (-2,-1), (-2,-1), 'RIGHT'), ('ALIGN', (-1,-1), (-1,-1), 'RIGHT'),
        ('RIGHTPADDING', (-1,-1), (-1,-1), 5), ('SPAN', (0,-1), (2,-1)), 
    ]))
    elements.append(item_table)
    elements.append(Spacer(1, 0.2 * inch))

    # --- Footer Section (Identical to Image) ---
    payment_material_data = [
        [Paragraph('<b>Payment Details:</b> 60% Advanced', payment_material_style_bold),
         Paragraph('<b>Material Used</b>', payment_material_style_bold)],
        [Paragraph('30% After delivery', payment_material_style_normal),
         Paragraph('17 MM ISI Mark Calibrated Plywood', payment_material_style_normal)],
        [Paragraph('10% After installation', payment_material_style_normal),
         Paragraph('1.00 MM Laminate', payment_material_style_normal)],
    ]

    payment_material_table = Table(payment_material_data, colWidths=[3*inch, 3*inch])
    payment_material_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'), ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(payment_material_table)

    doc.build(elements)
    
    # Reset the buffer position to the start for reading
    output_buffer.seek(0)
    return output_buffer

# --- Streamlit App Layout ---
st.title("📄 Shree Balaji Interiors Quotation Generator")
st.markdown("Enter customer details and line items to generate the PDF quotation.")

# --- Session State for Dynamic Item Management ---
if 'items' not in st.session_state:
    # Initialize with one empty item
    st.session_state.items = [{'name': '', 'qty': 0, 'rate': 0}]

def add_item():
    """Adds a new empty row to the items list."""
    st.session_state.items.append({'name': '', 'qty': 0, 'rate': 0})

def remove_item(index):
    """Removes an item row by index."""
    if len(st.session_state.items) > 1:
        st.session_state.items.pop(index)

# --- User Input Section ---
user_name = st.text_input("Customer Name:", "Mr. Pavan kasat")

st.subheader("Item Details")

# Display and handle input for each item
total_cost = 0
for i, item in enumerate(st.session_state.items):
    col1, col2, col3, col4, col5 = st.columns([3, 1.5, 1.5, 2, 0.5])
    
    with col1:
        item['name'] = st.text_input(f"Description {i+1}", item['name'], key=f"name_{i}", label_visibility="collapsed")
    with col2:
        # Using number_input for quantity
        item['qty'] = st.number_input(f"Qty {i+1}", min_value=0.0, step=0.01, value=float(item.get('qty', 0)), key=f"qty_{i}", label_visibility="collapsed")
    with col3:
        # Using number_input for rate
        item['rate'] = st.number_input(f"Rate {i+1}", min_value=0.0, step=1.0, value=float(item.get('rate', 0)), key=f"rate_{i}", label_visibility="collapsed")
    
    amount = item['qty'] * item['rate']
    total_cost += amount
    
    with col4:
        st.markdown(f"**Amount:** ₹{amount:,.2f}")
    with col5:
        if st.session_state.items and len(st.session_state.items) > 1:
            st.button("❌", key=f"remove_{i}", on_click=remove_item, args=(i,))

# Add Row Button
st.button("➕ Add Item Row", on_click=add_item)

st.divider()

st.markdown(f"### Grand Total: ₹{total_cost:,.2f}")

# --- PDF Generation and Download ---
if st.button("Generate Quotation PDF"):
    # Filter out empty rows before generating the PDF
    valid_items = [item for item in st.session_state.items if item['name'] and (item['qty'] > 0 and item['rate'] > 0)]
    
    if not valid_items:
        st.error("Please add at least one valid item with a description, quantity, and rate.")
    else:
        # Use BytesIO to create the PDF in memory
        buffer = BytesIO()
        pdf_buffer = create_quotation_pdf(user_name, valid_items, buffer)
        
        st.success("PDF generated successfully!")
        
        # Streamlit download button
        st.download_button(
            label="⬇️ Download Quotation",
            data=pdf_buffer,
            file_name=f"Quotation_{user_name.replace(' ', '_')}_{date.today().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )


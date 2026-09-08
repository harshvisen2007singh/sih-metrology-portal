import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="Legal Metrology Verification Portal",
    page_icon="⚖️",
    layout="wide"
)

# Initialize Session State for Database Simulation
if 'certificates' not in st.session_state:
    st.session_state['certificates'] = []

if 'payments' not in st.session_state:
    st.session_state['payments'] = []

# Header Section
st.title("⚖️ Online Verification System for Weighing & Measuring Instruments")
st.caption("Department of Consumer Affairs (DoCA) | Legal Metrology Act, 2009")

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Issue Certificate (LMO)", 
    "🔍 Consumer Verification Portal", 
    "📊 Registry Dashboard",
    "💳 Fee Payment Gateway"
])

# ---------------------------------------------------------
# TAB 1: LMO CERTIFICATE ISSUANCE
# ---------------------------------------------------------
with tab1:
    st.header("Legal Metrology Officer (LMO) Portal")
    st.subheader("Issue New Stamping & Verification Certificate")
    
    with st.form("verification_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            trader_name = st.text_input("Business / Trader Name", placeholder="e.g., Apex Retail Solutions")
            trader_location = st.text_input("Location / District", placeholder="e.g., Central Delhi")
            instrument_type = st.selectbox("Instrument Category", [
                "Electronic Weighing Scale (Class III)",
                "Non-Automatic Weighing Instrument",
                "Fuel Dispenser Pump",
                "Flow Meter",
                "Capacity Measure / Container"
            ])
            serial_number = st.text_input("Instrument Serial / ID Number", placeholder="e.g., SN-987654321")

        with col2:
            lmo_name = st.text_input("Inspecting Officer Name (LMO)", placeholder="e.g., Officer R. Sharma")
            inspection_date = st.date_input("Inspection Date", value=datetime.today())
            validity_years = st.selectbox("Validity Period (Years)", [1, 2, 5], index=0)
            status = st.radio("Verification Result", ["APPROVED & STAMPED", "REJECTED / DEFECTIVE"], horizontal=True)

        submit_btn = st.form_submit_button("Generate Digital Certificate & QR Code")

    if submit_btn:
        if trader_name and serial_number and lmo_name:
            due_date = inspection_date + timedelta(days=validity_years * 365)
            cert_id = f"LMO-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            # Create Record Data
            record = {
                "Certificate ID": cert_id,
                "Trader Name": trader_name,
                "Location": trader_location,
                "Instrument": instrument_type,
                "Serial Number": serial_number,
                "LMO Name": lmo_name,
                "Inspection Date": str(inspection_date),
                "Next Verification Due": str(due_date),
                "Status": status
            }

            st.session_state['certificates'].append(record)
            st.success(f"Certificate {cert_id} generated successfully!")

            # Generate QR Code
            qr_data = f"CERTIFICATE VERIFIED\nID: {cert_id}\nTrader: {trader_name}\nInstrument: {instrument_type}\nSerial: {serial_number}\nStatus: {status}\nDue Date: {due_date}"
            qr = qrcode.QRCode(version=1, box_size=8, border=2)
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Save QR to Bytes
            buf = BytesIO()
            img.save(buf)
            byte_im = buf.getvalue()

            # Display Certificate Preview
            st.divider()
            st.subheader("Generated Digital Verification Certificate Preview")
            c1, c2 = st.columns([2, 1])
            with c1:
                st.write(f"**Certificate Number:** {cert_id}")
                st.write(f"**Trader / Business:** {trader_name} ({trader_location})")
                st.write(f"**Instrument Type:** {instrument_type}")
                st.write(f"**Serial Number:** {serial_number}")
                st.write(f"**Inspection Date:** {inspection_date} | **Next Due Date:** {due_date}")
                st.write(f"**Inspecting Officer:** {lmo_name}")
                if status == "APPROVED & STAMPED":
                    st.success(f"STATUS: {status}")
                else:
                    st.error(f"STATUS: {status}")
            with c2:
                st.image(byte_im, caption="Official Verification QR Code")

        else:
            st.error("Please fill in all mandatory fields before submitting.")

# ---------------------------------------------------------
# TAB 2: PUBLIC / CONSUMER VERIFICATION
# ---------------------------------------------------------
with tab2:
    st.header("Public & Consumer Verification Portal")
    st.write("Verify the legal accuracy and stamping status of any weighing or measuring instrument.")

    search_id = st.text_input("Enter Instrument Serial Number or Certificate ID:")
    
    if st.button("Search Registry"):
        found = False
        for cert in st.session_state['certificates']:
            if search_id.strip() in [cert['Certificate ID'], cert['Serial Number']]:
                found = True
                st.success("Record Found in Official Metrology Registry!")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.json(cert)
                with col_b:
                    if cert['Status'] == "APPROVED & STAMPED":
                        st.info("Status: VALID & LEGALLY STAMPED")
                    else:
                        st.error("Status: EXPIRED / REJECTED")
                break
        if not found:
            st.warning("No matching records found. Please check the Serial Number or Certificate ID.")

# ---------------------------------------------------------
# TAB 3: REGISTRY DASHBOARD
# ---------------------------------------------------------
with tab3:
    st.header("Central Legal Metrology Registry")
    if st.session_state['certificates']:
        df = pd.DataFrame(st.session_state['certificates'])
        st.dataframe(df, use_container_width=True)
        
        # Metrics summary
        total_stamped = len(df[df['Status'] == 'APPROVED & STAMPED'])
        total_rejected = len(df[df['Status'] == 'REJECTED / DEFECTIVE'])
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Inspections", len(df))
        m2.metric("Approved & Stamped", total_stamped)
        m3.metric("Rejected / Defective", total_rejected)
    else:
        st.info("No records present in the system yet. Issue certificates to view dashboard analytics.")

# ---------------------------------------------------------
# TAB 4: INSPECTION FEE PAYMENT GATEWAY (MOCK)
# ---------------------------------------------------------
with tab4:
    st.header("Legal Metrology Stamping & Inspection Fee Portal")
    st.info("Pay mandatory government verification fees online to receive verification stamping.")

    pay_col1, pay_col2 = st.columns(2)

    with pay_col1:
        st.subheader("Fee Breakdown")
        applicant_name = st.text_input("Trader / Business Name", placeholder="e.g., Apex Retail Solutions")
        cert_num = st.text_input("Application / Certificate Reference ID", placeholder="e.g., LMO-20260908")
        fee_type = st.selectbox("Verification Fee Category", [
            "Commercial Electronic Scale (₹500)",
            "Fuel Dispenser Inspection (₹2,000)",
            "Industrial Flow Meter (₹5,000)",
            "Annual Renewal Fee (₹1,000)"
        ])
        
        amounts = {
            "Commercial Electronic Scale (₹500)": 500,
            "Fuel Dispenser Inspection (₹2,000)": 2000,
            "Industrial Flow Meter (₹5,000)": 5000,
            "Annual Renewal Fee (₹1,000)": 1000
        }
        payable_amount = amounts[fee_type]
        st.markdown(f"### Total Payable Amount: **₹{payable_amount}**")

    with pay_col2:
        st.subheader("Payment Gateway")
        pay_method = st.radio("Select Payment Method", ["UPI / QR Code", "Debit / Credit Card", "Net Banking"])

        if pay_method == "UPI / QR Code":
            st.write("Scan QR using BHIM, Paytm, Google Pay, or PhonePe:")
            qr_pay_data = f"upi://pay?pa=gov.metrology@upi&pn=DoCA_Metrology&am={payable_amount}&cu=INR"
            
            p_qr = qrcode.QRCode(version=1, box_size=6, border=2)
            p_qr.add_data(qr_pay_data)
            p_qr.make(fit=True)
            p_img = p_qr.make_image(fill_color="black", back_color="white")
            
            p_buf = BytesIO()
            p_img.save(p_buf)
            st.image(p_buf.getvalue(), width=180)

        elif pay_method in ["Debit / Credit Card", "Net Banking"]:
            st.text_input("Card Holder / Account Name", placeholder="Name as per Bank")
            st.text_input("Card / Account Number", type="password", placeholder="XXXX XXXX XXXX XXXX")

        if st.button("💳 Complete Fee Payment"):
            if applicant_name and cert_num:
                txn_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}"
                st.session_state['payments'].append({
                    "Transaction ID": txn_id,
                    "Trader Name": applicant_name,
                    "Reference ID": cert_num,
                    "Amount": f"₹{payable_amount}",
                    "Status": "SUCCESSFUL"
                })
                st.balloons()
                st.success(f"✅ Payment Successful! Transaction ID: **{txn_id}**")
                st.json({
                    "Transaction ID": txn_id,
                    "Amount Paid": f"₹{payable_amount}",
                    "Payer": applicant_name,
                    "Status": "PAID & VERIFIED"
                })
            else:
                st.error("Please enter Trader Name and Reference ID before making payment.")
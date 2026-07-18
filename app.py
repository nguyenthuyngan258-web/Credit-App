import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Cấu hình trang
st.set_page_config(page_title="Credit Score Pro", layout="wide")

# CSS tạo giao diện bo góc & chuyên nghiệp
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stMetric {background-color: white; padding: 20px; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);}
    h1 {color: #2c3e50;}
    </style>
""", unsafe_allow_html=True)

st.title("🏦 Credit Analyzer Pro")
st.markdown("---")

# Sidebar - Thông tin đầu vào
with st.sidebar:
    st.header("⚙️ Cấu hình thẩm định")
    thu_nhap = st.number_input("Thu nhập hàng tháng (VNĐ)", 0, 1000000000, 20000000)
    nguoi_phu_thuoc = st.number_input("Số người phụ thuộc", 0, 10, 0)
    chi_phi_sinh_hoat = thu_nhap * (0.3 + 0.1 * nguoi_phu_thuoc) # Giả định chi phí
    st.info(f"Chi phí sinh hoạt ước tính: {chi_phi_sinh_hoat:,.0f} VNĐ")

# Layout chính
col1, col2 = st.columns(2)
with col1:
    st.subheader("Thông tin Khoản vay")
    so_tien_vay = st.number_input("Số tiền vay (VNĐ)", 0, 10000000000, 500000000)
    thoi_han = st.slider("Thời gian vay (tháng)", 6, 360, 60)
    lai_suat = st.number_input("Lãi suất (%/năm)", 0.0, 30.0, 10.0)
    
with col2:
    st.subheader("Tài sản & Tín dụng")
    gia_tri_tsdb = st.number_input("Giá trị TSĐB (VNĐ)", 0, 10000000000, 1000000000)
    du_no_cu = st.number_input("Dư nợ khoản vay cũ (VNĐ)", 0)
    cic_score = st.select_slider("Điểm tín dụng (CIC)", options=["Xấu", "Trung bình", "Khá", "Tốt"])

# Logic tính toán
goc_lai_thang = (so_tien_vay / thoi_han) + (so_tien_vay * (lai_suat/100/12))
dti = ((du_no_cu + goc_lai_thang) / (thu_nhap + 1)) * 100
ltv = (so_tien_vay / (gia_tri_tsdb + 1)) * 100

# Hiển thị kết quả
if st.button("📊 PHÂN TÍCH HỒ SƠ", use_container_width=True):
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Chỉ số DTI", f"{dti:.2f}%")
    col_m2.metric("Chỉ số LTV", f"{ltv:.2f}%")
    col_m3.metric("Kết quả", "ĐẠT" if dti < 40 and ltv < 80 else "RỦI RO")
    
    # Biểu đồ Plotly
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = dti,
        title = {'text': "DTI Risk Level"},
        gauge = {'axis': {'range': [0, 100]},
                 'bar': {'color': "darkblue"},
                 'steps' : [{'range': [0, 40], 'color': "lightgreen"},
                            {'range': [40, 70], 'color': "orange"}]}))
    st.plotly_chart(fig, use_container_width=True)
    
    if dti < 40:
        st.success("Hồ sơ đáp ứng tiêu chuẩn. Tiến hành lập tờ trình vay.")
    else:
        st.error("Hồ sơ không đạt tiêu chuẩn. Cần bổ sung TSĐB hoặc giảm số tiền vay.")

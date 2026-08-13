import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# =========================================================================
# 1. NGÂN HÀNG CÂU HỎI GỐC CỐ ĐỊNH (Khởi tạo danh sách câu hỏi mẫu ban đầu)
# =========================================================================
if 'questions_db' not in st.session_state:
    st.session_state.questions_db = [
        {
            "CauHoi": "Xử lý đối tượng có nợ 5 hóa đơn (không thể ghi hóa đơn cho tội phạm) Trường hợp nào?",
            "A": "Ra báo TTC, tố cáo tội phạm không chịu thanh toán",
            "B": "Bỏ qua hóa đơn và tiếp tục xử lý",
            "C": "Phạt tù thêm thời gian quy định",
            "DapAnDung": "Ra báo TTC, tố cáo tội phạm không chịu thanh toán",
            "GiaiThich": "Theo luật định, đối tượng nợ 5 hóa đơn cần được xử lý thông qua báo cáo TTC.",
            "PhanLoai": "Mục thi & Ôn tập"
        },
        {
            "CauHoi": "Số người tối thiểu có thể trấn áp 02 PD đang cầm súng là bao nhiêu?",
            "A": "6",
            "B": "4",
            "C": "2",
            "DapAnDung": "6",
            "GiaiThich": "Quy tắc an toàn vũ lực yêu cầu số lượng áp đảo tối thiểu là 6 người chống lại 2 người có súng.",
            "PhanLoai": "Mục thi & Ôn tập"
        },
        {
            "CauHoi": "Số người tối thiểu có thể trấn áp 02 PD không có súng là bao nhiêu?",
            "A": "4",
            "B": "2",
            "C": "6",
            "DapAnDung": "4",
            "GiaiThich": "Khi đối phương không có súng, số lượng tối thiểu được giảm xuống còn 4 người.",
            "PhanLoai": "Mục thi & Ôn tập"
        },
        {
            "CauHoi": "Mức độ ưu tiên nhận Dispatch",
            "A": "Buôn Lậu Tranh",
            "B": "Cướp cửa hàng tiện lợi",
            "C": "Trộm cắp xe máy",
            "DapAnDung": "Buôn Lậu Tranh",
            "GiaiThich": "Buôn lậu tranh thuộc danh mục tội phạm nghiêm trọng cấp độ cao cần ưu tiên dispatch.",
            "PhanLoai": "Mục thi & Ôn tập"
        }
    ]

# Khởi tạo cơ sở dữ liệu tài khoản và các trạng thái hệ thống
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"pass": "admin123", "role": "Quản trị viên", "can_exam": True},
        "GIANGVIEN": {"pass": "123456", "role": "Giảng viên", "can_exam": True},
        "S-01": {"pass": "123456", "role": "Học viên", "can_exam": False}
    }

if 'exam_results' not in st.session_state: st.session_state.exam_results = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = ""
if 'user_role' not in st.session_state: st.session_state.user_role = ""
if 'exam_submitted' not in st.session_state: st.session_state.exam_submitted = False

if 'current_q_index' not in st.session_state: st.session_state.current_q_index = 0
if 'user_exam_answers' not in st.session_state: st.session_state.user_exam_answers = {}
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'shuffled_exam_qs' not in st.session_state: st.session_state.shuffled_exam_qs = []

# =========================================================================
# GIAO DIỆN & STYLE CSS
# =========================================================================
st.set_page_config(page_title="FTO WEPD - Hệ Thống Sát Hạch Lý Thuyết", page_icon="🚓", layout="wide")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .banner-container {
        background: linear-gradient(135deg, #07162c 0%, #1b355a 100%);
        border-radius: 12px; padding: 25px; text-align: center; color: white;
        border: 2px solid #324d77; margin-bottom: 20px;
    }
    .banner-title { font-size: 42px; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; font-family: sans-serif; }
    .banner-subtitle { font-size: 15px; color: #a0aec0; letter-spacing: 3px; }
    .user-info-bar { background-color: #051329; border-radius: 8px; padding: 12px 20px; margin-bottom: 25px; border-left: 5px solid #ffcc00; color: white;}
    .login-box { background-color: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.08); width: 450px; margin: 50px auto; text-align: center; }
    .login-header { background-color: #0b1e36; color: white; padding: 30px 20px; border-radius: 10px 10px 0 0; margin: -40px -40px 30px -40px; }
    .logo-circle { background-color: #ffcc00; color: #0b1e36; width: 60px; height: 60px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 18px; margin: 0 auto 15px auto; }
    .timer-text { font-size: 24px; font-weight: bold; color: #ef4444; text-align: center; background-color: #fee2e2; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
    .explain-box { background-color: #fffbeb; border-left: 5px solid #d97706; padding: 12px; margin-top: 5px; border-radius: 4px; color: #92400e; font-size: 14px; }
    
    /* Thiết kế nút bấm Lưu Câu Hỏi màu xanh thẫm chữ trắng */
    .stButton > button {
        background-color: #0c2340 !important;
        color: white !important;
        font-weight: bold !important;
        padding: 10px 24px !important;
        border-radius: 6px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- MÀN HÌNH ĐĂNG NHẬP ---
if not st.session_state.logged_in:
    st.markdown("""
        <div class="login-box">
            <div class="login-header">
                <div class="logo-circle">WPD</div>
                <div class="title-main" style="font-weight:bold; font-size:16px;">WESTSIDE POLICE DEPARTMENT</div>
                <div class="title-sub" style="font-size:11px; color:#a0aec0;">Hệ Thống Quản Lý & Sát Hạch</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col2:
        input_user = st.text_input("TÊN ĐĂNG NHẬP / SỐ PHÙ HIỆU", placeholder="Nhập tài khoản")
        input_pass = st.text_input("MÃ BẢO MẬT", type="password", placeholder="Nhập mật khẩu")
        
        if st.button("ĐĂNG NHẬP HỆ THỐNG", use_container_width=True):
            if input_user in st.session_state.users_db and st.session_state.users_db[input_user]["pass"] == input_pass:
                st.session_state.logged_in = True
                st.session_state.username = input_user
                st.session_state.user_role = st.session_state.users_db[input_user]["role"]
                st.session_state.exam_submitted = False
                st.session_state.shuffled_exam_qs = []
                st.rerun()
            else: st.error("⚠️ Tài khoản hoặc mã bảo mật không chính xác!")

# --- MÀN HÌNH CHÍNH ---
else:
    st.markdown(f"""
        <div class="banner-container"><div class="banner-title">FTO WEPD</div><div class="banner-subtitle">WESTSIDE POLICE DEPARTMENT - HỆ THỐNG SÁT HẠCH</div></div>
    """, unsafe_allow_html=True)

    info_col, btn_col = st.columns(2)
    with info_col:
        st.markdown(f"<div class='user-info-bar'>👤 Tài khoản: <b>{st.session_state.username}</b> | Chức vụ: <span style='color:#3b82f6;'><b>{st.session_state.user_role}</b></span></div>", unsafe_allow_html=True)
    with btn_col:
        st.write("<style>div.stButton > button {background-color:#ef4444 !important; color:white !important; margin-top:5px;}</style>", unsafe_allow_html=True)
        if st.button("ĐĂNG XUẤT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.exam_submitted = False
            st.session_state.shuffled_exam_qs = []
            st.rerun()

    # --- LUỒNG QUẢN LÝ (ADMIN / GIẢNG VIÊN) ---
    if st.session_state.user_role in ["Quản trị viên", "Giảng viên"]:
        tab_users, tab_edit_matrix, tab_results = st.tabs([
            "👥 QUẢN LÝ THÀNH VIÊN", 
            "⚙️ NGÂN HÀNG CÂU HỎI TRẮC NGHIỆM", 
            "📊 THỐNG KÊ ĐIỂM SỐ"
        ])
        
        with tab_users:
            st.markdown("### ➕ Thêm Tài Khoản Mới")
            c1, c2, c3 = st.columns(3)
            with c1: new_u = st.text_input("Username mới:", key="add_u")
            with c2: new_p = st.text_input("Mật khẩu:", type="password", key="add_p")
            with c3: new_r = st.selectbox("Chức vụ:", ["Học viên", "Giảng viên"], key="add_r")
            if st.button("Xác nhận thêm người dùng", type="primary"):
                if new_u and new_p:
                    st.session_state.users_db[new_u] = {"pass": new_p, "role": new_r, "can_exam": False}
                    st.success(f"Đã thêm tài khoản: {new_u}")
                    st.rerun()
            st.divider()
            for user, data in st.session_state.users_db.items():
                if data["role"] == "Học viên":
                    col_u, col_status = st.columns(2)
                    with col_u: st.write(f"• **{user}** (Mật khẩu: {data['pass']})")
                    with col_status:
                        current_status = st.checkbox("Cho phép thi", value=data["can_exam"], key=f"perm_{user}")
                        if current_status != data["can_exam"]:
                            st.session_state.users_db[user]["can_exam"] = current_status
                            st.toast(f"Đã cập nhật quyền thi cho {user}!")
        
        # --- ĐÃ THÊM: GIAO DIỆN BẢNG CHỈNH SỬA EXCEL CHUYÊN NGHIỆP Y HỆT TRONG ẢNH ---
        with tab_edit_matrix:
            st.markdown("### ⚙️ BẢNG QUẢN TRỊ NGÂN HÀNG ĐỀ THI")
            st.caption("💡 Hướng dẫn: Nhấp đúp chuột vào bất kỳ ô nào để chỉnh sửa trực tiếp. Để THÊM câu hỏi mới, hãy cuộn xuống dòng dưới cùng của bảng để nhập.")
            
            # Chuyển đổi danh sách câu hỏi hiện tại thành dạng DataFrame bảng tính
            df_questions = pd.DataFrame(st.session_state.questions_db)

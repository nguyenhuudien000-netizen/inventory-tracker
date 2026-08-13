import streamlit as st
import pandas as pd
import time
import random

# =========================================================================
# 1. KHỞI TẠO CƠ SỞ DỮ LIỆU BỘ NHỚ
# =========================================================================
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"pass": "admin123", "role": "Quản trị viên", "can_exam": True},
        "GIANGVIEN": {"pass": "123456", "role": "Giảng viên", "can_exam": True},
        "S-01": {"pass": "123456", "role": "Học viên", "can_exam": False},
        "HocVien02": {"pass": "123456", "role": "Học viên", "can_exam": False}
    }

if 'questions_db' not in st.session_state:
    st.session_state.questions_db = [
        {
            "id": 1,
            "question": "Khi gặp tín hiệu đèn vàng nhấp nháy, bạn phải xử lý như thế nào?",
            "options": ["Dừng lại trước vạch dừng.", "Đi tiếp nhưng giảm tốc độ, chú ý quan sát.", "Tăng tốc vượt qua."],
            "answer": "Đi tiếp nhưng giảm tốc độ, chú ý quan sát.",
            "explain": "Theo luật giao thông đường bộ WEPD, đèn vàng nhấp nháy báo hiệu được đi nhưng phải giảm tốc độ và chú ý quan sát an toàn.",
            "type": "Mục thi & Ôn tập"
        }
    ]

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
st.set_page_config(page_title="FTO WEPD - Hệ Thống Quản Lý Sát Hạch", page_icon="🚓", layout="wide")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .banner-container {
        background: linear-gradient(135deg, #07162c 0%, #1b355a 100%);
        border-radius: 12px; padding: 25px; text-align: center; color: white;
        border: 2px solid #324d77; margin-bottom: 20px;
    }
    .banner-title { font-size: 48px; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; font-family: sans-serif; }
    .banner-subtitle { font-size: 16px; color: #a0aec0; letter-spacing: 3px; }
    .user-info-bar { background-color: #051329; border-radius: 8px; padding: 12px 20px; margin-bottom: 25px; border-left: 5px solid #ffcc00; color: white;}
    .login-box { background-color: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.08); width: 450px; margin: 50px auto; text-align: center; }
    .login-header { background-color: #0b1e36; color: white; padding: 30px 20px; border-radius: 10px 10px 0 0; margin: -40px -40px 30px -40px; }
    .logo-circle { background-color: #ffcc00; color: #0b1e36; width: 60px; height: 60px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 18px; margin: 0 auto 15px auto; }
    .timer-text { font-size: 24px; font-weight: bold; color: #ef4444; text-align: center; background-color: #fee2e2; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
    .explain-box { background-color: #fffbeb; border-left: 5px solid #d97706; padding: 12px; margin-top: 5px; border-radius: 4px; color: #92400e; font-size: 14px; }
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
... (Còn74 dòng dòng)

message.txt
11 KB

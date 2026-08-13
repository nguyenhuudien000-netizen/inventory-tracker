import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# =========================================================================
# 1. KHỞI TẠO CƠ SỞ DỮ LIỆU BAN ĐẦU TRONG BỘ NHỚ HỆ THỐNG
# =========================================================================
if 'announcements_db' not in st.session_state:
    st.session_state.announcements_db = [
        {"Ngay": "05/03/2026", "TieuDe": "Tranh thủ thời gian học", "NoiDung": "Khi không có giảng viên, các Sĩ quan vui lòng tự học trên web nha."},
        {"Ngay": "02/08/2026", "TieuDe": "MDT và F1", "NoiDung": "Hiện tại bảng MDT và F1 đã thay đổi giáo trình đã được cập nhật. Chúc các học viên thi tốt điểm tốt. Thân!"},
        {"Ngay": "24/07/2026", "TieuDe": "Giấy phép cư dân", "NoiDung": "CCCD đang bị lỗi nên học viên yêu cầu cư dân xuất trình nếu không có thì không phạt. GPLX và giấy tờ xe không bị lỗi học viên yêu cầu cư dân xuất trình."}
    ]

# Gá sẵn một số câu hỏi mẫu thực tế. Bạn có thể thêm vào đây hoặc gõ thêm trên giao diện web không giới hạn số lượng.
if 'questions_db' not in st.session_state:
    st.session_state.questions_db = [
        {"CauHoi": "Xử lý đối tượng có nợ 5 hóa đơn (không thể ghi hóa đơn cho tội phạm) Trường hợp nào?", "A": "Ra báo TTC, tố cáo tội phạm không chịu thanh toán", "B": "Bỏ qua hóa đơn và tiếp tục xử lý", "C": "Phạt tù thêm thời gian quy định", "DapAnDung": "Ra báo TTC, tố cáo tội phạm không chịu thanh toán", "GiaiThich": "Theo luật định, đối tượng nợ 5 hóa đơn cần được xử lý thông qua báo cáo TTC.", "PhanLoai": "Mục thi & Ôn tập"},
        {"CauHoi": "Số người tối thiểu có thể trấn áp 02 PD đang cầm súng là bao nhiêu?", "A": "6", "B": "4", "C": "2", "DapAnDung": "6", "GiaiThich": "Quy tắc an toàn vũ lực yêu cầu số lượng áp đảo tối thiểu là 6 người chống lại 2 người có súng.", "PhanLoai": "Mục thi & Ôn tập"},
        {"CauHoi": "Số người tối thiểu có thể trấn áp 02 PD không có súng là bao nhiêu?", "A": "4", "B": "2", "C": "6", "DapAnDung": "4", "GiaiThich": "Khi đối phương không có súng, số lượng tối thiểu được giảm xuống còn 4 người.", "PhanLoai": "Mục thi & Ôn tập"},
        {"CauHoi": "Mức độ ưu tiên nhận Dispatch", "A": "Buôn Lậu Tranh", "B": "Cướp cửa hàng tiện lợi", "C": "Trộm cắp xe máy", "DapAnDung": "Buôn Lậu Tranh", "GiaiThich": "Buôn lậu tranh thuộc danh mục tội phạm nghiêm trọng cấp độ cao cần ưu tiên dispatch.", "PhanLoai": "Mục thi & Ôn tập"}
    ]

if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"pass": "admin123", "role": "Quản trị viên", "can_exam": True},
        "GIANGVIEN": {"pass": "123456", "role": "Giảng viên", "can_exam": True},
        "2229": {"pass": "123456", "role": "Học viên", "can_exam": True},
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
# GIAO DIỆN VÀ STYLE CSS ĐỒ HỌA
# =========================================================================
st.set_page_config(page_title="FTO WEPD - Hệ Thống Sát Hạch", page_icon="🚓", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .login-wrapper { max-width: 480px; margin: 40px auto; }
    .banner-graphic {
        background: linear-gradient(180deg, #0e1e38 0%, #050d1a 100%);
        border: 3px solid #1a2e4c; border-radius: 12px; padding: 25px 20px; text-align: center; color: white; box-shadow: 0px 8px 24px rgba(0,0,0,0.4); margin-bottom: 20px;
    }
    .banner-title-wpd { font-size: 46px; font-weight: 900; letter-spacing: 2px; color: #ffffff; font-family: 'Impact', 'Arial Black', sans-serif; margin-bottom: 2px; }
    .banner-sub-wpd { font-size: 13px; color: #cfd8dc; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 12px; }
    .banner-tag-wpd { font-size: 22px; font-weight: bold; color: #ffcc00; letter-spacing: 3px; border-top: 1px solid #1a2e4c; padding-top: 8px; }
    .user-info-bar-custom { background-color: #06152b; border: 1px solid #14283f; border-radius: 6px; padding: 10px 15px; margin-bottom: 20px; }
    .noti-flat-card { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 15px; margin-bottom: 12px; box-shadow: 0px 2px 4px rgba(0,0,0,0.02); }
    .noti-flat-header { font-size: 14px; font-weight: bold; color: #1e3a8a; margin-bottom: 5px; }
    .noti-flat-body { font-size: 13px; color: #334155; line-height: 1.6; }
    .timer-text { font-size: 24px; font-weight: bold; color: #ef4444; text-align: center; background-color: #fee2e2; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
    .explain-box { background-color: #fffbeb; border-left: 5px solid #d97706; padding: 12px; margin-top: 5px; border-radius: 4px; color: #92400e; font-size: 14px; }
    .score-card-custom { background-color: #ffffff; border-left: 5px solid #3b82f6; padding: 15px; border-radius: 6px; margin-bottom: 10px; box-shadow: 0px 2px 8px rgba(0,0,0,0.05); }
    div.stButton > button { background-color: #0b1e36 !important; color: white !important; font-weight: bold !important; border-radius: 4px !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- MÀN HÌNH ĐĂNG NHẬP CHÍNH ---
if not st.session_state.logged_in:
    st.markdown("""
        <div class="login-wrapper">
            <div class="banner-graphic">
                <div class="banner-title-wpd">FTO WEPD</div>
                <div class="banner-sub-wpd">WESTSIDE POLICE DEPARTMENT</div>
                <div class="banner-tag-wpd">HỌC VÀ THI TRẮC NGHIỆM</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l2:
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
            else: st.error("⚠️ Tài khoản hoặc mã bảo mật không đúng!")

# --- MÀN HÌNH CHÍNH BIÊN CHẾ ---
else:
    st.markdown("""
        <div class="banner-graphic">
            <div class="banner-title-wpd">FTO WEPD</div>
            <div class="banner-sub-wpd">WESTSIDE POLICE DEPARTMENT - HỆ THỐNG SÁT HẠCH</div>
        </div>
    """, unsafe_allow_html=True)

    info_col, btn_col = st.columns(2)
    with info_col:
        st.info(f"👤 Tài khoản: {st.session_state.username} | Chức vụ: {st.session_state.user_role}")
    with btn_col:
        if st.button("🔴 ĐĂNG XUẤT HỆ THỐNG", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.exam_submitted = False
            st.session_state.shuffled_exam_qs = []
            st.rerun()

    # --- LUỒNG QUẢN LÝ (Admin / Giảng viên) ---
    if st.session_state.user_role in ["Quản trị viên", "Giảng viên"]:
        tab_users, tab_edit_forms, tab_results, tab_news_manage = st.tabs([
            "👥 QUẢN LÝ THÀNH VIÊN", 
            "⚙️ NGÂN HÀNG CÂU HỎI TRẮC NGHIỆM", 
            "📊 THỐNG KÊ ĐIỂM SỐ",
            "📋 QUẢN LÝ THÔNG BÁO"
        ])
        
        with tab_users:
            st.markdown("### ➕ Thêm Tài Khoản Người Dùng Mới")
            c1, c2 = st.columns(2)
            with c1: add_u = st.text_input("Tên tài khoản mới:", key="reg_u")
            with c2: add_p = st.text_input("Mật khẩu bảo mật:", type="password", key="reg_p")
            if st.button("➕ Xác nhận thêm người dùng", use_container_width=True):
                if add_u and add_p:
                    st.session_state.users_db[add_u] = {"pass": add_p, "role": "Học viên", "can_exam": False}
                    st.success(f"Đã thêm thành công học viên: {add_u}")
                    st.rerun()
            st.divider()
            st.markdown("### 🔐 Danh Sách Thí Sinh & Công Tắc Bật Quyền Thi")
            for user, data in st.session_state.users_db.items():
                if data["role"] == "Học viên":
                    col_u, col_chk = st.columns(2)
                    with col_u: st.write(f"• **{user}** (Mật khẩu: `{data['pass']}`)")
                    with col_chk:
                        status = st.checkbox("Cấp quyền thi chính thức", value=data["can_exam"], key=f"p_check_{user}")
                        if status != data["can_exam"]:
                            st.session_state.users_db[user]["can_exam"] = status
                            st.toast(f"Đã cập nhật quyền thi cho {user}!")

        with tab_edit_forms:
            st.markdown("### 📝 Soạn Thảo Câu Hỏi Trắc Nghiệm Mới (Không giới hạn số lượng)")

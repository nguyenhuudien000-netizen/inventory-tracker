import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# =========================================================================
# 1. KHỞI TẠO CƠ SỞ DỮ LIỆU BAN ĐẦU (Nếu chưa có trong bộ nhớ tạm)
# =========================================================================
# Ngân hàng thông báo trang chủ mặc định (Dạng bảng chỉnh sửa trực tiếp)
if 'announcements_db' not in st.session_state:
    st.session_state.announcements_db = [
        {
            "Ngay": "05/03/2026",
            "TieuDe": "Tranh thủ thời gian học",
            "NoiDung": "Khi không có giảng viên, các Sĩ quan vui lòng tự học trên web nha."
        },
        {
            "Ngay": "02/08/2026",
            "TieuDe": "MDT và F1",
            "NoiDung": "Hiện tại bảng MDT và F1 đã thay đổi giáo trình đã được cập nhật. Chúc các học viên thi tốt điểm tốt. Thân!"
        },
        {
            "Ngay": "24/07/2026",
            "TieuDe": "Giấy phép cư dân",
            "NoiDung": "CCCD đang bị lỗi nên học viên yêu cầu cư dân xuất trình nếu không có thì không phạt. GPLX và giấy tờ xe không bị lỗi học viên yêu cầu cư dân xuất trình."
        }
    ]

# Ngân hàng câu hỏi trắc nghiệm dạng ma trận bảng tính
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
        }
    ]

# Cơ sở dữ liệu tài khoản người dùng và phân quyền cho thi
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"pass": "admin123", "role": "Quản trị viên", "can_exam": True},
        "GIANGVIEN": {"pass": "123456", "role": "Giảng viên", "can_exam": True},
        "S-01": {"pass": "123456", "role": "Học viên", "can_exam": False},
        "HocVien02": {"pass": "123456", "role": "Học viên", "can_exam": False}
    }

# Các biến trạng thái vận hành hệ thống bài thi và kết quả
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
# GIAO DIỆN & STYLE CSS ĐỒ HỌA THỰC TẾ TRONG ẢNH
# =========================================================================
st.set_page_config(page_title="FTO GCPD - Học Và Thi Trắc Nghiệm", page_icon="🚓", layout="centered")

st.markdown("""
    <style>
    /* Ẩn các thành phần thừa mặc định */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Canh giữa hộp đăng nhập ngoài màn hình chính */
    .login-wrapper {
        max-width: 480px;
        margin: 40px auto;
    }
    
    /* Thiết kế thanh Banner đồ họa thẫm chứa Text */
    .banner-graphic {
        background: linear-gradient(180deg, #0e1e38 0%, #050d1a 100%);
        border: 3px solid #1a2e4c;
        border-radius: 12px;
        padding: 25px 20px;
        text-align: center;
        color: white;
        box-shadow: 0px 8px 24px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }
    .banner-title-wpd {
        font-size: 46px;
        font-weight: 900;
        letter-spacing: 2px;
        color: #ffffff;
        font-family: 'Impact', 'Arial Black', sans-serif;
        margin-bottom: 2px;
    }
    .banner-sub-wpd {
        font-size: 13px;
        color: #cfd8dc;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .banner-tag-wpd {
        font-size: 22px;
        font-weight: bold;
        color: #ffcc00;
        letter-spacing: 3px;
        border-top: 1px solid #1a2e4c;
        padding-top: 8px;
    }

    /* Thanh thông tin người dùng màu xanh đen chuẩn trong ảnh */
    .user-info-bar-custom {
        background-color: #06152b;
        border: 1px solid #14283f;
        border-radius: 6px;
        padding: 10px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .user-badge-flex {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .logo-circle-gold {
        background-color: #ffcc00;
        color: #06152b;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        font-size: 11px;
    }
    .user-text-meta {
        font-family: sans-serif;
        color: white;
    }
    .user-system-title {
        font-size: 12px;
        font-weight: bold;
        color: #ffcc00;
        letter-spacing: 0.5px;
    }
    .user-login-name {
        font-size: 13px;
        color: #ffffff;
    }

    /* Định dạng hộp thông báo tĩnh dạng thẻ phẳng ở trang chủ */
    .noti-flat-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.02);
    }
    .noti-flat-header {
        font-size: 14px;
        font-weight: bold;
        color: #1e3a8a;
        margin-bottom: 5px;
    }
    .noti-flat-body {
        font-size: 13px;
        color: #334155;
        line-height: 1.5;
    }

    /* Đồng hồ đếm ngược bài thi */
    .timer-text-custom {
        font-size: 20px;
        font-weight: bold;
        color: #ef4444;
        text-align: center;
        background-color: #fee2e2;
        padding: 8px;
        border-radius: 6px;
        margin-bottom: 15px;
    }

    /* Tùy chỉnh màu sắc nút Lưu hệ thống màu xanh navy thẫm chữ trắng */
    div.stButton > button {
        background-color: #0b1e36 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 4px !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- MÀN HÌNH ĐĂNG NHẬP CHÍNH ---
if not st.session_state.logged_in:
    st.markdown("""
        <div class="login-wrapper">
            <div class="banner-graphic">
                <div class="banner-title-wpd">FTO GCPD</div>
                <div class="banner-sub-wpd">GACHA CITY POLICE DEPARTMENT</div>
                <div class="banner-tag-wpd">HỌC VÀ THI TRẮC NGHIỆM</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 4, 1])
    with col_l2:
        input_user = st.text_input("TÊN ĐĂNG NHẬP / SỐ PHÙ HIỆU", placeholder="Nhập tài khoản (Ví dụ: GIANGVIEN)")
        input_pass = st.text_input("MÃ BẢO MẬT", type="password", placeholder="Nhập mật khẩu")
        
        if st.button("ĐĂNG NHẬP HỆ THỐNG", use_container_width=True):
            if input_user in st.session_state.users_db and st.session_state.users_db[input_user]["pass"] == input_pass:
                st.session_state.logged_in = True
                st.session_state.username = input_user
                st.session_state.user_role = st.session_state.users_db[input_user]["role"]
                st.session_state.exam_submitted = False
                st.session_state.shuffled_exam_qs = []
                st.rerun()
            else:
                st.error("⚠️ Tài khoản hoặc mã bảo mật không chính xác!")

# --- MÀN HÌNH CHÍNH SAU KHI ĐĂNG NHẬP (GIAO DIỆN 5 TAB ĐẦY ĐỦ) ---
else:
    # Khối đồ họa Banner trên đỉnh trang
    st.markdown("""
        <div class="banner-graphic">
            <div class="banner-title-wpd">FTO GCPD</div>
            <div class="banner-subtitle" style="font-size:14px; color:#a0aec0; letter-spacing:2px; text-transform:uppercase; margin-bottom:10px;">GACHA CITY POLICE DEPARTMENT</div>
            <div class="banner-tag-wpd">HỌC VÀ THI TRẮC NGHIỆM</div>
        </div>
    """, unsafe_allow_html=True)

    # Thanh thông tin người dùng kết hợp nút Đăng xuất nằm ngang
    info_col, btn_col = st.columns([4, 1])
    with info_col:
        st.markdown(f"""
            <div class="user-info-bar">
                <div class="user-badge-flex">
                    <div class="logo-circle-gold">FTO</div>
                    <div class="user-text-meta">
                        <div class="user-system-title">GCPD - THÔNG TIN</div>
                        <div class="user-login-name">👤 {st.session_state.username} | {st.session_state.user_role}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with btn_col:
        # Nút Đăng xuất màu đỏ cam thẫm

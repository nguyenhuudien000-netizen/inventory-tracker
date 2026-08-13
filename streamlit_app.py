import streamlit as st
import pandas as pd

# =========================================================================
# CẤU HÌNH HỆ THỐNG BAN ĐẦU
# =========================================================================
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": "admin123",
        "GIANGVIEN": "123456",
        "S-01": "123456"
    }

# Khởi tạo trạng thái đăng nhập nếu chưa có
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = ""

# =========================================================================
# CẤU HÌNH TRANG & CSS TÙY BIẾN GIAO DIỆN
# =========================================================================
st.set_page_config(page_title="FTO WEPD - Hệ Thống Sát Hạch", page_icon="🚓", layout="wide")

st.markdown("""
    <style>
    /* Ẩn các thành phần thừa mặc định */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Thiết kế Banner lớn phía trên cùng */
    .banner-container {
        background: linear-gradient(135deg, #07162c 0%, #1b355a 100%);
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        color: white;
        border: 2px solid #324d77;
        margin-bottom: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    .banner-title {
        font-size: 56px;
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 0px;
        font-family: 'Arial Black', Gadget, sans-serif;
    }
    .banner-subtitle {
        font-size: 18px;
        color: #a0aec0;
        letter-spacing: 3px;
        margin-bottom: 10px;
    }
    .banner-tag {
        font-size: 28px;
        font-weight: bold;
        color: #ffffff;
        letter-spacing: 1px;
    }

    /* Thanh thông tin người dùng màu xanh đen */
    .user-info-bar {
        background-color: #051329;
        border-radius: 8px;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        border-left: 5px solid #ffcc00;
    }
    .user-badge {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .logo-circle-small {
        background-color: #ffcc00;
        color: #0b1e36;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        font-size: 13px;
    }
    .user-text {
        color: white;
        font-family: sans-serif;
    }
    .user-name-title {
        font-size: 15px;
        font-weight: bold;
        letter-spacing: 0.5px;
    }
    .user-role {
        font-size: 13px;
        color: #3b82f6;
        font-weight: bold;
    }

    /* Thiết kế các hộp thông báo */
    .noti-box {
        background-color: #eef6ff;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 5px solid #3b82f6;
        font-family: sans-serif;
    }
    .noti-date-title {
        font-size: 15px;
        font-weight: bold;
        color: #1e3a8a;
        margin-bottom: 8px;
    }
    .noti-content {
        font-size: 14px;
        color: #334155;
        line-height: 1.6;
    }

    /* Định dạng form đăng nhập */
    .login-box { 
        background-color: #ffffff; 
        padding: 40px; 
        border-radius: 12px; 
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.08); 
        width: 450px; 
        margin: 50px auto;
        text-align: center; 
    }
    .login-header { background-color: #0b1e36; color: white; padding: 30px 20px; border-radius: 10px 10px 0 0; margin: -40px -40px 30px -40px; }
    .logo-circle { background-color: #ffcc00; color: #0b1e36; width: 60px; height: 60px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 18px; margin: 0 auto 15px auto; }
    </style>
""", unsafe_allow_html=True)

# --- 1. MÀN HÌNH ĐĂNG NHẬP ---
if not st.session_state.logged_in:
    st.markdown("""
        <div class="login-box">
            <div class="login-header">
                <div class="logo-circle">WPD</div>
                <div class="title-main" style="font-weight:bold; font-size:16px;">WESTSIDE POLICE DEPARTMENT</div>
                <div class="title-sub" style="font-size:11px; color:#a0aec0;">Hệ Thống Đăng Nhập Sát Hạch</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        input_user = st.text_input("TÊN ĐĂNG NHẬP / SỐ PHÙ HIỆU", placeholder="Nhập tài khoản (Ví dụ: GIANGVIEN)")
        input_pass = st.text_input("MÃ BẢO MẬT", type="password", placeholder="Nhập mật khẩu")
        
        if st.button("ĐĂNG NHẬP HỆ THỐNG", use_container_width=True):
            if input_user in st.session_state.users_db and st.session_state.users_db[input_user] == input_pass:
                st.session_state.logged_in = True
                st.session_state.username = input_user
                st.rerun()
            else:
                st.error("⚠️ Tài khoản hoặc mã bảo mật không chính xác!")

# --- 2. GIAO DIỆN CHÍNH SAU KHI ĐĂNG NHẬP ---
else:
    # --- PHẦN BANNER ĐỈNH TRANG ---
    st.markdown("""
        <div class="banner-container">
            <div class="banner-title">FTO WEPD</div>
            <div class="banner-subtitle">WESTSIDE POLICE DEPARTMENT</div>
            <div class="banner-tag">HỌC VÀ THI TRẮC NGHIỆM</div>
        </div>
    """, unsafe_allow_html=True)

    # --- THANH THÔNG TIN USER VÀ NÚT ĐĂNG XUẤT ---
    # Sử dụng HTML kết hợp với một nút bấm của Streamlit để xử lý đăng xuất nhanh gọn
    info_col, btn_col = st.columns([5, 1])
    with info_col:
        st.markdown(f"""
            <div class="user-info-bar">
                <div class="user-badge">
                    <div class="logo-circle-small">FTO</div>
                    <div class="user-text">
                        <div class="user-name-title">WEPD - THÔNG TIN</div>
                        <div class="user-role">👤 Tài khoản: {st.session_state.username}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with btn_col:
        st.write("<style>div.stButton > button {margin-top:12px; background-color:#ef4444; color:white; border:none;}</style>", unsafe_allow_html=True)
        if st.button("ĐĂNG XUẤT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    # --- THANH MENU ĐIỀU HƯỚNG DẠNG TAB ---
    tab_info, tab_perm, tab_quiz, tab_docs, tab_news = st.tabs([
        "📢 THÔNG TIN", "👥 CẤP QUYỀN", "📝 CÂU HỎI", "📚 TÀI LIỆU", "📋 THÔNG BÁO"
    ])

    # Nội dung chính của tab chính "📢 THÔNG TIN"
    with tab_info:
        left_col, right_col = st.columns([1.1, 1])
        
        # CỘT TRÁI: THÔNG BÁO MỚI NHẤT
        with left_col:
            st.markdown("## 📢 THÔNG BÁO MỚI NHẤT")
            
            # Thông báo 1
            st.markdown("""
                <div class="noti-box">
                    <div class="noti-date-title">📅 24/07/2026 | Giấy phép cư dân</div>
                    <div class="noti-content">
                        CCCD đang bị lỗi nên học viên yêu cầu cư dân xuất trình nếu không có thì không phạt. 
                        GPLX và giấy tờ xe không bị lỗi học viên yêu cầu cư dân xuất trình khi cư dân sử dụng phương tiện làm bẩn hoặc không làm bẩn (traffic stop). 
                        Nếu không có GPLX phạt 5.000$, không có giấy tờ xe phạt 10.000$, không có cả 2 phạt 15.000$. Thân!
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Thông báo 2
            st.markdown("""
                <div class="noti-box">
                    <div class="noti-date-title">📅 02/08/2026 | MDT và F1</div>
                    <div class="noti-content">
                        Hiện tại bảng MDT và F1 đã thay đổi giáo trình đã được cập nhật. Chúc các học viên thi tốt điểm tốt. Thân!
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Thông báo 3
            st.markdown("""
                <div class="noti-box">
                    <div class="noti-date-title">📅 05/03/2026 | Tranh thủ thời gian học</div>
                    <div class="noti-content">
                        Khi không có giảng viên, các Sĩ quan vui lòng tự học trên web nha.
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # CỘT PHẢI: BẢNG VÀNG KỶ LỤC
        with right_col:
            st.markdown("## 🥇 BẢNG VÀNG KỶ LỤC")
            
            # Tạo bảng dữ liệu giống y hệt như hình mẫu của bạn
            leaderboard_data = {
                "Xếp Hạng": ["🥇 Top 1", "🥈 Top 2", "🥉 Top 3", "4", "5", "6", "7", "8", "9", "10"],
                "Sĩ Quan": ["Ang tony", "Học Viên", "Phạm Seven", "HAI AN", "phùng thanh huy", "Tran Duy", "Pinot Cris", "Hồ Huy Hoàng", "Life Boy", "MR Bean"],
                "Điểm Kỷ Lục": ["50/50", "50/50", "49/50", "49/50", "48/50", "48/50", "48/50", "48/50", "48/50", "48/50"],
                "Đã Thi": ["1 lần", "2 lần", "1 lần", "9 lần", "1 lần", "2 lần", "4 lần", "4 lần", "5 lần", "5 lần"]
            }
            df = pd.DataFrame(leaderboard_data)
            
            # Hiển thị bảng dạng bảng dữ liệu gọn gàng, đẹp mắt
            st.dataframe(df, use_container_width=True, hide_index=True)

    # Các tab còn lại bạn có thể tự thiết kế thêm nội dung tùy thích vào đây
    with tab_quiz:
        st.write("### 📝 Khu vực làm bài thi lý thuyết của Học viên")
        st.info("Nhấp vào tab này để bắt đầu làm các bộ đề trắc nghiệm tính điểm.")

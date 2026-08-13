import streamlit as st
import pandas as pd

# =========================================================================
# CẤU HÌNH HỆ THỐNG BAN ĐẦU
# =========================================================================
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": "admin123",
        "GIANGVIEN": "123456",
        "S-01": "123456",
        "HocVienMoi": "123456"
    }

# 🥇 KHỞI TẠO BẢNG VÀNG RỖNG (Xóa sạch thông tin cũ để người mới cập nhật)
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

# Ngân hàng câu hỏi trắc nghiệm mẫu
if 'questions_db' not in st.session_state:
    st.session_state.questions_db = [
        {
            "question": "Câu 1: Khi gặp tín hiệu đèn vàng nhấp nháy, bạn phải xử lý như thế nào?",
            "options": [
                "Dừng lại ngay lập tức trước vạch dừng.",
                "Được đi tiếp nhưng phải giảm tốc độ và chú ý quan sát.",
                "Tăng tốc độ để nhanh chóng vượt qua giao lộ."
            ],
            "answer": "Được đi tiếp nhưng phải giảm tốc độ và chú ý quan sát."
        },
        {
            "question": "Câu 2: Hành vi điều khiển xe cơ giới chạy quá tốc độ quy định bị nghiêm cấm hay không?",
            "options": [
                "Bị nghiêm cấm hoàn toàn.",
                "Không bị nghiêm cấm nếu đường vắng.",
                "Chỉ bị nhắc nhở nếu không gây tai nạn."
            ],
            "answer": "Bị nghiêm cấm hoàn toàn."
        }
    ]

# Khởi tạo trạng thái đăng nhập
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = ""
if 'submitted' not in st.session_state: st.session_state.submitted = False

# =========================================================================
# GIAO DIỆN & STYLE CSS
# =========================================================================
st.set_page_config(page_title="FTO WEPD - Hệ Thống Sát Hạch", page_icon="🚓", layout="wide")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .banner-container {
        background: linear-gradient(135deg, #07162c 0%, #1b355a 100%);
        border-radius: 12px; padding: 30px; text-align: center; color: white;
        border: 2px solid #324d77; margin-bottom: 20px; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    .banner-title { font-size: 56px; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; font-family: 'Arial Black', sans-serif; }
    .banner-subtitle { font-size: 18px; color: #a0aec0; letter-spacing: 3px; margin-bottom: 10px; }
    .banner-tag { font-size: 28px; font-weight: bold; color: #ffffff; letter-spacing: 1px; }
    .user-info-bar { background-color: #051329; border-radius: 8px; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; border-left: 5px solid #ffcc00; }
    .user-badge { display: flex; align-items: center; gap: 15px; }
    .logo-circle-small { background-color: #ffcc00; color: #0b1e36; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 13px; }
    .user-text { color: white; font-family: sans-serif; }
    .user-name-title { font-size: 15px; font-weight: bold; letter-spacing: 0.5px; }
    .user-role { font-size: 13px; color: #3b82f6; font-weight: bold; }
    .noti-box { background-color: #eef6ff; border-radius: 8px; padding: 20px; margin-bottom: 15px; border-left: 5px solid #3b82f6; font-family: sans-serif; }
    .noti-date-title { font-size: 15px; font-weight: bold; color: #1e3a8a; margin-bottom: 8px; }
    .noti-content { font-size: 14px; color: #334155; line-height: 1.6; }
    .login-box { background-color: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.08); width: 450px; margin: 50px auto; text-align: center; }
    .login-header { background-color: #0b1e36; color: white; padding: 30px 20px; border-radius: 10px 10px 0 0; margin: -40px -40px 30px -40px; }
    .logo-circle { background-color: #ffcc00; color: #0b1e36; width: 60px; height: 60px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 18px; margin: 0 auto 15px auto; }
    div.stButton > button { background-color:#ef4444; color:white; border:none; }
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
    
    col1, col2, col3 = st.columns()
    with col2:
        input_user = st.text_input("TÊN ĐĂNG NHẬP / SỐ PHÙ HIỆU", placeholder="Nhập số phù hiệu")
        input_pass = st.text_input("MÃ BẢO MẬT", type="password", placeholder="Nhập mật khẩu")
        
        st.markdown("<style>div.stButton > button {background-color:#0b1e36; color:#ffcc00; font-weight:bold;}</style>", unsafe_allow_html=True)
        if st.button("ĐĂNG NHẬP HỆ THỐNG", use_container_width=True):
            if input_user in st.session_state.users_db and st.session_state.users_db[input_user] == input_pass:
                st.session_state.logged_in = True
                st.session_state.username = input_user
                st.rerun()
            else:
                st.error("⚠️ Tài khoản hoặc mã bảo mật không chính xác!")

# --- 2. GIAO DIỆN CHÍNH SAU KHI ĐĂNG NHẬP ---
else:
    # Banner đỉnh trang
    st.markdown("""
        <div class="banner-container">
            <div class="banner-title">FTO WEPD</div>
            <div class="banner-subtitle">WESTSIDE POLICE DEPARTMENT</div>
            <div class="banner-tag">HỌC VÀ THI TRẮC NGHIỆM</div>
        </div>
    """, unsafe_allow_html=True)

    # Thanh thông tin user
    info_col, btn_col = st.columns([4, 1])
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
        st.write("<style>div.stButton > button {margin-top:12px; background-color:#ef4444 !important; color:white;}</style>", unsafe_allow_html=True)
        if st.button("ĐĂNG XUẤT", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.submitted = False
            st.rerun()

    # Các Tab điều hướng
    tab_info, tab_quiz = st.tabs(["📢 THÔNG TIN & BẢNG VÀNG", "📝 BÀI THI LÝ THUYẾT"])

    # --- TAB 1: THÔNG TIN VÀ BẢNG VÀNG TỰ ĐỘNG CẬP NHẬT ---
    with tab_info:
        left_col, right_col = st.columns([1.1, 1])
        
        with left_col:
            st.markdown("## 📢 THÔNG BÁO MỚI NHẤT")
            st.markdown("""
                <div class="noti-box">
                    <div class="noti-date-title">📅 24/07/2026 | Giấy phép cư dân</div>
                    <div class="noti-content">CCCD lỗi, yêu cầu học viên xuất trình giấy tờ xe và GPLX. Nếu không có GPLX phạt 5.000$, không giấy tờ xe phạt 10.000$.</div>
                </div>
            """, unsafe_allow_html=True)

        with right_col:
            st.markdown("## 🥇 BẢNG VÀNG KỶ LỤC MỚI")
            
            if len(st.session_state.leaderboard) == 0:
                st.info("Chưa có học viên nào nộp bài. Hệ thống đang đợi cập nhật thành tích đầu tiên!")
            else:
                # Chuyển đổi danh sách kỷ lục thành bảng dữ liệu xử lý trực quan
                df_leaderboard = pd.DataFrame(st.session_state.leaderboard)
                
                # Sắp xếp theo điểm số cao nhất lên đầu
                df_leaderboard = df_leaderboard.sort_values(by=["Số Câu Đúng"], ascending=False).reset_index(drop=True)
                
                # Định dạng cột xếp hạng hiển thị biểu tượng huy chương
                ranks = []
                for i in range(len(df_leaderboard)):
                    if i == 0: ranks.append("🥇 Top 1")
                    elif i == 1: ranks.append("🥈 Top 2")
                    elif i == 2: ranks.append("🥉 Top 3")
                    else: ranks.append(str(i + 1))
                df_leaderboard.insert(0, "Xếp Hạng", ranks)
                
                # Hiển thị bảng xếp hạng ra màn hình
                st.dataframe(df_leaderboard[["Xếp Hạng", "Sĩ Quan", "Điểm Kỷ Lục", "Đã Thi"]], use_container_width=True, hide_index=True)

    # --- TAB 2: KHU VỰC THI TRẮC NGHIỆM ---
    with tab_quiz:
        st.write("### 📝 Làm Bài Sát Hạch Lý Thuyết")
        
        user_answers = {}
        for i, item in enumerate(st.session_state.questions_db):
            st.markdown(f"#### {item['question']}")
            user_answers[i] = st.radio("Chọn phương án đúng:", item["options"], key=f"exam_q_{i}", disabled=st.session_state.submitted)
            st.write("")

        st.divider()

        if not st.session_state.submitted:
            st.write("<style>div.stButton > button {background-color:#0b1e36; color:#ffcc00;}</style>", unsafe_allow_html=True)
            if st.button("NỘP BÀI THI SÁT HẠCH", use_container_width=True):
                st.session_state.submitted = True
                
                # Tính toán điểm thi sau khi bấm nộp bài
                

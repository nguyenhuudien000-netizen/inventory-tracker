import streamlit as stimport streamlit as st
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

# =========================================================================
# CẤU HÌNH HỆ THỐNG BAN ĐẦU (Tự động lưu vào bộ nhớ trang web)
# =========================================================================
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": "admin123",  # 💻 ĐÂY LÀ TÀI KHOẢN ADMIN ĐỂ CHỈNH SỬA
        "S-01": "123456",
        "H-01": "654321",
        "test": "test"
    }

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
        }
    ]

# Khởi tạo các trạng thái ứng dụng
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = ""
if 'is_admin' not in st.session_state: st.session_state.is_admin = False
if 'submitted' not in st.session_state: st.session_state.submitted = False

# =========================================================================
# GIAO DIỆN & STYLE
# =========================================================================
st.set_page_config(page_title="FTO WEPD - Hệ Thống Sát Hạch", page_icon="🚓", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .login-box { background-color: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.08); width: 100%; text-align: center; margin-bottom: 20px;}
    .login-header { background-color: #0b1e36; color: white; padding: 30px 20px; border-radius: 10px 10px 0 0; margin: -40px -40px 30px -40px; }
    .logo-circle { background-color: #ffcc00; color: #0b1e36; width: 60px; height: 60px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 18px; margin: 0 auto 15px auto; }
    .title-main { font-size: 16px; font-weight: bold; letter-spacing: 1px; margin-bottom: 5px; }
    .title-sub { font-size: 11px; color: #a0aec0; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# --- 1. MÀN HÌNH ĐĂNG NHẬP ---
if not st.session_state.logged_in:
    st.markdown("""
        <div class="login-box">
            <div class="login-header">
                <div class="logo-circle">FTO</div>
                <div class="title-main">WESTSIDE POLIECE DEPARTMENT</div>
                <div class="title-sub">Hệ Thống Đăng Nhập Sát Hạch & Quản Trị</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        input_user = st.text_input("TÊN ĐĂNG NHẬP / SỐ PHÙ HIỆU", placeholder="Nhập tài khoản của bạn")
        input_pass = st.text_input("MÃ BẢO MẬT", type="password", placeholder="Nhập mật khẩu")
        
        if st.button("ĐĂNG NHẬP系統", use_container_width=True):
            if input_user in st.session_state.users_db and st.session_state.users_db[input_user] == input_pass:
                st.session_state.logged_in = True
                st.session_state.username = input_user
                st.session_state.submitted = False
                # Kiểm tra xem có phải tài khoản admin không
                st.session_state.is_admin = (input_user == "admin")
                st.rerun()
            else:
                st.error("⚠️ Tài khoản hoặc mã bảo mật không chính xác!")

# --- MÀN HÌNH SAU KHI ĐĂNG NHẬP ---
else:
    # Thanh điều hướng trên cùng
    score_col, logout_col = st.columns([4, 1])
    with score_col:
        if st.session_state.is_admin:
            st.subheader("🛠️ QUẢN TRỊ VIÊN: Hệ thống Admin")
        else:
            st.subheader(f"🚓 Thí sinh: {st.session_state.username}")
    with logout_col:
        if st.button("Đăng xuất", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.is_admin = False
            st.rerun()
            
    st.divider()

    # --- 2. GIAO DIỆN DÀNH RIÊNG CHO ADMIN ---
    if st.session_state.is_admin:
        tab1, tab2 = st.tabs(["👥 Quản Lý Tài Khoản Thí Sinh", "📝 Quản Lý Đề Thi"])
        
        # TAB 1: THÊM TÀI KHOẢN
        with tab1:
            st.markdown("### Thêm tài khoản mới")
            new_user = st.text_input("Nhập Số phù hiệu / Username mới:")
            new_pass = st.text_input("Nhập Mật khẩu mới:", type="password")
            
            if st.button("➕ Thêm tài khoản", type="primary"):
                if new_user and new_pass:
                    if new_user in st.session_state.users_db:
                        st.warning(f"Tài khoản '{new_user}' đã tồn tại!")
                    else:
                        st.session_state.users_db[new_user] = new_pass
                        st.success(f"Đã thêm thành công thí sinh: {new_user}")
                        st.rerun()
                else:
                    st.error("Vui lòng điền đầy đủ cả tài khoản và mật khẩu!")
            
            st.divider()
            st.markdown("### Danh sách tài khoản hiện tại")
            for u, p in st.session_state.users_db.items():
                st.text(f"• Tài khoản: {u} | Mật khẩu: {p}")

        # TAB 2: QUẢN LÝ CÂU HỎI
        with tab2:
            st.markdown("### Thêm câu hỏi trắc nghiệm mới")
            new_q = st.text_area("Nội dung câu hỏi:")
            op1 = st.text_input("Đáp án A:")
            op2 = st.text_input("Đáp án B:")
            op3 = st.text_input("Đáp án C:")
            
            correct_op = st.selectbox("Chọn đáp án đúng chính xác nhất:", [op1, op2, op3])
            
            if st.button("💾 Thêm câu hỏi vào đề thi", type="primary"):
                if new_q and op1 and op2 and op3 and correct_op:
                    new_item = {
                        "question": f"Câu {len(st.session_state.questions_db) + 1}: {new_q}",
                        "options": [op1, op2, op3],
                        "answer": correct_op
                    }
                    st.session_state.questions_db.append(new_item)
                    st.success("Đã thêm câu hỏi mới thành công vào đề thi!")
                    st.rerun()
                else:
                    st.error("Vui lòng nhập đầy đủ câu hỏi và tất cả các đáp án!")
            
            st.divider()
            st.markdown("### Danh sách câu hỏi trong đề")
            for idx, q_item in enumerate(st.session_state.questions_db):
                st.markdown(f"**{q_item['question']}**")
                st.caption(f"Đáp án đúng: {q_item['answer']}")

    # --- 3. GIAO DIỆN THI DÀNH CHO THÍ SINH ---
    else:
        user_answers = {}
        for i, item in enumerate(st.session_state.questions_db):
            st.markdown(f"#### {item['question']}")
            user_answers[i] = st.radio("Chọn câu trả lời:", item["options"], key=f"user_q_{i}", disabled=st.session_state.submitted)
            st.write("")

        st.divider()

        if not st.session_state.submitted:
            if st.button("NỘP BÀI THI", type="primary", use_container_width=True):
                st.session_state.submitted = True
                st.rerun()
        else:
            correct_count = 0
            total_questions = len(st.session_state.questions_db)
            st.markdown("### 📊 KẾT QUẢ BÀI THI CỦA BẠN:")
            
            for i, item in enumerate(st.session_state.questions_db):
                if user_answers[i] == item["answer"]:
                    correct_count += 1
                    st.success(f"✓ **{item['question']}** - Bạn đã chọn đúng!")
                else:
                    st.error(f"✗ **{item['question']}**\n- Bạn chọn: {user_answers[i]}\n- Đáp án đúng: {item['answer']}")
                    
            score_percentage = (correct_count / total_questions) * 100
            st.metric(label="Tổng số câu đúng", value=f"{correct_count} / {total_questions}", delta=f"{score_percentage:.1f}%")
            
            if score_percentage >= 70:
                st.balloons()
                st.success("🎉 CHÚC MỪNG! Bạn đã VƯỢT QUA bài sát hạch.")
            else:
                st.warning("⚠️ KẾT QUẢ: KHÔNG ĐẠT.")
                
            if st.button("LÀM LẠI BÀI THI", use_container_width=True):
                st.session_state.submitted = False
                st.rerun()

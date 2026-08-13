import streamlit as st
import pandas as pd

# =========================================================================
# 1. KHỞI TẠO CƠ SỞ DỮ LIỆU BỘ NHỚ (Duy trì trong phiên chạy)
# =========================================================================
# Cơ sở dữ liệu tài khoản và quyền hạn ban đầu
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"pass": "admin123", "role": "Quản trị viên", "can_exam": True},
        "GIANGVIEN": {"pass": "123456", "role": "Giảng viên", "can_exam": True},
        "S-01": {"pass": "123456", "role": "Học viên", "can_exam": False},  # Mặc định chưa cấp quyền thi
        "HocVien02": {"pass": "123456", "role": "Học viên", "can_exam": False}
    }

# Ngân hàng câu hỏi (Tự động chia nhóm Ôn tập và Thi)
if 'questions_db' not in st.session_state:
    st.session_state.questions_db = [
        {
            "id": 1,
            "question": "Khi gặp tín hiệu đèn vàng nhấp nháy, bạn phải xử lý như thế nào?",
            "options": ["Dừng lại trước vạch dừng.", "Đi tiếp nhưng giảm tốc độ, chú ý quan sát.", "Tăng tốc vượt qua."],
            "answer": "Đi tiếp nhưng giảm tốc độ, chú ý quan sát.",
            "type": "Mục thi & Ôn tập"  # Câu hỏi dùng cho cả 2 mục
        },
        {
            "id": 2,
            "question": "Hành vi chạy quá tốc độ quy định có bị nghiêm cấm không?",
            "options": ["Bị nghiêm cấm hoàn toàn.", "Không bị cấm nếu đường vắng.", "Chỉ nhắc nhở."],
            "answer": "Bị nghiêm cấm hoàn toàn.",
            "type": "Mục ôn tập"  # Chỉ xuất hiện khi ôn tập
        }
    ]

# Lưu lịch sử điểm số thi
if 'exam_results' not in st.session_state:
    st.session_state.exam_results = []

# Khởi tạo các trạng thái hệ thống
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = ""
if 'user_role' not in st.session_state: st.session_state.user_role = ""
if 'exam_submitted' not in st.session_state: st.session_state.exam_submitted = False

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
    </style>
""", unsafe_allow_html=True)

# --- 2. MÀN HÌNH ĐĂNG NHẬP ---
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
    
    col1, col2, col3 = st.columns()
    with col2:
        input_user = st.text_input("TÊN ĐĂNG NHẬP / SỐ PHÙ HIỆU", placeholder="Nhập tài khoản")
        input_pass = st.text_input("MÃ BẢO MẬT", type="password", placeholder="Nhập mật khẩu")
        
        if st.button("ĐĂNG NHẬP HỆ THỐNG", use_container_width=True):
            if input_user in st.session_state.users_db and st.session_state.users_db[input_user]["pass"] == input_pass:
                st.session_state.logged_in = True
                st.session_state.username = input_user
                st.session_state.user_role = st.session_state.users_db[input_user]["role"]
                st.session_state.exam_submitted = False
                st.rerun()
            else:
                st.error("⚠️ Tài khoản hoặc mã bảo mật không chính xác!")

# --- 3. MÀN HÌNH CHÍNH SAU KHI ĐĂNG NHẬP ---
else:
    # Banner đỉnh trang
    st.markdown(f"""
        <div class="banner-container">
            <div class="banner-title">FTO WEPD</div>
            <div class="banner-subtitle">WESTSIDE POLICE DEPARTMENT - HỆ THỐNG SÁT HẠCH</div>
        </div>
    """, unsafe_allow_html=True)

    # Thanh trạng thái người dùng
    info_col, btn_col = st.columns([4, 1])
    with info_col:
        st.markdown(f"""
            <div class="user-info-bar">
                👤 Tài khoản: <b>{st.session_state.username}</b> | Chức vụ: <span style='color:#3b82f6;'><b>{st.session_state.user_role}</b></span>
            </div>
        """, unsafe_allow_html=True)
    with btn_col:
        if st.button("ĐĂNG XUẤT", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_role = ""
            st.session_state.exam_submitted = False
            st.rerun()

    # Phân chia luồng giao diện theo Chức vụ
    # A. GIAO DIỆN QUẢN LÝ (Dành cho Admin và Giảng viên)
    if st.session_state.user_role in ["Quản trị viên", "Giảng viên"]:
        tab_users, tab_add_q, tab_results = st.tabs([
            "👥 QUẢN LÝ THÀNH VIÊN & CẤP QUYỀN THI", 
            "📝 TỰ BIÊN SOẠN CÂU HỎI", 
            "📊 THỐNG KÊ ĐIỂM SỐ KIỂM TRA"
        ])
        
        # TAB QUẢN LÝ THÀNH VIÊN & CẤP QUYỀN
        with tab_users:
            st.markdown("### ➕ Thêm Tài Khoản Mới Vào Hệ Thống")
            c1, c2, c3 = st.columns(3)
            with c1: new_u = st.text_input("Số phù hiệu / Username mới:", key="add_u")
            with c2: new_p = st.text_input("Mật khẩu truy cập:", type="password", key="add_p")
            with c3: new_r = st.selectbox("Vai trò chức vụ:", ["Học viên", "Giảng viên"], key="add_r")
            
            if st.button("Xác nhận thêm người dùng", type="primary"):
                if new_u and new_p:
                    st.session_state.users_db[new_u] = {"pass": new_p, "role": new_r, "can_exam": False}
                    st.success(f"Đã thêm thành công tài khoản: {new_u} ({new_r})")
                    st.rerun()
                else: st.error("Vui lòng điền đủ thông tin!")
                
            st.divider()
            st.markdown("### 🔐 Danh Sách Thành Viên & Cấp Quyền Lượt Thi")
            st.caption("Gợi ý: Tích chọn vào ô tương ứng để cho phép Học viên đó được quyền vào làm 'Bài thi chính thức'.")
            
            # Hiển thị và cập nhật quyền thi trực tiếp bằng bảng checkbox
            for user, data in st.session_state.users_db.items():
                if data["role"] == "Học viên":
                    col_u, col_status = st.columns([3, 1])
                    with col_u:
                        st.write(f"• **{user}** (Mật khẩu: {data['pass']})")
                    with col_status:
                        # Checkbox bật tắt quyền thi trực tiếp vào dữ liệu nền
                        current_status = st.checkbox("Cho phép thi", value=data["can_exam"], key=f"perm_{user}")
                        if current_status != data["can_exam"]:
                            st.session_state.users_db[user]["can_exam"] = current_status
                            st.toast(f"Đã cập nhật quyền thi cho {user}!")
        
        # TAB TỰ BIÊN SOẠN CÂU HỎI
        with tab_add_q:
            st.markdown("### 📝 Soạn Thảo Câu Hỏi Trắc Nghiệm Mới")
            q_text = st.text_area("Nội dung câu hỏi:")
            o1 = st.text_input("Phương án A:")
            o2 = st.text_input("Phương án B:")
            o3 = st.text_input("Phương án C:")
            q_ans = st.selectbox("Lựa chọn phương án chính xác nhất:", [o1, o2, o3])
            q_type = st.radio("Phân loại danh mục câu hỏi:", ["Mục thi & Ôn tập", "Mục ôn tập"])
            
            if st.button("Lưu câu hỏi vào ngân hàng đề", type="primary"):
                if q_text and o1 and o2 and o3:
                    new_q_item = {
                        "id": len(st.session_state.questions_db) + 1,
                        "question": q_text,
                        "options": [o1, o2, o3],
                        "answer": q_ans,
                        "type": q_type
                    }
                    st.session_state.questions_db.append(new_q_item)
                    st.success("Đã lưu câu hỏi mới vào hệ thống thành công!")
                    st.rerun()
                else: st.error("Vui lòng không để trống thông tin soạn thảo!")

        # TAB THỐNG KÊ ĐIỂM SỐ
        with tab_results:
            st.markdown("### 📊 Kết Quả Kiểm Tra Chi Tiết Của Học Viên")
            if len(st.session_state.exam_results) == 0:
                st.info("Chưa có dữ liệu thi kiểm tra điểm số nào được ghi nhận.")
            else:
                df_res = pd.DataFrame(st.session_state.exam_results)
                

import streamlit as st

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

pythonimport streamlit as st
import time

# =========================================================================
# 1. PHẦN CẤU HÌNH TÀI KHOẢN NGƯỜI ĐĂNG NHẬP (Tự do thêm bớt tài khoản)
# Format: "Số Phù Hiệu / Username": "Mật khẩu / Mã bảo mật"
# =========================================================================
USER_CREDENTIALS = {
    "S-01": "123456",
    "H-01": "654321",
    "PHO-99": "admin123",
    "test": "test"
}

# =========================================================================
# 2. NGÂN HÀNG CÂU HỎI TRẮC NGHIỆM (Tự do sửa câu hỏi và đáp án)
# - "question": Nội dung câu hỏi lý thuyết
# - "options": Danh sách các đáp án lựa chọn
# - "answer": Nội dung đáp án đúng (Phải viết chính xác giống 1 trong các options)
# =========================================================================
QUIZ_QUESTIONS = [
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
    },
    {
        "question": "Câu 3: Tại nơi đường giao nhau không có báo hiệu đi theo vòng xuyến, người điều khiển phải nhường đường thế nào?",
        "options": [
            "Nhường đường cho xe đi từ bên trái.",
            "Nhường đường cho xe đi từ bên phải.",
            "Xe nào to hơn thì được đi trước."
        ],
        "answer": "Nhường đường cho xe đi từ bên phải."
    }
]

# =========================================================================
# 3. GIAO DIỆN & LOGIC HỆ THỐNG (Giữ nguyên phần này)
# =========================================================================
st.set_page_config(page_title="FTO GCPD - Sát Hạch Lý Thuyết", page_icon="🚓", layout="centered")

# Thêm CSS tùy biến giao diện giống ảnh mẫu
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .main .block-container { display: flex; justify-content: center; align-items: center; padding-top: 3rem; }
    .login-box { background-color: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.08); width: 450px; text-align: center; }
    .login-header { background-color: #0b1e36; color: white; padding: 30px 20px; border-radius: 10px 10px 0 0; margin: -40px -40px 30px -40px; }
    .logo-circle { background-color: #ffcc00; color: #0b1e36; width: 60px; height: 60px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 18px; margin: 0 auto 15px auto; }
    .title-main { font-size: 16px; font-weight: bold; letter-spacing: 1px; margin-bottom: 5px; }
    .title-sub { font-size: 11px; color: #a0aec0; text-transform: uppercase; }
    div.stButton > button:first-child { background-color: #0b1e36; color: #ffcc00; font-weight: bold; width: 100%; border-radius: 5px; border: none; padding: 10px; margin-top: 10px; }
    div.stButton > button:first-child:hover { background-color: #163254; color: #ffcc00; }
    </style>
""", unsafe_allow_html=True)

# Quản lý Session State (Trạng thái ứng dụng)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# --- MÀN HÌNH ĐĂNG NHẬP ---
if not st.session_state.logged_in:
    st.markdown("""
        <div class="login-box">
            <div class="login-header">
                <div class="logo-circle">FTO</div>
                <div class="title-main">GACHA CITY POLICE DEPARTMENT</div>
                <div class="title-sub">Học & Thi Trắc Nghiệm Lý Thuyết</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        input_user = st.text_input("SỐ PHÙ HIỆU", placeholder="Nhập số PHO/HO của bạn")
        input_pass = st.text_input("MÃ BẢO MẬT", type="password", placeholder="Nhập mật khẩu truy cập")
        
        if st.button("ĐĂNG NHẬP"):
            if input_user in USER_CREDENTIALS and USER_CREDENTIALS[input_user] == input_pass:
                st.session_state.logged_in = True
                st.session_state.username = input_user
                st.session_state.submitted = False  # Reset trạng thái nộp bài cho lượt mới
                st.rerun()
            else:
                st.error("⚠️ Số phù hiệu hoặc mã bảo mật không chính xác!")

# --- MÀN HÌNH THI TRẮC NGHIỆM ---
else:
    # Thanh điều hướng phía trên
    score_col, logout_col = st.columns([4, 1])
    with score_col:
        st.subheader(f"🚓 Thí sinh: {st.session_state.username}")
    with logout_col:
        if st.button("Đăng xuất"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
            
    st.divider()
    st.write("👉 Hãy đọc kỹ câu hỏi và chọn duy nhất một phương án đúng chính xác nhất.")

    # Hiển thị bài thi trắc nghiệm tự động dựa trên ngân hàng câu hỏi
    user_answers = {}
    for i, item in enumerate(QUIZ_QUESTIONS):
        st.markdown(f"#### {item['question']}")
        # Lưu câu trả lời của người dùng dựa theo index
        user_answers[i] = st.radio(
            "Chọn câu trả lời:", 
            item["options"], 
            key=f"q_{i}", 
            disabled=st.session_state.submitted
        )
        st.write("") # Tạo khoảng cách

    st.divider()

    # Xử lý kết quả khi bấm nộp bài
    if not st.session_state.submitted:
        if st.button("NỘP BÀI THI"):
            st.session_state.submitted = True
            st.rerun()
    else:
        # Tính điểm
        correct_count = 0
        total_questions = len(QUIZ_QUESTIONS)
        
        st.markdown("### 📊 KẾT QUẢ BÀI THI CỦA BẠN:")
        
        for i, item in enumerate(QUIZ_QUESTIONS):
            if user_answers[i] == item["answer"]:
                correct_count += 1
                st.success(f"✓ **{item['question']}** - Bạn đã chọn đúng!")
            else:
                st.error(f"✗ **{item['question']}**\n- Câu trả lời của bạn: {user_answers[i]}\n- Đáp án đúng: {item['answer']}")
                
        # Hiển thị tổng số điểm nhận được
        score_percentage = (correct_count / total_questions) * 100
        st.metric(label="Tổng số câu đúng", value=f"{correct_count} / {total_questions}", delta=f"{score_percentage:.1f}% Điểm")
        
        if score_percentage >= 70:
            st.balloons()
            st.success("🎉 CHÚC MỪNG! Bạn đã VƯỢT QUA bài sát hạch lý thuyết.")
        else:
            st.sidebar.warning("⚠️ KẾT QUẢ: KHÔNG ĐẠT. Bạn cần trả lời đúng tối thiểu 70% số câu hỏi.")
            
        if st.button("LÀM LẠI BÀI THI"):
            st.session_state.submitted = False
            st.rerun()

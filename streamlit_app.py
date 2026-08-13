import streamlit as st
import time
import random
from datetime import datetime

# =========================================================================
# 1. NGÂN HÀNG ĐỀ THI GỐC (ĐÃ NẠP SẴN 10 CÂU HỎI THỰC TẾ CỦA BẠN - LƯU VĨNH VIỄN)
# =========================================================================
if 'questions_db' not in st.session_state:
    st.session_state.questions_db = [
        {
            "id": 1, "CauHoi": "Xử lý đối tượng có nợ 5 hóa đơn (không thể ghi hóa đơn cho tội phạm) Trường hợp nào?",
            "options": ["Ra báo TTC, tố cáo tội phạm không chịu thanh toán", "Bỏ qua hóa đơn và tiếp tục xử lý", "Phạt tù thêm thời gian"],
            "answer": "Ra báo TTC, tố cáo tội phạm không chịu thanh toán", "explain": "Theo luật, đối tượng nợ 5 hóa đơn cần thông báo qua hệ thống TTC."
        },
        {
            "id": 2, "CauHoi": "Số người tối thiểu có thể trấn áp 02 PD đang cầm súng là bao nhiêu?",
            "options": ["6 người", "4 người", "2 người"],
            "answer": "6 người", "explain": "Vũ lực súng trường yêu cầu tối thiểu áp đảo là 6 người để đảm bảo an toàn."
        },
        {
            "id": 3, "CauHoi": "Số người tối thiểu có thể trấn áp 02 PD không có súng là bao nhiêu?",
            "options": ["4 người", "2 người", "6 người"],
            "answer": "4 người", "explain": "Đối phương không vũ trang súng thì số lượng tối thiểu yêu cầu là 4."
        },
        {
            "id": 4, "CauHoi": "Mức độ ưu tiên nhận Dispatch:",
            "options": ["Buôn Lậu Tranh", "Cướp cửa hàng tiện lợi", "Trộm cắp phương tiện"],
            "answer": "Buôn Lậu Tranh", "explain": "Tội phạm buôn lậu tranh được xếp vào danh mục khẩn cấp cao."
        },
        {
            "id": 5, "CauHoi": "Trong tình huống Giao hàng trắng, tính từ lúc lấy hàng trắng, PD có quyền triệt hạ từ giây thứ bao nhiêu?",
            "options": ["15 giây", "30 giây", "Chỉ được bắt giữ"],
            "answer": "15 giây", "explain": "Học viên chú ý mốc thời gian phản ứng 15 giây quy định trong giáo trình."
        },
        {
            "id": 6, "CauHoi": "PD có thể mua các vật phẩm bẩn để đổi ra huân chương hay không?",
            "options": ["Có, nếu 2 bên giao dịch công bằng", "Không, hành vi này bị cấm hoàn toàn", "Có thể mua nếu được phép của cấp trên"],
            "answer": "Có, nếu 2 bên giao dịch công bằng", "explain": "Giao dịch công bằng hợp pháp được chấp thuận quy đổi huân chương."
        },
        {
            "id": 7, "CauHoi": "Tội phạm bán túi bột mì cho NPC, khi chạy trốn PD thì họ không được phép trốn vào đâu?",
            "options": ["Khu quân sự", "Khu dân cư", "Nhà riêng"],
            "answer": "Khu quân sự", "explain": "Khu vực quân sự là vùng cấm nghiêm ngặt đối với tội phạm lẩn trốn."
        },
        {
            "id": 8, "CauHoi": "Máy bay hàng trắng đáp xuống đường băng hoặc sát đường băng mà hỏng hóc, PD có được triệt hạ hay không?",
            "options": ["Có, bắt ngay và luôn", "Không được triệt hạ, chỉ bao vây", "Phải đợi lệnh từ Dispatch cấp cao"],
            "answer": "Có, bắt ngay và luôn", "explain": "Hành vi xâm nhập đường băng bằng máy bay lậu cần trấn áp ngay lập tức."
        },
        {
            "id": 9, "CauHoi": "Trong tình huống 2 PD - 2 máy bay truy đuổi, 1 PD triệt hạ Fail khiến máy bay bị nổ hoặc lỗi, xử lý thế nào?",
            "options": ["Không được triệt hạ, chỉ được hạn chế khả năng hạ cánh", "Tiếp tục triệt hạ máy bay còn lại", "Rút lui toàn bộ đội hình"],
            "answer": "Không được triệt hạ, chỉ được hạn chế khả năng hạ cánh", "explain": "Tránh gây nguy hiểm dây chuyền, chuyển sang phương án hạn chế tối đa."
        },
        {
            "id": 10, "CauHoi": "RP KHÔNG SỢ PD, thì PD được phép làm gì sau đây?",
            "options": ["PD chỉ được phép dùng Tazer bắn ngay lập tức", "Dùng súng lethal triệt hạ", "Cảnh cáo bằng lời nói 3 lần"],
            "answer": "PD chỉ được phép dùng Tazer bắn ngay lập tức", "explain": "Sử dụng súng điện Tazer để áp chế hành vi không hợp tác RP ngay lập tức."
        }
    ]

# Khởi tạo dữ liệu người dùng, thông báo và lịch sử điểm
if 'announcements_db' not in st.session_state:
    st.session_state.announcements_db = [
        {"Ngay": "05/03/2026", "TieuDe": "Tranh thủ thời gian học", "NoiDung": "Khi không có giảng viên, các Sĩ quan vui lòng tự học trên web nha."},
        {"Ngay": "02/08/2026", "TieuDe": "MDT và F1", "NoiDung": "Hiện tại bảng MDT và F1 đã thay đổi giáo trình đã được cập nhật. Chúc các học viên thi tốt điểm tốt. Thân!"}
    ]
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"pass": "admin123", "role": "Quản trị viên", "can_exam": True},
        "GIANGVIEN": {"pass": "123456", "role": "Giảng viên", "can_exam": True},
        "2229": {"pass": "123456", "role": "Học viên", "can_exam": True}
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
# ĐỊNH DẠNG GIAO DIỆN CHUẨN ĐẸP
# =========================================================================
st.set_page_config(page_title="FTO WEPD - Hệ Thống Sát Hạch", page_icon="🚓", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .banner-graphic {
        background: linear-gradient(180deg, #0e1e38 0%, #050d1a 100%);
        border: 3px solid #1a2e4c; border-radius: 12px; padding: 25px 20px; text-align: center; color: white; margin-bottom: 20px;
    }
    .banner-title-wpd { font-size: 46px; font-weight: 900; color: #ffffff; font-family: 'Impact', sans-serif; }
    .banner-tag-wpd { font-size: 22px; font-weight: bold; color: #ffcc00; border-top: 1px solid #1a2e4c; padding-top: 8px; }
    .noti-flat-card { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 15px; margin-bottom: 12px; }
    .timer-text { font-size: 24px; font-weight: bold; color: #ef4444; text-align: center; background-color: #fee2e2; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
    .explain-box { background-color: #fffbeb; border-left: 5px solid #d97706; padding: 12px; color: #92400e; font-size: 14px; }
    .score-card-custom { background-color: #ffffff; border-left: 5px solid #3b82f6; padding: 15px; border-radius: 6px; margin-bottom: 10px; box-shadow: 0px 2px 4px rgba(0,0,0,0.05); }
    div.stButton > button { background-color: #0b1e36 !important; color: white !important; font-weight: bold !important; width: 100%; border-radius: 4px !important; }
    </style>
""", unsafe_allow_html=True)

# --- MÀN HÌNH ĐĂNG NHẬP ---
if not st.session_state.logged_in:
    st.markdown('<div class="banner-graphic"><div class="banner-title-wpd">FTO WEPD</div><div class="banner-tag-wpd">HỌC VÀ THI TRẮC NGHIỆM</div></div>', unsafe_allow_html=True)
    input_user = st.text_input("TÊN ĐĂNG NHẬP / SỐ PHÙ HIỆU", key="login_username_field")
    input_pass = st.text_input("MÃ BẢO MẬT", type="password", key="login_password_field")
    if st.button("ĐĂNG NHẬP HỆ THỐNG"):
        if input_user in st.session_state.users_db and st.session_state.users_db[input_user]["pass"] == input_pass:
            st.session_state.logged_in = True
            st.session_state.username = input_user
            st.session_state.user_role = st.session_state.users_db[input_user]["role"]
            st.session_state.exam_submitted = False
            st.rerun()
        else: st.error("⚠️ Sai tài khoản hoặc mật khẩu!")

# --- MÀN HÌNH CHÍNH CHẠY ONLINE ---
else:
    st.markdown('<div class="banner-graphic"><div class="banner-title-wpd">FTO WEPD</div><div class="banner-tag-wpd">WESTSIDE POLICE DEPARTMENT</div></div>', unsafe_allow_html=True)
    st.info(f"👤 Tài khoản: {st.session_state.username} | Chức vụ: {st.session_state.user_role}")
    
    if st.button("🔴 ĐĂNG XUẤT HỆ THỐNG"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.exam_submitted = False
        st.session_state.shuffled_exam_qs = []
        st.rerun()

    # PHÂN CHIA GIAO DIỆN THEO CHỨC VỤ
    if st.session_state.user_role in ["Quản trị viên", "Giảng viên"]:
        tab_users, tab_add_q, tab_results, tab_news_manage = st.tabs(["👥 QUẢN LÝ THÀNH VIÊN", "📝 SOẠN CÂU HỎI MỚI", "📊 THỐNG KÊ ĐIỂM SỐ", "📋 QUẢN LÝ THÔNG BÁO"])
        
        with tab_users:
            st.markdown("### ➕ Thêm học viên mới")
            add_u = st.text_input("Tên tài khoản mới:", key="create_user_u")
            add_p = st.text_input("Mật khẩu bảo mật:", type="password", key="create_user_p")
            if st.button("Xác nhận thêm tài khoản", key="btn_confirm_user_add"):
                if add_u and add_p:
                    st.session_state.users_db[add_u] = {"pass": add_p, "role": "Học viên", "can_exam": False}
                    st.success(f"Đã thêm học viên: {add_u}")
                    st.rerun()
            st.divider()
            st.markdown("### 🔐 Danh sách cấp quyền thi")
            for user, data in st.session_state.users_db.items():
                if data["role"] == "Học viên":
                    col_u, col_chk = st.columns(2)
                    with col_u: st.write(f"• **{user}** (Mật khẩu: `{data['pass']}`)")
                    with col_chk:

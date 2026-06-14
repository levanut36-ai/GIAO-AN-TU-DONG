import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện trang web
st.set_page_config(page_title="Giáo Án AI & NLS", page_icon="📚", layout="centered")

st.markdown("<h2 style='text-align: center; color: #1E88E5;'>📚 ỨNG DỤNG SOẠN GIÁO ÁN TỰ ĐỘNG TÍCH HỢP NLS & AI</h2>", unsafe_allow_html=True)
st.write("---")

# Thanh nhập khóa bảo mật ở bên trái màn hình
st.sidebar.header("🔑 Cấu hình hệ thống")
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password", help="Lấy mã này từ Google AI Studio")

st.sidebar.markdown("""
---
**Hướng dẫn sử dụng:**
1. Nhập API Key vào ô phía trên.
2. Điền thông tin bài học ở khung bên phải.
3. Bấm **'Bắt đầu soạn giáo án'** và đợi kết quả.
""")

# Giao diện chính để điền thông tin bài học
st.subheader("📝 Thông tin bài học")
col1, col2 = st.columns(2)

with col1:
    mon_hoc = st.text_input("Tên môn học / Hoạt động:", placeholder="Ví dụ: Toán, Tiếng Việt, Kỹ năng sống...")
    lop = st.text_input("Khối lớp / Độ tuổi:", placeholder="Ví dụ: Lớp 3, Lớp 5, Mầm non 4-5 tuổi...")

with col2:
    chu_de = st.text_input("Tên bài học / Chủ đề:", placeholder="Ví dụ: Phép cộng phân số, Bảo vệ môi trường...")
    thoi_gian = st.text_input("Thời lượng (phút):", placeholder="Ví dụ: 35 phút, 45 phút...")

muc_tieu = st.text_area("Mục tiêu bài học (Kiến thức, Kỹ năng, Thái độ - Nếu có):", 
                        placeholder="Để trống nếu muốn AI tự gợi ý mục tiêu dựa trên tên bài học.")

# Nút bấm kích hoạt AI
if st.button("🚀 Bắt đầu soạn giáo án", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ Vui lòng nhập API Key ở thanh menu bên trái trước khi bắt đầu!")
    elif not mon_hoc or not chu_de:
        st.warning("⚠️ Vui lòng điền ít nhất 'Tên môn học' và 'Tên bài học'.")
    else:
        with st.spinner("⏳ Trợ lý AI đang thiết kế giáo án tích hợp NLS... Vui lòng đợi trong giây lát!"):
            try:
                # Cấu hình AI với API Key do người dùng nhập
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Câu lệnh (Prompt) chuẩn hóa để AI viết giáo án
                prompt = f"""
                Bạn là một chuyên gia giáo dục xuất sắc. Hãy thiết kế một giáo án chi tiết, khoa học cho bài học sau:
                - Môn học/Hoạt động: {mon_hoc}
                - Khối lớp: {lop}
                - Tên bài học/Chủ đề: {chu_de}
                - Thời lượng: {thoi_gian}
                - Mục tiêu bài học (yêu cầu bổ sung thêm nếu cần): {muc_tieu}

                YÊU CẦU ĐẶC BIỆT:
                1. Tích hợp sâu phương pháp NLS (Năng lực số / Năng lực số hóa hoặc Phương pháp học tập tích cực tương ứng) vào các hoạt động dạy học.
                2. Thiết kế giáo án có cấu trúc rõ ràng bao gồm các phần: 
                   - Mục tiêu (Kiến thức, Kỹ năng, Phát triển năng lực đặc biệt là năng lực số)
                   - Chuẩn bị (Giáo viên, Học sinh, Thiết bị công nghệ nếu có)
                   - Các hoạt động dạy và học chi tiết (Khởi động, Khám phá, Thực hành, Vận dụng). Trong từng hoạt động phải chỉ rõ hoạt động của Giáo viên và Học sinh.
                3. Ngôn từ sư phạm chuẩn mực, trình bày đẹp mắt bằng định dạng Markdown (sử dụng các tiêu đề, bảng, dấu đầu dòng rõ ràng).
                """
                
                # Gửi yêu cầu cho AI và nhận kết quả
                response = model.generate_content(prompt)
                
                st.success("🎉 Đã soạn xong giáo án thành công!")
                st.markdown(response.text)
                
                # Nút tải về dưới dạng văn bản text (Tùy chọn)
                st.download_button(label="📥 Tải giáo án về máy (.txt)", data=response.text, file_name=f"Giao_an_{chu_de}.txt", mime="text/plain")
                
            except Exception as e:
                st.error(f"🔴 Đã xảy ra lỗi hệ thống: {e}. Vui lòng kiểm tra lại API Key hoặc thử lại.")

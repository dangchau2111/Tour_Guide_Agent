import streamlit as st
import requests

# ==========================================
# CẤU HÌNH GIAO DIỆN TRANG WEB
# ==========================================
st.set_page_config(
    page_title="Quy Nhơn AI Tour Guide",
    page_icon="🏝️",
    layout="centered"
)

st.title("🏝️ Trợ Lý Du Lịch Quy Nhơn")
st.markdown("Xin chào! Mình là AI Tour Guide. Mình có thể giúp bạn tìm kiếm món ăn, nhà hàng, điểm tham quan và lên lịch trình chi tiết tại Quy Nhơn.")

# ==========================================
# HÀM GỌI FASTAPI CHÍNH THỨC
# ==========================================
def call_fastapi(user_message):
    """
    Hàm này gửi câu hỏi của người dùng đến FastAPI và nhận câu trả lời.
    """
    api_url = "http://localhost:8000/api/chat"
    
    # Payload khớp với Pydantic model (ChatRequest) bên FastAPI
    payload = {
        "user_prompt": user_message
    }
    
    try:
        # Gửi request POST đến API, cài đặt timeout để tránh treo app quá lâu
        response = requests.post(api_url, json=payload, timeout=60)
        
        # Kiểm tra xem API có trả về mã lỗi HTTP không (ví dụ: 404, 500)
        response.raise_for_status()
        
        # Lấy dữ liệu JSON trả về và trích xuất trường "data"
        result = response.json()
        return result.get("data", "Xin lỗi, mình không nhận được dữ liệu phản hồi từ hệ thống.")
        
    except requests.exceptions.ConnectionError:
        return "⚠️ Lỗi kết nối: Không thể kết nối đến máy chủ. Bạn hãy kiểm tra xem FastAPI đã được chạy chưa nhé."
    except requests.exceptions.Timeout:
        return "⚠️ Lỗi thời gian chờ: Hệ thống đang xử lý quá lâu, vui lòng thử lại sau."
    except Exception as e:
        return f"⚠️ Đã xảy ra lỗi hệ thống: {str(e)}"

# ==========================================
# QUẢN LÝ LỊCH SỬ TRÒ CHUYỆN (SESSION STATE)
# ==========================================
# Kiểm tra xem lịch sử chat đã tồn tại chưa, nếu chưa thì tạo mới với lời chào
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Chào bạn! Rất vui khi được gặp bạn, mình có thể hỗ trợ cho bạn những gì về du lịch Quy Nhơn nhỉ?"}
    ]

# Render lại toàn bộ tin nhắn cũ mỗi khi ứng dụng tải lại
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# XỬ LÝ KHI NGƯỜI DÙNG NHẬP CÂU HỎI
# ==========================================
if user_input := st.chat_input("Nhập câu hỏi của bạn tại đây..."):
    
    # 1. Hiển thị tin nhắn của người dùng
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Hiển thị trạng thái chờ và gọi API thực tế
    with st.chat_message("assistant"):
        with st.spinner("Đang phân tích yêu cầu và tìm kiếm thông tin..."):
            
            # GỌI FASTAPI TẠI ĐÂY
            bot_response = call_fastapi(user_input)
            
            # Hiển thị kết quả
            st.markdown(bot_response)
            
    # 3. Lưu tin nhắn của AI vào lịch sử
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
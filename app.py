import streamlit as st
from pathlib import Path
import hashlib
import google.generativeai as genai

# 설정
genai.configure(api_key="AIzaSyAIrfL3t3dbg6R-tQJhSiY1sXMw5UVfPL0")

# 생성 설정
generation_config = {
  "temperature": 0.9,
  "top_p": 0.95,
  "top_k": 32,
  "max_output_tokens": 1024,
}

safety_settings = [
  {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
  {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def main():
    st.title("이미지 용도 제안 AI 서비스")
    
    uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="업로드된 이미지", use_column_width=True)
        
        image_path = f"uploaded_image.{uploaded_file.name.split('.')[-1]}"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 파일 해시 생성
        file_hash = hashlib.sha256(uploaded_file.getbuffer()).hexdigest()
        
        prompt_parts = [
            "이미지의 물건에 대한 다양한 용도를 제시해줘. 가장 기본적인 용도부터. 정말 이색적인 사용처도 제시해줘. 한글로 답변해줘",
            "Object: ",
            genai.upload_file(image_path),
            "Description: 이미지에 대한 설명을 여기에 입력하세요.",
        ]

        response = model.generate_content(prompt_parts)
        st.subheader("이미지 용도 제안")
        st.write(response.text)

if __name__ == "__main__":
    main()

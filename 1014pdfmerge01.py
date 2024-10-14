import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO
import time

st.title("PDF 파일 합치기")

# HTML을 사용하여 글자 크기 조절
st.markdown("<h3 style='font-size: 150%;'>한국건설기술인협회 PDF 병합 프로그램 😎</h3>", unsafe_allow_html=True)

# 파일 업로드
st.title("파일 업로드")
uploaded_files = st.file_uploader("2개 이상의 PDF 파일을 업로드하세요", type=["pdf"], accept_multiple_files=True)

if uploaded_files and len(uploaded_files) > 1:
    # 사용자에게 파일 순서를 선택할 수 있도록 함
    file_names = [file.name for file in uploaded_files]
    selected_order = st.multiselect("병합할 파일 순서를 선택하세요", file_names, default=file_names)
    
    # 선택한 순서에 따라 파일 병합
    if selected_order and len(selected_order) == len(file_names):
        merger = PdfMerger()
        
        # 선택된 순서대로 파일 병합
        for selected_file in selected_order:
            for pdf in uploaded_files:
                if pdf.name == selected_file:
                    merger.append(pdf)
        
        # 병합된 PDF를 메모리에 저장
        merged_pdf = BytesIO()
        merger.write(merged_pdf)
        merger.close()
        merged_pdf.seek(0)
        
        # 다운로드 버튼
        st.success("PDF 파일이 성공적으로 병합되었습니다.")
        st.download_button(
            label="병합된 PDF 다운로드",
            data=merged_pdf,
            file_name="merged_file.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("모든 파일의 순서를 선택하세요.")
else:
    st.info("2개 이상의 PDF 파일을 업로드하세요.")

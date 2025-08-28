import streamlit as st
import mariadb
import pandas as pd
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="Room2 목록",
    page_icon="🏠",
    layout="wide"
)

def get_room2_data():
    """room2 테이블 데이터 가져오기"""
    try:
        conn = mariadb.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        
        # room2 테이블 모든 데이터 가져오기
        df = pd.read_sql("SELECT * FROM room2", conn)
        conn.close()
        return df
        
    except Exception as e:
        st.error(f"데이터 조회 실패: {e}")
        return None

# 메인 화면
st.title(" Room2 데이터 목록")
st.markdown("---")

# 데이터 가져오기
df = get_room2_data()

if df is not None and not df.empty:
    # 총 개수 표시
    st.subheader(f" 총 {len(df)}개의 데이터")
    
    # 데이터 목록 표시
    st.dataframe(
        df,
        use_container_width=True,
        height=600
    )
    
else:
    st.warning(" 데이터가 없습니다.")
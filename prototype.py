# bangoo_full_embed.py
# 회원가입/로그인/게스트 → 셀렉(매물검색) 올인원 Streamlit 앱

import streamlit as st
import datetime
import folium
from streamlit_folium import st_folium
import time
from PIL import Image

st.markdown("""
<style>
/* 모든 기본 버튼에 연한 살구색 배경 */
div.stButton > button {
  background: #ffe3d9; 
  border: 1px solid #ffd2c5; 
  color: #222;
  border-radius: 8px; 
  font-weight: 700; 
  height: 40px;
  transition: all 0.2s ease;
}

/* 버튼 호버 효과 (채도 더 어둡게) */
div.stButton > button:hover {
  background: #ffb89f !important;
  border: 1px solid #ff9d7a !important;
}

/* 버튼 클릭/활성 효과 (더 어둡게) */
div.stButton > button:active {
  background: #ff9d7a !important;
  border: 1px solid #ff8355 !important;
}

/* 게스트 버튼 (회색) */
button[kind="secondary"] { 
  background: #ddd !important; 
  border-color: #d0d0d0 !important; 
}

/* 게스트 버튼 호버 효과 (짙은 회색) */
button[kind="secondary"]:hover { 
  background: #888 !important; 
  border-color: #777 !important; 
}

/* 게스트 버튼 클릭 효과 */
button[kind="secondary"]:active { 
  background: #666 !important; 
  border-color: #555 !important; 
}

.st-key-box {
    width : 700px;
    display: flex;
    height: auto;
    align-items: center;
    margin: 0 auto;
}

</style>
""", unsafe_allow_html=True)

# -------------------- 세션 상태 --------------------
if "step" not in st.session_state:
    st.session_state["step"] = "메인"

def go(step: str):
    st.session_state["step"] = step
    st.rerun()

# -------------------- 헤더 정의 --------------------
def page_header(page_name):
    img = Image.open('./bangu.png')
    col1, col2, e1, col3, e2 = st.columns([1,1,1,3,1])
    with col1:
        st.image(img, width=150)
    with col2:
        st.header("방구")
    with col3:
        st.title(page_name)
    st.divider()

# -------------------- 페이지 정의 --------------------
def page_home():
    st.markdown(
        """
        <div style="text-align:center; padding: 60px 0 40px 0;">
            <h1 style="font-size: 48px; margin-bottom: 16px; font-weight: 800;">방구</h1>
            <p style="font-size:20px; color: #666; margin-bottom: 50px;">사회 초년생들을 위한 원룸 구하기 서비스</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # wide 레이아웃에서도 가운데 정렬되도록 더 넓은 여백 사용
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col2:
        # 로그인, 회원가입 버튼 (같은 줄에 균등하게)
        login_col, signup_col = st.columns(2, gap="medium")
        
        with login_col:
            if st.button("로그인", key="home_login", type="primary", use_container_width=True):
                go("로그인")
        
        with signup_col:
            if st.button("회원가입", key="home_signup", type="primary", use_container_width=True):
                go("회원가입")
        
        # 간격 추가
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # 게스트 버튼 (정중앙에 적당한 크기로)
        guest_col1, guest_col2, guest_col3 = st.columns([0.5, 1, 0.5])
        with guest_col2:
            if st.button("게스트로 이용", key="home_guest", type="secondary", use_container_width=True):
                # 게스트 모드로 설정하고 알림 후 셀렉으로 이동
                st.session_state["guest_mode"] = True
                st.info("게스트로 이용 시 일부 기능이 제한됩니다")
                time.sleep(1.5)
                go("셀렉")

def page_signup():
    st.set_page_config(layout="wide")
    page_header("회원가입")
    with st.container(key='box'):
        st.header("회원가입")
        st.text_input("아이디", key="su_id")
        st.text_input("비밀번호", type="password", key="su_pw")
        st.text_input("닉네임", key="su_nick")
        birth = st.date_input("생일", value=datetime.date(2000, 1, 1), key="su_birth")
        st.selectbox("성별", ["성별 선택", "남성", "여성", "기타/응답안함"], key="su_gender")

        # 회원가입 완료 버튼을 성별 선택 바로 아래에 배치
        if st.button("회원가입", key="signup_submit", type="primary", use_container_width=True):
            st.success(f"회원가입 완료! 선택한 생일: {birth}")
            st.session_state["guest_mode"] = False  # 회원가입 후엔 게스트 모드 해제
            go("셀렉")
        
        # 간격 추가
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # 뒤로가기 버튼을 왼쪽에 배치
        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            if st.button("뒤로가기", key="signup_back"):
                st.set_page_config(layout="centered")
                go("메인")

def page_login():
    st.header("로그인")
    st.text_input("아이디", key="li_id")
    st.text_input("비밀번호", type="password", key="li_pw")

    # 로그인 버튼을 비밀번호 바로 아래에 배치
    if st.button("로그인", key="login_submit", type="primary", use_container_width=True):
        st.success("로그인 성공 (데모)")
        st.session_state["guest_mode"] = False  # 로그인 후엔 게스트 모드 해제
        go("셀렉")
    
    # 간격 추가
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # 뒤로가기 버튼을 왼쪽에 배치
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        if st.button("뒤로가기", key="login_back"):
            go("메인")

    # 아이디/비밀번호 찾기 링크
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <span style='cursor: pointer; text-decoration: underline;'>[아이디 찾기]</span>
            &nbsp;&nbsp;&nbsp;
            <span style='cursor: pointer; text-decoration: underline;'>[비밀번호 찾기]</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

def page_guest():
    # 이제 이 페이지는 사용하지 않음 - 바로 셀렉으로 이동
    go("셀렉")

# -------------------- 셀렉 페이지 (원래 select_web_demo.py 내용) --------------------
def format_money(amount):
    """숫자를 억/만원 단위로 포맷"""
    if amount >= 10000:
        억 = amount // 10000
        만 = amount % 10000
        return f"{억}억" if 만 == 0 else f"{억}억 {만}만원"
    else:
        return f"{amount}만원"

def option_tab_1():
    tab1, tab2, tab3 = st.tabs(['구조', '층 수 옵션', '전용 면적'])
    # Tab1: 구조
    with tab1:
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        if col1.button("전체", key="structure_all"): st.session_state['selected']="전체"
        if col2.button("오픈형(방1)", key="structure_open"): st.session_state['selected']="오픈형"
        if col3.button("분리형(방1,거실1)", key="structure_sep"): st.session_state['selected']="분리형"
        if col4.button("복층형", key="structure_duplex"): st.session_state['selected']="복층형"
        st.write("선택:", st.session_state.get('selected',"없음"))

    # Tab2: 층수
    with tab2:
        c1,c2 = st.columns(2); c3,c4 = st.columns(2)
        if c1.button("전체", key="floor_all"): st.session_state['floor']="전체"
        if c2.button("지상층", key="floor_ground"): st.session_state['floor']="지상층"
        if c3.button("반지하", key="floor_half"): st.session_state['floor']="반지하"
        if c4.button("옥탑", key="floor_roof"): st.session_state['floor']="옥탑"
        st.write("선택:", st.session_state.get('floor',"없음"))

    # Tab3: 면적
    with tab3:
        cols = st.columns(4)+st.columns(4)
        areas=["전체","10평 이하","10평대","20평대","30평대","40평대","50평대","60평 이상"]
        for i,(col, area) in enumerate(zip(cols, areas)):
            if col.button(area, key=f"area_{i}"):
                st.session_state['area']=area
        st.write("선택:", st.session_state.get('area',"없음"))


def option_tab_2():
    c1,c2,c3 = st.columns(3)
    if c1.button("에어컨"): st.session_state['opt']="에어컨"
    if c2.button("냉장고"): st.session_state['opt']="냉장고"
    if c3.button("세탁기"): st.session_state['opt']="세탁기"
    st.write("선택:", st.session_state.get('opt',"없음"))

def page_select():
    st.set_page_config(layout="wide")
    
    # 게스트 모드일 때 알림 표시
    if st.session_state.get("guest_mode", False):
        st.warning("⚠️ 게스트로 이용 시 일부 기능이 제한됩니다")
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    st.header("🌎 방구 | 원룸 매물 검색 어플 | 셀렉")

    st.sidebar.title("🔍 검색 필터")
    building_types=['원룸','투룸','오피스텔','아파트']
    selected_types=[t for t in building_types if st.sidebar.checkbox(t)]
    st.sidebar.write("선택된 유형:", selected_types)

    with st.sidebar.expander("구조/면적"):
        option_tab_1()
    with st.sidebar.expander("옵션"):
        option_tab_2()

    st.sidebar.toggle("주차 가능만 보기")

    with st.sidebar.expander("전세"):
        p=st.slider("전세금(만원)",1000,30000,(3000,10000),step=200)
        st.write(format_money(p[0]), "~", format_money(p[1]))
    with st.sidebar.expander("월세"):
        d=st.slider("보증금(만원)",500,10000,(2000,5000),step=100)
        r=st.slider("월세(만원)",10,300,(30,80),step=10)
        st.write("보증금:",format_money(d[0]),"~",format_money(d[1]))
        st.write("월세:",format_money(r[0]),"~",format_money(r[1]))

    if st.sidebar.button("검색"): st.write("검색 실행!")

    m=folium.Map(location=[37.513083,126.938559],zoom_start=16)
    folium.Marker(location=[37.5662952,126.9779451]).add_to(m)
    st_folium(m, use_container_width=True, height=600)
    
    if st.button("뒤로가기"):
        st.set_page_config(layout="centered")
        go("메인")

# -------------------- 라우팅 --------------------
page = st.session_state["step"]
if page=="메인": page_home()
elif page=="회원가입": page_signup()
elif page=="로그인": page_login()
elif page=="게스트": page_guest()
elif page=="셀렉": page_select()
else: page_home()
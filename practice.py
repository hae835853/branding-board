import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- 차단 걱정 없는 RSS 방식 크롤링 함수 ---
def get_branding_rss(keyword):
    # 구글 뉴스 RSS 피드를 이용 (차단이 거의 없음)
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, features="xml") # RSS는 xml 형식을 사용함
        
        items = soup.findAll('item')
        results = []
        
        for item in items[:6]: # 6개만 가져오기
            title = item.title.text
            link = item.link.text
            results.append({"title": title, "link": link})
        return results
    except Exception as e:
        st.error(f"연결 중 오류 발생: {e}")
        return []

# --- 웹 화면 구성 (디자인 레이아웃) ---
st.set_page_config(page_title="브랜딩 스터디", layout="wide")

st.title("🎨 마케팅 & 브랜딩 인사이트 보드")

# 안내 문구 박스
st.info("💡 **알림:** 아래 버튼을 누르면 실시간 브랜딩 스터디 자료를 수집합니다.")

# 탭 구성
tab1, tab2 = st.tabs(["🚀 브랜드 성공 사례", "💡 마케팅 전략"])

with tab1:
    st.subheader("🏁 최신 브랜드 케이스 스터디")
    if st.button("성공 사례 새로고침"):
        with st.spinner('데이터를 안전하게 가져오는 중...'):
            # '브랜딩 사례'로 검색
            data = get_branding_rss("브랜딩 사례")
            if data:
                for item in data:
                    # 깔끔한 박스 형태로 출력
                    st.markdown(f"📦 **[{item['title']}]({item['link']})**")
            else:
                st.warning("현재 가져올 수 있는 자료가 없습니다. 잠시 후 다시 시도해 주세요.")

with tab2:
    st.subheader("🔍 최신 마케팅 트렌드")
    if st.button("마케팅 트렌드 새로고침"):
        with st.spinner('인사이트 수집 중...'):
            # '마케팅 트렌드'로 검색
            data = get_branding_rss("마케팅 트렌드")
            if data:
                for item in data:
                    st.info(f"💎 [{item['title']}]({item['link']})")
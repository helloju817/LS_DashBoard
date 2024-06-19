import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_extras.let_it_rain import rain

# 이미지 로드
image1 = Image.open('images\OIL.png')
image2 = Image.open('images\yeah.png')

st.set_page_config(
    page_title="OIL ANALYSIS LAB",
    page_icon=image1,  # 이모지로 페이지 아이콘 설정
    layout="wide",
    initial_sidebar_state="expanded",
)

st.image(image2, width=400)

# 이미지와 제목 출력
col1, col2 = st.columns([0.7, 8])  # 첫 번째 컬럼은 이미지를 넓게, 두 번째 컬럼은 비우기 위해 사용

with col1:
    st.image(image1, width=100)
with col2:
    st.title('ABOUT US')

rain(emoji="🛢️",font_size=54,falling_speed=10,animation_length=5)
"""
------------------
"""

st.markdown(
    """


## 👨🏻‍🔧 적절한 시기의 오일 교체를 위한 대시보드

이상 오일로 가동된 차량은 쉽게 부식되며 이러한 상태가 지속되었을 경우 고장이 발생될 가능성이 있습니다. 이는 정확한 오일 교체 시기 및 이상 오일을 판단하여 적절한 시기에 교환과 수리를 필요로 합니다.
이러한 요구에 부응하기 위해, 저희 OIL LAB은 뛰어난 오일 진단기술을 이용하여 건설기계 오일 상태 데이터를 기반으로 하는 최첨단 대시보드를 소개합니다.
이 대시보드는 데이터를 효율적으로 시각화하고, 오일의 상태 조회 서비스를 제공하여 교체시기와 수리여부를 알 수 있는 등의 모든 측면을 개선할 수 있도록 설계되었습니다.

---

### 🙌핵심 기능 및 이점

이상 오일 사용으로 발생된 건설 차량 고장으로 인한 큰 비용 지출 및 인명 사고를 예방합니다. 

또, 기름이 새어 나오는 누유나 폐유의 양을 줄이게 되면 토양 및 수질 오염을 줄여 환경 보호에도 이바지 합니다.

---

### 📊 실시간 데이터 시각화

추출한 오일을 여러 방면으로 분석하여 데이터의 형태로 만들고 이를 시각화합니다. 이 시각화를 통하여 오일 상태를 한눈에 파악할 수 있으며, 사용자의 빠른 의사결정을 도웁니다.

---

### 🤖 현재 오일상태 분석

과거 데이터를 기반으로 현재의 오일 상태를 예측합니다. 예측 분석 기능을 통해 현재 차량오일 상태를 직관적으로 파악하여 건설차량 운영작업의 질을 향상시킬 수 있습니다.

---

### 🗺 맞춤형 대시보드

사용자의 필요에 맞게 대시보드를 맞춤화할 수 있습니다. 각 사용자에게 가장 유용한 정보를 손쉽게 확인할 수 있도록 합니다.

"""
)

# 사이드바에 파일 업로더 추가
uploaded_file = st.sidebar.file_uploader("📤데이터 파일 업로드", type=['csv'])

"""
--------------------------
"""

if uploaded_file is not None:
    
    # 업로드된 파일을 데이터프레임으로 읽기
    df = pd.read_csv(uploaded_file)

    # 데이터프레임 확인
    st.write("### 📥업로드된 데이터")
    st.write(df.head())
    
    # 업로드 완료 안내 메시지
    st.sidebar.success('✅분석 준비 완료!')
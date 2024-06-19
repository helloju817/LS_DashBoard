import streamlit as st
from PIL import Image

# 페이지 설정
st.set_page_config(
    page_icon="https://www.blackstone-labs.com/wp-content/themes/blackstone/favicon.png",
)

# 페이지 제목과 설명
st.markdown("""
    <style>
    .center-text {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="center-text">💼 우리의 못다한 이야기 💼</h1>', unsafe_allow_html=True)
st.markdown('<p class="center-text">여기에는 우리가 프로젝트를 진행하며 찍은 함께한 시간들을 추억해봐요! 😊</p>', unsafe_allow_html=True)

# 이미지 파일 경로 리스트
image_paths = [
    r'images\image5.jpg',
    r'images\image2.jpg',
    r'images\image4.jpg',
    r'images\image7.jpg',
    r'images\image3.jpg',
    r'images\image6.jpg'
]

# 각 이미지에 대한 설명 리스트
descriptions = [
    '💡 첫 번째 미팅에서 아이디어를 논의하는 모습',
    '📅 두 번째 스프린트 계획 회의',
    '🔍 중간 점검 회의에서의 모습',
    '🎨 리뷰 및 피드백 세션',
    '💻 코딩하면서 토론하는 모습',
    '📢 최종 발표 준비하는 모습'
]

# 이미지를 2개씩 한 행에 표시하기 위한 레이아웃 설정
cols = st.columns(2)

for i, (image_path, description) in enumerate(zip(image_paths, descriptions)):
    with cols[i % 2]:
        image = Image.open(image_path)
        st.image(image, caption=description, use_column_width=True)

st.markdown('<p class="center-text subtitle">이 프로젝트는 우리의 몰입과 열정을 담은 결과물입니다. 🌱</p>', unsafe_allow_html=True)

# 마지막 이미지를 크게 삽입
st.markdown("##")
last_image_path = r'images\image1.jpg'
last_image = Image.open(last_image_path)
st.image(last_image, caption='LS빅데이터스쿨에서 다함께 지내며 감사했습니다! 🎓', use_column_width=True)

# 감동적인 텍스트 추가
st.markdown(
    """
    <style>
    .highlight {
        font-size: 1.2em;
        font-weight: bold;
        color: #ff6347;
        text-align: center;
    }
    .subtitle {
        font-size: 1.1em;
        color: #2e8b57;
        text-align: center;
    }
    .emphasis {
        color: #ff4500;
        font-weight: bold;
    }
    .center-text {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True
)
st.balloons()
st.markdown('<p class="center-text">함께한 시간들에 감사드리며, 앞으로도 더 큰 성과를 이루길 바랍니다! 🙌</p>', unsafe_allow_html=True)

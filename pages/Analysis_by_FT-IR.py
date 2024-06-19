import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 정상 출력 설정

# CSV 파일을 읽어오기
file_path = r'C:\Users\USER\projects\Group4_dashboard\data\train_for_streamlit.csv'
df = pd.read_csv(file_path)

# 특정 열만 선택하기
columns_to_display = ['COMPONENT_ARBITRARY', 'FH2O', 'FNOX', 'FOXID', 'FSO4', 'FTBN']
df_selected = df[columns_to_display]

# COMPONENT_ARBITRARY 열의 고유값들을 가져오기
unique_values = df_selected['COMPONENT_ARBITRARY'].unique()

# 고유값들로 필터 만들기 (하나의 값만 선택할 수 있도록 selectbox 사용)
selected_value = st.selectbox('컴포넌트 선택', unique_values)

# 데이터 필터링
if selected_value:
    df_filtered = df_selected[df_selected['COMPONENT_ARBITRARY'] == selected_value]
else:
    df_filtered = df_selected

# 결측값 비율 계산
# COMPONENT_ARBITRARY 열을 제외하고 결측치 비율 계산
cols_to_calculate_missing_ratio = df_filtered.columns[df_filtered.columns != 'COMPONENT_ARBITRARY']
missing_ratio = df_filtered[cols_to_calculate_missing_ratio].isnull().mean() * 100

# 선택한 열을 Streamlit 앱에 표시하기 (전체 너비 사용)
st.dataframe(df_filtered, use_container_width=True)

# 결측값 비율 출력
st.write('### 결측치 비율')
st.write('각 열의 결측치 비율을 표시')

# 결측치 비율을 보기 좋게 테이블로 출력
missing_ratio_df = pd.DataFrame(missing_ratio, columns=['결측치 비율'])
missing_ratio_df.index.name = '열 이름'
st.table(missing_ratio_df)

# 추가적인 설명을 위한 텍스트 블록
st.write("""
    COMPONENT1에서 FT-IR을 이용한 원소 측정이 이루어졌음을 알 수 있다.
""")

# COMPONENT_ARBITRARY가 'COMPONENT1'인 데이터 필터링
df_component1 = df[df['COMPONENT_ARBITRARY'] == 'COMPONENT1']

# 변수 리스트
variables = ['FH2O', 'FNOX', 'FOXID', 'FSO4', 'FTBN']

# 드롭다운 형태로 변수 선택
selected_variable = st.selectbox('변수 선택', variables)

# 선택한 변수에 대한 Y_LABEL의 분포를 violin plot으로 시각화
st.write(f'### {selected_variable} 값에 따른 Y_LABEL 분포 (COMPONENT_ARBITRARY = COMPONENT1)')
plt.figure(figsize=(12, 6))
sns.violinplot(x='Y_LABEL', y=selected_variable, data=df_component1, palette='Set2', inner='quartile')
plt.xlabel('Y_LABEL', fontsize=12)
plt.ylabel(selected_variable, fontsize=12)
plt.title(f'{selected_variable} 값에 따른 Y_LABEL 분포', fontsize=14)
st.pyplot(plt)

# 추가적인 설명을 위한 텍스트 블록
st.write("""
    **분석 설명:**
    - 각 violin plot은 COMPONENT_ARBITRARY가 'COMPONENT1'일 때, 선택된 변수의 값에 따른 Y_LABEL의 분포를 시각화한 것입니다.
    - 선택된 변수에 대해 Y_LABEL이 0값을 갖는지 1값을 갖는지 확인할 수 있습니다.
""")

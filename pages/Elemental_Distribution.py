import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 정상 출력 설정

# CSV 파일을 읽어오기
file_path = r'C:\Users\USER\projects\Group4_dashboard\data\train_for_streamlit.csv'
df = pd.read_csv(file_path)

# 특정 열만 선택하기 (AG, AL, B, BA, BE, CA, CD, CO, CR, CU, FE, K, LI, MG, MN, MO, NA, NI, P, PB, S, SB, SI, SN, TI, V, ZN)
columns_to_display = ['COMPONENT_ARBITRARY', 'AG', 'AL', 'B', 'BA', 'BE', 'CA', 'CD', 'CO', 'CR', 'CU', 'FE', 'K',
                      'LI', 'MG', 'MN', 'MO', 'NA', 'NI', 'P', 'PB', 'S', 'SB', 'SI', 'SN', 'TI', 'V', 'ZN']
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

# 결측값 비율 출력 (결측치 비율이 0이 아닌 열만 표시)
st.write('### 결측치 비율 (결측치 비율이 0이 아닌 열만 표시)')
st.write('각 열의 결측치 비율을 표시')

# 결측치 비율을 보기 좋게 테이블로 출력
missing_ratio_non_zero_df = pd.DataFrame(missing_ratio[missing_ratio != 0], columns=['결측치 비율'])
missing_ratio_non_zero_df.index.name = '열 이름'
st.table(missing_ratio_non_zero_df)

# 추가적인 설명을 위한 텍스트 블록
st.write("""
    COMPONENT_ARBITRARY가 'COMPONENT1'에서 AG, AL, B, BA, BE, CA, CD, CO, CR, CU, FE, K, LI, MG, MN, MO, NA, NI, P, PB, S, SB, SI, SN, TI, V, ZN 값을 분석합니다.
""")

# COMPONENT_ARBITRARY가 'COMPONENT1'인 데이터 필터링
df_component1 = df[df['COMPONENT_ARBITRARY'] == 'COMPONENT1']

# 변수 리스트 (AG, AL, B, BA, BE, CA, CD, CO, CR, CU, FE, K, LI, MG, MN, MO, NA, NI, P, PB, S, SB, SI, SN, TI, V, ZN)
variables = columns_to_display[1:]  # 'COMPONENT_ARBITRARY' 제외한 나머지 변수

# 변수 선택 드롭다운 추가
selected_variable = st.selectbox('변수 선택', variables)

# Y_LABEL이 1이 되는 값의 범위 히스토그램 시각화
st.write(f'### {selected_variable} 값이 Y_LABEL = 1 일 때와 Y_LABEL = 0 일 때의 범위')
fig, ax = plt.subplots(figsize=(12, 6))

# Y_LABEL = 1일 때의 히스토그램
sns.histplot(df_component1[df_component1['Y_LABEL'] == 1][selected_variable], bins=20, kde=False, color='red', alpha=0.5, label='Y_LABEL = 1', edgecolor='black', ax=ax)

# Y_LABEL = 0일 때의 히스토그램
sns.histplot(df_component1[df_component1['Y_LABEL'] == 0][selected_variable], bins=20, kde=False, color='blue', alpha=0.5, label='Y_LABEL = 0', edgecolor='black', ax=ax)

ax.set_xlabel(selected_variable, fontsize=12)
ax.set_ylabel('빈도', fontsize=12)
ax.set_title(f'{selected_variable} 값의 Y_LABEL에 따른 분포', fontsize=14)
ax.legend()
st.pyplot(fig)

# 추가적인 설명을 위한 텍스트 블록
st.write("""
    **분석 설명:**
    - 각 변수에 대해 Y_LABEL이 1이 되는 값과 0이 되는 값의 범위를 히스토그램으로 시각화하였습니다.
    - 이를 통해 각 변수가 Y_LABEL = 1을 예측하는 데 어떤 값 범위에서 중요한 역할을 할 수 있는지 확인할 수 있습니다.
""")

# 선택한 변수에 대해 모든 컴포넌트에 대한 Y_LABEL 값에 따른 히스토그램 시각화 함수 정의
def plot_histogram_for_variable(df, variable, label_value, color, alpha=0.5):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(df[df['Y_LABEL'] == label_value][variable], bins=20, kde=False, color=color, alpha=alpha, edgecolor='black', ax=ax)
    ax.set_xlabel(variable, fontsize=12)
    ax.set_ylabel('빈도', fontsize=12)
    ax.set_title(f'{variable} 값이 Y_LABEL = {label_value} 일 때의 범위', fontsize=14)
    return fig

# 모든 컴포넌트에 대해 Y_LABEL 값에 따른 히스토그램 시각화
for component in unique_values:
    st.write(f'### 컴포넌트: {component}')
    
    # COMPONENT_ARBITRARY가 해당 컴포넌트인 데이터 필터링
    df_component = df[df['COMPONENT_ARBITRARY'] == component]
    
    # Y_LABEL = 1 인 경우 히스토그램 시각화
    plt_histogram_label1 = plot_histogram_for_variable(df_component, selected_variable, 1, 'red')
    
    # Y_LABEL = 0 인 경우 히스토그램 시각화
    plt_histogram_label0 = plot_histogram_for_variable(df_component, selected_variable, 0, 'blue', alpha=0.5)
    
    # 그래프 출력
    st.pyplot(plt_histogram_label1)
    st.pyplot(plt_histogram_label0)

    # 추가적인 설명
    st.write("""
    **분석 설명:**
    - 각 컴포넌트에 대해 선택한 변수가 Y_LABEL = 1 또는 Y_LABEL = 0 일 때의 범위를 히스토그램으로 시각화하였습니다.
    """)

    # 플롯 초기화 (중요)
    plt_histogram_label1.clf()
    plt_histogram_label0.clf()
    
    # 선택한 COMPONENT_ARBITRARY 값에 따라 히스토그램 표시
if selected_component:
    st.write(f'### {selected_component}의 변수별 Y_LABEL 값에 따른 히스토그램')

    # COMPONENT_ARBITRARY가 선택된 값인 데이터 필터링
    df_component = df[df['COMPONENT_ARBITRARY'] == selected_component]

    # 변수 리스트 (AG, AL, B, BA, BE, CA, CD, CO, CR, CU, FE, K, LI, MG, MN, MO, NA, NI, P, PB, S, SB, SI, SN, TI, V, ZN)
    variables = columns_to_display[1:]  # 'COMPONENT_ARBITRARY' 제외한 나머지 변수

    # 변수 선택 드롭다운 추가
    selected_variable = st.selectbox('변수 선택', variables)

    # Y_LABEL이 1일 때와 0일 때의 범위 히스토그램 시각화
    fig, ax = plt.subplots(figsize=(12, 6))

    # Y_LABEL = 1일 때의 히스토그램
    sns.histplot(df_component[df_component['Y_LABEL'] == 1][selected_variable], bins=20, kde=False, color='red',
                 alpha=0.5, label='Y_LABEL = 1', edgecolor='black', ax=ax)

    # Y_LABEL = 0일 때의 히스토그램
    sns.histplot(df_component[df_component['Y_LABEL'] == 0][selected_variable], bins=20, kde=False, color='blue',
                 alpha=0.5, label='Y_LABEL = 0', edgecolor='black', ax=ax)

    ax.set_xlabel(selected_variable, fontsize=12)
    ax.set_ylabel('빈도', fontsize=12)
    ax.set_title(f'{selected_variable} 값의 Y_LABEL에 따른 분포', fontsize=14)
    ax.legend()
    st.pyplot(fig)

    # 추가적인 설명
    st.write("""
        **분석 설명:**
        - 선택한 COMPONENT_ARBITRARY 값에 따라 변수가 Y_LABEL = 1 또는 Y_LABEL = 0 일 때의 범위를 히스토그램으로 시각화하였습니다.
    """)
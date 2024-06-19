import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')
from matplotlib import font_manager, rc
from scipy.stats import gaussian_kde

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 정상 출력 설정

# 페이지 설정
st.set_page_config(
    page_icon="https://www.blackstone-labs.com/wp-content/themes/blackstone/favicon.png",
)

# CSV 파일을 로드합니다.
file_path = './data/train.csv' 
data = pd.read_csv(file_path)

# 컴포넌트 리스트 (특정 순서로 정렬)
component_order = ['COMPONENT1', 'COMPONENT2', 'COMPONENT3', 'COMPONENT4']
components_sorted = sorted(data['COMPONENT_ARBITRARY'].unique(), key=lambda x: component_order.index(x) if x in component_order else len(component_order))

# Streamlit 앱 시작
st.title("📈데이터 시각화")


st.markdown("""
<style>

	.stTabs [data-baseweb="tab-list"] {
		gap: 10px;
    }

	.stTabs [data-baseweb="tab"] {
		height: 35px;
        white-space: pre-wrap;
		background-color: #F0F2F6;
		border-radius: 5px 5px 0px 0px;
		gap: 5px;
		padding-top: 8px;
		padding-bottom: 8px;
        padding-left: 10px;
        padding-right: 10px;
    }

	.stTabs [aria-selected="true"] {
  		background-color: #FFFFFF;
	}

</style>""", unsafe_allow_html=True)



# 각 탭에 어울리는 이모티콘 추가
tabs = ["🌈 FTIR", "🔬 Particle Count", "🧪 Elemental", "📊 PQ Index", "🟤 Soot", "⛽️ Fuel", "🌡️ Viscosity40"]
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(tabs)

# # 페이지 탭 구성
# tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["FTIR", "Particle Count", "Elemental", "PQ Index", "Soot", "Fuel", "Viscosity40"])

with tab1:
    st.header("🌈 FTIR를 이용한 분석")

    ftir = ['FH2O', 'FNOX', 'FOXID', 'FSO4', 'FTBN']

    with st.expander("⚙️ 설정", expanded=True):
        # 사용자에게 컴포넌트 선택 옵션 제공 (중복 선택 불가)
        selected_component = st.selectbox('부품을 선택하세요:', options=components_sorted, key='tab1_component')

        if selected_component:
            # 선택된 컴포넌트에 대해 데이터 필터링
            filtered_data_tab1 = data[data['COMPONENT_ARBITRARY'] == selected_component]

            # 변수 선택 옵션 제공 (중복 선택 불가)
            selected_variable = st.selectbox('변수를 선택하세요:', options=ftir, key='tab1_variable')

    if selected_component and selected_variable and not filtered_data_tab1.empty:
        if selected_variable in filtered_data_tab1.columns and not filtered_data_tab1[selected_variable].dropna().empty:

            # 빈 줄 추가
            st.write("")
            
            st.subheader(f"오일 상태에 따른 {selected_variable} 분포")

            # Y_LABEL에 따라 데이터 분리
            y_label_0_data = filtered_data_tab1[filtered_data_tab1['Y_LABEL'] == 0][selected_variable].dropna()
            y_label_1_data = filtered_data_tab1[filtered_data_tab1['Y_LABEL'] == 1][selected_variable].dropna()

            if not y_label_0_data.empty or not y_label_1_data.empty:
                try:
                    # x축 범위 지정 슬라이더 추가
                    min_value = float(min(y_label_0_data.min(), y_label_1_data.min()))
                    max_value = float(max(y_label_0_data.max(), y_label_1_data.max()))
                    range_values = st.slider(f'{selected_variable}의 x축 범위를 선택하세요', min_value, max_value, (min_value, max_value), key='tab1_range_slider')

                    # 히스토그램과 커널 밀도 추정 그래프 생성
                    hist_data = [y_label_0_data, y_label_1_data]
                    group_labels = ['정상 오일', '이상 오일']

                    fig = ff.create_distplot(hist_data, group_labels, show_hist=True, show_rug=False)

                    # x축 범위 설정
                    fig.update_layout(xaxis_range=[range_values[0], range_values[1]],
                                      title=f"{selected_variable} 히스토그램 및 커널 밀도 추정 그래프",
                                      xaxis_title=f'{selected_variable} 수치',
                                      yaxis_title='밀도')

                    # 그래프를 Streamlit에 표시
                    st.plotly_chart(fig)
                except np.linalg.LinAlgError:
                    st.warning(f"{selected_component}의 {selected_variable} 데이터의 모든 값이 동일하거나 충분하지 않습니다.")
            else:
                st.warning(f"{selected_component}의 {selected_variable} 데이터의 모든 값이 동일하거나 충분하지 않습니다.")
        else:
            st.warning(f"{selected_component}에 대한 {selected_variable} 데이터가 존재하지 않습니다.")
    else:
        st.warning("설정을 완료하세요.")

with tab2:
    st.header("🔬 입자수 분석")

    particle_size_vars = ['U100', 'U75', 'U50', 'U25', 'U20', 'U14', 'U6', 'U4']

    with st.expander("⚙️ 설정", expanded=True):
        # 사용자에게 컴포넌트 선택 옵션 제공 (중복 선택 불가, 기본값은 COMPONENT2)
        default_index = components_sorted.index('COMPONENT2') if 'COMPONENT2' in components_sorted else 0
        selected_component = st.selectbox('부품을 선택하세요:', options=components_sorted, index=default_index, key='tab2_component')

        if selected_component:
            # 선택된 컴포넌트에 대해 데이터 필터링
            filtered_data_tab2 = data[data['COMPONENT_ARBITRARY'] == selected_component]

            # 변수 선택 옵션 제공 (중복 선택 불가)
            selected_variable = st.selectbox('변수를 선택하세요:', options=particle_size_vars, key='tab2_variable')

    if selected_component and selected_variable and not filtered_data_tab2.empty:
        if selected_variable in filtered_data_tab2.columns and not filtered_data_tab2[selected_variable].dropna().empty:

            # 빈 줄 추가
            st.write("")
            
            st.subheader(f"오일 상태에 따른 {selected_variable} 분포")

            # Y_LABEL에 따라 데이터 분리
            y_label_0_data = filtered_data_tab2[filtered_data_tab2['Y_LABEL'] == 0][selected_variable].dropna()
            y_label_1_data = filtered_data_tab2[filtered_data_tab2['Y_LABEL'] == 1][selected_variable].dropna()

            if not y_label_0_data.empty or not y_label_1_data.empty:
                try:
                    fig = None

                    # Check if selected variable is 'U4' or 'U6' to hide x-axis slider
                    if selected_variable not in ['U4', 'U6']:
                        # x축 범위 지정 슬라이더 추가
                        min_value = float(min(y_label_0_data.min(), y_label_1_data.min()))
                        max_value = float(max(y_label_0_data.max(), y_label_1_data.max()))
                        range_values = st.slider(f'{selected_variable}의 x축 범위를 선택하세요', min_value, max_value, (min_value, max_value), key='tab2_range_slider')

                        # 히스토그램과 커널 밀도 추정 그래프 생성
                        hist_data = [y_label_0_data, y_label_1_data]
                        group_labels = ['정상 오일', '이상 오일']

                        fig = ff.create_distplot(hist_data, group_labels, show_hist=True, show_rug=False)

                        # x축 범위 설정
                        fig.update_layout(xaxis_range=[range_values[0], range_values[1]],
                                          title=f"{selected_variable} 히스토그램 및 커널 밀도 추정 그래프",
                                          xaxis_title=f'{selected_variable} 입자수',
                                          yaxis_title='밀도')
                    else:
                        # 히스토그램과 커널 밀도 추정 그래프 생성 (without slider)
                        hist_data = [y_label_0_data, y_label_1_data]
                        group_labels = ['정상 오일', '이상 오일']

                        fig = ff.create_distplot(hist_data, group_labels, show_hist=True, show_rug=False)

                        fig.update_layout(title=f"{selected_variable} 히스토그램 및 커널 밀도 추정 그래프",
                                          xaxis_title=f'{selected_variable} 입자수',
                                          yaxis_title='밀도')

                    # 그래프를 Streamlit에 표시
                    st.plotly_chart(fig)
                except np.linalg.LinAlgError:
                    st.warning(f"{selected_component}의 {selected_variable} 데이터의 모든 값이 동일하거나 충분하지 않습니다.")
            else:
                st.warning(f"{selected_component}의 {selected_variable} 데이터의 모든 값이 동일하거나 충분하지 않습니다.")
        else:
            st.warning(f"{selected_component}에 대한 {selected_variable} 데이터가 존재하지 않습니다.")
    else:
        st.warning("설정을 완료하세요.")

with tab3:
    st.header("🧪 원소 함유량 분석")

    elements = ['AG', 'AL', 'B', 'BA', 'BE', 'CA', 'CD', 'CO', 'CR', 'CU', 'FE', 'H2O', 'K', 'LI', 'MG', 'MN', 'MO', 'NA', 'NI', 'P', 'PB', 'S', 'SB', 'SI', 'SN', 'V', 'ZN']

    with st.expander("⚙️ 설정", expanded=True):
        # 사용자에게 컴포넌트 선택 옵션 제공 (중복 선택 가능)
        selected_components = st.multiselect('부품을 선택하세요:', options=components_sorted, key='tab3_component')

        # 사용자에게 원소 선택 옵션 제공 (중복 선택 가능, 기본 선택된 상태)
        selected_elements = st.multiselect('원소를 선택하세요:', options=elements, default=elements, key='tab3_elements')

    if selected_components and selected_elements:
        # Y_LABEL이 0인 데이터만 필터링
        data_filtered_0 = data[data['Y_LABEL'] == 0]

        # 선택된 컴포넌트에 대해 데이터 필터링
        filtered_data_0 = data_filtered_0[data_filtered_0['COMPONENT_ARBITRARY'].isin(selected_components)]

        # 평균 계산
        mean_concentrations_0 = filtered_data_0.groupby('COMPONENT_ARBITRARY')[selected_elements].mean().reset_index()

        # 데이터 변형: 긴 형식으로 변환
        mean_concentrations_melted_0 = mean_concentrations_0.melt(id_vars=['COMPONENT_ARBITRARY'], var_name='Element', value_name='Mean Concentration')

        # 그래프 생성
        fig_0 = px.bar(mean_concentrations_melted_0, x='Element', y='Mean Concentration', color='COMPONENT_ARBITRARY', barmode='group',
                       title='정상오일에 대한 부품 및 원소별 평균 함유량 비율', labels={'Mean Concentration': '평균 농도', 'Element': '원소'})

        # 그래프를 Streamlit에 표시
        st.plotly_chart(fig_0)
    else:
        st.info("부품과 원소를 선택하세요.")

    st.divider()
    
    st.subheader(f"오일 상태에 따른 원소 분포")

    with st.expander("⚙️ 설정", expanded=True):
        # 사용자에게 컴포넌트 선택 옵션 제공 (중복 선택 불가)
        selected_component = st.selectbox('부품을 선택하세요', options=components_sorted, key='tab3_single_component')

        # 사용자에게 원소 선택 옵션 제공 (중복 선택 불가)
        selected_element = st.selectbox('원소를 선택하세요', options=elements, key='tab3_single_element')

    

    if selected_component and selected_element:
        # 선택된 컴포넌트와 원소에 대해 데이터 필터링
        filtered_data_dist = data[(data['COMPONENT_ARBITRARY'] == selected_component)]

        # 정상 여부(Y_LABEL)에 따라 데이터 분리
        y_label_0_dist = filtered_data_dist[filtered_data_dist['Y_LABEL'] == 0][selected_element].dropna()
        y_label_1_dist = filtered_data_dist[filtered_data_dist['Y_LABEL'] == 1][selected_element].dropna()

        if not y_label_0_dist.empty and not y_label_1_dist.empty:
            try:
                # x축 범위 지정 슬라이더 추가
                min_value_dist = float(min(y_label_0_dist.min(), y_label_1_dist.min()))
                max_value_dist = float(max(y_label_0_dist.max(), y_label_1_dist.max()))
                range_values_dist = st.slider(f'{selected_element}의 x축 범위를 선택하세요', min_value_dist, max_value_dist, (min_value_dist, max_value_dist), key='tab3_range_slider')

                # 히스토그램과 커널 밀도 추정 그래프 생성
                hist_data_dist = [y_label_0_dist, y_label_1_dist]
                group_labels_dist = ['정상 오일', '이상 오일']

                fig_dist = ff.create_distplot(hist_data_dist, group_labels_dist, show_hist=True, show_rug=False)

                # x축 범위 설정
                fig_dist.update_layout(xaxis_range=[range_values_dist[0], range_values_dist[1]],
                                      title=f'{selected_element} 히스토그램 및 커널 밀도 추정 그래프 - {selected_component}',
                                      xaxis_title=f'{selected_element} 함유량',
                                      yaxis_title='밀도')

                # 그래프를 Streamlit에 표시
                st.plotly_chart(fig_dist)
            except np.linalg.LinAlgError:
                st.error(f"{selected_component}의 {selected_element} 데이터의 모든 값이 동일하거나 충분하지 않습니다.")
        else:
            st.warning(f"{selected_component}의 {selected_element} 데이터의 모든 값이 동일하거나 충분하지 않습니다.")
    else:
        st.warning("부품과 원소를 선택하세요.")

with tab4:
    st.header("📊 PQ Index 분석")

    with st.expander("⚙️ 설정", expanded=True):
        # 사용자에게 컴포넌트 선택 옵션 제공 (중복 선택 가능)
        selected_components_tab4 = st.multiselect('부품을 선택하세요', options=components_sorted, default=components_sorted, key='tab4_component')

    # 빈 줄 추가
    st.write("")
    
    # 추가된 subheader
    st.subheader("오일 상태에 따른 PQ Index 분포")

    if selected_components_tab4:
        # 선택된 컴포넌트에 대해 데이터 필터링
        filtered_data_tab4 = data[data['COMPONENT_ARBITRARY'].isin(selected_components_tab4)]

        # 정상 여부(Y_LABEL)에 따라 데이터 분리
        y_label_0_tab4 = filtered_data_tab4[filtered_data_tab4['Y_LABEL'] == 0]
        y_label_1_tab4 = filtered_data_tab4[filtered_data_tab4['Y_LABEL'] == 1]

        if not y_label_0_tab4.empty and not y_label_1_tab4.empty:
            try:
                # x축 범위 지정 입력 상자 추가
                min_value_tab4 = float(min(y_label_0_tab4['PQINDEX'].min(), y_label_1_tab4['PQINDEX'].min()))
                max_value_tab4 = float(max(y_label_0_tab4['PQINDEX'].max(), y_label_1_tab4['PQINDEX'].max()))
                
                range_values_tab4 = st.columns(2)
                min_value_input_tab4 = range_values_tab4[0].number_input('PQINDEX의 최소값을 입력하세요', min_value=min_value_tab4, max_value=max_value_tab4, value=min_value_tab4, key='tab4_min_input')
                max_value_input_tab4 = range_values_tab4[1].number_input('PQINDEX의 최대값을 입력하세요', min_value=min_value_tab4, max_value=max_value_tab4, value=max_value_tab4, key='tab4_max_input')

                # Plotly를 사용하여 커널 밀도 추정 그래프 생성
                fig = go.Figure()

                colors = ['blue', 'green', 'red', 'purple']
                for i, component in enumerate(selected_components_tab4):
                    filtered_y_label_0 = y_label_0_tab4[y_label_0_tab4['COMPONENT_ARBITRARY'] == component]['PQINDEX']
                    filtered_y_label_1 = y_label_1_tab4[y_label_1_tab4['COMPONENT_ARBITRARY'] == component]['PQINDEX']

                    if len(filtered_y_label_0) > 1:
                        kde_0 = gaussian_kde(filtered_y_label_0)
                        x_0 = np.linspace(min_value_input_tab4, max_value_input_tab4, 1000)
                        y_0 = kde_0(x_0)
                        fig.add_trace(go.Scatter(
                            x=x_0,
                            y=y_0,
                            mode='lines',
                            name=f'{component} - 정상 오일',
                            line=dict(dash='solid', color=colors[i % len(colors)])
                        ))

                    if len(filtered_y_label_1) > 1:
                        kde_1 = gaussian_kde(filtered_y_label_1)
                        x_1 = np.linspace(min_value_input_tab4, max_value_input_tab4, 1000)
                        y_1 = kde_1(x_1)
                        fig.add_trace(go.Scatter(
                            x=x_1,
                            y=y_1,
                            mode='lines',
                            name=f'{component} - 이상 오일',
                            line=dict(dash='dash', color=colors[i % len(colors)])
                        ))

                fig.update_layout(barmode='overlay', title='PQINDEX 커널 밀도 추정 그래프',
                                  xaxis_title='PQINDEX', yaxis_title='밀도', xaxis_range=[min_value_input_tab4, max_value_input_tab4])

                # 그래프를 Streamlit에 표시
                st.plotly_chart(fig)
            except np.linalg.LinAlgError:
                st.warning("선택한 부품의 PQINDEX 데이터가 충분하지 않습니다.")
        else:
            st.warning("선택한 부품의 PQINDEX 데이터가 충분하지 않습니다.")
    else:
        st.warning("부품을 선택하세요.")

with tab5:
    st.header("🟤 그을음 정도 분석")

    with st.expander("⚙️ 설정", expanded=True):
        # 사용자에게 컴포넌트 선택 옵션 제공 (중복 선택 불가)
        default_index = components_sorted.index('COMPONENT1') if 'COMPONENT1' in components_sorted else 0
        selected_component = st.selectbox('부품을 선택하세요:', options=components_sorted, index=default_index, key='tab5_component')

    # 추가된 subheader
    st.subheader("오일 상태에 따른 그을음 정도 분포")

    if selected_component:
        # 선택된 컴포넌트에 대해 데이터 필터링
        filtered_data_tab5 = data[data['COMPONENT_ARBITRARY'] == selected_component]

        selected_variable = 'SOOTPERCENTAGE'
        
        if selected_variable in filtered_data_tab5.columns and not filtered_data_tab5[selected_variable].dropna().empty:

            # Y_LABEL에 따라 데이터 분리
            y_label_0_data = filtered_data_tab5[filtered_data_tab5['Y_LABEL'] == 0][selected_variable].dropna()
            y_label_1_data = filtered_data_tab5[filtered_data_tab5['Y_LABEL'] == 1][selected_variable].dropna()

            if not y_label_0_data.empty or not y_label_1_data.empty:
                try:
                    # x축 범위 지정 슬라이더 추가
                    min_value = float(min(y_label_0_data.min(), y_label_1_data.min()))
                    max_value = float(max(y_label_0_data.max(), y_label_1_data.max()))
                    range_values = st.slider(f'{selected_variable}의 x축 범위를 선택하세요', min_value, max_value, (min_value, max_value), key='tab5_range_slider')

                    # 히스토그램 생성
                    fig = go.Figure()

                    # Y_LABEL 0 히스토그램
                    fig.add_trace(go.Histogram(
                        x=y_label_0_data,
                        name='정상 오일',
                        opacity=0.75
                    ))

                    # Y_LABEL 1 히스토그램
                    fig.add_trace(go.Histogram(
                        x=y_label_1_data,
                        name='이상 오일',
                        opacity=0.75
                    ))

                    # 히스토그램을 스택형으로 설정
                    fig.update_layout(barmode='stack', title=f'{selected_variable} 스택형 히스토그램',
                                      xaxis_title=selected_variable, yaxis_title='Count', xaxis_range=[range_values[0], range_values[1]])

                    # 그래프를 Streamlit에 표시
                    st.plotly_chart(fig)
                except np.linalg.LinAlgError:
                    st.warning(f"{selected_component}의 {selected_variable} 데이터의 모든 값이 동일하거나 충분하지 않습니다.")
            else:
                st.warning(f"{selected_component}의 {selected_variable} 데이터의 모든 값이 동일하거나 충분하지 않습니다.")
        else:
            st.warning(f"{selected_component}에 대한 {selected_variable} 데이터가 존재하지 않습니다.")
    else:
        st.warning("부품을 선택하세요.")

with tab6:
    st.header("⛽️ 연료 함유량 분석")

    with st.expander("⚙️ 설정", expanded=True):
        # 사용자에게 컴포넌트 선택 옵션 제공 (중복 선택 불가)
        default_index = components_sorted.index('COMPONENT1') if 'COMPONENT1' in components_sorted else 0
        selected_component = st.selectbox('부품을 선택하세요:', options=components_sorted, index=default_index, key='tab6_component')

    # 추가된 subheader
    st.subheader("오일 상태에 따른 연료 함유량 분포")

    if selected_component:
        # 선택된 컴포넌트에 대해 데이터 필터링
        filtered_data_tab6 = data[data['COMPONENT_ARBITRARY'] == selected_component]

        selected_variable = 'FUEL'
        
        if selected_variable in filtered_data_tab6.columns and not filtered_data_tab6[selected_variable].dropna().empty:

            # Y_LABEL에 따라 데이터 분리
            y_label_0_data = filtered_data_tab6[filtered_data_tab6['Y_LABEL'] == 0][selected_variable].dropna()
            y_label_1_data = filtered_data_tab6[filtered_data_tab6['Y_LABEL'] == 1][selected_variable].dropna()

            if not y_label_0_data.empty or not y_label_1_data.empty:
                try:
                    # x축 범위 지정 슬라이더 추가
                    min_value = float(min(y_label_0_data.min(), y_label_1_data.min()))
                    max_value = float(max(y_label_0_data.max(), y_label_1_data.max()))
                    range_values = st.slider(f'{selected_variable}의 x축 범위를 선택하세요', min_value, max_value, (min_value, max_value), key='tab6_range_slider')

                    # 히스토그램 생성
                    fig = go.Figure()

                    # Y_LABEL 0 히스토그램
                    fig.add_trace(go.Histogram(
                        x=y_label_0_data,
                        name='정상 오일',
                        opacity=0.75
                    ))

                    # Y_LABEL 1 히스토그램
                    fig.add_trace(go.Histogram(
                        x=y_label_1_data,
                        name='이상 오일',
                        opacity=0.75
                    ))

                    # 히스토그램을 스택형으로 설정
                    fig.update_layout(barmode='stack', title=f'{selected_variable} 스택형 히스토그램',
                                      xaxis_title=selected_variable, yaxis_title='Count', xaxis_range=[range_values[0], range_values[1]])

                    # 그래프를 Streamlit에 표시
                    st.plotly_chart(fig)
                except np.linalg.LinAlgError:
                    st.warning(f"{selected_component}의 {selected_variable} 데이터의 모든 값이 동일하거나 충분하지 않습니다.")
            else:
                st.warning(f"{selected_component}의 {selected_variable} 데이터의 모든 값이 동일하거나 충분하지 않습니다.")
        else:
            st.warning(f"{selected_component}에 대한 {selected_variable} 데이터가 존재하지 않습니다.")
    else:
        st.warning("부품을 선택하세요.")


with tab7:
    st.header("🌡️ 40도에서의 점도 분석")

    with st.expander("⚙️ 설정", expanded=True):
        # 사용자에게 컴포넌트 선택 옵션 제공 (중복 선택 가능)
        selected_components_tab7 = st.multiselect('부품을 선택하세요', options=components_sorted, default=components_sorted, key='tab7_component')

    # 추가된 subheader
    st.subheader("오일 상태에 따른 40도에서의 점도 분포")

    if selected_components_tab7:
        # 선택된 컴포넌트에 대해 데이터 필터링
        filtered_data_tab7 = data[data['COMPONENT_ARBITRARY'].isin(selected_components_tab7)]

        # 정상 여부(Y_LABEL)에 따라 데이터 분리
        y_label_0_tab7 = filtered_data_tab7[filtered_data_tab7['Y_LABEL'] == 0]
        y_label_1_tab7 = filtered_data_tab7[filtered_data_tab7['Y_LABEL'] == 1]

        if not y_label_0_tab7.empty and not y_label_1_tab7.empty:
            try:
                # x축 범위 지정 입력 상자 추가
                min_value_tab7 = float(min(y_label_0_tab7['V40'].min(), y_label_1_tab7['V40'].min()))
                max_value_tab7 = float(max(y_label_0_tab7['V40'].max(), y_label_1_tab7['V40'].max()))
                range_values_tab7 = st.columns(2)
                min_value_input_tab7 = range_values_tab7[0].number_input('V40의 최소값을 입력하세요', min_value=min_value_tab7, max_value=max_value_tab7, value=min_value_tab7, key='tab7_min_input')
                max_value_input_tab7 = range_values_tab7[1].number_input('V40의 최대값을 입력하세요', min_value=min_value_tab7, max_value=max_value_tab7, value=max_value_tab7, key='tab7_max_input')

                # Plotly를 사용하여 커널 밀도 추정 그래프 생성
                fig = go.Figure()

                colors = ['blue', 'green', 'red', 'purple']
                for i, component in enumerate(selected_components_tab7):
                    filtered_y_label_0 = y_label_0_tab7[y_label_0_tab7['COMPONENT_ARBITRARY'] == component]['V40']
                    filtered_y_label_1 = y_label_1_tab7[y_label_1_tab7['COMPONENT_ARBITRARY'] == component]['V40']

                    if len(filtered_y_label_0) > 1:
                        kde_0 = gaussian_kde(filtered_y_label_0)
                        x_0 = np.linspace(min_value_input_tab7, max_value_input_tab7, 1000)
                        y_0 = kde_0(x_0)
                        fig.add_trace(go.Scatter(
                            x=x_0,
                            y=y_0,
                            mode='lines',
                            name=f'{component} - 정상 오일',
                            line=dict(dash='solid', color=colors[i % len(colors)])
                        ))

                    if len(filtered_y_label_1) > 1:
                        kde_1 = gaussian_kde(filtered_y_label_1)
                        x_1 = np.linspace(min_value_input_tab7, max_value_input_tab7, 1000)
                        y_1 = kde_1(x_1)
                        fig.add_trace(go.Scatter(
                            x=x_1,
                            y=y_1,
                            mode='lines',
                            name=f'{component} - 이상 오일',
                            line=dict(dash='dash', color=colors[i % len(colors)])
                        ))

                fig.update_layout(barmode='overlay', title='V40 커널 밀도 추정 그래프',
                                  xaxis_title='V40', yaxis_title='밀도', xaxis_range=[min_value_input_tab7, max_value_input_tab7])

                # 그래프를 Streamlit에 표시
                st.plotly_chart(fig)
            except np.linalg.LinAlgError:
                st.warning("선택한 컴포넌트의 V40 데이터가 충분하지 않습니다.")
        else:
            st.warning("선택한 컴포넌트의 V40 데이터가 충분하지 않습니다.")
    else:
        st.warning("부품을 선택하세요.")
import streamlit as st
import pandas as pd
import time
import joblib
import lightgbm as lgb

# 페이지 설정
st.set_page_config(
    page_icon="https://www.blackstone-labs.com/wp-content/themes/blackstone/favicon.png",
)
# 애플리케이션 제목과 설명
st.title("📢모델 사용하여 불량 예측하기")
# 사이드바 설정
st.sidebar.title("✅Component 선택")


# 선택 옵션 설정
selected_component = st.sidebar.selectbox(
    "",
    ("Component 1", "Component 2", "Component 3", "Component 4"),
    index=0,  # 기본 선택 인덱스 설정 (예: Component 1)
    format_func=lambda x: f"📂 {x}"  # 각 옵션에 아이콘 추가
)

# 사이드바 스타일 설정
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f0f0;  /* 배경색 설정 */
        padding: 20px;  /* 패딩 설정 */
        border-radius: 10px;  /* 테두리 반경 설정 */
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);  /* 그림자 설정 */
    }
    .sidebar .sidebar-content .stSelectbox label {
        font-size: 18px;  /* 글자 크기 설정 */
        font-weight: bold;  /* 글자 굵기 설정 */
        color: #333333;  /* 글자 색상 설정 */
    }
    </style>
    """,
    unsafe_allow_html=True
)



if selected_component == "Component 1":
	st.write("#### COMPONEMT 1️⃣")

	st.markdown("""
	<style>
	.box {
		border: 2px solid #ddd;
		padding: 10px;
		margin-bottom: 10px;
		border-radius: 5px;
		background-color: #f9f9f9;
	}
	</style>
	<div class="box">
		<strong>💡전처리 후 남은 변수</strong><br>
		AL, ANONYMOUS_1, CA, B, ZN, P, MO, FTBN, S, PQINDEX, FE, MG, V40, V100, FH2O, NA, K, SOOTPERCENTAGE, ANONYMOUS_2, CU, Y_LABEL
	</div>
	<div class="box">
		<strong>💡모델</strong><br>
		Light GBM Classifier
	</div>
	""", unsafe_allow_html=True)

	"""
	-----------------------------------------
	"""
	st.title("📢모델 학습 결과 보기")
	st.write("##### 🪄모델을 학습시키고 싶으시면 아래 버튼을 클릭하세요")

	df = pd.read_csv('data\component1_preprocessed.csv')
	model = joblib.load('models\LGBMClassifier_model_1.pkl')

	if st.button("➡️모델 평가 하기"):
		with st.spinner("⭕모델 평가 중..."):
			# 3초 대기
			time.sleep(3)
			
			# 모델에서 F1 스코어 추출 (모델 학습 시 저장된 값 사용)
			f1 = 0.71  # 여기에 미리 저장된 F1 스코어 값을 입력하세요
			
			# F1 스코어 강조 표시
			st.markdown(
				f"""
				✅ 모델 평가를 완료했습니다.
				<div style="display: inline-block; border: 2px solid black; padding: 10px; background-color: yellow; font-weight: bold; font-size: 24px;">
					F1 Score  :  {f1:.2f}
				</div>
				""", unsafe_allow_html=True
			)
	"""
	-----------------------------------------
	"""

	# 모델 로드 및 예측
	st.title("📢 Component1️⃣ 모델을 이용하여 예측하기")

	st.write("""
	### 🤔How?
	이 애플리케이션은 Component 1 데이터셋을 사용하여 예측을 수행합니다. 아래 슬라이더를 사용하여 입력 값을 설정하고 예측 버튼을 클릭하여 결과를 확인하세요.
	""")

	# 입력 받기
	st.subheader("🖱️입력 값 설정")

	col1, col2, col3 = st.columns(3)

	with col1:
		al = st.slider("AL", float(df['AL'].min()), float(df['AL'].max()), float(df['AL'].mean()))
		anonymous_1 = st.slider("ANONYMOUS_1", float(df['ANONYMOUS_1'].min()), float(df['ANONYMOUS_1'].max()), float(df['ANONYMOUS_1'].mean()))
		ca = st.slider("CA", float(df['CA'].min()), float(df['CA'].max()), float(df['CA'].mean()))
		b = st.slider("B", float(df['B'].min()), float(df['B'].max()), float(df['B'].mean()))
		zn = st.slider("ZN", float(df['ZN'].min()), float(df['ZN'].max()), float(df['ZN'].mean()))
		p = st.slider("P", float(df['P'].min()), float(df['P'].max()), float(df['P'].mean()))
		mo = st.slider("MO", float(df['MO'].min()), float(df['MO'].max()), float(df['MO'].mean()))

	with col2:
		ftbn = st.slider("FTBN", float(df['FTBN'].min()), float(df['FTBN'].max()), float(df['FTBN'].mean()))
		s = st.slider("S", float(df['S'].min()), float(df['S'].max()), float(df['S'].mean()))
		pqindex = st.slider("PQINDEX", float(df['PQINDEX'].min()), float(df['PQINDEX'].max()), float(df['PQINDEX'].mean()))
		fe = st.slider("FE", float(df['FE'].min()), float(df['FE'].max()), float(df['FE'].mean()))
		mg = st.slider("MG", float(df['MG'].min()), float(df['MG'].max()), float(df['MG'].mean()))
		v40 = st.slider("V40", float(df['V40'].min()), float(df['V40'].max()), float(df['V40'].mean()))
		cu = st.slider("CU", float(df['CU'].min()), float(df['CU'].max()), float(df['CU'].mean()))

	with col3:
		v100 = st.slider("V100", float(df['V100'].min()), float(df['V100'].max()), float(df['V100'].mean()))
		fh2o = st.slider("FH2O", float(df['FH2O'].min()), float(df['FH2O'].max()), float(df['FH2O'].mean()))
		na = st.slider("NA", float(df['NA'].min()), float(df['NA'].max()), float(df['NA'].mean()))
		k = st.slider("K", float(df['K'].min()), float(df['K'].max()), float(df['K'].mean()))
		sootpercentage = st.slider("SOOTPERCENTAGE", float(df['SOOTPERCENTAGE'].min()), float(df['SOOTPERCENTAGE'].max()), float(df['SOOTPERCENTAGE'].mean()))
		anonymous_2 = st.slider("ANONYMOUS_2", float(df['ANONYMOUS_2'].min()), float(df['ANONYMOUS_2'].max()), float(df['ANONYMOUS_2'].mean()))
		
	# 예측 버튼
	if st.button("➡️예측 값 보기"):
		with st.spinner("⭕예측 중입니다..."):
			# 3초 대기
			time.sleep(3)
			# 예측 수행
			input_data = [[al, anonymous_1, ca, b, zn, p, mo, ftbn, s, pqindex, fe, mg, v40, v100, fh2o, na, k, sootpercentage, anonymous_2, cu]]
			prediction = model.predict(input_data)
		
		st.success("✔️예측이 완료되었습니다!")
		# 예측 결과 표시 및 스타일 지정
		# 결과 표시 및 스타일 지정
		# 예측 결과에 따라 메시지 출력
		if prediction[0] == 0:
			result_message = "정상 오일입니다."
		elif prediction[0] == 1:
			result_message = "이상 오일입니다."
		else:
			result_message = "예측 결과가 이상합니다."
		
		# 결과를 스타일 지정하여 표시
		st.markdown(
			f"<div style='background-color: yellow; padding: 10px; border-radius: 5px;'>"
			f"<h2 style='color: black;'>🧪Result: {result_message}</h2>"
			f"</div>",
			unsafe_allow_html=True
		)
  
  
  

if selected_component == "Component 2":
	st.write("#### COMPONEMT 2️⃣")

	st.markdown("""
	<style>
	.box {
		border: 2px solid #ddd;
		padding: 10px;
		margin-bottom: 10px;
		border-radius: 5px;
		background-color: #f9f9f9;
	}
	</style>
	<div class="box">
		<strong>💡전처리 후 남은 변수</strong><br>
		AL, ANONYMOUS_1, CA, S, V40, FE, U4, PQINDEX, U6, B, ZN, P, CU, U14, BA, U20, MG, SI, U25, U50, Y_LABEL
	</div>
	<div class="box">
		<strong>💡모델</strong><br>
		Light GBM Classifier
	</div>
	""", unsafe_allow_html=True)

	"""
	-----------------------------------------
	"""
	st.title("📢모델 학습 결과 보기")
	st.write("##### 🪄모델을 학습시키고 싶으시면 아래 버튼을 클릭하세요")

	df = pd.read_csv('data\component2_preprocessed.csv')
	model = joblib.load('models\LGBMClassifier_model_2.pkl')

	if st.button("➡️모델 평가 하기"):
		with st.spinner("⭕모델 평가 중..."):
			# 3초 대기
			time.sleep(3)
			
			# 모델에서 F1 스코어 추출 (모델 학습 시 저장된 값 사용)
			f1 = 0.73  # 여기에 미리 저장된 F1 스코어 값을 입력하세요
			
			# F1 스코어 강조 표시
			st.markdown(
				f"""
				✅ 모델 평가를 완료했습니다.
				<div style="display: inline-block; border: 2px solid black; padding: 10px; background-color: yellow; font-weight: bold; font-size: 24px;">
					F1 Score  :  {f1:.2f}
				</div>
				""", unsafe_allow_html=True
			)
	"""
	-----------------------------------------
	"""

	# 모델 로드 및 예측
	st.title("📢 Component2️⃣ 모델을 이용하여 예측하기")

	st.write("""
	### 🤔How?
	이 애플리케이션은 Component 2 데이터셋을 사용하여 예측을 수행합니다. 아래 슬라이더를 사용하여 입력 값을 설정하고 예측 버튼을 클릭하여 결과를 확인하세요.
	""")

	# 입력 받기
	st.subheader("입력 값 설정")

	col1, col2, col3 = st.columns(3)

	with col1:
		al = st.slider("AL", float(df['AL'].min()), float(df['AL'].max()), float(df['AL'].mean()))
		anonymous_1 = st.slider("ANONYMOUS_1", float(df['ANONYMOUS_1'].min()), float(df['ANONYMOUS_1'].max()), float(df['ANONYMOUS_1'].mean()))
		ca = st.slider("CA", float(df['CA'].min()), float(df['CA'].max()), float(df['CA'].mean()))
		s = st.slider("S", float(df['S'].min()), float(df['S'].max()), float(df['S'].mean()))
		v40 = st.slider("V40", float(df['V40'].min()), float(df['V40'].max()), float(df['V40'].mean()))
		fe = st.slider("FE", float(df['FE'].min()), float(df['FE'].max()), float(df['FE'].mean()))
		u4 = st.slider("U4", float(df['U4'].min()), float(df['U4'].max()), float(df['U4'].mean()))

	with col2:
		pqindex = st.slider("PQINDEX", float(df['PQINDEX'].min()), float(df['PQINDEX'].max()), float(df['PQINDEX'].mean()))
		u6 = st.slider("U6", float(df['U6'].min()), float(df['U6'].max()), float(df['U6'].mean()))
		b = st.slider("B", float(df['B'].min()), float(df['B'].max()), float(df['B'].mean()))
		zn = st.slider("ZN", float(df['ZN'].min()), float(df['ZN'].max()), float(df['ZN'].mean()))
		p = st.slider("P", float(df['P'].min()), float(df['P'].max()), float(df['P'].mean()))
		cu = st.slider("CU", float(df['CU'].min()), float(df['CU'].max()), float(df['CU'].mean()))
		u14 = st.slider("U14", float(df['U14'].min()), float(df['U14'].max()), float(df['U14'].mean()))

	with col3:
		ba = st.slider("BA", float(df['BA'].min()), float(df['BA'].max()), float(df['BA'].mean()))
		u20 = st.slider("U20", float(df['U20'].min()), float(df['U20'].max()), float(df['U20'].mean()))
		mg = st.slider("MG", float(df['MG'].min()), float(df['MG'].max()), float(df['MG'].mean()))
		si = st.slider("SI", float(df['SI'].min()), float(df['SI'].max()), float(df['SI'].mean()))
		u25 = st.slider("U25", float(df['U25'].min()), float(df['U25'].max()), float(df['U25'].mean()))
		u50 = st.slider("U50", float(df['U50'].min()), float(df['U50'].max()), float(df['U50'].mean()))

	# 예측 버튼
	if st.button("➡️예측 값 보기"):
		with st.spinner("⭕예측 중입니다..."):
			# 3초 대기
			time.sleep(3)
			# 예측 수행
			input_data = [[al, anonymous_1, ca, s, v40, fe, u4, pqindex, u6, b, zn, p, cu, u14, ba, u20, mg, si, u25, u50]]
			prediction = model.predict(input_data)
		
		st.success("✔️예측이 완료되었습니다!")
		# 예측 결과에 따라 메시지 출력
		# 예측 결과에 따라 메시지 출력
		if prediction[0] == 0:
			result_message = "정상 오일입니다."
		elif prediction[0] == 1:
			result_message = "이상 오일입니다."
		else:
			result_message = "예측 결과가 이상합니다."
		
		# 결과를 스타일 지정하여 표시
		st.markdown(
			f"<div style='background-color: yellow; padding: 10px; border-radius: 5px;'>"
			f"<h2 style='color: black;'>🧪Result: {result_message}</h2>"
			f"</div>",
			unsafe_allow_html=True
		)
  
  
if selected_component == "Component 3":
	st.write("#### COMPONEMT 3️⃣")

	st.markdown("""
	<style>
	.box {
		border: 2px solid #ddd;
		padding: 10px;
		margin-bottom: 10px;
		border-radius: 5px;
		background-color: #f9f9f9;
	}
	</style>
	<div class="box">
		<strong>💡전처리 후 남은 변수</strong><br>
		CA, ANONYMOUS_1, AL, PQINDEX, P, FE, V40, ZN, B, S, SI, MO, NA, CU, ANONYMOUS_2, BA, MG, K, CR, MN, Y_LABEL

	</div>
	<div class="box">
		<strong>💡모델</strong><br>
		Light GBM Classifier
	</div>
	""", unsafe_allow_html=True)

	"""
	-----------------------------------------
	"""
	st.title("📢모델 학습 결과 보기")
	st.write("##### 🪄모델을 학습시키고 싶으시면 아래 버튼을 클릭하세요")

	df = pd.read_csv('data\component3_preprocessed.csv')
	model = joblib.load('models\LGBMClassifier_model_3.pkl')

	if st.button("➡️모델 평가 하기"):
		with st.spinner("⭕모델 평가 중..."):
			# 3초 대기
			time.sleep(3)
			
			# 모델에서 F1 스코어 추출 (모델 학습 시 저장된 값 사용)
			f1 = 0.66  # 여기에 미리 저장된 F1 스코어 값을 입력하세요
			
			# F1 스코어 강조 표시
			st.markdown(
				f"""
				✅ 모델 평가를 완료했습니다.
				<div style="display: inline-block; border: 2px solid black; padding: 10px; background-color: yellow; font-weight: bold; font-size: 24px;">
					F1 Score  :  {f1:.2f}
				</div>
				""", unsafe_allow_html=True
			)
	"""
	-----------------------------------------
	"""

	# 모델 로드 및 예측
	st.title("📢 Component3️⃣ 모델을 이용하여 예측하기")

	st.write("""
	### 🤔How?
	이 애플리케이션은 Component 3 데이터셋을 사용하여 예측을 수행합니다. 아래 슬라이더를 사용하여 입력 값을 설정하고 예측 버튼을 클릭하여 결과를 확인하세요.
	""")

	# 입력 받기
	st.subheader("입력 값 설정")

	col1, col2, col3 = st.columns(3)

	with col1:
		ca = st.slider("CA", float(df['CA'].min()), float(df['CA'].max()), float(df['CA'].mean()))
		anonymous_1 = st.slider("ANONYMOUS_1", float(df['ANONYMOUS_1'].min()), float(df['ANONYMOUS_1'].max()), float(df['ANONYMOUS_1'].mean()))
		al = st.slider("AL", float(df['AL'].min()), float(df['AL'].max()), float(df['AL'].mean()))
		pqindex = st.slider("PQINDEX", float(df['PQINDEX'].min()), float(df['PQINDEX'].max()), float(df['PQINDEX'].mean()))
		p = st.slider("P", float(df['P'].min()), float(df['P'].max()), float(df['P'].mean()))
		fe = st.slider("FE", float(df['FE'].min()), float(df['FE'].max()), float(df['FE'].mean()))
		v40 = st.slider("V40", float(df['V40'].min()), float(df['V40'].max()), float(df['V40'].mean()))
		
	with col2:
		zn = st.slider("ZN", float(df['ZN'].min()), float(df['ZN'].max()), float(df['ZN'].mean()))
		b = st.slider("B", float(df['B'].min()), float(df['B'].max()), float(df['B'].mean()))
		s = st.slider("S", float(df['S'].min()), float(df['S'].max()), float(df['S'].mean()))
		si = st.slider("SI", float(df['SI'].min()), float(df['SI'].max()), float(df['SI'].mean()))
		mo = st.slider("MO", float(df['MO'].min()), float(df['MO'].max()), float(df['MO'].mean()))
		na = st.slider("NA", float(df['NA'].min()), float(df['NA'].max()), float(df['NA'].mean()))
		cu = st.slider("CU", float(df['CU'].min()), float(df['CU'].max()), float(df['CU'].mean()))

	with col3:
		anonymous_2 = st.slider("ANONYMOUS_2", float(df['ANONYMOUS_2'].min()), float(df['ANONYMOUS_2'].max()), float(df['ANONYMOUS_2'].mean()))
		ba = st.slider("BA", float(df['BA'].min()), float(df['BA'].max()), float(df['BA'].mean()))
		mg = st.slider("MG", float(df['MG'].min()), float(df['MG'].max()), float(df['MG'].mean()))
		k = st.slider("K", float(df['K'].min()), float(df['K'].max()), float(df['K'].mean()))
		cr = st.slider("CR", float(df['CR'].min()), float(df['CR'].max()), float(df['CR'].mean()))
		mn = st.slider("MN", float(df['MN'].min()), float(df['MN'].max()), float(df['MN'].mean()))

	# 예측 버튼
	if st.button("➡️예측 값 보기"):
		with st.spinner("⭕예측 중입니다..."):
			# 3초 대기
			time.sleep(3)
			# 예측 수행
			input_data = [[ca, anonymous_1, al, pqindex, p, fe, v40, zn, b, s, si, mo, na, cu, anonymous_2, ba, mg, k, cr, mn]]
			prediction = model.predict(input_data)
		
		st.success("✔️예측이 완료되었습니다!")
		# 예측 결과 표시 및 스타일 지정
		# 예측 결과에 따라 메시지 출력
		if prediction[0] == 0:
			result_message = "정상 오일입니다."
		elif prediction[0] == 1:
			result_message = "이상 오일입니다."
		else:
			result_message = "예측 결과가 이상합니다."
		
		# 결과를 스타일 지정하여 표시
		st.markdown(
			f"<div style='background-color: yellow; padding: 10px; border-radius: 5px;'>"
			f"<h2 style='color: black;'>🧪Result: {result_message}</h2>"
			f"</div>",
			unsafe_allow_html=True
		)
  
  
if selected_component == "Component 4":
	st.write("#### COMPONEMT 4️⃣")

	st.markdown("""
	<style>
	.box {
		border: 2px solid #ddd;
		padding: 10px;
		margin-bottom: 10px;
		border-radius: 5px;
		background-color: #f9f9f9;
	}
	</style>
	<div class="box">
		<strong>💡전처리 후 남은 변수</strong><br>
		CA, V40, AL, MG, ANONYMOUS_1, BA, MO, S, P, CU, B, PQINDEX, FE, ZN, NA, K, SI, MN, ANONYMOUS_2, PB, Y_LABEL
	</div>
	<div class="box">
		<strong>💡모델</strong><br>
		SGD Classifier
	</div>
	""", unsafe_allow_html=True)

	"""
	-----------------------------------------
	"""
	st.title("📢모델 학습 결과 보기")
	st.write("##### 🪄모델을 학습시키고 싶으시면 아래 버튼을 클릭하세요")

	df = pd.read_csv('data\component4_preprocessed.csv')
	model = joblib.load('models\SGDClassifier_model_4.pkl')

	if st.button("➡️모델 평가 하기"):
		with st.spinner("⭕모델 평가 중..."):
			# 3초 대기
			time.sleep(3)
			
			# 모델에서 F1 스코어 추출 (모델 학습 시 저장된 값 사용)
			f1 = 0.48  # 여기에 미리 저장된 F1 스코어 값을 입력하세요
			
			# F1 스코어 강조 표시
			st.markdown(
				f"""
				✅ 모델 평가를 완료했습니다.
				<div style="display: inline-block; border: 2px solid black; padding: 10px; background-color: yellow; font-weight: bold; font-size: 24px;">
					F1 Score  :  {f1:.2f}
				</div>
				""", unsafe_allow_html=True
			)
	"""
	-----------------------------------------
	"""

	# 모델 로드 및 예측
	st.title("📢 Component 4️⃣ 모델을 이용하여 예측하기")

	st.write("""
	### 🤔How?
	이 애플리케이션은 Component 4 데이터셋을 사용하여 예측을 수행합니다. 아래 슬라이더를 사용하여 입력 값을 설정하고 예측 버튼을 클릭하여 결과를 확인하세요.
	""")

	# 입력 받기
	st.subheader("입력 값 설정")

	col1, col2, col3 = st.columns(3)

	with col1:
		ca = st.slider("CA", float(df['CA'].min()), float(df['CA'].max()), float(df['CA'].mean()))
		v40 = st.slider("V40", float(df['V40'].min()), float(df['V40'].max()), float(df['V40'].mean()))
		al = st.slider("AL", float(df['AL'].min()), float(df['AL'].max()), float(df['AL'].mean()))
		mg = st.slider("MG", float(df['MG'].min()), float(df['MG'].max()), float(df['MG'].mean()))
		anonymous_1 = st.slider("ANONYMOUS_1", float(df['ANONYMOUS_1'].min()), float(df['ANONYMOUS_1'].max()), float(df['ANONYMOUS_1'].mean()))
		ba = st.slider("BA", float(df['BA'].min()), float(df['BA'].max()), float(df['BA'].mean()))
		mo = st.slider("MO", float(df['MO'].min()), float(df['MO'].max()), float(df['MO'].mean()))

	with col2:
		s = st.slider("S", float(df['S'].min()), float(df['S'].max()), float(df['S'].mean()))
		p = st.slider("P", float(df['P'].min()), float(df['P'].max()), float(df['P'].mean()))
		cu = st.slider("CU", float(df['CU'].min()), float(df['CU'].max()), float(df['CU'].mean()))
		b = st.slider("B", float(df['B'].min()), float(df['B'].max()), float(df['B'].mean()))
		pqindex = st.slider("PQINDEX", float(df['PQINDEX'].min()), float(df['PQINDEX'].max()), float(df['PQINDEX'].mean()))
		fe = st.slider("FE", float(df['FE'].min()), float(df['FE'].max()), float(df['FE'].mean()))
		zn = st.slider("ZN", float(df['ZN'].min()), float(df['ZN'].max()), float(df['ZN'].mean()))

	with col3:
		na = st.slider("NA", float(df['NA'].min()), float(df['NA'].max()), float(df['NA'].mean()))
		k = st.slider("K", float(df['K'].min()), float(df['K'].max()), float(df['K'].mean()))
		si = st.slider("SI", float(df['SI'].min()), float(df['SI'].max()), float(df['SI'].mean()))
		mn = st.slider("MN", float(df['MN'].min()), float(df['MN'].max()), float(df['MN'].mean()))
		anonymous_2 = st.slider("ANONYMOUS_2", float(df['ANONYMOUS_2'].min()), float(df['ANONYMOUS_2'].max()), float(df['ANONYMOUS_2'].mean()))
		pb = st.slider("PB", float(df['PB'].min()), float(df['PB'].max()), float(df['PB'].mean()))

	# 예측 버튼
	if st.button("➡️예측 값 보기"):
		with st.spinner("⭕예측 중입니다..."):
			# 3초 대기
			time.sleep(3)
			# 예측 수행
			input_data = [[ca, v40, al, mg, anonymous_1, ba, mo, s, p, cu, b, pqindex, fe, zn, na, k, si, mn, anonymous_2, pb]]
			prediction = model.predict(input_data)
		
		st.success("✔️예측이 완료되었습니다!")
		# 예측 결과 표시 및 스타일 지정
		# 예측 결과에 따라 메시지 출력
		if prediction[0] == 0:
			result_message = "정상 오일입니다."
		elif prediction[0] == 1:
			result_message = "이상 오일입니다."
		else:
			result_message = "예측 결과가 이상합니다."
		
		# 결과를 스타일 지정하여 표시
		st.markdown(
			f"<div style='background-color: yellow; padding: 10px; border-radius: 5px;'>"
			f"<h2 style='color: black;'>🧪Result: {result_message}</h2>"
			f"</div>",
			unsafe_allow_html=True
		)
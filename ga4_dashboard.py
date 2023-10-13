import streamlit as st
import pandas as pd
import altair as alt

def main():
    # 지금이 2021년 2월이라고 가정하고, 2021년 1월의 데이터를 12월 데이터와 비교하는 대시보드를 만듭어 봅시다.

    # 데이터 로드
    df = pd.read_csv('data/ga4_sample.csv') # 20년 11월 ~ 21년 1월 google merchandise store 판매 데이터 (GA4)
   
    # 데이터 전처리 함수 정의
    def data_prep(data):
        data = data.dropna()
        # user_pseudo_id 열을 문자열로 변환
        data['user_pseudo_id'] = data['user_pseudo_id'].astype(str)

        # item_id 열의 '(not set)' 값을 NA로 변환하고 숫자로 변환 후 int로 변환
        data['item_id'] = pd.to_numeric(data['item_id'], errors='coerce')
        data['item_id'] = data['item_id'].astype(int)

        # item_name 열을 문자열로 변환
        data['item_name'] = data['item_name'].astype(str)

        # 가격 데이터 유형 변환
        data['price_in_usd'] = data['price_in_usd'].astype(float)
        data['price'] = data['price'].astype(float)
        data['quantity'] = data['quantity'].astype(int)
        data['item_revenue_in_usd'] = data['item_revenue_in_usd'].astype(float)
        data['item_revenue'] = data['item_revenue'].astype(float)

        # 날짜 데이터 유형 변환
        data['event_date'] = pd.to_datetime(data['event_date'], format="%Y%m%d")
        data['event_timestamp'] = pd.to_datetime(data['event_timestamp'], unit='us')

        # 지역, 기기명 데이터 유형 변환
        data['country'] = data['country'].astype(str)
        data['region'] = data['region'].astype(str)
        data['mobile_brand_name'] = data['mobile_brand_name'].astype(str)
        data['mobile_model_name'] = data['mobile_model_name'].astype(str)

        return data

    df = data_prep(df)

    # 20년 11, 12월, 21년 1월 데이터 추출
    nov_df = df[(pd.to_datetime(df['event_date']) >= pd.to_datetime("2020-11-01")) & (df['event_date'] <= pd.to_datetime("2020-11-30"))]
    dec_df = df[(pd.to_datetime(df['event_date']) >= pd.to_datetime("2020-12-01")) & (df['event_date'] <= pd.to_datetime("2020-12-31"))]
    jan_df = df[(pd.to_datetime(df['event_date']) >= pd.to_datetime("2021-01-01")) & (df['event_date'] <= pd.to_datetime("2021-01-31"))]

    # page config
    st.set_page_config(page_title = "GA Dashboard", 
        page_icon = "🎲", 
        layout = "wide", 
        initial_sidebar_state = "auto" 
        )
    
    # 제목
    st.title("Google Merchandise Store 대시보드", anchor = None) 
    st.caption("21년 1월 매출 기준")
    col1, col2, col3, col4 = st.columns(4)

    # 총 매출 계산 (12월 vs 1월)
    dec_revenue = dec_df['item_revenue_in_usd'].sum()
    jan_revenue = jan_df['item_revenue_in_usd'].sum()

    # 평균 주문 가치 (AOV) 계산 (12월 vs 1월)
    dec_AOV = dec_df.groupby('user_pseudo_id')['item_revenue_in_usd'].mean().mean()
    jan_AOV = jan_df.groupby('user_pseudo_id')['item_revenue_in_usd'].mean().mean()

    # 신규 고객 수 (11, 12월 vs 1월)
    new_customers = len(set(jan_df['user_pseudo_id']) - set(nov_df['user_pseudo_id']) - set(dec_df['user_pseudo_id']))

    # 1월 미구매 고객 수 (11월 혹은 12월에는 구매했지만, 1월에는 구매하지 않은 고객)
    churned_customers = len((set(nov_df['user_pseudo_id']) | set(dec_df['user_pseudo_id'])) - set(jan_df['user_pseudo_id']))

    # 각 지표에 대한 증가, 감소 비율 계산
    # 이전 달과 비교하여 증가 또는 감소한 비율을 계산합니다.
    def calculate_percentage_change(current_value, previous_value):
        if previous_value == 0:
            return "previous_value가 0입니다"
        percentage_change = ((current_value - previous_value) / previous_value) * 100
        return f"{percentage_change:.2f}%"
        
    # 지표 출력
    col1.metric("총 매출", f'$ {round(jan_revenue, 1)}', f'{calculate_percentage_change(jan_revenue, dec_revenue)}') 
    col2.metric("평균 주문 가치 (AOV)", (f'$ {round(jan_AOV,1)}'), calculate_percentage_change(jan_AOV, dec_AOV)) 
    col3.metric("신규 고객 수", f'{new_customers} 명')
    col4.metric("1월 미구매 고객 수", f'{churned_customers} 명')

    st.divider()

    # Side bar 코호트 옵션 추가
    st.sidebar.subheader('유저 그룹 선택')
    country_options = ['All Countries'] + list(df['country'].unique())
    selected_country = st.sidebar.selectbox('Select Country', country_options)
    user_type = st.sidebar.radio('Select User Type', ('모든 유저', '신규 유저'))

    # 신규 유저 필터
    if user_type == '모든 유저':
        selected_df = jan_df
    else:
        new_customers = set(jan_df['user_pseudo_id']) - set(nov_df['user_pseudo_id']) - set(dec_df['user_pseudo_id'])
        selected_df = jan_df[jan_df['user_pseudo_id'].isin(new_customers)]

    # 국가 필터
    if selected_country != 'All Countries':
        selected_df = selected_df[selected_df['country'] == selected_country]

    col1, col2 = st.columns([0.6, 0.4])

    # 차트 1. 구매시간 (event_timestamp)
    col1.subheader("시간대 별 구매 건 수")
    selected_df['event_timestamp'] = pd.to_datetime(selected_df['event_timestamp'], unit='s')
    selected_df['event_timestamp_hour'] = selected_df['event_timestamp'].dt.floor('H')

    timeline_chart = alt.Chart( 
        selected_df
        ).mark_area( 
            line={'color':'darkgreen'},
            interpolate='basis',
            color=alt.Gradient(
                gradient='linear',
                stops=[
                    alt.GradientStop(color='white', offset=0),
                    alt.GradientStop(color='darkgreen', offset=1)
                    ],
                x1=1,
                x2=1,
                y1=1,
                y2=0
                )
        ).encode( # https://altair-viz.github.io/user_guide/encodings/index.html#encoding-data-types
            x=alt.X('event_timestamp_hour:T', title=''),
            y=alt.Y('count():Q', title='구매 건 수'),
            tooltip='count():Q'
        ).properties(
            height=300
        ).interactive()

    col1.altair_chart(timeline_chart, use_container_width=True)

    # 차트 2. 가장 많이 팔린 상품 top 10 
    df_top10 = selected_df['item_name'].value_counts().nlargest(10).reset_index()
    color_scale = alt.Scale(scheme='greens')
    chart_top10 = (
        alt.Chart()
        .mark_bar()
        .encode(
            x=alt.X("count:Q", title="구매 건 수"),
            y=alt.Y("item_name:N", title="").sort('-x'),
            color=alt.Color("count:Q", scale=color_scale, legend=None),
        )
        .properties(height=240)
    )

    top_items_chart = alt.vconcat(chart_top10, data=df_top10, title="") # Altair 라이브러리 사용: 이런 식으로 차트와 데이터를 합쳐줄 수도 있습니다
    col2.subheader("인기상품 Top 10")
    col2.altair_chart(top_items_chart, theme="streamlit", use_container_width=True)
    
    col1, col2 = st.columns(2) 

    # 차트 3. 구매 요청 소스
    traffic_source = selected_df['mobile_model_name'].value_counts()
    traffic_source_df = pd.DataFrame({
        'source': traffic_source.index, 
        'count': traffic_source.values, 
        'percent': traffic_source.values/sum(traffic_source.values) * 100
        })
    traffic_source_df = traffic_source_df.round(1)

    color_scale = alt.Scale(scheme='greens', reverse=True)
    pie_chart = (
        alt.Chart(traffic_source_df)
        .mark_arc()
        .encode(
            theta=alt.Theta('count:Q'),
            color=alt.Color('source:N', scale=color_scale, sort=["descending"]),
            tooltip=['source:N', 'count:Q', 'percent:Q']
        )
    ).properties(
        width=300,
        height=300,
        title='구매 요청 소스'
    )
    col1.altair_chart(pie_chart, use_container_width=True)

    # 차트 4. 월별 이용자 수 집계 (11,12,1월 데이터 모두 활용)
    nov_user_count = len(nov_df['user_pseudo_id'].unique())
    dec_user_count = len(dec_df['user_pseudo_id'].unique())
    jan_user_count = len(jan_df['user_pseudo_id'].unique())

    df_user_num = pd.DataFrame({
        'Month': ['Nov 2020', 'Dec 2020', 'Jan 2021'],
        'User Count': [nov_user_count, dec_user_count, jan_user_count]
    })
    month_order = ['Nov 2020', 'Dec 2020', 'Jan 2021']
    df_user_num['Month'] = pd.Categorical(df_user_num['Month'], categories=month_order, ordered=True)

    line_chart = (
        alt.Chart(df_user_num)
        .mark_line(interpolate='basis')
        .encode(
            x=alt.X('Month:N', sort=month_order),
            y='User Count:Q',
            tooltip=['Month:N', 'User Count:Q'],
            color=alt.value("green")
        )
        .properties(
            height=300,
            title='이용자 수 증감 차트'
        )
    )
    col2.altair_chart(line_chart, use_container_width=True)

if __name__ == "__main__":
    main()

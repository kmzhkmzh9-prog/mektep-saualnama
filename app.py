import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title='Оқушылар сауалнамасы', page_icon='📊', layout='wide')
DATA_FILE = Path('responses.csv')

Q = {
    'q1': '1. Сабаққа қызығушылық деңгейіңіз қандай?',
    'q2': '2. Қосымша үйірмеге қатысасыз ба?',
    'q3': '3. Қай оқу тәсілі сізге көбірек ұнайды?',
    'q4': '4. Оқу барысында негізгі қиындық қандай?',
    'q5': '5. Қай пәнді көбірек ұнатасыз?'
}

def load_data():
    if DATA_FILE.exists():
        try: return pd.read_csv(DATA_FILE, encoding='utf-8-sig')
        except Exception: return pd.DataFrame()
    return pd.DataFrame()

def save_row(row):
    old = load_data()
    new = pd.DataFrame([row])
    pd.concat([old, new], ignore_index=True).to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

st.title('📊 Мектеп оқушыларының сапалық деректерін талдау')
st.caption('Оқушы сауалнамасы және мұғалімнің талдау панелі')

student, teacher = st.tabs(['📝 Оқушы сауалнамасы', '📈 Мұғалім панелі'])

with student:
    st.header('Оқушы сауалнамасы')
    with st.form('survey'):
        cls = st.text_input('Сыныбыңыз', placeholder='Мысалы: 8А')
        q1 = st.radio(Q['q1'], ['Жоғары','Орташа','Төмен'], horizontal=True)
        q2 = st.radio(Q['q2'], ['Иә','Жоқ'], horizontal=True)
        q3 = st.radio(Q['q3'], ['Практика','Видео','Топпен жұмыс','Мұғалім түсіндірмесі'])
        q4 = st.radio(Q['q4'], ['Қиындық жоқ','Тақырыпты түсіну','Мотивация','Үй тапсырмасы','Уақыт жетіспеуі'])
        q5 = st.radio(Q['q5'], ['Информатика','Физика','Математика','Ағылшын тілі','Тарих'])
        sent = st.form_submit_button('✅ Жауапты жіберу', use_container_width=True)
    if sent:
        if not cls.strip():
            st.warning('Сыныбыңызды енгізіңіз.')
        else:
            save_row({'Уақыты': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Сынып': cls.strip(), Q['q1']: q1, Q['q2']: q2, Q['q3']: q3, Q['q4']: q4, Q['q5']: q5})
            st.success('🎉 Жауабыңыз сәтті қабылданды!')

with teacher:
    st.header('📈 Мұғалім панелі')
    data = load_data()
    if data.empty:
        st.info('Әзірге жауаптар жоқ.')
    else:
        a,b,c = st.columns(3)
        a.metric('👨‍🎓 Жауап саны', len(data))
        b.metric('🏫 Сынып саны', data['Сынып'].nunique())
        c.metric('⭐ Жоғары қызығушылық', int((data[Q['q1']] == 'Жоғары').sum()))
        classes = sorted(data['Сынып'].dropna().astype(str).unique())
        selected = st.selectbox('Сынып бойынша сүзгі', ['Барлық сынып'] + classes)
        view = data if selected == 'Барлық сынып' else data[data['Сынып'].astype(str) == selected]
        for title, col in [('1️⃣ Сабаққа қызығушылық',Q['q1']),('2️⃣ Қосымша үйірме',Q['q2']),('3️⃣ Ұнайтын оқу тәсілі',Q['q3']),('4️⃣ Негізгі қиындық',Q['q4']),('5️⃣ Ұнайтын пән',Q['q5'])]:
            st.subheader(title)
            st.bar_chart(view[col].value_counts())
        st.subheader('📋 Жауаптар кестесі')
        st.dataframe(view, use_container_width=True)
        csv = view.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button('⬇️ CSV жүктеу', csv, 'okushy_saualnama.csv', 'text/csv', use_container_width=True)

st.divider()
st.caption('Ескерту: Streamlit Community Cloud-та жергілікті CSV файлды тұрақты ортақ дерекқор ретінде қолдану дұрыс емес. Көп оқушыдан нақты онлайн жауап жинау үшін келесі нұсқада Google Sheets/бұлттық дерекқорды қосқан жөн.')

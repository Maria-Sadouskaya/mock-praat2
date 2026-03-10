"""
🎤 Анализатор интонации для студентов-лингвистов
Основан на Praat (метод Filtered Autocorrelation)
"""

import streamlit as st
import parselmouth
import matplotlib.pyplot as plt
import numpy as np
import tempfile

# Настройка страницы
st.set_page_config(
    page_title="Анализатор интонации",
    page_icon="🎤",
    layout="centered"
)

# Заголовок
st.title("🎤 Анализатор интонации")
st.markdown("---")

# Инструкция
with st.expander("📚 Инструкция", expanded=True):
    st.markdown("""
    1. **Выберите способ:** запись с микрофона или загрузка файла
    2. **Настройте параметры** под ваш голос
    3. **Нажмите кнопку** для анализа
    4. **Изучите график** интонации
    
    **Рекомендации:**
    - Мужской голос: floor=75, ceiling=250
    - Женский голос: floor=100, ceiling=600
    - Ребенок: floor=180, ceiling=800
    """)

# Боковая панель с настройками
with st.sidebar:
    st.header("⚙️ Настройки")
    
    # Пресеты
    preset = st.selectbox(
        "Пресет голоса",
        ["Мужской", "Женский", "Ребенок", "Свой"]
    )
    
    # Ползунки для частот
    if preset == "Мужской":
        pitch_floor = st.slider("Pitch floor (мин. частота)", 50, 150, 75)
        pitch_ceiling = st.slider("Pitch ceiling (макс. частота)", 200, 400, 250)
    elif preset == "Женский":
        pitch_floor = st.slider("Pitch floor (мин. частота)", 80, 200, 100)
        pitch_ceiling = st.slider("Pitch ceiling (макс. частота)", 400, 800, 600)
    elif preset == "Ребенок":
        pitch_floor = st.slider("Pitch floor (мин. частота)", 150, 250, 180)
        pitch_ceiling = st.slider("Pitch ceiling (макс. частота)", 600, 1200, 800)
    else:
        pitch_floor = st.slider("Pitch floor (мин. частота)", 40, 250, 75)
        pitch_ceiling = st.slider("Pitch ceiling (макс. частота)", 200, 1200, 600)

# Основной интерфейс
tab1, tab2 = st.tabs(["🎤 Запись", "📁 Загрузка"])

# Вкладка 1: Запись
with tab1:
    st.subheader("Запись с микрофона")
    audio_bytes = st.audio_input("Нажмите для записи")
    
    if audio_bytes:
        st.audio(audio_bytes)
        
        if st.button("🔬 Анализировать запись", type="primary"):
            with st.spinner("Анализирую..."):
                # Сохраняем во временный файл
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
                    tmp.write(audio_bytes.getvalue())
                    audio_path = tmp.name
                
                # Анализируем
                analyze_intonation(audio_path, pitch_floor, pitch_ceiling)

# Вкладка 2: Загрузка
with tab2:
    st.subheader("Загрузить аудиофайл")
    st.info("Поддерживаются форматы: WAV, MP3")
    
    uploaded_file = st.file_uploader(
        "Выберите файл",
        type=['wav', 'mp3']
    )
    
    if uploaded_file:
        st.audio(uploaded_file)
        
        if st.button("🔬 Анализировать файл", type="primary"):
            with st.spinner("Анализирую..."):
                # Сохраняем во временный файл
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
                    tmp.write(uploaded_file.getvalue())
                    audio_path = tmp.name
                
                # Анализируем
                analyze_intonation(audio_path, pitch_floor, pitch_ceiling)

def analyze_intonation(audio_path, pitch_floor, pitch_ceiling):
    """Анализ интонации и построение графика"""
    
    try:
        # Загружаем звук
        sound = parselmouth.Sound(audio_path)
        
        # Анализируем интонацию
        pitch = sound.to_pitch(
            time_step=0.01,
            pitch_floor=pitch_floor,
            pitch_ceiling=pitch_ceiling
        )
        
        # Получаем данные
        pitch_values = pitch.selected_array['frequency']
        times = pitch.xs()
        
        # Проверяем, есть ли голос
        valid = pitch_values > 0
        if not any(valid):
            st.error("❌ Голос не распознан. Попробуйте другие настройки.")
            return
        
        # Создаем график
        fig, ax = plt.subplots(figsize=(12, 5))
        
        # Рисуем интонационный контур (паузы как разрывы)
        plot_pitch = pitch_values.copy()
        plot_pitch[plot_pitch == 0] = np.nan
        
        ax.plot(times, plot_pitch, 'b-', linewidth=2.5, label='Интонация')
        
        # Отмечаем максимум
        max_idx = np.argmax(pitch_values[valid])
        max_time = times[valid][max_idx]
        max_f0 = pitch_values[valid][max_idx]
        ax.plot(max_time, max_f0, 'ro', markersize=10, label=f'Пик: {max_f0:.1f} Гц')
        
        # Средняя линия
        mean_f0 = np.mean(pitch_values[valid])
        ax.axhline(y=mean_f0, color='g', linestyle='--', alpha=0.7, 
                   label=f'Среднее: {mean_f0:.1f} Гц')
        
        # Настройки графика
        ax.set_xlabel('Время (секунды)', fontsize=12)
        ax.set_ylabel('Частота (Гц)', fontsize=12)
        ax.set_title('Интонационный рисунок (спектрограмма)', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(pitch_floor, pitch_ceiling)
        ax.legend(loc='upper right')
        
        # Показываем график
        st.pyplot(fig)
        plt.close()
        
        # Минимальная статистика
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Минимум", f"{np.min(pitch_values[valid]):.1f} Гц")
        with col2:
            st.metric("Среднее", f"{mean_f0:.1f} Гц")
        with col3:
            st.metric("Максимум", f"{max_f0:.1f} Гц")
        
        # Простой анализ
        if max_time > times[valid][-1] * 0.7 and (max_f0 - mean_f0) > 30:
            st.success("🔍 Обнаружен восходящий тон в конце — возможно, вопрос")
        elif np.std(pitch_values[valid]) < 20:
            st.info("🔍 Ровная интонация — повествовательное предложение")
        else:
            st.info("🔍 Интонация с перепадами — эмоциональная речь")
        
    except Exception as e:
        st.error(f"Ошибка при анализе: {e}")

# Подвал
st.markdown("---")
st.caption("🎓 Для студентов-лингвистов • Метод Filtered Autocorrelation (Praat)") 

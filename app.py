Skip to content
Maria-Sadouskaya
mock-praat2
Repository navigation
Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
mock-praat2
/
app.py
in
main

Edit

Preview
Indent mode

Spaces
Indent size

4
Line wrap mode

No wrap
Editing app.py file contents
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
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

Use Control + Shift + m to toggle the tab key moving focus. Alternatively, use esc then tab to move to the next interactive element on the page.

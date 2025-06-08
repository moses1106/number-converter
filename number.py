import streamlit as st

# Custom CSS for dark mode
dark_mode_css = """
<style>
    /* Background & text colors */
    body, .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stButton>button {
        background-color: #222;
        color: #fafafa;
    }
    .stTextInput>div>input {
        background-color: #222;
        color: #fafafa;
    }
    .stSelectbox>div>div>div>select {
        background-color: #222;
        color: #fafafa;
    }
</style>
"""

light_mode_css = """
<style>
    body, .main {
        background-color: white;
        color: black;
    }
</style>
"""

def convert_number(num_str, from_base, to_base):
    try:
        decimal_num = int(num_str, from_base)
    except ValueError:
        return "Invalid input for the given base"
    
    if to_base == 10:
        return str(decimal_num)
    
    digits = "0123456789ABCDEF"
    result = ""
    while decimal_num > 0:
        result = digits[decimal_num % to_base] + result
        decimal_num //= to_base
    
    return result or "0"

st.title("Number System Converter")

# Dark mode toggle checkbox
dark_mode = st.checkbox("Enable Dark Mode")

# Apply the CSS based on toggle
if dark_mode:
    st.markdown(dark_mode_css, unsafe_allow_html=True)
else:
    st.markdown(light_mode_css, unsafe_allow_html=True)

bases = {
    "Binary (Base 2)": 2,
    "Octal (Base 8)": 8,
    "Decimal (Base 10)": 10,
    "Hexadecimal (Base 16)": 16
}

num_str = st.text_input("Enter the number:")
from_base_name = st.selectbox("From Base:", list(bases.keys()))
to_base_name = st.selectbox("To Base:", list(bases.keys()))

from_base = bases[from_base_name]
to_base = bases[to_base_name]

if st.button("Convert"):
    if num_str:
        result = convert_number(num_str.strip().upper(), from_base, to_base)
        st.success(f"Converted Number: {result}")
    else:
        st.error("Please enter a number to convert.")

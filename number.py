import streamlit as st
import re

# CSS styling
dark_mode_css = """
<style>
    body, .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stButton>button, .stTextInput>div>input, .stSelectbox>div>div>div>select {
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

def validate_input(num_str, base):
    pattern = {
        2: r'^[01]+(\.[01]+)?$',
        8: r'^[0-7]+(\.[0-7]+)?$',
        10: r'^[0-9]+(\.[0-9]+)?$',
        16: r'^[0-9A-F]+(\.[0-9A-F]+)?$'
    }
    return re.fullmatch(pattern[base], num_str.upper()) is not None

def base_to_decimal(num_str, base):
    digits = "0123456789ABCDEF"
    num_str = num_str.upper()
    if '.' in num_str:
        int_part, frac_part = num_str.split('.')
    else:
        int_part, frac_part = num_str, ''
    
    # Integer conversion
    total = 0
    working = []
    for i, digit in enumerate(reversed(int_part)):
        value = digits.index(digit)
        subtotal = value * (base ** i)
        total += subtotal
        working.append(f"{digit} × {base}^{i} = {subtotal}")

    # Fractional conversion
    frac_total = 0
    for i, digit in enumerate(frac_part, 1):
        value = digits.index(digit)
        subtotal = value * (base ** -i)
        frac_total += subtotal
        working.append(f"{digit} × {base}^-{i} = {subtotal}")

    return total + frac_total, working

def decimal_to_base(num, to_base, precision=10):
    digits = "0123456789ABCDEF"
    int_part = int(num)
    frac_part = num - int_part

    int_str = ''
    working = []

    # Integer part conversion
    if int_part == 0:
        int_str = '0'
        working.append(f"0 ÷ {to_base} = 0 R0")
    else:
        while int_part > 0:
            quotient = int_part // to_base
            remainder = int_part % to_base
            working.append(f"{int_part} ÷ {to_base} = {quotient} R{remainder}")
            int_str = digits[remainder] + int_str
            int_part = quotient

    # Fractional part conversion
    frac_str = ''
    if frac_part > 0:
        working.append("---- Fractional Part ----")
        count = 0
        while frac_part > 0 and count < precision:
            frac_part *= to_base
            digit = int(frac_part)
            frac_str += digits[digit]
            working.append(f"{frac_part:.10f} → {digit}")
            frac_part -= digit
            count += 1

    return int_str + ('.' + frac_str if frac_str else ''), working

# Streamlit app
st.title("🔢 Number System Converter")

dark_mode = st.checkbox("Enable Dark Mode")
st.markdown(dark_mode_css if dark_mode else light_mode_css, unsafe_allow_html=True)

bases = {
    "Binary (Base 2)": 2,
    "Octal (Base 8)": 8,
    "Decimal (Base 10)": 10,
    "Hexadecimal (Base 16)": 16
}

num_str = st.text_input("Enter the number (can be fractional):").strip().upper()
from_base_name = st.selectbox("From Base:", list(bases.keys()))
to_base_name = st.selectbox("To Base:", list(bases.keys()))
precision = st.slider("Fractional Precision", min_value=1, max_value=15, value=10)

from_base = bases[from_base_name]
to_base = bases[to_base_name]

if st.button("Convert"):
    if not num_str:
        st.error("Please enter a number to convert.")
    elif not validate_input(num_str, from_base):
        st.error(f"Invalid number for base {from_base}.")
    else:
        decimal_val, to_decimal_working = base_to_decimal(num_str, from_base)

        if to_base == 10:
            result = str(decimal_val)
            full_working = to_decimal_working
        else:
            result, from_decimal_working = decimal_to_base(decimal_val, to_base, precision)
            full_working = to_decimal_working + [""] + from_decimal_working

        st.success(f"Converted Number: {result}")
        st.subheader("📘 Working Steps:")
        for step in full_working:
            st.markdown(f"- {step}")


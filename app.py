import streamlit as st
import subprocess,os,tempfile

st.write("Online Compiler")
option=st.radio("Select the language",["Python","Java","C","C++"],horizontal=True)
suffix={"Python":".py","C":".c","C++":".cpp"}
code = st.text_area("Enter your code", height=300)
input=st.text_area("Output",height=80)
if st.button("Run"):
    if option=="Java":
        jdir=tempfile.mkdtemp()
        jpath=os.path.join(jdir,"Main.java")
        with open(jpath,mode="w") as f:
            f.write(code)
        subprocess.run(["javac",jpath],capture_output=True,text=True)
        result=subprocess.run(["java","-cp",jdir,"Main"],input=input,capture_output=True,text=True)
    else:
        with tempfile.NamedTemporaryFile(mode="w",delete=False,suffix=suffix[option]) as f:
            f.write(code)
        g=f.name+".out"
        if option=="Python":
            result = subprocess.run(["python3", f.name],input=input, capture_output=True, text=True)
        elif option in ["C++","C"] :
            subprocess.run(["g++", f.name,"-o",g], capture_output=True, text=True)
            result=subprocess.run([g],input=input, capture_output=True, text=True)
    st.write("Output:")
    st.code(result.stdout)
    if result.stderr:
        st.code(result.stderr)

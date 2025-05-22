import streamlit as st
import pandas as pd
import mysql.connector

# Set custom page title and layout
st.set_page_config(
    page_title="MySQL Visualizer",
    page_icon="🧮",
    layout="wide"
)

# Custom CSS Styling
st.markdown("""
    <style>
        .main-title {
            font-size: 45px;
            color: #009688;
            text-align: center;
            margin-bottom: 40px;
        }
        .section-title {
            font-size: 24px;
            margin-top: 40px;
            color: #37474F;
            border-bottom: 2px solid #009688;
            padding-bottom: 5px;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
        }
        .stButton>button {
            background-color: #009688;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 100%;
            font-size: 16px;
        }
        .stTextArea textarea {
            border-radius: 8px;
        }
    </style>
    <div class="main-title">MySQL Visualizer with CSV Uploader</div>
""", unsafe_allow_html=True)

# Section: Run SQL Query
st.markdown('<div class="section-title">Run SQL Query</div>', unsafe_allow_html=True)
query_db = st.text_input("Enter Database Name", key="query_db")
query = st.text_area("Enter SQL Query", key="sql_query")

if st.button("Run Query"):
    try:
        mydb = mysql.connector.connect(
            host="localhost", user="root", password="R@ghav_2005", database=query_db
        )
        cursor = mydb.cursor()
        cursor.execute(query)

        if query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=columns)
            st.dataframe(df)
        else:
            mydb.commit()
            st.success("Query executed successfully!")
    except Exception as e:
        st.error(f"Error: {e}")

# Section: Upload CSV and Insert
st.markdown('<div class="section-title">Upload CSV and Insert to Table</div>', unsafe_allow_html=True)

upload_db = st.text_input("Enter Database Name for Upload", key="upload_db")
uploaded_file = st.file_uploader("Upload CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("CSV Preview:")
    st.dataframe(df)

create_query = st.text_area("Enter CREATE TABLE SQL", key="create_table")

if st.button("Create Table and Insert Data"):
    if upload_db and uploaded_file and create_query:
        try:
            mydb = mysql.connector.connect(
                host="localhost", user="root", password="R@ghav_2005", database=upload_db
            )
            cursor = mydb.cursor()

            # Create table
            cursor.execute(create_query)
            mydb.commit()
            st.success("Table created successfully!")

            # Extract table name from query
            table_name = create_query.split()[2]

            # Insert rows
            for _, row in df.iterrows():
                placeholders = ', '.join(['%s'] * len(row))
                insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
                cursor.execute(insert_query, tuple(row))

            mydb.commit()
            st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please fill all fields and upload CSV.")
import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configure API Key
genai.configure(api_key="AIzaSyBUSyS2AOlh8rXADFjfAkeVJ5B_uYh7lxA")

# Use working model
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Page title
st.title("📊 AI Financial Statement Analyzer")
st.write("Upload financial data to generate insights and visualizations automatically.")

# File uploader
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])


# Function to load file
def load_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)


# Function to generate AI summary
def generate_summary(data):
    prompt = f"""
    Analyze this financial sales data and provide:
    1. Key trends
    2. Best performing country
    3. Best performing product
    4. Any useful business insights

    Data:
    {data.head(20).to_dict()}
    """

    response = model.generate_content(prompt)
    return response.text


# Main logic
if uploaded_file is not None:

    data = load_file(uploaded_file)

    st.subheader("📂 Uploaded Data")
    st.write(data)

    # Dashboard metrics
    if "Gross Sales" in data.columns and "Units Sold" in data.columns:

        total_sales = data["Gross Sales"].sum()
        total_units = data["Units Sold"].sum()
        avg_price = data["Sale Price"].mean()

        st.subheader("📊 Key Insights")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sales", round(total_sales, 2))
        col2.metric("Units Sold", round(total_units, 2))
        col3.metric("Average Price", round(avg_price, 2))

    # AI Summary Button
    if st.button("Generate AI Insights"):
        with st.spinner("Analyzing data..."):
            summary = generate_summary(data)

            st.subheader("🤖 AI Insights")
            st.write(summary)

            st.success("Analysis completed successfully!")

    # Charts
    st.subheader("📈 Sales by Country")
    sales_country = data.groupby("Country")["Gross Sales"].sum()
    st.bar_chart(sales_country)

    st.subheader("📈 Sales by Product")
    sales_product = data.groupby("Product")["Gross Sales"].sum()
    st.bar_chart(sales_product)

else:
    st.warning("Please upload a file to begin.")

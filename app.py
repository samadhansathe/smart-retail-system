import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Smart Retail System",
    page_icon="🛒",
    layout="wide"
)

# ---------------- DATABASE CONNECTION ---------------- #

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Samadhan@2141",
    database="smart_retail_system"
)

cursor = connection.cursor()

# ---------------- LOGIN SYSTEM ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():

    st.markdown("""
    <h1 style='text-align:center;'>
    🔐 Smart Retail Login
    </h1>
    """, unsafe_allow_html=True)

    st.write("Welcome to Smart Retail System 😎")

    with st.form("login_form"):

        username = st.text_input(
            "👤 Username"
        )

        password = st.text_input(
            "🔑 Password",
            type="password"
        )

        login_button = st.form_submit_button(
            "Login"
        )

        if login_button:

            if (
                username == "admin"
                and
                password == "admin123"
            ):

                st.session_state.logged_in = True
                st.rerun()

            else:

                st.error(
                    "❌ Invalid Username or Password"
                )


# SHOW LOGIN ONLY IF NOT LOGGED IN
if not st.session_state.logged_in:

    login()

    st.stop()


# ---------------- PREMIUM CSS ---------------- #

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

section[data-testid="stSidebar"] {
    background-color: #1e293b;
}

section[data-testid="stSidebar"] * {
    color: white;
}

div[data-testid="metric-container"] {
    background: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

st.markdown("""
<h1 style='text-align:center;'>
🛒 Smart Retail Operations System
</h1>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ADMIN PANEL ---------------- #

st.sidebar.title("🛍️ Smart Retail")

st.sidebar.markdown("---")

st.sidebar.subheader("👤 Admin Panel")

st.sidebar.success("🟢 Online")

st.sidebar.write(
    "**Username:** Admin"
)

today = datetime.now()

st.sidebar.write(
    f"📅 Date: {today.strftime('%d-%m-%Y')}"
)

st.sidebar.write(
    f"🕒 Time: {today.strftime('%I:%M %p')}"
)

st.sidebar.markdown("---")

# Logout Button
if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False

    st.rerun()

# ---------------- MENU ---------------- #

menu = st.sidebar.selectbox(
    "📌 Choose Option",
    [
        "🏠 Home Dashboard",
        "📦 View Products",
        "➕ Add Product",
        "✏️ Update Product",
        "🗑️ Delete Product",
        "🔍 Search Product",
        "📊 Product Statistics"
    ]
)

# ---------------- HOME DASHBOARD ---------------- #

if menu == "🏠 Home Dashboard":

    st.title("👋 Welcome Admin")

    st.write(
        "Manage products, analytics and retail operations."
    )

    st.markdown("---")

    # KPI Data
    cursor.execute(
        "SELECT COUNT(*) FROM products"
    )

    total_products = cursor.fetchone()[0]

    cursor.execute(
        "SELECT SUM(stock_quantity) FROM products"
    )

    total_stock = cursor.fetchone()[0]

    cursor.execute(
        "SELECT AVG(price) FROM products"
    )

    avg_price = cursor.fetchone()[0]

    # KPI Cards
    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📦 Total Products",
            total_products
        )

    with col2:

        st.metric(
            "📦 Total Stock",
            total_stock
        )

    with col3:

        st.metric(
            "💰 Avg Product Price",
            f"₹{avg_price:.2f}"
        )

    st.markdown("---")

    st.subheader(
        "📈 Retail Overview"
    )

    cursor.execute("""
    SELECT category,
    COUNT(*)
    FROM products
    GROUP BY category
    """)

    category_data = cursor.fetchall()

    category_df = pd.DataFrame(
        category_data,
        columns=[
            "Category",
            "Count"
        ]
    )

    chart = px.pie(
        category_df,
        names="Category",
        values="Count"
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )

    # ---------------- VIEW PRODUCTS ---------------- #

elif menu == "📦 View Products":

    st.subheader("📦 Product List")

    cursor.execute(
        "SELECT * FROM products"
    )

    products = cursor.fetchall()

    df = pd.DataFrame(
        products,
        columns=[
            "Product ID",
            "Product Name",
            "Category",
            "Price",
            "Stock",
            "Supplier ID"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------- ADD PRODUCT ---------------- #

elif menu == "➕ Add Product":

    st.subheader("➕ Add Product")

    name = st.text_input(
        "Product Name"
    )

    category = st.text_input(
        "Category"
    )

    price = st.number_input(
        "Price",
        min_value=0.0
    )

    stock = st.number_input(
        "Stock Quantity",
        min_value=0
    )

    supplier_id = st.number_input(
        "Supplier ID",
        min_value=1
    )

    if st.button("Add Product"):

        query = """
        INSERT INTO products
        (
            product_name,
            category,
            price,
            stock_quantity,
            supplier_id
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            name,
            category,
            price,
            stock,
            supplier_id
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        st.success(
            "✅ Product Added Successfully!"
        )

# ---------------- UPDATE PRODUCT ---------------- #

elif menu == "✏️ Update Product":

    st.subheader(
        "✏️ Update Product"
    )

    cursor.execute("""
        SELECT product_id,
        product_name
        FROM products
    """)

    products = cursor.fetchall()

    product_dict = {
        f"{row[0]} - {row[1]}":
        row[0]
        for row in products
    }

    selected_product = st.selectbox(
        "Select Product",
        list(product_dict.keys())
    )

    selected_id = product_dict[
        selected_product
    ]

    new_price = st.number_input(
        "New Price",
        min_value=0.0
    )

    new_stock = st.number_input(
        "New Stock Quantity",
        min_value=0
    )

    if st.button("Update Product"):

        query = """
        UPDATE products
        SET
        price = %s,
        stock_quantity = %s
        WHERE product_id = %s
        """

        cursor.execute(
            query,
            (
                new_price,
                new_stock,
                selected_id
            )
        )

        connection.commit()

        st.success(
            "✅ Product Updated Successfully!"
        )

# ---------------- DELETE PRODUCT ---------------- #

elif menu == "🗑️ Delete Product":

    st.subheader(
        "🗑️ Delete Product"
    )

    cursor.execute("""
        SELECT product_id,
        product_name
        FROM products
    """)

    products = cursor.fetchall()

    product_dict = {
        f"{row[0]} - {row[1]}":
        row[0]
        for row in products
    }

    selected_product = st.selectbox(
        "Select Product to Delete",
        list(product_dict.keys())
    )

    selected_id = product_dict[
        selected_product
    ]

    if st.button(
        "Delete Product"
    ):

        try:

            query = """
            DELETE FROM products
            WHERE product_id = %s
            """

            cursor.execute(
                query,
                (selected_id,)
            )

            connection.commit()

            st.success(
                "✅ Product Deleted Successfully!"
            )

        except:

            st.error(
                "❌ Product linked to orders"
            )

# ---------------- SEARCH PRODUCT ---------------- #

elif menu == "🔍 Search Product":

    st.subheader(
        "🔍 Search Product"
    )

    product_name = st.text_input(
        "Enter Product Name"
    )

    if st.button("Search"):

        query = """
        SELECT *
        FROM products
        WHERE product_name = %s
        """

        cursor.execute(
            query,
            (product_name,)
        )

        result = cursor.fetchall()

        if result:

            df = pd.DataFrame(
                result,
                columns=[
                    "Product ID",
                    "Product Name",
                    "Category",
                    "Price",
                    "Stock",
                    "Supplier ID"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.error(
                "❌ Product Not Found"
            )

# ---------------- PRODUCT STATISTICS ---------------- #

elif menu == "📊 Product Statistics":

    st.subheader(
        "📊 Product Statistics Dashboard"
    )

    # KPI DATA
    cursor.execute(
        "SELECT COUNT(*) FROM products"
    )

    total_products = cursor.fetchone()[0]

    cursor.execute(
        "SELECT SUM(stock_quantity) FROM products"
    )

    total_stock = cursor.fetchone()[0]

    cursor.execute(
        "SELECT AVG(price) FROM products"
    )

    avg_price = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
        product_name,
        price
        FROM products
        ORDER BY price DESC
        LIMIT 1
    """)

    expensive_product = (
        cursor.fetchone()
    )

    # KPI CARDS
    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📦 Total Products",
            total_products
        )

    with col2:

        st.metric(
            "📦 Total Stock",
            total_stock
        )

    with col3:

        st.metric(
            "💰 Average Price",
            f"₹{avg_price:.2f}"
        )

    with col4:

        st.metric(
            "🏆 Expensive Product",
            expensive_product[0]
        )

    st.markdown("---")

    st.subheader(
        "📈 Analytics Dashboard"
    )

    # CHART DATA
    cursor.execute("""
        SELECT
        product_name,
        category,
        price,
        stock_quantity
        FROM products
    """)

    chart_data = cursor.fetchall()

    chart_df = pd.DataFrame(
        chart_data,
        columns=[
            "Product",
            "Category",
            "Price",
            "Stock"
        ]
    )

    # PIE + STOCK CHART
    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "🥧 Category Distribution"
        )

        pie_chart = px.pie(
            chart_df,
            names="Category",
            title="Products by Category"
        )

        st.plotly_chart(
            pie_chart,
            use_container_width=True
        )

    with col2:

        st.subheader(
            "📦 Product Stock"
        )

        stock_chart = px.bar(
            chart_df,
            x="Product",
            y="Stock",
            title="Stock Analysis"
        )

        st.plotly_chart(
            stock_chart,
            use_container_width=True
        )

    # PRICE COMPARISON
    st.subheader(
        "💰 Product Price Comparison"
    )

    price_chart = px.bar(
        chart_df,
        x="Product",
        y="Price",
        title="Price Comparison"
    )

    st.plotly_chart(
        price_chart,
        use_container_width=True
    )

# ---------------- CLOSE DATABASE ---------------- #

connection.close()
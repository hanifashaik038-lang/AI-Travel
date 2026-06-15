# app.py
# MiniStore homepage built with Streamlit only.
# This page includes:
# - Hero / welcome section
# - Featured products
# - Product grid using st.columns
# - Sidebar with categories and shopping cart summary
# - Custom CSS styling
# - Floating support button that navigates to the Support Chatbot page

import streamlit as st
from catalog import PRODUCTS, CATEGORIES, get_product_by_id

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="MiniStore",
    page_icon="🛍️",
    layout="wide",
)

# ---------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------
if "cart" not in st.session_state:
    # Cart stores product_id -> quantity
    st.session_state.cart = {}

# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------
def add_to_cart(product_id: str):
    """Add one unit of a product to the cart."""
    st.session_state.cart[product_id] = st.session_state.cart.get(product_id, 0) + 1


def cart_total_items() -> int:
    """Return total number of items in the cart."""
    return sum(st.session_state.cart.values())


def cart_total_price() -> float:
    """Return the total cart value."""
    total = 0.0
    for product_id, quantity in st.session_state.cart.items():
        product = get_product_by_id(product_id)
        if product:
            total += product["price"] * quantity
    return total


# ---------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
        }

        .hero {
            padding: 2.5rem 2rem;
            border-radius: 24px;
            background: linear-gradient(135deg, #111827 0%, #1f2937 40%, #4f46e5 100%);
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 20px 50px rgba(15, 23, 42, 0.20);
        }

        .hero h1 {
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }

        .hero p {
            font-size: 1.08rem;
            color: #e5e7eb;
            margin-bottom: 0;
        }

        .section-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #111827;
            margin-top: 1rem;
            margin-bottom: 0.75rem;
        }

        .featured-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
            min-height: 160px;
        }

        .product-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 20px;
            padding: 1.2rem;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
            margin-bottom: 0.75rem;
        }

        .product-icon {
            font-size: 2rem;
            margin-bottom: 0.35rem;
        }

        .product-name {
            font-size: 1.2rem;
            font-weight: 700;
            color: #111827;
            margin-bottom: 0.35rem;
        }

        .product-category {
            display: inline-block;
            background: #eef2ff;
            color: #4338ca;
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 0.7rem;
        }

        .product-description {
            color: #4b5563;
            min-height: 72px;
            margin-bottom: 0.8rem;
        }

        .product-price {
            font-size: 1.25rem;
            font-weight: 800;
            color: #111827;
            margin-bottom: 0.5rem;
        }

        .floating-support {
            position: fixed;
            right: 24px;
            bottom: 24px;
            z-index: 99999;
        }

        .floating-support a {
            text-decoration: none;
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white !important;
            padding: 0.95rem 1.2rem;
            border-radius: 999px;
            box-shadow: 0 12px 30px rgba(79, 70, 229, 0.35);
            font-weight: 700;
            font-size: 0.95rem;
        }

        .sidebar-note {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 0.85rem;
            color: #374151;
            font-size: 0.92rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
st.sidebar.title("MiniStore")
st.sidebar.caption("Browse categories and review your cart.")

selected_category = st.sidebar.radio("Product categories", CATEGORIES, index=0)

st.sidebar.markdown("---")
st.sidebar.subheader("Shopping cart summary")

if st.session_state.cart:
    for product_id, quantity in st.session_state.cart.items():
        product = get_product_by_id(product_id)
        if product:
            st.sidebar.write(
                f"**{product['name']}** x {quantity} — ${product['price'] * quantity:.2f}"
            )
else:
    st.sidebar.info("Your cart is empty.")

st.sidebar.metric("Items in cart", cart_total_items())
st.sidebar.metric("Cart total", f"${cart_total_price():.2f}")

st.sidebar.markdown("---")
st.sidebar.page_link(
    "pages/1_Support_Chatbot.py",
    label="Open Support Chatbot",
    icon="💬",
)

st.sidebar.markdown(
    """
    <div class="sidebar-note">
        Need help with products, shipping, refunds, returns, payments, or order questions?
        Open the support chatbot anytime.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Hero section
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>MiniStore</h1>
        <p>
            Welcome to MiniStore — a modern demo e-commerce experience built with Streamlit.
            Explore curated products, add items to your cart, and get instant help from our support assistant.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Welcome stats / highlights
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="featured-card">
            <h4>Fast Delivery</h4>
            <p>Standard delivery in 3–5 business days and express shipping in 1–2 business days.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="featured-card">
            <h4>Easy Returns</h4>
            <p>Unused items can be returned within 30 days in original packaging.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="featured-card">
            <h4>Secure Payments</h4>
            <p>Checkout support for major cards, PayPal, Apple Pay, and Google Pay.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# Featured products section
# ---------------------------------------------------------
st.markdown('<div class="section-title">Featured Products</div>', unsafe_allow_html=True)

featured_cols = st.columns(3)
for col, product in zip(featured_cols, PRODUCTS[:3]):
    with col:
        st.markdown(
            f"""
            <div class="featured-card">
                <div style="font-size:2rem;">{product["icon"]}</div>
                <div style="font-weight:700; font-size:1.1rem; color:#111827;">{product["name"]}</div>
                <div style="color:#4f46e5; font-weight:700; margin:0.35rem 0;">${product["price"]:.2f}</div>
                <div style="color:#4b5563;">{product["description"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# Product grid section
# ---------------------------------------------------------
st.markdown('<div class="section-title">Shop the Collection</div>', unsafe_allow_html=True)

if selected_category == "All":
    filtered_products = PRODUCTS
else:
    filtered_products = [
        product for product in PRODUCTS if product["category"] == selected_category
    ]

if not filtered_products:
    st.warning("No products found in this category.")
else:
    # Create a responsive 3-column product grid
    for i in range(0, len(filtered_products), 3):
        cols = st.columns(3)
        for col, product in zip(cols, filtered_products[i : i + 3]):
            with col:
                st.markdown(
                    f"""
                    <div class="product-card">
                        <div class="product-icon">{product["icon"]}</div>
                        <div class="product-name">{product["name"]}</div>
                        <div class="product-category">{product["category"]}</div>
                        <div class="product-description">{product["description"]}</div>
                        <div class="product-price">${product["price"]:.2f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    f"Add to Cart • ${product['price']:.2f}",
                    key=f"add_{product['id']}",
                    use_container_width=True,
                ):
                    add_to_cart(product["id"])
                    st.success(f"{product['name']} added to cart.")

# ---------------------------------------------------------
# Floating support button
# This uses the Streamlit multipage route for the Support Chatbot page.
# ---------------------------------------------------------
st.markdown(
    """
    <div class="floating-support">
        <a href="./Support_Chatbot" target="_self">💬 Support</a>
    </div>
    """,
    unsafe_allow_html=True,
)

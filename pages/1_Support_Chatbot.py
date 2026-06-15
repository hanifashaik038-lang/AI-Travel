# pages/1_Support_Chatbot.py
# OpenAI-powered support chatbot for MiniStore.
# Features:
# - Uses Streamlit chat components
# - Preserves chat history with st.session_state
# - Reads API key from st.secrets["OPENAI_API_KEY"]
# - Restricts responses to MiniStore support topics only
# - Includes store catalog data in the system prompt

import streamlit as st
from openai import OpenAI
from catalog import PRODUCTS, get_catalog_text

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Support Chatbot | MiniStore",
    page_icon="💬",
    layout="wide",
)

# ---------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .support-header {
            padding: 1.6rem 1.8rem;
            border-radius: 22px;
            background: linear-gradient(135deg, #111827 0%, #312e81 100%);
            color: white;
            margin-bottom: 1rem;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.18);
        }

        .support-header h1 {
            margin-bottom: 0.35rem;
        }

        .support-header p {
            margin-bottom: 0;
            color: #e5e7eb;
        }

        .policy-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
            margin-bottom: 0.75rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Validate secrets
# ---------------------------------------------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error(
        "Missing OPENAI_API_KEY in Streamlit secrets. Add it to .streamlit/secrets.toml before running the chatbot."
    )
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------------------------------------------------
# Session state for persistent chat history
# ---------------------------------------------------------
if "support_messages" not in st.session_state:
    st.session_state.support_messages = [
        {
            "role": "assistant",
            "content": (
                "Hello and welcome to MiniStore Support. I can help with products, "
                "delivery, refunds, returns, payments, and order-related questions."
            ),
        }
    ]

# ---------------------------------------------------------
# Build the system prompt
# ---------------------------------------------------------
def build_system_prompt() -> str:
    catalog_text = get_catalog_text()

    return f"""
You are a professional customer support representative for MiniStore, a demo e-commerce store.

Your job is to help customers only with store-related topics, including:
- product information
- product comparisons
- delivery and shipping
- refunds
- returns
- payment methods
- order status guidance
- cart and checkout help

Store catalog:
{catalog_text}

MiniStore support policies:
- Standard delivery: 3 to 5 business days
- Express delivery: 1 to 2 business days
- Returns: accepted within 30 days for unused items in original packaging
- Refunds: processed within 5 to 7 business days after a return is approved
- Payment methods: Visa, Mastercard, American Express, PayPal, Apple Pay, Google Pay
- Order status: this demo app does not connect to a real order database, so never invent live order details

Behavior rules:
- Be helpful, concise, polite, and professional
- Answer only MiniStore support questions
- If asked unrelated questions, politely redirect the user back to MiniStore support topics
- Use the catalog above when answering product questions
- Do not invent products, prices, policies, or order data
- If the user asks for live order tracking, explain this is a demo store and offer general order-status guidance instead
- When helpful, mention product names and prices exactly as listed in the catalog
""".strip()


def build_openai_messages():
    """Convert Streamlit chat history into OpenAI Responses API input format."""
    messages = [
        {
            "role": "system",
            "content": [{"type": "input_text", "text": build_system_prompt()}],
        }
    ]

    for message in st.session_state.support_messages:
        messages.append(
            {
                "role": message["role"],
                "content": [{"type": "input_text", "text": message["content"]}],
            }
        )

    return messages


# ---------------------------------------------------------
# Page header
# ---------------------------------------------------------
st.markdown(
    """
    <div class="support-header">
        <h1>MiniStore Support Chatbot</h1>
        <p>
            Ask about products, delivery, refunds, returns, payment options, or order support.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
st.sidebar.title("Support Center")
st.sidebar.page_link("app.py", label="Back to Homepage", icon="🏠")

st.sidebar.markdown("### MiniStore products")
for product in PRODUCTS:
    st.sidebar.markdown(
        f"**{product['name']}**  \n{product['category']} • ${product['price']:.2f}"
    )

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    ### Quick support topics
    - Product details
    - Shipping and delivery
    - Refunds
    - Returns
    - Payment methods
    - Order status
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div class="policy-card">
        <strong>Demo Notice</strong><br>
        This support assistant can answer store questions, but it does not connect to a live order system.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Display chat history
# ---------------------------------------------------------
for message in st.session_state.support_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------
user_prompt = st.chat_input("Ask MiniStore Support a question...")

if user_prompt:
    # Save and display the user's message
    st.session_state.support_messages.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate assistant response from OpenAI
    with st.chat_message("assistant"):
        with st.spinner("MiniStore Support is typing..."):
            try:
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=build_openai_messages(),
                )

                assistant_reply = response.output_text.strip()

                if not assistant_reply:
                    assistant_reply = (
                        "I’m sorry, but I couldn’t generate a response just now. "
                        "Please try asking your MiniStore support question again."
                    )

            except Exception:
                assistant_reply = (
                    "I’m sorry, but the support service is temporarily unavailable. "
                    "Please try again in a moment."
                )

        st.markdown(assistant_reply)

    # Save assistant reply into session state
    st.session_state.support_messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

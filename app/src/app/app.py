import time

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from loguru import logger

from src.agent.agent import graph

# Load environment variables
load_dotenv()

# Setup logging
logger.add("logs/app.log")
logger.info("Streamlit app initialized")


logger.info("Agent graph imported successfully")
st.set_page_config(
    page_title="TravelBuddy - Trợ lý Du lịch",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .main {
            background-color: #f8f9fa;
        }
        .stChatMessage {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
        }
        .travel-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.85rem;
            font-weight: 600;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
        .flight-badge { background-color: #e3f2fd; color: #1976d2; }
        .hotel-badge { background-color: #f3e5f5; color: #7b1fa2; }
        .budget-badge { background-color: #e8f5e9; color: #388e3c; }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.title("✈️ TravelBuddy")
    st.write("**Trợ lý Du lịch Thông minh**")
    st.write("Vietnamese Travel Planning AI Agent")

    st.divider()

    st.subheader("📍 Available Cities")
    cities = ["Hà Nội", "Đà Nẵng", "Phú Quốc", "Hồ Chí Minh"]
    for city in cities:
        st.text(f"• {city}")

    st.divider()

    st.subheader("🛠️ Features")
    st.write("""
    - ✈️ Flight Search
    - 🏨 Hotel Recommendations
    - 💰 Budget Calculation
    - 🗺️ Travel Planning
    """)

    st.divider()

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    with st.expander("ℹ️ About"):
        st.write("""
        **TravelBuddy** is an AI-powered travel assistant built with:
        - LangChain for tool management
        - LangGraph for agent orchestration
        - OpenAI GPT-4o-mini for language understanding
        - Streamlit for the web interface
        """)


# Main content
st.title("🧳 TravelBuddy - Your Travel Planning Assistant")
st.write("Ask me about flights, hotels, and travel planning in Vietnam!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "tools_used" in message and message["tools_used"]:
            cols = st.columns(len(message["tools_used"]))
            for col, tool in zip(cols, message["tools_used"]):
                with col:
                    if tool == "search_flights":
                        st.markdown('<span class="travel-badge flight-badge">✈️ Flights</span>', unsafe_allow_html=True)
                    elif tool == "search_hotels":
                        st.markdown('<span class="travel-badge hotel-badge">🏨 Hotels</span>', unsafe_allow_html=True)
                    elif tool == "calculate_budget":
                        st.markdown('<span class="travel-badge budget-badge">💰 Budget</span>', unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask me about travel planning... (e.g., 'Tìm chuyến bay từ Hà Nội đến Phú Quốc')"):
    logger.info("=" * 80)
    logger.info("NEW QUERY - STREAMLIT APP")
    logger.info("=" * 80)
    logger.info(f"User Input: {prompt}")
    logger.debug(f"Input length: {len(prompt)} characters")

    user_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    logger.info(f"Total user queries so far: {user_count}")

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    logger.debug("User message added to session state")

    # Get agent response
    with st.spinner("🤔 TravelBuddy is thinking..."):
        try:
            logger.info("Starting agent invocation...")

            # Prepare messages for the agent
            agent_messages = [
                HumanMessage(content=msg["content"]) for msg in st.session_state.messages if msg["role"] == "user"
            ]

            logger.debug(f"Prepared {len(agent_messages)} messages for agent")
            for i, msg in enumerate(agent_messages):
                preview = msg.content[:80] + "..." if len(msg.content) > 80 else msg.content
                logger.debug(f"  Message {i}: {preview}")

            # Invoke the agent
            logger.info("Invoking graph...")
            start_time = time.time()

            result = graph.invoke({"messages": agent_messages})

            elapsed_time = time.time() - start_time
            logger.info(f"Graph invocation completed in {elapsed_time:.2f}s")

            logger.debug(f"Result messages count: {len(result['messages'])}")

            # Extract response
            logger.debug("Extracting response from result...")
            last_message = result["messages"][-1]
            response_text = last_message.content

            logger.info(f"Response content length: {len(response_text)} characters")

            # Detect which tools were used
            tools_used = []
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                tools_used = [tc["name"] for tc in last_message.tool_calls]
                logger.info(f"Tool calls detected: {len(tools_used)}")
                for tc in last_message.tool_calls:
                    logger.debug(f"  Tool: {tc['name']}")
                    logger.debug(f"    Arguments: {tc['args']}")
            else:
                logger.info("No tool calls - Direct LLM response")

            logger.debug(f"Response preview: {response_text[:200]}...")

            # Display agent response
            with st.chat_message("assistant"):
                st.markdown(response_text)

                # Show tools used
                if tools_used:
                    st.divider()
                    st.caption(f"🔧 Tools used: {', '.join(tools_used)}")

            # Add to session state
            st.session_state.messages.append({"role": "assistant", "content": response_text, "tools_used": tools_used})

            logger.info("Response added to session state")
            logger.info("Query processing complete")
            logger.info("=" * 80)

        except Exception as e:
            logger.error("=" * 80)
            logger.error("EXCEPTION DURING AGENT INVOCATION")
            logger.error("=" * 80)
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception message: {str(e)}")
            logger.exception("Full traceback:")
            logger.error("=" * 80)

            st.error(f"❌ Error: {str(e)}")

# Footer
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: #666;">
        <small>
        🌍 TravelBuddy v1.0 | Built with ❤️ using LangChain, LangGraph & Streamlit
        </small>
    </div>
""",
    unsafe_allow_html=True,
)

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from loguru import logger
from src.agent.agent import graph

# Load environment variables
load_dotenv()

# Setup logging
logger.add("logs/demo.log")


logger.info("=" * 70)
logger.info("TravelBuddy - Trợ lý Du lịch Thông minh")
logger.info("Vietnamese Travel Planning AI Agent Demo")
logger.info("=" * 70)


def run_demo_query(query: str, description: str = ""):
    """Run a single demo query and display results."""
    logger.info(f"{'─' * 70}")
    if description:
        logger.info(f"📌 Demo: {description}")
    logger.info(f"👤 User: {query}")
    logger.info(f"{'─' * 70}")

    try:
        result = graph.invoke({"messages": [HumanMessage(content=query)]})

        # Extract and display the response
        last_message = result["messages"][-1]
        response_text = last_message.content

        logger.info("🤖 TravelBuddy:")
        logger.info(response_text)

    except Exception as e:
        logger.error(f"Query failed: {e}")


def run_interactive_mode():
    """Run interactive mode where user can chat freely."""
    logger.info("=" * 70)
    logger.info("🎯 Interactive Mode")
    logger.info("=" * 70)
    logger.info("You can now chat with TravelBuddy. Type 'quit' or 'exit' to end.\n")

    messages = []
    while True:
        try:
            user_input = input("👤 You: ").strip()

            if user_input.lower() in ["quit", "exit", "thoát", "thoát khỏi"]:
                logger.info("👋 Goodbye! Have a great trip!")
                break

            if not user_input:
                continue

            logger.info(f"👤 User: {user_input}")
            messages.append(HumanMessage(content=user_input))
            result = graph.invoke({"messages": messages})

            last_message = result["messages"][-1]
            response_text = last_message.content

            logger.info(f"🤖 TravelBuddy: {response_text}\n")
            messages = result["messages"]

        except KeyboardInterrupt:
            logger.info("👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Interactive mode error: {e}")


def main():
    """Run the demo."""

    # Demo 1: Greeting
    run_demo_query("Xin chào", "Greeting - Initial conversation")

    # Demo 2: Flight search request
    run_demo_query("Tôi muốn tìm chuyến bay từ Hà Nội đến Phú Quốc", "Flight search - Simple query")

    # Demo 3: Hotel search with budget
    run_demo_query(
        "Bạn có thể giúp tôi tìm khách sạn ở Đà Nẵng với giá dưới 1.5 triệu đồng một đêm không?",
        "Hotel search - With budget constraint",
    )

    # Demo 4: Budget calculation
    run_demo_query(
        "Tôi có ngân sách 5 triệu đồng. Chuyến bay hết 1.35 triệu, khách sạn 2 đêm hết 3 triệu. Còn bao nhiêu tiền?",
        "Budget calculation - Expense tracking",
    )

    # Demo 5: Complex travel planning query
    run_demo_query(
        "Tôi muốn đi từ Hà Nội đến Phú Quốc trong 3 ngày với ngân sách 5 triệu. Có cách nào tối ưu hóa chi phí không?",
        "Complex travel planning - Multiple requirements",
    )

    # Demo 6: Out of scope query
    run_demo_query("Giúp tôi với công thức numpy đi", "Out of scope - Agent should politely redirect")

    # Demo 7: Hotel information for multiple cities
    run_demo_query(
        "Bạn có thể so sánh giá khách sạn ở Đà Nẵng, Phú Quốc và Hồ Chí Minh không?",
        "Hotel comparison - Multiple locations",
    )

    logger.info("=" * 70)
    logger.info("📊 Demo Summary - All demo queries completed successfully!")
    logger.info("=" * 70)
    logger.info("""The TravelBuddy agent demonstrated:
✅ Greeting and natural conversation
✅ Flight search with origin/destination queries
✅ Hotel recommendations with budget filtering
✅ Budget calculation and financial planning
✅ Complex travel itinerary planning
✅ Out-of-scope query handling
✅ Multi-location hotel comparisons""")

    print("\n" + "=" * 70)
    print("Would you like to try interactive mode? (y/n)")
    choice = input().strip().lower()

    if choice in ["y", "yes", "có"]:
        run_interactive_mode()
    else:
        logger.info("👋 Thank you for watching the demo!")


if __name__ == "__main__":
    main()

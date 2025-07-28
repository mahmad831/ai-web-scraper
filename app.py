import streamlit as st
from scrapegraphai.graphs import SmartScraperGraph

# Set page configuration for a wider layout
st.set_page_config(layout="wide")

# --- Sidebar for Configuration ---
st.sidebar.header("Configuration")

api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
model_option = st.sidebar.selectbox(
    "Select OpenAI Model:",
    ("openai/gpt-4o-mini", "openai/gpt-3.5-turbo", "openai/gpt-4")
)
verbose_mode = st.sidebar.checkbox("Enable Verbose Output", value=True)
headless_mode = st.sidebar.checkbox("Run Browser in Headless Mode (no GUI)", value=False)


# --- Main Application Area ---
st.title("🤖 AI Web Scraper")
st.markdown("Extract information from websites using the power of AI.")

st.subheader("What do you want to extract?")
prompt = st.text_area(
    "Describe the information you need (e.g., 'all product names and their prices', 'the main article content and author').",
    height=100
)

st.subheader("Where do you want to scrape from?")
source_url = st.text_input("Enter the source URL (e.g., 'https://www.example.com'):")

# Instructions for the user
with st.expander("💡 How to Use"):
    st.markdown("""
    1. **Enter your OpenAI API Key** in the sidebar. This is required for the AI to function.
    2. **Select an OpenAI Model** from the dropdown in the sidebar. `gpt-4o-mini` is a good default.
    3. **Describe the information** you want to extract in the "What do you want to extract?" text area. Be as specific as possible.
    4. **Enter the URL** of the website you want to scrape in the "Where do you want to scrape from?" input box.
    5. Optionally, **toggle Verbose Output** to see more details about the scraping process in your console.
    6. Optionally, **toggle Headless Mode** to run the web browser invisibly in the background. If unchecked, a browser window might appear.
    7. Click on the "🚀 Start Scraping" button.
    """)

# Button to start the scraping process
if st.button("🚀 Start Scraping", use_container_width=True):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not prompt:
        st.error("Please provide the information you want to extract.")
    elif not source_url:
        st.error("Please provide the source URL.")
    else:
        st.info("Scraping in progress... This may take a moment.")
        
        # Configuration for the scraping pipeline
        graph_config = {
            "llm": {
                "api_key": api_key,
                "model": model_option,
            },
            "verbose": verbose_mode,
            "headless": headless_mode,
        }

        try:
            with st.spinner("Thinking and scraping..."):
                # Create the SmartScraperGraph instance
                smart_scraper_graph = SmartScraperGraph(
                    prompt=prompt,
                    source=source_url,
                    config=graph_config
                )

                # Run the pipeline
                result = smart_scraper_graph.run()

            st.success("Scraping complete!")
            st.subheader("Extracted Information:")
            st.json(result) # Display as JSON for structured data
            
        except Exception as e:
            st.error(f"An error occurred during scraping: {e}")
            st.warning("Please check your API key, prompt, and URL. Also ensure the website is accessible.")

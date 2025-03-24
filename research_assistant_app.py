# research_assistant_app.py
import streamlit as st
from streamlit_chat import message
import random

# Set page configuration
st.set_page_config(
    page_title="Research Assistant AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_stage" not in st.session_state:
    st.session_state.current_stage = "welcome"
if "research_data" not in st.session_state:
    st.session_state.research_data = {
        "topic": "",
        "research_question": "",
        "sources": [],
        "outline": "",
        "methodology": ""
    }

# CSS for better styling
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .research-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.bot {
        background-color: #475063;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with research project tracking
with st.sidebar:
    st.title("📚 Research Project Tracker")
    
    with st.expander("📋 Project Overview", expanded=True):
        if st.session_state.research_data["topic"]:
            st.markdown(f"**Topic:** {st.session_state.research_data['topic']}")
        else:
            st.markdown("**Topic:** *Not defined yet*")
            
        if st.session_state.research_data["research_question"]:
            st.markdown(f"**Research Question:** {st.session_state.research_data['research_question']}")
        else:
            st.markdown("**Research Question:** *Not defined yet*")
    
    with st.expander("📚 Sources", expanded=False):
        if st.session_state.research_data["sources"]:
            for i, source in enumerate(st.session_state.research_data["sources"]):
                st.markdown(f"{i+1}. {source}")
        else:
            st.markdown("*No sources added yet*")
    
    with st.expander("🗂️ Research Tools", expanded=False):
        tool_options = [
            "Topic Selection Guide",
            "Source Credibility Checker",
            "Citation Generator",
            "Research Methods Explainer",
            "Literature Review Assistant"
        ]
        
        selected_tool = st.selectbox("Select a research tool:", tool_options)
        
        if st.button("Launch Tool"):
            st.session_state.messages.append({"role": "user", "content": f"I need help with {selected_tool}"})
            if "Topic Selection" in selected_tool:
                response = "Let's work on finding a good research topic. A good topic should be:\n\n1. Specific enough to be manageable\n2. Broad enough to find sufficient sources\n3. Interesting to you personally\n4. Relevant to your field\n\nWhat general area are you interested in researching?"
            elif "Credibility" in selected_tool:
                response = "To evaluate source credibility, consider the CRAAP test:\n\n• Currency: When was it published?\n• Relevance: Does it relate to your topic?\n• Authority: Who is the author/publisher?\n• Accuracy: Is it supported by evidence?\n• Purpose: Why does this information exist?\n\nWhat source would you like to evaluate?"
            elif "Citation" in selected_tool:
                response = "I can help format citations. What citation style do you need (APA, MLA, Chicago)? And what type of source are you citing?"
            elif "Methods" in selected_tool:
                response = "Research methods fall into several categories:\n\n• Qualitative: Interviews, observations, case studies\n• Quantitative: Surveys, experiments, statistical analysis\n• Mixed Methods: Combination of both\n\nWhat type of research question are you working with?"
            elif "Literature Review" in selected_tool:
                response = "A good literature review should:\n\n• Synthesize rather than summarize\n• Identify patterns and gaps\n• Connect to your research question\n• Be organized thematically or methodologically\n\nWould you like help organizing your literature or analyzing specific sources?"
                
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.markdown("---")
    st.markdown("### About This Tool")
    st.markdown("This AI research assistant helps undergraduate students with research projects by providing guidance on methodology, source evaluation, and academic writing.")

# Main interface
st.title("🔍 Research Assistant AI")

# Welcome message
if st.session_state.current_stage == "welcome":
    st.markdown("""
    <div class="research-card">
        <h3>Welcome to your Research Assistant AI! 👋</h3>
        <p>I'm here to help you with your undergraduate research project. I can assist with:</p>
        <ul>
            <li>Developing research questions</li>
            <li>Finding and evaluating sources</li>
            <li>Structuring your paper</li>
            <li>Research methodology</li>
            <li>Academic writing guidance</li>
        </ul>
        <p>Let's start by discussing your research interests!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Get Started"):
        st.session_state.current_stage = "chat"
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hi there! I'm your research assistant. What topic are you considering for your research project?"
        })
        st.experimental_rerun()

# Main chat interface
if st.session_state.current_stage == "chat":
    # Display chat messages
    for i, msg in enumerate(st.session_state.messages):
        message(msg["content"], is_user=msg["role"]=="user", key=f"msg_{i}")
    
    # Chat input
    user_input = st.text_area("Your message:", key="input", height=100)
    
    col1, col2 = st.columns([1, 6])
    with col1:
        submit_button = st.button("Send")
    with col2:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.experimental_rerun()
    
    # Process input
    if submit_button and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Simple response logic based on input
        if not st.session_state.research_data["topic"] and "topic" in user_input.lower():
            topic = user_input.replace("My topic is ", "").replace("I want to research ", "").strip()
            st.session_state.research_data["topic"] = topic
            response = f"Great choice on researching {topic}! A few questions to help refine this:\n\n1. What specific aspect of {topic} interests you most?\n2. Is this for a specific class or assignment?\n3. What's your preliminary research question about {topic}?"
        
        elif not st.session_state.research_data["research_question"] and "research question" in user_input.lower():
            question = user_input.strip()
            st.session_state.research_data["research_question"] = question
            response = f"That's an excellent research question! Now let's think about methodology. Would you be using:\n\n1. Quantitative methods (surveys, experiments, statistical analysis)\n2. Qualitative methods (interviews, observations, case studies)\n3. Mixed methods approach\n4. Literature-based research\n\nWhich approach seems most appropriate for your question?"
        
        elif "source" in user_input.lower() or "reference" in user_input.lower():
            if ":" in user_input:
                source = user_input.split(":", 1)[1].strip()
                st.session_state.research_data["sources"].append(source)
                response = f"I've added this source to your collection. When evaluating this source, consider:\n\n• Who are the authors? Are they experts in this field?\n• Is it peer-reviewed?\n• How recent is it?\n• Does it directly relate to your research question?\n\nWould you like guidance on finding more sources?"
            else:
                response = "To help with sources, I'll need more information. Are you looking for help finding sources, evaluating their credibility, or organizing them? Also, you can add a source to your project by typing 'Source: [citation details]'"
        
        elif "methodology" in user_input.lower() or "method" in user_input.lower():
            st.session_state.research_data["methodology"] = user_input
            response = "Let's develop your methodology further. Consider these aspects:\n\n1. **Sample/Participants**: Who/what will you study?\n2. **Data Collection**: How will you gather information?\n3. **Analysis Approach**: How will you interpret your findings?\n4. **Limitations**: What constraints might affect your research?\n\nWould you like me to elaborate on any of these aspects?"
        
        elif "outline" in user_input.lower() or "structure" in user_input.lower():
            response = "A strong research paper typically follows this structure:\n\n1. **Introduction**: Research question, significance, brief context\n2. **Literature Review**: Analysis of existing research\n3. **Methodology**: How you conducted the research\n4. **Results/Findings**: What you discovered\n5. **Discussion**: Interpretation of findings\n6. **Conclusion**: Summary and implications\n\nWould you like suggestions for any specific section?"
        
        elif "literature review" in user_input.lower():
            response = "For your literature review, follow these best practices:\n\n• **Organize thematically** rather than listing sources one by one\n• **Identify patterns and contradictions** in the existing research\n• **Highlight gaps** that your research addresses\n• **Connect each source** to your research question\n\nShould we work on developing categories for organizing your literature review?"
        
        elif "writing" in user_input.lower() or "academic" in user_input.lower():
            response = "For strong academic writing:\n\n• Use precise language and discipline-specific terminology\n• Make evidence-based claims with proper citations\n• Maintain an objective tone\n• Structure paragraphs with clear topic sentences\n• Revise for clarity and concision\n\nWould you like feedback on a specific paragraph or section you're working on?"
        
        else:
            responses = [
                "That's an interesting point. Could you elaborate on how this connects to your research question?",
                "I see what you're thinking. Have you considered how this might fit into your overall methodology?",
                "Good perspective. How does this relate to the sources you've gathered so far?",
                "That's a valuable insight. Would you like to explore some academic sources that address this aspect?",
                "I understand. Let's think about how to incorporate this into your research framework. What section of your paper would this information best support?"
            ]
            response = random.choice(responses)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.experimental_rerun()

# Research Resources Card
if st.session_state.current_stage == "chat":
    st.markdown("""
    <div class="research-card">
        <h3>📖 Research Resources</h3>
        <p><strong>Academic Databases:</strong> JSTOR, Google Scholar, PubMed, EBSCO, ProQuest</p>
        <p><strong>Writing Centers:</strong> Most universities offer free writing center consultations</p>
        <p><strong>Citation Tools:</strong> Zotero, Mendeley, EndNote</p>
        <p><strong>Research Guides:</strong> Check your university library's research guides</p>
    </div>
    """, unsafe_allow_html=True)

"""
GRE Vocabulary Learning App
A beautiful, hierarchical vocabulary navigation system built with Streamlit
"""

import streamlit as st
import json
from typing import Dict, List, Any
import random

# Page configuration
st.set_page_config(
    page_title="GRE Vocabulary Master",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #4A90E2;
        --secondary-color: #50C878;
        --accent-color: #FF6B6B;
        --bg-color: #F8F9FA;
        --card-color: #FFFFFF;
    }

    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }

    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }

    /* Category cards */
    .category-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }

    .category-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .category-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2C3E50;
        margin-bottom: 0.5rem;
    }

    .category-stats {
        color: #7F8C8D;
        font-size: 0.9rem;
    }

    /* Word cards */
    .word-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }

    .word-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2C3E50;
        margin-bottom: 0.5rem;
    }

    .word-meaning {
        font-size: 1.1rem;
        color: #34495E;
        line-height: 1.6;
    }

    /* Breadcrumb navigation */
    .breadcrumb {
        background: #ECF0F1;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        font-size: 1rem;
    }

    .breadcrumb-item {
        display: inline;
        color: #3498DB;
        cursor: pointer;
    }

    .breadcrumb-separator {
        margin: 0 0.5rem;
        color: #95A5A6;
    }

    /* Stats boxes */
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        display: block;
    }

    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }

    /* Search box */
    .search-box {
        margin-bottom: 2rem;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    /* Progress indicator */
    .progress-text {
        font-size: 0.9rem;
        color: #7F8C8D;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_vocabulary_data():
    """Load the vocabulary data from JSON file"""
    try:
        with open('vocab_hierarchical.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("❌ Vocabulary file not found! Please ensure 'vocab_hierarchical.json' is in the same directory.")
        return {}

def initialize_session_state():
    """Initialize session state variables"""
    if 'navigation_stack' not in st.session_state:
        st.session_state.navigation_stack = []
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'home'
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None
    if 'selected_subgroup' not in st.session_state:
        st.session_state.selected_subgroup = None
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'favorites' not in st.session_state:
        st.session_state.favorites = set()

def navigate_to_home():
    """Navigate to home view"""
    st.session_state.current_view = 'home'
    st.session_state.selected_category = None
    st.session_state.selected_subgroup = None
    st.session_state.navigation_stack = []

def navigate_to_category(category_name):
    """Navigate to a specific category"""
    st.session_state.current_view = 'category'
    st.session_state.selected_category = category_name
    st.session_state.selected_subgroup = None
    st.session_state.navigation_stack = [('home', 'Home'), ('category', category_name)]

def navigate_to_subgroup(category_name, subgroup_name):
    """Navigate to a specific subgroup"""
    st.session_state.current_view = 'subgroup'
    st.session_state.selected_category = category_name
    st.session_state.selected_subgroup = subgroup_name
    st.session_state.navigation_stack = [
        ('home', 'Home'),
        ('category', category_name),
        ('subgroup', subgroup_name)
    ]

def render_breadcrumb():
    """Render breadcrumb navigation"""
    if not st.session_state.navigation_stack:
        return

    breadcrumb_html = '<div class="breadcrumb">'

    for i, (view_type, name) in enumerate(st.session_state.navigation_stack):
        if i > 0:
            breadcrumb_html += '<span class="breadcrumb-separator">›</span>'

        breadcrumb_html += f'<span class="breadcrumb-item">{name}</span>'

    breadcrumb_html += '</div>'

    st.markdown(breadcrumb_html, unsafe_allow_html=True)

    # Back button
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if len(st.session_state.navigation_stack) > 1:
            if st.button("⬅️ Back", use_container_width=True):
                # Navigate back one level
                st.session_state.navigation_stack.pop()
                prev_view, prev_name = st.session_state.navigation_stack[-1]

                if prev_view == 'home':
                    navigate_to_home()
                elif prev_view == 'category':
                    navigate_to_category(prev_name)
                st.rerun()

    with col3:
        if st.button("🏠 Home", use_container_width=True):
            navigate_to_home()
            st.rerun()

def render_home_view(vocab_data):
    """Render the home view with all main categories"""

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📚 GRE Vocabulary Master</h1>
        <p>Master 934 essential GRE words through intelligent thematic grouping</p>
    </div>
    """, unsafe_allow_html=True)

    # Statistics
    total_categories = len(vocab_data)
    total_words = sum(cat_data.get('total_words', 0) for cat_data in vocab_data.values())
    total_subgroups = sum(len(cat_data.get('subgroups', {})) for cat_data in vocab_data.values())

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <span class="stat-number">{total_categories}</span>
            <span class="stat-label">Categories</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <span class="stat-number">{total_subgroups}</span>
            <span class="stat-label">Study Groups</span>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-box">
            <span class="stat-number">{total_words}</span>
            <span class="stat-label">Vocabulary Words</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Search bar
    st.markdown("### 🔍 Search or Browse Categories")
    search_query = st.text_input("Search for categories or words...", key="home_search", placeholder="e.g., criticism, praise, stubborn...")

    # Filter categories based on search
    if search_query:
        filtered_categories = {
            name: data for name, data in vocab_data.items()
            if search_query.lower() in name.lower()
        }
    else:
        filtered_categories = vocab_data

    # Sort categories by total words (descending)
    sorted_categories = sorted(
        filtered_categories.items(),
        key=lambda x: x[1].get('total_words', 0),
        reverse=True
    )

    # Display categories in a grid
    st.markdown("### 📖 Browse by Category")

    # Create columns for grid layout
    cols_per_row = 3
    for i in range(0, len(sorted_categories), cols_per_row):
        cols = st.columns(cols_per_row)

        for j, (category_name, category_data) in enumerate(sorted_categories[i:i+cols_per_row]):
            with cols[j]:
                total_words = category_data.get('total_words', 0)
                num_subgroups = len(category_data.get('subgroups', {}))

                # Determine color based on size
                if total_words > 20:
                    color = "#E74C3C"  # Red for large
                elif total_words > 10:
                    color = "#F39C12"  # Orange for medium
                else:
                    color = "#27AE60"  # Green for small

                st.markdown(f"""
                <div class="category-card" style="border-left-color: {color};">
                    <div class="category-title">{category_name}</div>
                    <div class="category-stats">
                        📝 {total_words} words • 📚 {num_subgroups} {"part" if num_subgroups == 1 else "parts"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Explore {category_name}", key=f"cat_{category_name}", use_container_width=True):
                    navigate_to_category(category_name)
                    st.rerun()

def render_category_view(vocab_data, category_name):
    """Render the category view with subgroups"""

    render_breadcrumb()

    category_data = vocab_data.get(category_name, {})
    subgroups = category_data.get('subgroups', {})
    total_words = category_data.get('total_words', 0)

    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>📂 {category_name}</h1>
        <p>{total_words} words across {len(subgroups)} {"part" if len(subgroups) == 1 else "parts"}</p>
    </div>
    """, unsafe_allow_html=True)

    # Progress indicator
    st.progress(0.5, text="🎯 Category Level - Choose a study group below")

    st.markdown("---")

    # Display subgroups
    st.markdown("### 📚 Study Groups")

    # Sort subgroups
    sorted_subgroups = sorted(subgroups.items())

    # Display in two columns
    col1, col2 = st.columns(2)

    for i, (subgroup_name, words) in enumerate(sorted_subgroups):
        with col1 if i % 2 == 0 else col2:
            with st.container():
                st.markdown(f"""
                <div class="category-card">
                    <div class="category-title">{subgroup_name}</div>
                    <div class="category-stats">📝 {len(words)} words</div>
                </div>
                """, unsafe_allow_html=True)

                # Show preview of first 3 words
                preview_words = [w['word'] for w in words[:3]]
                preview_text = ", ".join(preview_words)
                if len(words) > 3:
                    preview_text += "..."

                st.caption(f"Preview: {preview_text}")

                if st.button(f"Study {subgroup_name}", key=f"sub_{category_name}_{subgroup_name}", use_container_width=True):
                    navigate_to_subgroup(category_name, subgroup_name)
                    st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)

def render_subgroup_view(vocab_data, category_name, subgroup_name):
    """Render the subgroup view with individual words"""

    render_breadcrumb()

    category_data = vocab_data.get(category_name, {})
    subgroups = category_data.get('subgroups', {})
    words = subgroups.get(subgroup_name, [])

    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>📖 {category_name} - {subgroup_name}</h1>
        <p>Learning {len(words)} vocabulary words</p>
    </div>
    """, unsafe_allow_html=True)

    # Progress indicator
    st.progress(1.0, text="📝 Word Level - Study these vocabulary words")

    st.markdown("---")

    # Display mode selector
    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        view_mode = st.radio("View Mode:", ["📋 List View", "🎴 Card View", "🎲 Quiz Mode"], horizontal=True)

    st.markdown("---")

    if "🎲 Quiz Mode" in view_mode:
        render_quiz_mode(words)
    elif "🎴 Card View" in view_mode:
        render_card_view(words)
    else:
        render_list_view(words)

def render_list_view(words):
    """Render words in a list view"""
    st.markdown("### 📝 Vocabulary Words")

    for i, word_data in enumerate(words, 1):
        word = word_data.get('word', 'Unknown')
        meaning = word_data.get('meaning', 'No definition available')

        with st.expander(f"**{i}. {word}**", expanded=False):
            st.markdown(f"""
            <div class="word-meaning">
                {meaning}
            </div>
            """, unsafe_allow_html=True)

            # Add to favorites
            fav_key = f"{word}_{meaning[:20]}"
            if fav_key in st.session_state.favorites:
                if st.button(f"💔 Remove from Favorites", key=f"fav_{i}"):
                    st.session_state.favorites.remove(fav_key)
                    st.rerun()
            else:
                if st.button(f"💙 Add to Favorites", key=f"fav_{i}"):
                    st.session_state.favorites.add(fav_key)
                    st.rerun()

def render_card_view(words):
    """Render words in a card view"""
    st.markdown("### 🎴 Vocabulary Cards")

    for i, word_data in enumerate(words, 1):
        word = word_data.get('word', 'Unknown')
        meaning = word_data.get('meaning', 'No definition available')

        st.markdown(f"""
        <div class="word-card">
            <div class="word-title">{i}. {word}</div>
            <div class="word-meaning">{meaning}</div>
        </div>
        """, unsafe_allow_html=True)

def render_quiz_mode(words):
    """Render quiz mode for testing knowledge"""
    st.markdown("### 🎲 Quiz Mode")

    if 'quiz_index' not in st.session_state:
        st.session_state.quiz_index = 0
        st.session_state.quiz_revealed = False
        st.session_state.quiz_words = random.sample(words, len(words))

    if st.session_state.quiz_index >= len(st.session_state.quiz_words):
        st.success("🎉 You've completed all words in this quiz!")
        if st.button("🔄 Restart Quiz"):
            st.session_state.quiz_index = 0
            st.session_state.quiz_revealed = False
            st.session_state.quiz_words = random.sample(words, len(words))
            st.rerun()
        return

    current_word = st.session_state.quiz_words[st.session_state.quiz_index]
    word = current_word.get('word', 'Unknown')
    meaning = current_word.get('meaning', 'No definition available')

    # Progress
    progress = (st.session_state.quiz_index + 1) / len(st.session_state.quiz_words)
    st.progress(progress, text=f"Word {st.session_state.quiz_index + 1} of {len(st.session_state.quiz_words)}")

    st.markdown(f"""
    <div class="word-card">
        <div class="word-title">🎯 {word}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if not st.session_state.quiz_revealed:
            if st.button("🔍 Reveal Meaning", use_container_width=True):
                st.session_state.quiz_revealed = True
                st.rerun()
        else:
            st.markdown(f"""
            <div class="word-card">
                <div class="word-meaning">{meaning}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if st.session_state.quiz_revealed:
            if st.button("✅ I Know This", use_container_width=True, type="primary"):
                st.session_state.quiz_index += 1
                st.session_state.quiz_revealed = False
                st.rerun()

    with col3:
        if st.session_state.quiz_revealed:
            if st.button("❌ Need Practice", use_container_width=True):
                # Add to end of quiz for review
                st.session_state.quiz_words.append(current_word)
                st.session_state.quiz_index += 1
                st.session_state.quiz_revealed = False
                st.rerun()

def render_sidebar(vocab_data):
    """Render the sidebar with additional features"""

    with st.sidebar:
        st.markdown("## 🎯 Quick Actions")

        # Random word feature
        if st.button("🎲 Random Word", use_container_width=True):
            # Get a random word from all categories
            all_words = []
            for category_data in vocab_data.values():
                for subgroup_words in category_data.get('subgroups', {}).values():
                    all_words.extend(subgroup_words)

            if all_words:
                random_word = random.choice(all_words)
                st.session_state.random_word = random_word

        if hasattr(st.session_state, 'random_word'):
            st.markdown("### 💡 Word of the Moment")
            word = st.session_state.random_word.get('word', 'Unknown')
            meaning = st.session_state.random_word.get('meaning', 'No definition available')

            st.markdown(f"""
            <div class="word-card">
                <div class="word-title">{word}</div>
                <div class="word-meaning" style="font-size: 0.9rem;">{meaning}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Favorites
        st.markdown("## 💙 Favorites")
        if st.session_state.favorites:
            st.info(f"You have {len(st.session_state.favorites)} favorite words")
            if st.button("🗑️ Clear Favorites", use_container_width=True):
                st.session_state.favorites.clear()
                st.rerun()
        else:
            st.caption("No favorites yet. Add words while studying!")

        st.markdown("---")

        # Statistics
        st.markdown("## 📊 Statistics")
        total_categories = len(vocab_data)
        total_words = sum(cat_data.get('total_words', 0) for cat_data in vocab_data.values())

        st.metric("Total Categories", total_categories)
        st.metric("Total Words", total_words)
        st.metric("Your Favorites", len(st.session_state.favorites))

        st.markdown("---")

        # About
        st.markdown("## ℹ️ About")
        st.caption("""
        This app helps you master GRE vocabulary through intelligent thematic grouping.

        Words are organized into categories and sub-groups for efficient learning.

        **Features:**
        - Hierarchical navigation
        - Multiple view modes
        - Quiz mode for practice
        - Favorites tracking

        Happy learning! 📚
        """)

def main():
    """Main application function"""

    # Initialize session state
    initialize_session_state()

    # Load vocabulary data
    vocab_data = load_vocabulary_data()

    if not vocab_data:
        st.stop()

    # Render sidebar
    render_sidebar(vocab_data)

    # Render appropriate view based on navigation state
    if st.session_state.current_view == 'home':
        render_home_view(vocab_data)
    elif st.session_state.current_view == 'category':
        render_category_view(vocab_data, st.session_state.selected_category)
    elif st.session_state.current_view == 'subgroup':
        render_subgroup_view(
            vocab_data,
            st.session_state.selected_category,
            st.session_state.selected_subgroup
        )

if __name__ == "__main__":
    main()

# 📚 GRE Vocabulary Master

A beautiful, interactive web application for mastering 934 essential GRE vocabulary words through intelligent thematic grouping.

## ✨ Features

### 🎯 Smart Navigation
- **Hierarchical Structure**: Navigate through 91 parent categories → 223 study groups → 934 words
- **Breadcrumb Navigation**: Always know where you are and easily go back
- **Search Functionality**: Quickly find categories or words
- **Responsive Design**: Clean, modern interface that works on all devices

### 📖 Multiple Learning Modes
- **📋 List View**: Expandable list with all words and meanings
- **🎴 Card View**: Beautiful cards for visual learners
- **🎲 Quiz Mode**: Interactive flashcard-style testing with self-assessment

### 💡 Smart Features
- **Random Word**: Get a random vocabulary word for quick study sessions
- **Favorites System**: Mark words for later review
- **Progress Tracking**: Visual indicators of your position in the hierarchy
- **Statistics Dashboard**: Track your learning progress

### 🎨 Beautiful UI
- Modern gradient designs
- Color-coded categories by size
- Smooth transitions and hover effects
- Intuitive button layouts
- Professional typography

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to `http://localhost:8501`

## 📁 Project Structure

```
GRE_VocabApp/
├── app.py                          # Main Streamlit application
├── vocab_hierarchical.json         # Hierarchical vocabulary data
├── vocab_thematic_groups.json      # Flat vocabulary data (backup)
├── word_meanings.csv               # Original CSV data
├── process_vocab_hierarchical.py   # Data processing script
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 📊 Data Organization

### Hierarchical Structure

The vocabulary is organized in a 3-level hierarchy:

1. **Level 1: Parent Categories (91 total)**
   - Main thematic groups like "Criticism", "Praise", "Stubbornness", etc.
   - Each category bundles related sub-groups

2. **Level 2: Sub-groups (223 total)**
   - Each parent category divided into manageable parts (~5 words each)
   - Example: "Decrease" → "Part 1" (5 words), "Part 2" (3 words)

3. **Level 3: Individual Words (934 total)**
   - Each word with its complete definition
   - Primary and secondary meanings combined where applicable

### Top Categories by Size

| Category | Words | Parts |
|----------|-------|-------|
| General | 287 | 58 |
| Scarcity | 30 | 6 |
| Deception | 29 | 6 |
| Clarity | 24 | 5 |
| Abundance | 20 | 4 |
| Friendly | 20 | 4 |

## 🎓 How to Use

### Navigation Flow

1. **Home Page**
   - Browse all 91 categories
   - View statistics (categories, study groups, total words)
   - Search for specific categories
   - Categories are color-coded by size:
     - 🔴 Red: 20+ words (large)
     - 🟠 Orange: 11-20 words (medium)
     - 🟢 Green: 1-10 words (small)

2. **Category Page**
   - See all sub-groups within a category
   - Preview first 3 words of each sub-group
   - Click to enter any sub-group for detailed study

3. **Study Page (Sub-group)**
   - Choose your learning mode:
     - **List View**: Expandable entries for all words
     - **Card View**: Visual cards for reading through
     - **Quiz Mode**: Test yourself with flashcards
   - Add words to favorites
   - Use breadcrumb navigation to go back

### Study Strategies

**For Beginners:**
1. Start with smaller categories (green badges)
2. Use Card View to read through words
3. Add difficult words to favorites

**For Advanced Learners:**
1. Focus on larger categories
2. Use Quiz Mode for self-testing
3. Mark words you don't know for review

**Random Practice:**
- Click "🎲 Random Word" in sidebar for quick study sessions
- Perfect for filling short time gaps

## 🎨 Customization

The app uses custom CSS for styling. To modify the appearance:

1. Open `app.py`
2. Find the `st.markdown()` call with `<style>` tags
3. Modify colors, fonts, or spacing as needed

### Color Scheme Variables
```css
--primary-color: #4A90E2;      /* Primary blue */
--secondary-color: #50C878;    /* Success green */
--accent-color: #FF6B6B;       /* Accent red */
```

## 🔧 Technical Details

### Technologies Used
- **Streamlit**: Web framework for Python
- **Python 3.7+**: Core programming language
- **JSON**: Data storage format

### Key Features Implementation
- **Session State**: Maintains navigation history and user preferences
- **Caching**: Vocabulary data loaded once for performance
- **Responsive Layout**: Streamlit columns for grid layouts
- **Custom CSS**: Enhanced styling beyond Streamlit defaults

## 📈 Statistics

- **Total Words**: 934 GRE vocabulary words
- **Categories**: 91 thematic parent groups
- **Study Groups**: 223 manageable sub-groups
- **Average Group Size**: ~5 words per sub-group
- **Coverage**: Essential GRE vocabulary across all major themes

## 🤝 Contributing

To add more words or improve categorization:

1. Edit `word_meanings.csv` with new words
2. Run `python process_vocab_hierarchical.py` to regenerate JSON
3. Restart the Streamlit app

## 📝 License

This project is for educational purposes. Feel free to use and modify as needed.

## 🙏 Acknowledgments

- Vocabulary data sourced from GRE preparation materials
- Thematic categorization using NLP keyword matching
- Built with ❤️ using Streamlit

## 📧 Support

If you encounter any issues:
1. Ensure all required files are present
2. Check that `vocab_hierarchical.json` exists
3. Verify Python version is 3.7+
4. Reinstall dependencies if needed

---

**Happy Learning! 📚✨**

Master your GRE vocabulary one category at a time!

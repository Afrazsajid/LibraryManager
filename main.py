import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
from datetime import datetime


st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #1E3A8A;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .cta-button {
        background-color: #1E3A8A;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        text-decoration: none;
    }
    .stat-card {
        background-color: #F3F4F6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .stat-number {
        font-size: 2rem;
        color: #1E3A8A;
        font-weight: bold;
    }
    .stat-label {
        color: #6B7280;
    }
</style>
""", unsafe_allow_html=True)

if 'library' not in st.session_state:
    st.session_state.library = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'last_save' not in st.session_state:
    st.session_state.last_save = None


def load_library():
    try:
        if os.path.exists("library.json"):
            with open("library.json", "r") as file:
                st.session_state.library = json.load(file)
            st.session_state.last_save = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True
        return False
    except Exception as e:
        st.error(f"Error loading library: {e}")
        return False


def save_library():
    try:
        with open("library.json", "w") as file:
            json.dump(st.session_state.library, file)
        st.session_state.last_save = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return True
    except Exception as e:
        st.error(f"Error saving library: {e}")
        return False


def add_book(title, author, year, genre, read):
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    }
    st.session_state.library.append(book)
    save_library()


def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        st.session_state.library.pop(index)
        save_library()
        return True
    return False


def get_stats():
    if not st.session_state.library:
        return {
            "total": 0,
            "read": 0,
            "unread": 0,
            "read_percentage": 0,
            "genres": {}
        }
    
    total = len(st.session_state.library)
    read = sum(1 for book in st.session_state.library if book["read"])
    unread = total - read
    read_percentage = (read / total) * 100 if total > 0 else 0
    
    genres = {}
    for book in st.session_state.library:
        genre = book["genre"]
        if genre in genres:
            genres[genre] += 1
        else:
            genres[genre] = 1
    
    return {
        "total": total,
        "read": read,
        "unread": unread,
        "read_percentage": read_percentage,
        "genres": genres
    }


with st.sidebar:
    st.image("data:image/jpeg;base64,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", width=150)
    st.markdown("### Menu")
    
    if st.button("📊 Dashboard", key="nav_dashboard"):
        st.session_state.current_page = "Home"
    
    if st.button("📚 View Library", key="nav_view"):
        st.session_state.current_page = "View"
    
    if st.button("➕ Add Book", key="nav_add"):
        st.session_state.current_page = "Add"
    
    if st.button("🔍 Search Books", key="nav_search"):
        st.session_state.current_page = "Search"
    
    if st.button("❌ Remove Book", key="nav_remove"):
        st.session_state.current_page = "Remove"
    
    with st.expander("File Operations"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Load Library"):
                if load_library():
                    st.success("Library loaded successfully!")
                else:
                    st.info("No library file found.")
        
        with col2:
            if st.button("📤 Save Library"):
                if save_library():
                    st.success("Library saved successfully!")
    
    if st.session_state.last_save:
        st.caption(f"Last saved: {st.session_state.last_save}")

# Try loading the library on startup
if not st.session_state.last_save:
    load_library()

# Main content area
if st.session_state.current_page == "Home":
    # Dashboard
    st.markdown('<h1 class="main-header">📚 Personal Library Manager</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Keep track of your reading journey</p>', unsafe_allow_html=True)
    
    stats = get_stats()
    
    # Statistics cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total']}</div>
            <div class="stat-label">Total Books</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['read']}</div>
            <div class="stat-label">Books Read</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['read_percentage']:.1f}%</div>
            <div class="stat-label">Completion Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualizations
    st.markdown('<h2 class="section-header">📊 Library Insights</h2>', unsafe_allow_html=True)
    
    if stats["total"] > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Read vs Unread pie chart
            read_data = pd.DataFrame({
                "Status": ["Read", "Unread"],
                "Count": [stats["read"], stats["unread"]]
            })
            fig1 = px.pie(
                read_data, 
                values="Count", 
                names="Status",
                title="Read vs. Unread Books",
                color_discrete_sequence=["#4C1D95", "#C7D2FE"],
                hole=0.4
            )
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Genres bar chart
            if stats["genres"]:
                genres_data = pd.DataFrame({
                    "Genre": list(stats["genres"].keys()),
                    "Count": list(stats["genres"].values())
                })
                fig2 = px.bar(
                    genres_data.sort_values("Count", ascending=False).head(10),
                    x="Genre",
                    y="Count",
                    title="Books by Genre (Top 10)",
                    color_discrete_sequence=["#4C1D95"]
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Add books with genres to see genre statistics.")
    else:
        st.info("Add some books to your library to see insights and visualizations.")
        
    # Recent additions
    st.markdown('<h2 class="section-header">📘 Recent Additions</h2>', unsafe_allow_html=True)
    if st.session_state.library:
        recent_books = st.session_state.library[-3:] if len(st.session_state.library) > 3 else st.session_state.library
        recent_books.reverse()  # Show most recent first
        
        for book in recent_books:
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.markdown("### 📖")
                with col2:
                    st.markdown(f"**{book['title']}**")
                    st.caption(f"by {book['author']} ({book['year']}) - {book['genre']}")
                with col3:
                    st.markdown("✅ Read" if book["read"] else "📌 Unread")
                st.divider()
    else:
        st.info("Your library is empty. Start adding books!")

elif st.session_state.current_page == "View":
    st.markdown('<h1 class="main-header">📚 My Library</h1>', unsafe_allow_html=True)
    
    if st.session_state.library:
        # Convert library to DataFrame for easier display
        df = pd.DataFrame(st.session_state.library)
        
        # Filter options
        with st.expander("Filter Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                if 'genre' in df.columns:
                    genres = ["All"] + sorted(df["genre"].unique().tolist())
                    selected_genre = st.selectbox("Filter by Genre", genres)
            
            with col2:
                read_filter = st.selectbox("Filter by Status", ["All", "Read", "Unread"])
        
        # Apply filters
        filtered_df = df.copy()
        
        if 'genre' in df.columns and selected_genre != "All":
            filtered_df = filtered_df[filtered_df["genre"] == selected_genre]
            
        if read_filter != "All":
            filtered_df = filtered_df[filtered_df["read"] == (read_filter == "Read")]
        
        # Display filtered library
        if not filtered_df.empty:
            st.write(f"Showing {len(filtered_df)} of {len(df)} books")
            
            # Display as a styled table with icons
            for i, book in filtered_df.iterrows():
                with st.expander(f"{book['title']} by {book['author']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Title:** {book['title']}")
                        st.markdown(f"**Author:** {book['author']}")
                        st.markdown(f"**Year:** {book['year']}")
                        st.markdown(f"**Genre:** {book['genre']}")
                        st.markdown(f"**Status:** {'✅ Read' if book['read'] else '📌 Unread'}")
                    
                    with col2:
                        if st.button("Remove", key=f"remove_{i}"):
                            index = st.session_state.library.index(book.to_dict())
                            if remove_book(index):
                                st.success(f"Removed '{book['title']}' from your library!")
                                st.rerun()
        else:
            st.info("No books match your filters.")
    else:
        st.info("Your library is empty. Start adding books!")

elif st.session_state.current_page == "Add":
    st.markdown('<h1 class="main-header">➕ Add a New Book</h1>', unsafe_allow_html=True)
    
    with st.form("add_book_form"):
        title = st.text_input("Title", key="title")
        author = st.text_input("Author", key="author")
        
        col1, col2 = st.columns(2)
        with col1:
            year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, value=2020, step=1)
        with col2:
            # Common book genres
            genres = [
                "Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                "Mystery", "Thriller", "Romance", "Horror", "Biography",
                "History", "Self-Help", "Business", "Science", "Travel",
                "Poetry", "Other"
            ]
            genre = st.selectbox("Genre", genres)
        
        read = st.checkbox("I've read this book")
        
        submit = st.form_submit_button("Add Book")
        
        if submit:
            if title and author:
                add_book(title, author, year, genre, read)
                st.success(f"'{title}' by {author} has been added to your library!")
                # Clear form fields by recreating the form
                st.rerun()
            else:
                st.error("Title and author are required!")

elif st.session_state.current_page == "Search":
    st.markdown('<h1 class="main-header">🔍 Search Books</h1>', unsafe_allow_html=True)
    
    if st.session_state.library:
        search_term = st.text_input("Search by title or author")
        
        if search_term:
            results = [
                book for book in st.session_state.library
                if search_term.lower() in book["title"].lower() or 
                   search_term.lower() in book["author"].lower()
            ]
            
            if results:
                st.write(f"Found {len(results)} books matching '{search_term}'")
                
                for i, book in enumerate(results):
                    with st.expander(f"{book['title']} by {book['author']}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**Title:** {book['title']}")
                            st.markdown(f"**Author:** {book['author']}")
                            st.markdown(f"**Year:** {book['year']}")
                            st.markdown(f"**Genre:** {book['genre']}")
                            st.markdown(f"**Status:** {'✅ Read' if book['read'] else '📌 Unread'}")
                        
                        with col2:
                            if st.button("Mark as Read" if not book["read"] else "Mark as Unread", key=f"toggle_read_{i}"):
                                index = st.session_state.library.index(book)
                                st.session_state.library[index]["read"] = not book["read"]
                                save_library()
                                st.success(f"Updated reading status for '{book['title']}'!")
                                st.rerun()
            else:
                st.info(f"No books found matching '{search_term}'")
    else:
        st.info("Your library is empty. Start adding books!")

elif st.session_state.current_page == "Remove":
    st.markdown('<h1 class="main-header">❌ Remove Books</h1>', unsafe_allow_html=True)
    
    if st.session_state.library:
        # Get list of book titles for selection
        book_titles = [book["title"] for book in st.session_state.library]
        book_to_remove = st.selectbox("Select a book to remove", book_titles)
        
        # Find the selected book
        selected_book = next((book for book in st.session_state.library if book["title"] == book_to_remove), None)
        
        if selected_book:
            st.write("Book details:")
            st.write(f"Title: {selected_book['title']}")
            st.write(f"Author: {selected_book['author']}")
            st.write(f"Year: {selected_book['year']}")
            st.write(f"Genre: {selected_book['genre']}")
            st.write(f"Status: {'Read' if selected_book['read'] else 'Unread'}")
            
            if st.button("Confirm Removal"):
                index = st.session_state.library.index(selected_book)
                if remove_book(index):
                    st.success(f"'{selected_book['title']}' has been removed from your library!")
                    st.rerun()
    else:
        st.info("Your library is empty. There are no books to remove.")

# Auto-save functionality on page exit
# This is the best we can do for auto-save in Streamlit
if st.session_state.library and not st.session_state.last_save:
    save_library()
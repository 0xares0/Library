import streamlit as st
import pandas as p
import random 

# Create book object
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.amount = 1
        self.available = True
        self.borrower = []
    
    def __str__(self):
        status = "Available" if self.amount > 0 else f"Borrowed by {', '.join(self.borrower)}"
        return f"{self.title} by {self.author} ISBN{self.isbn} - {status}"

#Create Member Object
class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed = []


    def __str__(self):
        status = "Not Borrowiing" if not self.borrowed else f"Is borrowing {', ' .join(self.borrowed)}"
        return (f"{self.name} with ID {self.member_id} has a borrowed {len(self.borrowed)} books")
    
#Create Library object
class Library:
    def __init__(self, name):
        self.name = name
        self.books = []
        self.members = []
    
    # add books
    def add_books(self, book):
        self.books.append(book)
        return f"{book.title} has been added to the library"

    # add member
    def add_member(self, member):
        self.members.append(member)
        return f"{member.name} with id {member.id} is officially a member of this library"
    
    # Find book by title
    def find_book_by_title(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None
            
    # Find members
    def find_member_by_id(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    # Borrow book function        
    def borrow_book(self, title, member_id):
        book = self.find_book_by_title(title)
        member = self.find_member_by_id(member_id)

        if not book:
            return f"Book '{title}' not found."
        
        if not member:
            return f"Member with ID {member_id} not found."
        
        if book.amount > 0:
            member.borrowed.append(book.title)
            book.borrower.append(member.name)
            book.amount -= 1
            if book.amount == 0:
                book.available = False
            return f"{book.title} successfully borrowed"
        else:
            return f"{book.title} is not available"

    #Return book function
    def return_book(self, title, member_id):
        book = self.find_book_by_title(title)
        member = self.find_member_by_id(member_id)

        if not book:
            return f"Book '{title}'  not found"
        
        if not member:
            return f"Member with ID {member_id} not found"
        
        if title in member.borrowed:
            member.borrowed.remove(title)
            book.borrower.remove(member.name)
            book.amount += 1
            book.available = True
            return f"{book.title} succesfully returned"
        else:
            return f"{member.name} did not borrow {title}"

    # Remove Book function
    def remove_book(self, title, isbn):
        book = Library.books

        if book.isbn and book.title:
            if book.amount >= 1:
                book.pop(book)
            
            else:
                st.warning(f"No book to remove")


    def remove_member(self, member_id):
        member = self.find_member_by_id(member_id)

        if member_id == member.id:
            member.pop(member)
        
        else:
            st.warning(f"Member doesn't exist")

        
    
    # Creating books Datframe
    def get_books_dataframe(self):
        book_data = []

        for book in self.books:
            status = "Available" if book.available else f"Borrowed by {', ' .join(book.borrower)}" 
            book_data.append({
                "Title": book.title,
                "Author": book.author,
                "ISBN": book.isbn,
                "Amount": book.amount,
                "status": status
            })
    
        return p.Dataframe(book_data)

    # Creating member dataframe
    def get_members_dataframe(self):
        member_data = []

        for member in self.members:
            books_titles = member.borrowed
            member_data.append({
                "Name": member.name,
                "id": member.member_id,
                "Books Borrowed": ",".join(books_titles) if books_titles else "None"
            })
        return p.DataFrame(member_data)


#Library App
def library_app():

    # Initialize session state
    if "library" not in st.session_state:
        st.session_state.library = Library("Regia Bibloteca")
        st.session_state.member_ids = set()

        book1 = Book("Qualify", "Vera Nazarian", 98328493)
        book2 = Book("Compete", "Vera Nazarian", 90423212)
        st.session_state.library.add_books(book1)
        st.session_state.library.add_books(book2)
        member1 = Member("Alice Bob", "L001")
        member2 = Member("John Doe", "L002")
        st.session_state.library.add_member(member1)
        st.session_state.library.add_member(member2)

    # Title
    st.title(f"Welcome to the {Library.name}")

   
    st.sidebar.title("Library Functions")
    function_option = st.sidebar.selectbox(
        "Select Function",
        ["Add book", "Register member", "Borrow Book", "Return Book",
        "Show Books", "Show members", "Remove Book", "Remove Member"]
    )

    if function_option == "Add book":
        st.title("Add New Book")
        
        with st.form("Add Book"):
            book_title = st.text_input("Please enter the book title")
            book_author = st.text_input("Please enter the author's name")
            book_isbn = st.number_input("Please enter the ISBN")

            if st.form_submit_button("Add Book") and book_isbn and book_author and book_title:
                
                duplicate = False
                for book in st.session_state.library.books:
                    if book.isbn == book_isbn:
                        duplicate = True
                        if book.title == book_title and book.author == book_author:
                            book.amount += 1
                            st.success(f"Added another copy of {book.title}")
                        else:
                            st.warning(f" ISBN {book.isbn} already exists with a different title/author")
                if not duplicate:
                    new_book = Book(book_title, book_author, book_isbn)
                    result = st.session_state.library.add_books(new_book)
                    st.success(result)
    
    def generate_unique_id():
        possible_ids = set(range(1, 9999 + 1))
        available_ids = possible_ids - st.session_state.member_ids

        if not available_ids:
            return None
        
        new_id = random.choice(list(available_ids))
        st.session_state.member_ids.add(new_id)
        return f"{new_id:04d}"
        
    if function_option == "Register Member":
        st.title("Register Member")

        with st.form("Register member"):
            member_name = st.text_input("Please enter the member's name")
            mem_id = generate_unique_id()

            if st.submit_button("Register Member"):

                new_member = Member(member_name, mem_id)
                if mem_id is not None:
                    st.session_state.Library.add_member(new_member)

                else:
                    st.warning(f"There is no more ID numbers")
        
    if function_option == "Borrow Book":
        st.title("Borrow Book")

        with st.form("Borrow Book"):
            available_books = [book.title for book in st.session_state.Library.books if book.available]
            member_ids = [member.id for member in st.session_state.Library.members]

            if available_books and member_ids:
                book_borrowed = st.selectbox("Select Book", options=available_books, placeholder="Please select the book to borrow")
                borrower = st.selectbox("Choose Member", options=member_ids, placeholder="Please select the member borrowing")

                if st.submit_button("Borrow Book"):
                    st.session_state.Library.borrow_book(book_borrowed, borrower)
                    st.write(f"{Book.title} successfully borrowed.")
                    st.rerun

            else:
                if not available_books:
                    st.warning(f"No available books to be borrowed")

                if not member_ids:
                    st.warning(f"No members to borrow books")

    if function_option == "Return Books":
        st.title("Return Books")

        with st.forms("Return Books"):
            books_borrowed = [book.title for book in st.session_state.Library.books.borrowed]
            borrower_ids = [member.id for member in st.session_state.members if any(book in member.borrowed for book in Book.borrowed)]

            if books_borrowed and borrower_ids:
                books_returned = st.selectbox("Select Book", options=books_borrowed, placeholder="Please select the books to return")
                borrower = st.selectbox("Choose member", options=borrower_ids, placeholder="Please select the borrower returning")

                if st.submit_button("Return Book"):
                    st.session_state.Library.return_book(book_borrowed, borrower)
                    st.write (f"{Book.title} successfully returned")
                    st.rerun()
            
            else:
                if not books_borrowed:
                    st.warning(f"No books borrowed")

                if not borrower_ids:
                    st.warning(f"No borrowes recorded")

    if function_option == "Remove Book":
        book_title = [book.title for book in st.session_state.Library.books if book.available]

        books_title = st.selectbox("Select Book", options=book_title, placeholder="Select book to remove")
        if books_title:
            book_isbn = [book.isbn for book in st.session_state.Library.books if book.title == books_title]
            
            # Select ISBN
            books_isbn = st.selectbox("Select Book ISBN", options=book_isbn, placeholder="Select book isbn")

        if st.button("Remove Book"):
            st.session_state.Library.remove_book(books_title, books_isbn)
            st.write(f"{Book.title} successfuly removed")

        

    if function_option == "Remove memeber":
        mem_id = [member.id for member in st.session_state.Library.member]

        m_id = st.selectbox("Select Member", options=mem_id, placeholder="Selece the member you wish to remove")

        if st.button("Remove member"):
            st.session_state.Library.remove_member()
            st.write(f"{Member.id} successfully removed")


    if function_option == "Show books":
        st.title("Book Management")

         # Show booksin a table
        b = st.session_state.library.get_books_dataframe
        st.dataframe(b)

    # Show members in a table
    if function_option == "Show members":
        st.title("Member Management")
        
        m = st.session_state.Library.get_members_dataframe
        st.dataframe(m)


st.divider()
st.write(f"© 2025 Royale Bibloteca Management System")

if __name__ == "__main__":
    library_app()    

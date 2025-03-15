import json
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017/"  # Update if your connection string is different
client = MongoClient(MONGO_URI)
db = client["LibraryDB"]  # Database Name
collection = db["Books"]  # Collection Name
JSON_FILE = "library.json"

# Function to save data to JSON file
def save_to_json():
    books = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB _id field
    with open(JSON_FILE, "w") as file:
        json.dump(books, file, indent=4)

# Function to load data from JSON file
def load_from_json():
    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Add a new book
def add_book():
    print("\n📖 Add a New Book")
    title = input("Enter book title: ").strip()
    author = input("Enter book author: ").strip()
    year = input("Enter publication year: ").strip()
    genre = input("Enter book genre: ").strip()
    read_status = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read_status
    }
    
    collection.insert_one(book)
    save_to_json()  # Update JSON file
    print(f"\n✅ '{title}' added successfully!")

# Remove a book
def remove_book():
    title_to_remove = input("\nEnter the title of the book to remove: ").strip()

    result = collection.delete_one({"title": title_to_remove})
    
    if result.deleted_count > 0:
        save_to_json()  # Update JSON file
        print(f"\n✅ '{title_to_remove}' has been removed!")
    else:
        print("\n⚠️ Book not found!")

# Search for a book by title or author
def search_book():
    print("\n🔍 Search by:")
    print("1. Title")
    print("2. Author")
    choice = input("Enter your choice (1/2): ").strip()
    
    query = input("\nEnter search term: ").strip()
    search_filter = {"title": query} if choice == "1" else {"author": query}

    results = collection.find(search_filter)

    books = list(results)
    if books:
        print("\n📖 Matching Books:")
        for idx, book in enumerate(books, start=1):
            status = "Read ✅" if book["read"] else "Unread ❌"
            print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        print("\n⚠️ No books found!")

# Display all books
def display_books():
    books = load_from_json()  # Load from JSON file

    if not books:
        print("\n📚 Your library is empty!")
        return

    print("\n📚 Your Book Collection:")
    for idx, book in enumerate(books, start=1):
        status = "Read ✅" if book["read"] else "Unread ❌"
        print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

# Display statistics
def display_statistics():
    total_books = collection.count_documents({})
    read_books = collection.count_documents({"read": True})
    
    if total_books == 0:
        print("\n📚 Your library is empty!")
        return

    percentage_read = (read_books / total_books) * 100

    print("\n📊 Library Statistics:")
    print(f"📚 Total books: {total_books}")
    print(f"✅ Books read: {read_books} ({percentage_read:.2f}%)")

# Main function with menu system
def main():
    while True:
        print("\n📚 Personal Library Manager (MongoDB & JSON)")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            search_book()
        elif choice == "4":
            display_books()
        elif choice == "5":
            display_statistics()
        elif choice == "6":
            print("\n📖 Goodbye! 👋")
            break
        else:
            print("\n⚠️ Invalid choice! Try again.")

# Run the program
if __name__ == "__main__":
    main()

db = db.getSiblingDB('bookdb');
db.books.insertMany([
  { id: 1, title: "Atomic Habits", author: "James Clear" },
  { id: 2, title: "The Alchemist", author: "Paulo Coelho" },
  { id: 3, title: "Deep Work", author: "Cal Newport" }
]);

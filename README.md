

# Student Class Management System

Welcome to the Student Class Management System! This project allows teachers to manage classes and students by performing CRUD (Create, Read, Update, Delete) operations. It also includes JWT token-based authentication to ensure secure access to the system.

## Technologies Used

- Flask
- MongoDB
- JWT (JSON Web Tokens)

## Features

- Teacher Role: Teachers have full access to perform CRUD operations on both classes and students.
- Student Role: Students have limited access, including fetching all students, updating their own profile, and creating new students.
- JWT Authentication: The system uses JWT tokens to ensure secure and authenticated access.
- Class Management: Teachers can create, read, update, and delete classes.
- Student Management: Teachers can create, read, update, and delete students. Students can also update their profiles.
- Assignment and Unassignment: Teachers can assign and unassign students to/from classes.
- Fetching Students: Teachers and students can fetch the list of all students present in a specific class.

## Getting Started

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up MongoDB and configure the database connection in the Flask app.
4. Generate JWT secret key and configure it in the Flask app.
5. Run the Flask app using `python app.py`.

## API Endpoints

- `/register`: Register a new teacher or student.
- `/login`: Log in as a teacher or student and get JWT token.
- `/class`: CRUD operations for classes.
- `/student`: CRUD operations for students.
- `/class/assign`: Assign a student to a class.
- `/class/unassign`: Unassign a student from a class.
- `/class/<class_id>/students`: Fetch all students in a specific class.

## Usage

1. Register as a teacher or student.
2. Log in to get JWT token.
3. Use the token to access the different API endpoints based on your role.


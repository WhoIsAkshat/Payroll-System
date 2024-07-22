import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="salary1"
)

cursor = conn.cursor()

# SQL statement to create the `emp` table if it doesn't exist
create_emp_table_query = """
CREATE TABLE IF NOT EXISTS emp (
    emp_name VARCHAR(30),
    salary INT,
    PF VARCHAR(5),
    ESI VARCHAR(5),
    Overtime VARCHAR(5),
    Rem_Advance INT,
    emp_id INT PRIMARY KEY,
    shift VARCHAR(5),
    dept VARCHAR(20)
)
"""
cursor.execute(create_emp_table_query)

# Data to be inserted into the `emp` table
emp_data = [
    ('Sunil Singh', 57000, 'Y', 'Y', 'N', 0, 1, 'D', 'CNC'),
    ('Shaiju Kakkariyal', 49000, 'Y', 'Y', 'N', 0, 2, 'D', 'Production'),
    ('Rajpati Yadav', 38000, 'N', 'N', 'N', 0, 3, 'D', 'Admin'),
    ('Anil Gupta', 35000, 'N', 'N', 'N', 0, 4, 'D', 'QA'),
    ('Aditya Kumar Singh', 38700, 'Y', 'Y', 'N', 0, 5, 'D', 'QA'),
    ('Dilip Kumar Tiwari', 26500, 'Y', 'Y', 'N', 0, 6, 'D', 'QA'),
    ('Sandeep', 17600, 'Y', 'Y', 'Y', 0, 7, 'D', 'QA'),
    ('Harish Vishwakarma', 16500, 'Y', 'Y', 'N', 0, 8, 'D', 'QA'),
    ('Dilip Kumar Giri', 12300, 'Y', 'Y', 'Y', 0, 9, 'D', 'QA'),
    ('Vijay Kumar', 10200, 'N', 'N', 'Y', 0, 10, 'D', 'QA'),
    ('Govind - QA', 10200, 'N', 'N', 'Y', 0, 11, 'D', 'QA'),
    ('Brikesh', 9500, 'N', 'N', 'Y', 0, 12, 'D', 'QA'),
    ('Harsh Verma', 15000, 'N', 'N', 'N', 0, 13, 'D', 'QA'),
    ('Pawan', 18200, 'Y', 'Y', 'Y', 0, 14, 'D', 'Stores'),
    ('Sachin Sharma', 26000, 'N', 'N', 'N', 0, 15, 'D', 'Accounts'),
    ('Gaurav Sharma', 24300, 'Y', 'Y', 'N', 0, 16, 'D', 'Accounts'),
    ('Shambhu Sharma', 16000, 'Y', 'Y', 'N', 0, 17, 'D', 'Accounts'),
    ('Bahadur Singh', 27200, 'N', 'N', 'Y', 0, 18, 'D', 'CNC'),
    ('Shobhit Sharma', 17100, 'Y', 'Y', 'Y', 0, 19, 'D', 'CNC'),
    ('Krishna', 15600, 'Y', 'Y', 'Y', 0, 20, 'D', 'CNC'),
    ('Satish Kumar', 11400, 'Y', 'Y', 'Y', 0, 21, 'D', 'CNC'),
    ('Anwar Hussain Khan', 12100, 'Y', 'Y', 'Y', 0, 22, 'D', 'CNC'),
    ('Bhagat Singh', 11400, 'Y', 'Y', 'Y', 0, 23, 'D', 'CNC'),
    ('Vijay Mal Yadav', 11000, 'Y', 'Y', 'Y', 0, 24, 'D', 'CNC'),
    ('Vinesh', 10500, 'N', 'N', 'Y', 0, 25, 'D', 'CNC'),
    ('Jatin', 11700, 'N', 'N', 'Y', 0, 26, 'D', 'CNC'),
    ('Pawan Kumar', 10500, 'N', 'N', 'Y', 0, 27, 'D', 'CNC'),
    ('Akash', 10200, 'N', 'N', 'Y', 0, 28, 'D', 'CNC'),
    ('Amit Kumar', 11200, 'N', 'N', 'Y', 0, 29, 'D', 'CNC'),
    ('Vivek Kumar', 10200, 'N', 'N', 'Y', 0, 30, 'D', 'CNC'),
    ('Monu Rajbhar', 10000, 'N', 'N', 'Y', 0, 31, 'D', 'CNC'),
    ('Akhilesh', 10500, 'N', 'N', 'Y', 0, 32, 'D', 'CNC'),
    ('Soman Bera', 9500, 'N', 'N', 'Y', 0, 33, 'D', 'CNC'),
    ('Tanuj Pachauri', 9500, 'N', 'N', 'Y', 0, 34, 'D', 'CNC'),
    ('Karan Sharma', 9000, 'N', 'N', 'Y', 0, 35, 'D', 'CNC'),
    ('Rohitash Tiwari', 28500, 'Y', 'Y', 'Y', 0, 36, 'D', 'Conventional'),
    ('Lokesh Kumar', 22400, 'Y', 'Y', 'Y', 0, 37, 'D', 'Conventional'),
    ('Jila Singh', 21400, 'Y', 'Y', 'Y', 0, 38, 'D', 'Conventional'),
    ('Rinku Kumar', 18000, 'Y', 'Y', 'Y', 0, 39, 'D', 'Conventional'),
    ('Neeraj Kumar', 16800, 'N', 'N', 'Y', 0, 40, 'D', 'Conventional'),
    ('Uttam Dalapati', 14100, 'N', 'N', 'Y', 0, 41, 'D', 'Conventional'),
    ('Prabhu Dayal', 14900, 'Y', 'Y', 'Y', 0, 42, 'D', 'Electrical'),
    ('Dharmender', 12400, 'Y', 'Y', 'Y', 0, 43, 'D', 'Conventional'),
    ('Govind', 11600, 'Y', 'Y', 'Y', 0, 44, 'D', 'Conventional'),
    ('Vipin Kumar', 14500, 'Y', 'Y', 'Y', 0, 45, 'D', 'Buffing'),
    ('Risi Kumar', 12500, 'Y', 'Y', 'Y', 0, 46, 'D', 'Buffing'),
    ('Manoj Kumar', 13900, 'Y', 'Y', 'Y', 0, 47, 'D', 'Buffing'),
    ('Dheerendra', 10000, 'N', 'N', 'Y', 0, 48, 'D', 'Buffing'),
    ('Lotan', 11000, 'N', 'N', 'Y', 0, 49, 'D', 'Buffing'),
    ('Varnit', 10700, 'N', 'N', 'N', 0, 50, 'D', 'Admin'),
    ('Daud', 12000, 'N', 'N', 'Y', 0, 51, 'D', 'Conventional'),
    ('Ramnaresh', 11100, 'N', 'N', 'Y', 0, 52, 'D', 'Conventional'),
    ('Santosh', 11200, 'N', 'N', 'Y', 0, 53, 'D', 'Conventional'),
    ('Ravinder', 11700, 'N', 'N', 'Y', 0, 54, 'D', 'Conventional'),
    ('Alok', 11100, 'N', 'N', 'Y', 0, 55, 'D', 'Conventional'),
    ('Rajesh', 11100, 'N', 'N', 'Y', 0, 56, 'D', 'Conventional'),
    ('Brijbhan Pal', 11300, 'N', 'N', 'Y', 0, 57, 'D', 'Conventional'),
    ('Anish Kumar', 11500, 'N', 'N', 'Y', 0, 58, 'D', 'Cutting'),
    ('Narayan', 10500, 'N', 'N', 'Y', 0, 59, 'D', 'Conventional'),
    ('Munendra Singh', 10200, 'N', 'N', 'Y', 0, 60, 'D', 'Conventional'),
    ('Raj Mangal', 10000, 'N', 'N', 'Y', 0, 61, 'D', 'Conventional'),
    ('Sukru Bage', 11000, 'N', 'N', 'Y', 0, 62, 'D', 'Conventional'),
    ('Karan Pal', 9500, 'N', 'N', 'Y', 0, 63, 'D', 'Conventional'),
    ('Bharat Mahto', 9500, 'N', 'N', 'Y', 0, 64, 'D', 'Cutting'),
    ('Nikas', 15000, 'N', 'N', 'N', 0, 65, 'D', 'Admin'),
    ('Ansh', 9000, 'N', 'N', 'Y', 0, 66, 'D', 'CNC'),
    ('Lallu', 9000, 'N', 'N', 'Y', 0, 67, 'D', 'Conventional'),
    ('Arjun', 12000, 'N', 'N', 'Y', 0, 68, 'D', 'Buffing'),
    ('Rahul', 12000, 'N', 'N', 'N', 0, 69, 'D', 'QA'),
    ('Ajay Kumar', 9500, 'N', 'N', 'Y', 0, 70, 'D', 'CNC')
]

# Insert data into the `emp` table
insert_emp_query = """
INSERT INTO emp (emp_name, salary, PF, ESI, Overtime, Rem_Advance, emp_id, shift, dept)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
cursor.executemany(insert_emp_query, emp_data)

# Commit the transaction
conn.commit()

# SQL statement to create the `remaining_holidays` table if it doesn't exist
create_remaining_holidays_table_query = """
CREATE TABLE IF NOT EXISTS remaining_holidays (
    emp_id INT PRIMARY KEY,
    holidays INT
)
"""
cursor.execute(create_remaining_holidays_table_query)

# Data to be inserted into the `remaining_holidays` table
remaining_holidays_data = [
    (1, 12),
    (2, 0),
    (3, 7),
    (4, 9),
    (5, 11),
    (6, 12),
    (8, 10),
    (13, 6),
    (15, 7),
    (16, 3),
    (17, 12),
    (50, 6),
    (65, 12),
    (69, 7)
]

# Insert data into the `remaining_holidays` table
insert_remaining_holidays_query = """
INSERT INTO remaining_holidays (emp_id, holidays)
VALUES (%s, %s)
"""
cursor.executemany(insert_remaining_holidays_query, remaining_holidays_data)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

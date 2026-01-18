import pymongo

# Configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "employee-management"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

print("--- Database Verification ---")
print(f"Employees: {db.Employee.count_documents({})}")
print(f"Projects: {db.Project.count_documents({})}")
print(f"Project Assignments: {db.ProjectEmployee.count_documents({})}")
print(f"Parent Departments: {db.DepartmentParent.count_documents({})}")
print(f"Child Departments: {db.DepartmentChild.count_documents({})}")
print("---------------------------")

import pymongo
from faker import Faker
import random
from datetime import datetime, timedelta

# Configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "employee-management"
fake = Faker()

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
col_counter = db["Counter"]
col_dept_parent = db["DepartmentParent"]
col_dept_child = db["DepartmentChild"]
col_employee = db["Employee"]
col_project = db["Project"]
col_project_employee = db["ProjectEmployee"]

# Counter Management
def get_next_sequence(key, start_at):
    # Ensure counter exists
    counter = col_counter.find_one({"key": key})
    if not counter:
        col_counter.insert_one({"key": key, "value": start_at - 1, "createdAt": datetime.now(), "updatedAt": datetime.now()})
    
    # Increment and return
    result = col_counter.find_one_and_update(
        {"key": key},
        {"$inc": {"value": 1}},
        return_document=pymongo.ReturnDocument.AFTER
    )
    return result["value"]

def populate_departments():
    print("Populating Departments...")
    departments = [
        {"name": "Engineering", "children": ["Frontend", "Backend", "DevOps", "QA"]},
        {"name": "Product", "children": ["Product Management", "Design"]},
        {"name": "HR", "children": ["Recruitment", "Employee Relations"]},
        {"name": "Sales", "children": ["Direct Sales", "Partner Sales"]},
        {"name": "Marketing", "children": ["Digital Marketing", "Content"]}
    ]

    dept_map = [] # To store (child_id, name) for employee assignment

    # Use simple integer IDs for departments if not strictly controlled by a counter in this specific app logic,
    # but looking at schema, they are Ints. I'll use a local counter or simple increment.
    # The app seems to rely on `departmentId` and `childDeptId` being Ints.
    
    # Clean up existing if needed? No, let's just find max or start from 1.
    # For safety in this script, I'll check existing max to avoid collision if data exists.
    
    parent_id = 1
    child_id = 1
    
    existing_parent = col_dept_parent.find_one(sort=[("departmentId", -1)])
    if existing_parent:
        parent_id = existing_parent["departmentId"] + 1

    existing_child = col_dept_child.find_one(sort=[("childDeptId", -1)])
    if existing_child:
        child_id = existing_child["childDeptId"] + 1

    for d in departments:
        # Create Parent
        p_doc = {
            "departmentId": parent_id,
            "departmentName": d["name"],
            "description": f"{d['name']} Department",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now()
        }
        col_dept_parent.insert_one(p_doc)
        current_p_id = parent_id
        parent_id += 1

        # Create Children
        for child_name in d["children"]:
            c_doc = {
                "childDeptId": child_id,
                "departmentName": child_name,
                "parentDeptId": current_p_id,
                "description": f"{child_name} Team",
                "createdAt": datetime.now(),
                "updatedAt": datetime.now()
            }
            col_dept_child.insert_one(c_doc)
            dept_map.append(child_id)
            child_id += 1
            
    return dept_map

def populate_employees(count, dept_ids):
    print(f"Populating {count} Employees...")
    employees = []
    
    roles = ["Developer", "Senior Developer", "Manager", "Designer", "Product Manager", "Sales Rep"]
    locations = ["New York", "London", "Remote", "Bangalore", "San Francisco"]

    for _ in range(count):
        emp_id = get_next_sequence("employee", 1000)
        first_name = fake.first_name()
        last_name = fake.last_name()
        name = f"{first_name} {last_name}"
        
        doc = {
            "employeeId": emp_id,
            "employeeName": name,
            "emailId": f"{first_name.lower()}.{last_name.lower()}@example.com",
            "deptId": random.choice(dept_ids) if dept_ids else None,
            "role": random.choice(roles),
            "contactNo": fake.phone_number(),
            "password": "password123", # Plain text as per sample, usually hashed but for synthetic...
            "isActive": True,
            "avatarUrl": f"https://api.dicebear.com/7.x/avataaars/svg?seed={name}",
            "location": random.choice(locations),
            "about": fake.text(max_nb_chars=200),
            "skills": random.sample(["Python", "Angular", "React", "Node.js", "MongoDB", "SQL", "AWS", "Design"], k=3),
            "createdAt": datetime.now(),
            "updatedAt": datetime.now()
        }
        col_employee.insert_one(doc)
        employees.append(emp_id)
        
    return employees

def populate_projects(count, employee_ids):
    print(f"Populating {count} Projects...")
    projects = []
    statuses = ["active", "draft", "completed", "on_hold"]
    
    for _ in range(count):
        proj_id = get_next_sequence("project", 5000)
        proj_name = fake.bs().title()
        
        start_date = datetime.now() - timedelta(days=random.randint(0, 365))
        end_date = start_date + timedelta(days=random.randint(30, 365))
        
        doc = {
            "projectId": proj_id,
            "projectName": proj_name,
            "clientName": fake.company(),
            "startDate": start_date,
            "endDate": end_date,
            "leadByEmpId": random.choice(employee_ids) if employee_ids else None,
            "status": random.choice(statuses),
            "readinessScore": random.randint(50, 100),
            "progress": random.randint(0, 100),
            "overview": {
                "summary": fake.paragraph(),
                "objectives": [fake.sentence() for _ in range(3)]
            },
            "createdAt": datetime.now(),
            "updatedAt": datetime.now()
        }
        col_project.insert_one(doc)
        projects.append(proj_id)
        
    return projects

def populate_assignments(projects, employees):
    print("Populating Project Assignments...")
    
    for proj_id in projects:
        # Assign 3-8 employees per project
        team_size = random.randint(3, min(8, len(employees)))
        team = random.sample(employees, team_size)
        
        for emp_id in team:
            assign_id = get_next_sequence("projectEmployee", 7000)
            
            doc = {
                "empProjectId": assign_id,
                "projectId": proj_id,
                "empId": emp_id,
                "role": random.choice(["Contributor", "Reviewer", "Lead"]),
                "isActive": True,
                "allocationPct": random.choice([25, 50, 100]),
                "assignedDate": datetime.now() - timedelta(days=random.randint(0, 100)),
                "createdAt": datetime.now(),
                "updatedAt": datetime.now()
            }
            col_project_employee.insert_one(doc)

def main():
    print("Starting Synthetic Data Generation...")
    
    # 1. Departments
    dept_ids = populate_departments()
    
    # 2. Employees (Generate 25 to be safe)
    emp_ids = populate_employees(25, dept_ids)
    
    # 3. Projects (Generate 8)
    proj_ids = populate_projects(8, emp_ids)
    
    # 4. Assignments
    populate_assignments(proj_ids, emp_ids)
    
    print("Data Generation Completed Successfully!")

if __name__ == "__main__":
    main()

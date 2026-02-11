Employee Leave Request App
1. **About This App**

Employee Leave Request is a custom Frappe application developed to manage employee leave approvals with proper validation and role-based control.

The application is built using:

Frappe Framework v15

ERPNext v15

HRMS v15

It uses the existing Employee DocType from HRMS and does not duplicate any core HR data.

2. **What We Implemented** (Step-by-Step Development)
Step 1: **Installed Required Applications**

Installed:

bench get-app erpnext
bench --site test install-app erpnext

bench get-app hrms
bench --site test install-app hrms


Verified installation:

bench --site test list-apps

Step 2: **Enabled Developer Mode**

Edited:

sites/test/site_config.json


Set:

"developer_mode": 1


Restarted bench:

bench restart


Developer mode allows exporting DocTypes and Client Scripts.

Step 3: **Created Employee Record**

Before testing leave requests, we created an Employee:

Go to HR → Employee

Create New Employee

Fill basic details:

First Name

Gender

Date of Birth

Date of Joining

Status = Active

Important: Link User ID

In User Details section:

Set User ID (example: rahmanshareef6303@gmail.com
)

Enable “Create User Permission”

This step is mandatory because:

✔ Leave approval validation checks employee.user_id
✔ Prevents self-approval
✔ Links employee to login user

Without linking User ID, approval validation will not work correctly.

Step 4: **Created Custom App**

Created new Frappe app:

bench new-app employee_leave_request
bench --site test install-app employee_leave_request

Step 5: **Created Custom DocType**

Created DocType: Employee leave request2

Fields added:

Employee (Link → Employee)

From Date (Date)

To Date (Date)

Total Days (Int)

Status (Select)

Reason (Small Text)

Step 6: **Implemented Server-Side Validation**

Inside: employee_leave_request/doctype/employee_leave_request2/employee_leave_request2.py

Approval Validation

Rules implemented:

Only HR Manager can approve

System Manager override allowed

Employee cannot approve their own leave

Validation runs in:

def validate(self):
    self.check_approval_rules()


This ensures security at server level.

Step 7: **Implemented Client Script**

Created Client Script:

Date diff and total days calculate


Logic:

Total Days = (To Date - From Date) + 1


This automatically calculates leave duration when dates are selected.

Step 8: **Exported Client Script Using Fixtures**

Updated hooks.py:

fixtures = [
    {
        "doctype": "Client Script",
        "filters": [
            ["name", "in", [
                "Date diff and total days calculate"
            ]]
        ]
    }
]


Exported using:

bench --site test export-fixtures


Generated:

employee_leave_request/fixtures/client_script.json

Step 9: **Pushed App to GitHub**

Initialized Git:

git add .
git commit -m "Initial version with leave validation and client script"
git push origin main


Repository:

https://github.com/rahmanshareef/employeeleaverequest

3. **How the Application Works (Functional Flow)**
For Employee

Login to system

Open Employee Leave Request module

Click New

Select:

Employee

From Date

To Date

Total Days auto-calculates

Save request

For HR Manager

Open submitted leave requests

Review request

Change Status to Approved

Save

System checks:

Is user HR Manager?

Is user not approving own leave?

If validation fails → system throws error.

4. Business Rules Enforced

From Date ≤ To Date

Total Days auto-calculated

Only HR Manager can approve

System Manager override allowed

Self-approval restricted

Employee must have linked User ID

5. Installation Guide
1 Get App
bench get-app https://github.com/rahmanshareef/employeeleaverequest.git

2 Install
bench --site test install-app employee_leave_request

3 Run Migration
bench migrate
bench restart

6. **Important Configuration Note**

Before using leave approval:

✔ Ensure Employee record has User ID linked
✔ Ensure HR Manager role assigned to approving user

Without this:

Approval logic will not work

Self-approval check cannot function

7. **Folder Structure**
employee_leave_request/
├── employee_leave_request/
│   ├── doctype/
│   │   └── employee_leave_request2/
│   ├── fixtures/
│   └── hooks.py
├── README.md
├── pyproject.toml
└── license.txt

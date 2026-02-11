import frappe
from frappe.model.document import Document

class Employeeleaverequest2(Document):

    def validate(self):
        self.check_approval_rules()


    def check_approval_rules(self):
        if self.status == "Approved":

            if "HR Manager" not in frappe.get_roles():
                frappe.throw("Only HR can approve leave requests")

            employee_user = frappe.db.get_value(
                "Employee", self.employee, "user_id"
            )

            if employee_user == frappe.session.user:
                frappe.throw("You cannot approve your own leave request")
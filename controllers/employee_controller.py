from flask import Blueprint, jsonify, request, render_template, redirect
from models.employee_model import employees

employee_bp = Blueprint("employee_bp", __name__)

# READ ALL -> GET /employees
@employee_bp.route("/employees", methods=["GET"])
def list_employees():
    return jsonify(employees), 200

# READ ONE -> GET /employees/3
@employee_bp.route("/employees/<int:id>", methods=["GET"])
def get_employee(id):
    for e in employees:
        if e["id"] == id:
            return jsonify(e), 200
    return jsonify({"error": "Not found"}), 404

# SHOW FORM TAMBAH -> GET /employees/new
@employee_bp.route("/employees/new", methods=["GET"])
def show_form():
    return render_template("form.html", employees=employees)

# PROSES TAMBAH -> POST /employees/new
@employee_bp.route("/employees/new", methods=["POST"])
def submit_form():
    name = request.form.get("name")
    position = request.form.get("position", "Staff")
    salary = request.form.get("salary", 0)

    if not name:
        return "Nama wajib diisi!", 400

    new_id = max([e["id"] for e in employees], default=0) + 1
    new = {
        "id": new_id,
        "name": name,
        "position": position,
        "salary": int(salary) if salary else 0,
    }
    employees.append(new)

    return redirect("/employees/new")

# DELETE -> POST /employees/delete/<int:id>
@employee_bp.route("/employees/delete/<int:id>", methods=["POST"])
def delete_employee(id):
    global employees
    employees = [e for e in employees if e["id"] != id]
    return redirect("/employees/new")

# TAMPILKAN FORM EDIT -> GET /employees/edit/<int:id>
@employee_bp.route("/employees/edit/<int:id>", methods=["GET"])
def show_edit_form(id):
    for e in employees:
        if e["id"] == id:
            return render_template("edit.html", employee=e)
    return "Pegawai tidak ditemukan!", 404

# PROSES SIMPAN EDIT -> POST /employees/edit/<int:id>
@employee_bp.route("/employees/edit/<int:id>", methods=["POST"])
def update_employee(id):
    name = request.form.get("name")
    position = request.form.get("position")
    salary = request.form.get("salary")

    for e in employees:
        if e["id"] == id:
            e["name"] = name
            e["position"] = position
            e["salary"] = int(salary) if salary else 0
            break

    return redirect("/employees/new")
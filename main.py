from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

#Updated as of 2/15

app = Flask(__name__)

ORDERS_FILE = os.path.join(os.path.dirname(__file__), "orders.json")
ADMIN_KEY = "thaiday2025"


def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, "r") as f:
        return json.load(f)


def save_orders(orders):
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        order = request.form.get("order", "").strip()
        notes = request.form.get("notes", "").strip()

        if name and order:
            orders = load_orders()
            orders.append({
                "id": len(orders) + 1,
                "name": name,
                "order": order,
                "notes": notes,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_orders(orders)
            return redirect(url_for("thanks", person=name))

    return render_template("index.html")


@app.route("/thanks")
def thanks():
    person = request.args.get("person", "")
    return render_template("thanks.html", person=person)


@app.route("/admin")
def admin():
    key = request.args.get("key", "")
    if key != ADMIN_KEY:
        return render_template("locked.html"), 403
    orders = load_orders()
    return render_template("admin.html", orders=orders, total=len(orders))


@app.route("/admin/clear", methods=["POST"])
def clear_orders():
    key = request.args.get("key", "")
    if key != ADMIN_KEY:
        return "Unauthorized", 403
    save_orders([])
    return redirect(url_for("admin", key=key))


@app.route("/admin/delete/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    key = request.args.get("key", "")
    if key != ADMIN_KEY:
        return "Unauthorized", 403
    orders = load_orders()
    orders = [o for o in orders if o["id"] != order_id]
    save_orders(orders)
    return redirect(url_for("admin", key=key))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

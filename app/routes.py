from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app import db

from app.models import (
    User,
    Product,
    CartItem,
    Order,
    OrderItem
)


main = Blueprint("main", __name__)


# --------------------------------------------------
# Authentication helpers
# --------------------------------------------------

def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("main.login"))

        return function(*args, **kwargs)

    return wrapper


def admin_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("main.login"))

        if session.get("role") != "admin":
            flash("Administrator access required.")
            return redirect(url_for("main.index"))

        return function(*args, **kwargs)

    return wrapper


# --------------------------------------------------
# Home
# --------------------------------------------------

@main.route("/")
def index():

    products = Product.query.all()

    return render_template(
        "index.html",
        products=products
    )


# --------------------------------------------------
# Registration
# --------------------------------------------------

@main.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            flash("Email already registered.")
            return redirect(url_for("main.register"))

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role="customer"
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully.")

        return redirect(url_for("main.login"))

    return render_template("register.html")


# --------------------------------------------------
# Login
# --------------------------------------------------

@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session.clear()

            session["user_id"] = user.id
            session["role"] = user.role

            return redirect(url_for("main.index"))

        flash("Invalid email or password.")

    return render_template("login.html")


# --------------------------------------------------
# Logout
# --------------------------------------------------

@main.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("main.index"))


# --------------------------------------------------
# Profile
# --------------------------------------------------

@main.route("/profile")
@login_required
def profile():

    user = User.query.get_or_404(
        session["user_id"]
    )

    return render_template(
        "profile.html",
        user=user
    )


# --------------------------------------------------
# Add to cart
# --------------------------------------------------

@main.route(
    "/cart/add/<int:product_id>",
    methods=["POST"]
)
@login_required
def add_to_cart(product_id):

    product = Product.query.get_or_404(product_id)

    if product.stock <= 0:
        flash("Product is out of stock.")
        return redirect(url_for("main.index"))

    user_id = session["user_id"]

    cart_item = CartItem.query.filter_by(
        user_id=user_id,
        product_id=product.id
    ).first()

    if cart_item:

        if cart_item.quantity < product.stock:
            cart_item.quantity += 1

    else:

        cart_item = CartItem(
            user_id=user_id,
            product_id=product.id,
            quantity=1
        )

        db.session.add(cart_item)

    db.session.commit()

    flash("Product added to cart.")

    return redirect(url_for("main.index"))


# --------------------------------------------------
# Cart
# --------------------------------------------------

@main.route("/cart")
@login_required
def cart():

    cart_items = CartItem.query.filter_by(
        user_id=session["user_id"]
    ).all()

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )


# --------------------------------------------------
# Remove cart item
# --------------------------------------------------

@main.route(
    "/cart/remove/<int:item_id>",
    methods=["POST"]
)
@login_required
def remove_from_cart(item_id):

    item = CartItem.query.filter_by(
        id=item_id,
        user_id=session["user_id"]
    ).first_or_404()

    db.session.delete(item)
    db.session.commit()

    return redirect(url_for("main.cart"))


# --------------------------------------------------
# Checkout
# --------------------------------------------------

@main.route(
    "/checkout",
    methods=["POST"]
)
@login_required
def checkout():

    user_id = session["user_id"]

    cart_items = CartItem.query.filter_by(
        user_id=user_id
    ).all()

    if not cart_items:
        flash("Your cart is empty.")
        return redirect(url_for("main.cart"))

    total = 0

    for item in cart_items:

        if item.quantity > item.product.stock:
            flash(
                f"Not enough stock for {item.product.name}."
            )

            return redirect(
                url_for("main.cart")
            )

        total += (
            item.product.price *
            item.quantity
        )

    order = Order(
        user_id=user_id,
        total=total,
        status="pending"
    )

    db.session.add(order)
    db.session.flush()

    for item in cart_items:

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )

        item.product.stock -= item.quantity

        db.session.add(order_item)
        db.session.delete(item)

    db.session.commit()

    flash(
        f"Order #{order.id} placed successfully."
    )

    return redirect(
        url_for("main.orders")
    )


# --------------------------------------------------
# Orders
# --------------------------------------------------

@main.route("/orders")
@login_required
def orders():

    orders = Order.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Order.id.desc()
    ).all()

    return render_template(
        "orders.html",
        orders=orders
    )


# --------------------------------------------------
# Single order
# --------------------------------------------------

@main.route("/orders/<int:order_id>")
@login_required
def order_detail(order_id):

    order = Order.query.filter_by(
        id=order_id,
        user_id=session["user_id"]
    ).first_or_404()

    return render_template(
        "order_detail.html",
        order=order
    )


# ==================================================
# ADMIN
# ==================================================

@main.route("/admin")
@admin_required
def admin_dashboard():

    users = User.query.count()
    products = Product.query.count()
    orders = Order.query.count()

    return render_template(
        "admin/dashboard.html",
        users=users,
        products=products,
        orders=orders
    )


@main.route("/admin/users")
@admin_required
def admin_users():

    users = User.query.order_by(
        User.id
    ).all()

    return render_template(
        "admin/users.html",
        users=users
    )


@main.route("/admin/products")
@admin_required
def admin_products():

    products = Product.query.order_by(
        Product.id
    ).all()

    return render_template(
        "admin/products.html",
        products=products
    )


@main.route("/admin/products/add", methods=["GET", "POST"])
@admin_required
def admin_add_product():

    if request.method == "POST":

        name = request.form.get("name")
        description = request.form.get("description")
        price = float(request.form.get("price"))
        stock = int(request.form.get("stock"))

        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock
        )

        db.session.add(product)
        db.session.commit()

        flash("Product created.")

        return redirect(
            url_for("main.admin_products")
        )

    return render_template(
        "admin/add_product.html"
    )


@main.route("/admin/orders")
@admin_required
def admin_orders():

    orders = Order.query.order_by(
        Order.id.desc()
    ).all()

    return render_template(
        "admin/orders.html",
        orders=orders
    )


# ==================================================
# API
# ==================================================

@main.route("/api/products")
def api_products():

    products = Product.query.all()

    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        }
        for product in products
    ])


@main.route("/api/profile")
@login_required
def api_profile():

    user = User.query.get_or_404(
        session["user_id"]
    )

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    })

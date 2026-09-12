from app import create_app, db
from app.models import User, Product
from werkzeug.security import generate_password_hash


app = create_app()


with app.app_context():

    if User.query.count() == 0:

        admin = User(
            name="Admin",
            email="admin@secureshop.local",
            password=generate_password_hash("AdminPassword123!"),
            role="admin"
        )

        customer = User(
            name="Test Customer",
            email="customer@secureshop.local",
            password=generate_password_hash("CustomerPassword123!"),
            role="customer"
        )

        db.session.add(admin)
        db.session.add(customer)

    if Product.query.count() == 0:

        products = [

            Product(
                name="Developer Laptop",
                description="15-inch development laptop",
                price=799.99,
                stock=20
            ),

            Product(
                name="Mechanical Keyboard",
                description="Mechanical keyboard",
                price=89.99,
                stock=50
            ),

            Product(
                name="Security Book",
                description="Application security reference",
                price=39.99,
                stock=100
            ),

            Product(
                name="USB-C Hub",
                description="Multi-port USB-C hub",
                price=49.99,
                stock=30
            )

        ]

        db.session.add_all(products)

    db.session.commit()

    print("Database seeded successfully.")

def test_db():
    new_product = insert_product("Cheese", 3.99, 50)
    if not new_product:
        print("Failed to add product.")
        return
    print(f"Added product: {new_product.product_name}")
    
    new_user = insert_user("the_admin", "admin123", "admin")
    if not new_user:
        print("Failed to add user.")
        return
    print(f"Added user: {new_user.user_name}")

    update_product_stock(new_product.product_id, 45)
    print("Updated product stock.")

    product = select_product(new_product.product_id)
    if product:
        print(f"Product ID {product.product_id}: {product.product_name} - Stock: {product.product_stock}")
    
    user = select_user(new_user.user_id)
    if user:
        print(f"User ID {user.user_id}: {user.user_name} - Role: {user.user_role}")

    print("All Products:")
    for product in select_products():
        print(f"{product.product_id}: {product.product_name} - {product.product_stock}")
        
    print("All Users:")
    for user in select_users():
        print(f"{user.user_id}: {user.user_name} - {user.user_role}")
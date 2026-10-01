from food_delivery import Customer, DeliveryPartner, Restaurant, MenuItem

# 1. Register customer Priya
priya = Customer("Priya", "9876543210", "Bangalore")
print("--- Customer ---")
priya.display_profile()

# 2. Register delivery partner Rajesh
rajesh = DeliveryPartner("Rajesh", "9123456780", "Bike")
print("\n--- Delivery Partner ---")
rajesh.display_profile()

# 3. Create Bawarchi at MG Road and add Biryani and Kebab
bawarchi = Restaurant("Bawarchi", "MG Road")
biryani = MenuItem("Biryani", 250, False)
kebab = MenuItem("Kebab", 150, False)
bawarchi.add_item(biryani)
bawarchi.add_item(kebab)
print("\n--- Menu:", bawarchi.name, "---")
for item in bawarchi.get_menu():
    print(f"{item.name}: Rs.{item.price}")

# 4. Top up wallet by 500, then attempt -100 (should be ignored)
print("\n--- Wallet ---")
priya.add_to_wallet(500)
print("After top-up of 500:", priya._wallet_balance)
priya.add_to_wallet(-100)
print("After attempted top-up of -100:", priya._wallet_balance)

# 5. Priya places an order for Biryani and Kebab
print("\n--- Order ---")
order = priya.place_order(bawarchi, [biryani, kebab])
order._otp = 1234  # fixed OTP so the demo is repeatable (real OTP is random)

# 6. Bill breakdown and estimated time
subtotal = sum(item.price for item in order._items)
gst = subtotal * 0.05
packaging_fee = 20
print(f"Subtotal: Rs.{subtotal}")
print(f"GST (5%): Rs.{gst}")
print(f"Packaging fee: Rs.{packaging_fee}")
print(f"Total: Rs.{order.calculate_bill()}")
print(f"Estimated delivery time: {order.estimated_time()} minutes")

# 7. Rajesh accepts, wrong OTP, then correct OTP
print("\n--- Delivery ---")
rajesh.accept_order(order)
print("Status:", order._status)

rajesh.deliver(order, 0)  # wrong OTP (real OTPs are always 4 digits)
print("After wrong OTP, status:", order._status)

rajesh.deliver(order, 1234)
print("After correct OTP, status:", order._status)

# 8. Notifications
print("\n--- Notifications ---")
priya.notify("Order delivered")
rajesh.notify("Order delivered")

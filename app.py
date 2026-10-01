import streamlit as st
from food_delivery import Customer, DeliveryPartner, Restaurant, MenuItem

st.set_page_config(page_title="Food Delivery", page_icon="🍔")
st.title("Food Delivery")


def bill_for(items):
    subtotal = sum(i.price for i in items)
    return subtotal + subtotal * 0.05 + 20


# ---------- State ----------
if "restaurant" not in st.session_state:
    r = Restaurant("Spice Garden", "Aurangabad")
    for n, p, v in [("Paneer Tikka", 220, True), ("Veg Biryani", 180, True),
                    ("Chicken Biryani", 260, False), ("Butter Naan", 40, True)]:
        r.add_item(MenuItem(n, p, v))
    st.session_state.restaurant = r
    st.session_state.customer = None
    st.session_state.partner = None
    st.session_state.order = None

ss = st.session_state

# ---------- 1. Customer ----------
st.header("1. Create customer")
with st.form("customer_form"):
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    address = st.text_input("Address")
    if st.form_submit_button("Create customer"):
        if name and phone and address:
            ss.customer = Customer(name, phone, address)
            st.success(f"Customer {name} created.")
        else:
            st.error("Fill in name, phone and address.")

if ss.customer is None:
    st.info("Create a customer to continue.")
    st.stop()

c = ss.customer
st.caption(f"{c._name} · {c._phone} · {c.address} · Wallet: ₹{c._wallet_balance:.2f}")

# ---------- 2. Wallet ----------
st.header("2. Add wallet balance")
amount = st.number_input("Amount (₹)", min_value=0, step=50, value=500)
if st.button("Add to wallet"):
    c.add_to_wallet(amount)
    st.success(f"Added ₹{amount}. Balance: ₹{c._wallet_balance:.2f}")

# ---------- 3. Menu ----------
st.header("3. Restaurant menu")
rest = ss.restaurant
st.write(f"**{rest.name}**, {rest.location} ({'Open' if rest.is_open() else 'Closed'})")
st.table([{"Item": i.name, "Price (₹)": i.price, "Type": "Veg" if i.is_veg else "Non-veg"}
          for i in rest.get_menu()])

# ---------- 4. Place order ----------
st.header("4. Place an order")
menu = {i.name: i for i in rest.get_menu()}
chosen = st.multiselect("Choose items", list(menu))
if chosen:
    st.write(f"Bill (incl. 5% GST and ₹20 packaging): **₹{bill_for([menu[n] for n in chosen]):.2f}**")

if st.button("Place order"):
    if not chosen:
        st.error("Select at least one item.")
    else:
        items = [menu[n] for n in chosen]
        bill = bill_for(items)
        if c._wallet_balance < bill:
            st.error(f"Wallet balance too low. Need ₹{bill:.2f}, have ₹{c._wallet_balance:.2f}.")
        else:
            c._wallet_balance -= bill
            ss.order = c.place_order(rest, items)
            st.success(f"Order {ss.order._order_id} placed.")

order = ss.order
if order:
    st.info(f"Order {order._order_id} · Status: **{order._status}** · "
            f"ETA {order.estimated_time()} min · Your OTP: **{order._otp}**")

# ---------- 5. Delivery partner ----------
st.header("5. Create delivery partner")
with st.form("partner_form"):
    pname = st.text_input("Partner name")
    pphone = st.text_input("Partner phone")
    vehicle = st.selectbox("Vehicle", ["Bike", "Scooter", "Bicycle"])
    if st.form_submit_button("Create partner"):
        if pname and pphone:
            ss.partner = DeliveryPartner(pname, pphone, vehicle)
            st.success(f"Partner {pname} created.")
        else:
            st.error("Fill in name and phone.")

p = ss.partner
if p:
    st.caption(f"{p._name} · {p.vehicle} · {'Available' if p.is_available else 'Busy'}")

# ---------- 6. Accept ----------
st.header("6. Accept the order")
if st.button("Accept order"):
    if not (order and p):
        st.error("Place an order and create a delivery partner first.")
    elif order._status != "Placed":
        st.warning(f"Order is already {order._status}.")
    elif not p.is_available:
        st.warning("Partner is busy.")
    else:
        p.accept_order(order)
        st.success(f"{p._name} accepted order {order._order_id}.")

# ---------- 7. OTP and delivery ----------
st.header("7. Enter OTP and complete delivery")
otp_text = st.text_input("Customer OTP", max_chars=4)
if st.button("Complete delivery"):
    if not (order and p):
        st.error("Place an order and create a delivery partner first.")
    elif order._status != "Accepted":
        st.warning("Accept the order first.")
    elif not otp_text.isdigit():
        st.error("OTP must be 4 digits.")
    else:
        p.deliver(order, int(otp_text))
        if order._status == "Delivered":
            st.success("Order delivered. Partner is available again.")
            st.balloons()
        else:
            st.error("Wrong OTP. Try again.")

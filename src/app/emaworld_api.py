import httpx


class EmaworldApiCleint:
    def __init__(self, email, password):
        print(f"Email: {email}, Password: {password}")
        self.email = email
        self.password = password
        self.base_url = "https://api.emaworld.store"
        self.session = httpx.Client(
            base_url=self.base_url,
            timeout=None,
        )
        self.login()
        self.session.headers["Authorization"] = f"Bearer {self.token}"

    def login(self):
        req = self.session.post(
            "auth/login",
            json={
                "email": self.email,
                "password": self.password,
            },
        )
        self.token = req.json().get("token")

    def get_all_orders_ids(self):  # ? Return list of in packing order ids
        req = self.session.get("/orders/all-orders?status=In%20packing")
        data = req.json()
        return [order.get("_id") for order in data.get("orders", {})]

    def get_all_orders_with_details(self): #? Return list of order with details
        orders = self.get_all_orders_ids()
        return [self.get_order_details(order) for order in orders]

    def get_order_details(self, order_id):  # ? Return order details
        req = self.session.get(
            "orders/order/",
            headers={
                "orderid": order_id,
            },
        )
        return req.json()

import httpx
from emaworld_api import EmaworldApiCleint


class StoxApiClient:
    def __init__(self, token, api_client: EmaworldApiCleint) -> None:
        self.api_client = api_client
        self.base_url = "https://merchants.stox-eg.com/api"
        self.session = httpx.Client(
            base_url=self.base_url,
            timeout=None,
        )
        self.session.headers["Authorization"] = f"Bearer {token}"
        self.fetch_areas()
        self.fetch_products()

    def fetch_areas(self):
        req = self.session.get("/areas")
        self.areas = req.json()["data"]

    def fetch_products(self):
        req = self.session.get("/products")
        self.products = req.json()["data"]

    def get_area_id(self, ar_name):
        for area in self.areas:
            if ar_name == area["ar_name"]:
                return area["id"]

    def get_product_id(self, name):
        for product in self.products:
            if name == f'{product["name"]} {product["sku"]}'.lower():
                print(product["id"])
                return product["id"]

    def parse_oreder(self, order):
        return {
            "customer_name": order["order"]["name"],
            "mobile_1": order["order"]["phone"],
            "mobile_2": order["order"].get("otherPhone", ""),
            "address": " - ".join(
                [
                    order["order"]["shipping"]["govId"]["englishName"],
                    order["order"]["shipping"]["areaId"]["englishName"],
                ]
            ),
            "area_id": self.get_area_id(
                order["order"]["shipping"]["areaId"]["englishName"]
            ),
            "payment_type": "COD",
            "cod_amount": order["order"]["totalCost"]["amount"],
            "note": order["order"].get("notes"),
            "reference_number": "",
            "products": [
                {
                    "id": self.get_product_id(order["order"]["products"][0]["product"]["product"]["title"]),
                    "qty": "1",
                }
            ],
        }

    def send_oreders(self):
        orders = self.api_client.get_all_orders_with_details()
        print(f"Got {len(orders)} orders")
        if not orders:
            return {"success": True}
        parsed_orders = [self.parse_oreder(order) for order in orders]
        req = self.session.post(
            "/orders/store",
            json={
                "orders": parsed_orders,
            },
        )
        return req.json()

    def list_orders(self):
        req = self.session.get("/orders")
        return req.json()

class Product:

    def get_product_by_id(self, product_id):
        product1 = {
            'product_id': 1,
            'product_name': 'Produto 1',
            'produtc_active': True,
            'product_sku': 1,
            'product_price': 10,
            'product_img': 'https://www.teste.com.br/img.png',
            'product_stock': 0
        }
        product2 = {
            'product_id': 2,
            'product_name': 'Produto 2',
            'produtc_active': True,
            'product_sku': 2,
            'product_price': 20,
            'product_img': 'https://www.teste.com.br/img2.png',
            'product_stock': 20
        }
        product3 = {
            'product_id': 3,
            'product_name': 'Produto 3',
            'produtc_active': True,
            'product_sku': 3,
            'product_price': 30,
            'product_img': 'https://www.teste.com.br/img3.png',
            'product_stock': 30
        }
        products = [product1, product2, product3]

        for product in products:
            if product_id == product['product_id']:
                return product
        return {'message_error': 'Product not found'}


class Customer:

    def get_customer_by_id(self, customer_id):
        customer1 = {
            'customer_id': 1,
            'customer_name': 'Customer 1',
            'customer_email': 'customer1@customer.com',
            'customer_phone': '21911111111',
            'customer_gender': 'M'
        }
        customer2 = {
            'customer_id': 2,
            'customer_name': 'Customer 2',
            'customer_email': 'customer2@customer.com',
            'customer_phone': '21922222222',
            'customer_gender': 'F'
        }
        customer3 = {
            'customer_id': 3,
            'customer_name': 'Customer 3',
            'customer_email': 'customer3@customer.com',
            'customer_phone': '21933333333',
            'customer_gender': 'F'
        }
        customers = [customer1, customer2, customer3]

        for customer in customers:
            if customer_id == customer['customer_id']:
                return customer
        return {'message_warning': 'Customer not found'}


class Coupon:

    def get_coupons_by_code(self, coupon_code):
        coupon1 = {
            'coupon_id': 1,
            'coupon_code': 'coupon_1',
            'coupon_percentage_value': 10
        }
        coupon2 = {
            'coupon_id': 1,
            'coupon_code': 'coupon_2',
            'coupon_percentage_value': 20
        }
        coupon3 = {
            'coupon_id': 1,
            'coupon_code': 'coupon_3',
            'coupon_percentage_value': 30
        }
        coupons = [coupon1, coupon2, coupon3]

        for coupon in coupons:
            if coupon_code == coupon['coupon_code']:
                return coupon
        return {'message_error': 'Coupon not found'}

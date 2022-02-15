import requests

class TestCars:
    url_base = 'http://localhost:8000/api/v1/'

    def test_get_cars(self):
        cars = requests.get(url=self.url_base)

        assert cars.status_code == 200

    def test_get_brands(self):
        brands = requests.get(url=f"{self.url_base}brands/")

        assert brands.status_code == 200
    
    def test_get_models(self):
        models = requests.get(url=f"{self.url_base}models/")

        assert models.status_code == 200

    def test_get_categorys(self):
        categorys = requests.get(url=f"{self.url_base}categorys/")

        assert categorys.status_code == 200

    def test_get_colors(self):
        colors = requests.get(url=f"{self.url_base}colors/")

        assert colors.status_code == 200

    def test_cars_pagination(self):
        cars = requests.get(url=self.url_base)

        assert len(cars.json()['results']) == 8

    def test_get_cars_only_color(self):
        cars = requests.get(url=f"{self.url_base}?page=1&color=branco")

        for car in cars.json()['results']:
            assert car['color'].lower() == 'branco'

        assert cars.status_code == 200
    
    def test_get_cars_only_brand(self):
        cars = requests.get(url=f"{self.url_base}?page=1&brand=Chevrolet")

        for car in cars.json()['results']:
            assert car['brand'].lower() == 'chevrolet'

        assert cars.status_code == 200

    def test_get_cars_only_model(self):
        cars = requests.get(url=f"{self.url_base}?page=1&model=Civic")

        for car in cars.json()['results']:
            assert car['model'].lower() == 'civic'

        assert cars.status_code == 200

    def test_get_cars_only_year(self):
        cars = requests.get(url=f"{self.url_base}?page=1&year=2018-2022")

        for car in cars.json()['results']:
            assert car['year'] >= 2018
            assert car['year'] <= 2022

        assert cars.status_code == 200

    def test_get_cars_only_price(self):
        cars = requests.get(url=f"{self.url_base}?page=1&price=10000-90000")

        for car in cars.json()['results']:
            assert float(car['price']) >= 10000
            assert float(car['price']) <= 90000

        assert cars.status_code == 200
    
    def test_get_cars_only_category(self):
        cars = requests.get(url=f"{self.url_base}?page=1&category=Hatch")

        for car in cars.json()['results']:
            assert car['category'].lower() == 'hatch'

        assert cars.status_code == 200
    
    def test_get_cars_only_exchange(self):
        cars = requests.get(url=f"{self.url_base}?page=1&exchange=Manual")

        for car in cars.json()['results']:
            assert car['exchange'].lower() == 'manual'

        assert cars.status_code == 200
    
    def test_get_cars_only_fuel(self):
        cars = requests.get(url=f"{self.url_base}?page=1&fuel=Gasolina")

        for car in cars.json()['results']:
            assert car['fuel'].lower() == 'gasolina'

        assert cars.status_code == 200
    
    def test_get_cars_only_doors(self):
        cars = requests.get(url=f"{self.url_base}?page=1&doors=4")

        for car in cars.json()['results']:
            assert car['doors'].lower() == '4'

        assert cars.status_code == 200
    
    def test_get_cars_full_params(self):
        cars = requests.get(url=f"{self.url_base}?page=1&brand=Volkswagen&model=Gol 1.6&year=0-2022&state=new&kms=0&price=10000-101000&category=Hatch&exchange=Manual&color=Branco&fuel=a/g&doors=2")

        for car in cars.json()['results']:
            assert car['brand'].lower() == 'volkswagen'
            assert car['model'].lower() == 'gol 1.6'
            assert car['year'] >= 0
            assert car['year'] <= 2022
            assert car['new'] == True
            assert car['kms'] == 0
            assert float(car['price']) >= 10000
            assert float(car['price']) <= 101000
            assert car['category'].lower() == 'hatch'
            assert car['exchange'].lower() == 'manual'
            assert car['color'].lower() == 'branco'
            assert car['fuel'].lower() == 'a/g'
            assert car['doors'] == '2'

        assert cars.status_code == 200
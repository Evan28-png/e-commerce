from unittest.mock import patch, MagicMock
import pytest
from app import app, Product  

# A simple mock Product class for the test
class MockProduct:
    def __init__(self, id, name):
        self.id = id
        self.name = name

@pytest.fixture
def client():
    # Set up a test client for the Flask app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# The actual test function
@patch('app.Product')  # The crucial line: We are mocking the Product class
def test_checkout_page_renders_with_product(mock_product_class, client):
    # Create a mock product instance
    mock_product = MagicMock()
    mock_product.id = 1
    mock_product.name = "Test PC"
    mock_product.price = 20000
    
    # Configure the mock query to return our mock product
    # The `return_value` of `query.filter_by().first()` is our mock_product
    mock_product_class.query.filter_by.return_value.first.return_value = mock_product

    # Make a GET request to the checkout endpoint
    response = client.get('/checkout/1')

    # Assertions to verify the test
    assert response.status_code == 200
    assert b'Test PC' in response.data  # Check if the product name is in the rendered HTML

    # Verify that the database query was called as expected
    mock_product_class.query.filter_by.assert_called_once_with(id='1')

@patch('app.Product')
def test_checkout_page_with_no_product(mock_product_class, client):
    # Configure the mock query to return None, simulating a product not found
    mock_product_class.query.filter_by.return_value.first.return_value = None

    # Make a GET request for a non-existent product
    response = client.get('/checkout/999')

    # Assertions
    assert response.status_code == 200
    # You might want to assert that a 'Product not found' message is displayed
    # in a real application. For this simple example, we'll just check for 200.

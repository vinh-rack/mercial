import sys
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))
sys.path.insert(0, str(root_path / "services" / "inventory"))

import logging

import grpc
import inventory_pb2
import inventory_pb2_grpc
import pytest

from shared.logger import setup_logger

log_file = Path(__file__).parent / "logs" / "test_inventory.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logger = setup_logger("test_inventory", str(log_file))


@pytest.fixture(scope="module")
def grpc_channel():
    channel = grpc.insecure_channel('localhost:50051')
    yield channel
    channel.close()


@pytest.fixture(scope="module")
def inventory_stub(grpc_channel):
    return inventory_pb2_grpc.InventoryServiceStub(grpc_channel)


@pytest.fixture(scope="module")
def test_product(inventory_stub):
    logger.info("Creating test product")
    response = inventory_stub.CreateProduct(inventory_pb2.CreateProductRequest(
        name="Test iPhone 15",
        sku="TEST-001",
        cat_id=1,
        short_desc="Test product",
        long_desc="This is a test product",
        price=999000,
        discount_price=899000,
        stock_qty=50,
        warranty_months=12,
        status=True
    ))
    logger.info(f"Created test product with ID: {response.prod_id}")
    yield response

    try:
        inventory_stub.DeleteProduct(inventory_pb2.DeleteProductRequest(prod_id=response.prod_id))
        logger.info(f"Cleaned up test product ID: {response.prod_id}")
    except grpc.RpcError:
        pass


def test_create_product(inventory_stub):
    logger.info("Testing CreateProduct")
    response = inventory_stub.CreateProduct(inventory_pb2.CreateProductRequest(
        name="Test Product",
        sku="TEST-CREATE-001",
        cat_id=1,
        short_desc="Test",
        long_desc="Test description",
        price=500000,
        discount_price=450000,
        stock_qty=100,
        warranty_months=12,
        status=True
    ))

    assert response.prod_id > 0
    assert response.name == "Test Product"
    assert response.stock_qty == 100
    logger.info(f"CreateProduct test passed, product ID: {response.prod_id}")

    inventory_stub.DeleteProduct(inventory_pb2.DeleteProductRequest(prod_id=response.prod_id))


def test_get_product_by_id(inventory_stub, test_product):
    logger.info(f"Testing GetProductById for ID: {test_product.prod_id}")
    response = inventory_stub.GetProductById(
        inventory_pb2.GetProductByIdRequest(prod_id=test_product.prod_id)
    )

    assert response.prod_id == test_product.prod_id
    assert response.name == test_product.name
    assert response.price == test_product.price
    logger.info("GetProductById test passed")


def test_get_product_by_sku(inventory_stub, test_product):
    logger.info(f"Testing GetProductBySku for SKU: {test_product.sku}")
    response = inventory_stub.GetProductBySku(
        inventory_pb2.GetProductBySkuRequest(sku=test_product.sku)
    )

    assert response.prod_id == test_product.prod_id
    assert response.sku == test_product.sku
    logger.info("GetProductBySku test passed")


def test_list_products(inventory_stub):
    logger.info("Testing ListProducts")
    response = inventory_stub.ListProducts(
        inventory_pb2.ListProductsRequest(limit=10, offset=0)
    )

    assert len(response.products) > 0
    logger.info(f"ListProducts test passed, found {len(response.products)} products")


def test_get_stock_level(inventory_stub, test_product):
    logger.info(f"Testing GetStockLevel for product ID: {test_product.prod_id}")
    response = inventory_stub.GetStockLevel(
        inventory_pb2.GetProductByIdRequest(prod_id=test_product.prod_id)
    )

    assert response.prod_id == test_product.prod_id
    assert response.stock_qty == test_product.stock_qty
    logger.info(f"GetStockLevel test passed, stock: {response.stock_qty}")


def test_adjust_stock(inventory_stub, test_product):
    logger.info(f"Testing AdjustStock for product ID: {test_product.prod_id}")
    initial_stock = test_product.stock_qty

    response = inventory_stub.AdjustStock(inventory_pb2.AdjustStockRequest(
        prod_id=test_product.prod_id,
        adjustment=-10
    ))

    assert response.stock_qty == initial_stock - 10
    logger.info(f"AdjustStock test passed, new stock: {response.stock_qty}")

    inventory_stub.AdjustStock(inventory_pb2.AdjustStockRequest(
        prod_id=test_product.prod_id,
        adjustment=10
    ))


def test_adjust_stock_insufficient(inventory_stub, test_product):
    logger.info("Testing AdjustStock with insufficient stock")

    with pytest.raises(grpc.RpcError) as exc_info:
        inventory_stub.AdjustStock(inventory_pb2.AdjustStockRequest(
            prod_id=test_product.prod_id,
            adjustment=-9999
        ))

    assert exc_info.value.code() == grpc.StatusCode.FAILED_PRECONDITION
    logger.info("AdjustStock insufficient stock test passed")


def test_update_product(inventory_stub, test_product):
    logger.info(f"Testing UpdateProduct for product ID: {test_product.prod_id}")
    response = inventory_stub.UpdateProduct(inventory_pb2.UpdateProductRequest(
        prod_id=test_product.prod_id,
        data=inventory_pb2.CreateProductRequest(
            name="Updated Test Product",
            sku=test_product.sku,
            cat_id=1,
            short_desc="Updated description",
            long_desc="Updated long description",
            price=1099000,
            discount_price=999000,
            stock_qty=test_product.stock_qty,
            warranty_months=24,
            status=True
        )
    ))

    assert response.prod_id == test_product.prod_id
    assert response.name == "Updated Test Product"
    assert response.price == 1099000
    logger.info("UpdateProduct test passed")


def test_deactivate_product(inventory_stub):
    logger.info("Testing DeactivateProduct")
    create_response = inventory_stub.CreateProduct(inventory_pb2.CreateProductRequest(
        name="Product to Deactivate",
        sku="TEST-DEACTIVATE-001",
        cat_id=1,
        short_desc="Test",
        long_desc="Test",
        price=100000,
        discount_price=90000,
        stock_qty=10,
        warranty_months=12,
        status=True
    ))

    response = inventory_stub.DeactivateProduct(
        inventory_pb2.DeleteProductRequest(prod_id=create_response.prod_id)
    )

    assert response.success is True
    logger.info("DeactivateProduct test passed")

    inventory_stub.DeleteProduct(inventory_pb2.DeleteProductRequest(prod_id=create_response.prod_id))


def test_delete_product(inventory_stub):
    logger.info("Testing DeleteProduct")
    create_response = inventory_stub.CreateProduct(inventory_pb2.CreateProductRequest(
        name="Product to Delete",
        sku="TEST-DELETE-001",
        cat_id=1,
        short_desc="Test",
        long_desc="Test",
        price=100000,
        discount_price=90000,
        stock_qty=10,
        warranty_months=12,
        status=True
    ))

    response = inventory_stub.DeleteProduct(
        inventory_pb2.DeleteProductRequest(prod_id=create_response.prod_id)
    )

    assert response.success is True
    logger.info("DeleteProduct test passed")


def test_get_nonexistent_product(inventory_stub):
    logger.info("Testing GetProductById with nonexistent ID")

    with pytest.raises(grpc.RpcError) as exc_info:
        inventory_stub.GetProductById(inventory_pb2.GetProductByIdRequest(prod_id=999999))

    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND
    logger.info("GetProductById nonexistent test passed")

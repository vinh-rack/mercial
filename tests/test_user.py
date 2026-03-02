import sys
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))
sys.path.insert(0, str(root_path / "services" / "user"))

import grpc
import pytest
import user_pb2
import user_pb2_grpc

from shared.logger import setup_logger

log_file = Path(__file__).parent / "logs" / "test_user.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logger = setup_logger("test_user", str(log_file))


@pytest.fixture(scope="module")
def grpc_channel():
    channel = grpc.insecure_channel('localhost:50052')
    yield channel
    channel.close()


@pytest.fixture(scope="module")
def user_stub(grpc_channel):
    return user_pb2_grpc.UserServiceStub(grpc_channel)


@pytest.fixture(scope="module")
def test_user(user_stub):
    logger.info("Creating test user")
    response = user_stub.Register(user_pb2.RegisterRequest(
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
        phone="+1234567899"
    ))
    logger.info(f"Created test user with ID: {response.user_id}")
    yield response

    try:
        user_stub.DeleteUser(user_pb2.DeleteUserRequest(user_id=response.user_id))
        logger.info(f"Cleaned up test user ID: {response.user_id}")
    except grpc.RpcError:
        pass


def test_register(user_stub):
    logger.info("Testing Register")
    response = user_stub.Register(user_pb2.RegisterRequest(
        email="newuser@example.com",
        password="password123",
        first_name="New",
        last_name="User",
        phone="+9876543210"
    ))

    assert response.user_id > 0
    assert response.email == "newuser@example.com"
    assert response.first_name == "New"
    assert response.status is True
    logger.info(f"Register test passed, user ID: {response.user_id}")

    user_stub.DeleteUser(user_pb2.DeleteUserRequest(user_id=response.user_id))


def test_login(user_stub, test_user):
    logger.info(f"Testing Login for user: {test_user.email}")
    response = user_stub.Login(user_pb2.LoginRequest(
        email=test_user.email,
        password="testpass123"
    ))

    assert response.user.user_id == test_user.user_id
    assert response.user.email == test_user.email
    assert response.token != ""
    logger.info("Login test passed")


def test_login_invalid_password(user_stub, test_user):
    logger.info("Testing Login with invalid password")

    with pytest.raises(grpc.RpcError) as exc_info:
        user_stub.Login(user_pb2.LoginRequest(
            email=test_user.email,
            password="wrongpassword"
        ))

    assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED
    logger.info("Login invalid password test passed")


def test_get_user_by_id(user_stub, test_user):
    logger.info(f"Testing GetUserById for ID: {test_user.user_id}")
    response = user_stub.GetUserById(
        user_pb2.GetUserByIdRequest(user_id=test_user.user_id)
    )

    assert response.user_id == test_user.user_id
    assert response.email == test_user.email
    assert response.first_name == test_user.first_name
    logger.info("GetUserById test passed")


def test_get_user_by_email(user_stub, test_user):
    logger.info(f"Testing GetUserByEmail for email: {test_user.email}")
    response = user_stub.GetUserByEmail(
        user_pb2.GetUserByEmailRequest(email=test_user.email)
    )

    assert response.user_id == test_user.user_id
    assert response.email == test_user.email
    logger.info("GetUserByEmail test passed")


def test_modify_user(user_stub, test_user):
    logger.info(f"Testing ModifyUser for user ID: {test_user.user_id}")
    response = user_stub.ModifyUser(user_pb2.ModifyUserRequest(
        user_id=test_user.user_id,
        data=user_pb2.RegisterRequest(
            email=test_user.email,
            password="",
            first_name="Updated",
            last_name="Name",
            phone="+1111111111"
        )
    ))

    assert response.user_id == test_user.user_id
    assert response.first_name == "Updated"
    assert response.last_name == "Name"
    assert response.phone == "+1111111111"
    logger.info("ModifyUser test passed")


def test_deactivate_user(user_stub):
    logger.info("Testing DeactivateUser")
    create_response = user_stub.Register(user_pb2.RegisterRequest(
        email="deactivate@example.com",
        password="password123",
        first_name="Deactivate",
        last_name="Test",
        phone="+1234567890"
    ))

    response = user_stub.DeactivateUser(
        user_pb2.DeactivateUserRequest(user_id=create_response.user_id)
    )

    assert response.success is True
    logger.info("DeactivateUser test passed")

    user_stub.DeleteUser(user_pb2.DeleteUserRequest(user_id=create_response.user_id))


def test_delete_user(user_stub):
    logger.info("Testing DeleteUser")
    create_response = user_stub.Register(user_pb2.RegisterRequest(
        email="delete@example.com",
        password="password123",
        first_name="Delete",
        last_name="Test",
        phone="+1234567890"
    ))

    response = user_stub.DeleteUser(
        user_pb2.DeleteUserRequest(user_id=create_response.user_id)
    )

    assert response.success is True
    logger.info("DeleteUser test passed")


def test_get_nonexistent_user(user_stub):
    logger.info("Testing GetUserById with nonexistent ID")

    with pytest.raises(grpc.RpcError) as exc_info:
        user_stub.GetUserById(user_pb2.GetUserByIdRequest(user_id=999999))

    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND
    logger.info("GetUserById nonexistent test passed")


def test_register_duplicate_email(user_stub, test_user):
    logger.info("Testing Register with duplicate email")

    with pytest.raises(grpc.RpcError) as exc_info:
        user_stub.Register(user_pb2.RegisterRequest(
            email=test_user.email,
            password="password123",
            first_name="Duplicate",
            last_name="User",
            phone="+1234567890"
        ))

    assert exc_info.value.code() == grpc.StatusCode.ALREADY_EXISTS
    logger.info("Register duplicate email test passed")

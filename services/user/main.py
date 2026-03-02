from concurrent import futures

import grpc
import user_pb2_grpc
from service import UserService

from shared.logger import setup_logger

logger = setup_logger("user", "user.log")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)

    server.add_insecure_port('[::]:50052')
    logger.info("User service starting on port 50052")
    server.start()
    logger.info("User service running on port 50052")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

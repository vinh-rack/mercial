from concurrent import futures

import grpc
import inventory_pb2_grpc
from service import InventoryService

from shared.logger import setup_logger

logger = setup_logger("inventory", "inventory.log")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryService(), server)

    server.add_insecure_port('[::]:50051')
    logger.info("Inventory service starting on port 50051")
    server.start()
    logger.info("Inventory service running on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

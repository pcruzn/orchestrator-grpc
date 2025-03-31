import grpc
from concurrent import futures
import delivery_service_unary_pb2_grpc as pb2_grpc
import delivery_service_unary_pb2 as pb2


class DeliveryServicer(pb2_grpc.DeliveryServiceServicer):
    def deliver_course(self, request, context):
        print("Course delivered!")
        response_map = {"status_code": 20}

        return pb2.DSStatus(**response_map)

    def undeliver_course(self, request, context):
        print("We're sorry, course undelivered! Contact your company for more information.")
        response_map = {"status_code": 10}

        return pb2.DSStatus(**response_map)


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_DeliveryServiceServicer_to_server(DeliveryServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

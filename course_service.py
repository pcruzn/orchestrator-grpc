import grpc
from concurrent import futures
import course_service_unary_pb2_grpc as pb2_grpc
import course_service_unary_pb2 as pb2


class CourseServicer(pb2_grpc.CourseServiceServicer):
    def add_course(self, request, context):
        print(request.user.name, "was successfully added to course", request.course_name)
        response_map = {"status_code": 10}

        return pb2.CSStatus(**response_map)

    def remove_course(self, request, context):
        print(request.user.name, "was successfully removed from course", request.course_name)
        response_map = {"status_code": 10}

        return pb2.CSStatus(**response_map)


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_CourseServiceServicer_to_server(CourseServicer(), server)
    server.add_insecure_port("[::]:50050")
    server.start()
    server.wait_for_termination()

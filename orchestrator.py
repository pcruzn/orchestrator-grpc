import json
import grpc
import delivery_service_unary_pb2_grpc as DSpb2_grpc
import delivery_service_unary_pb2 as DSpb2
import course_service_unary_pb2_grpc as CSpb2_grpc
import course_service_unary_pb2 as CSpb2
from google.protobuf.json_format import MessageToJson


def course_saga():
    # services return a status code: 10 for OK, any other number for failed.
    failed = False
    with (grpc.insecure_channel("localhost:50051") as channel):
        DSstub = DSpb2_grpc.DeliveryServiceStub(channel)

        DSmessage = DSpb2.DSCourseUser(
            id="TF2002",
            course_name="Backend Python",
            user=DSpb2.DSUser(
                id="10101010-2",
                name="Clodomiro",
                email="clodo.silva@survival.com"
            )
        )

        print(f"Message sent:\n{MessageToJson(DSmessage)}\n")

        # call remote method
        DSresponse = DSstub.deliver_course(DSmessage)

        print(f"Message received:\n{MessageToJson(DSresponse)}\n")

        if int(json.loads(MessageToJson(DSresponse))["statusCode"]) != 10:
            failed = True

    with (grpc.insecure_channel("localhost:50050") as channel):
        CSstub = CSpb2_grpc.CourseServiceStub(channel)

        CSmessage = CSpb2.CSCourseUser(
            id="TF2002",
            course_name="Backend Python",
            user=CSpb2.CSUser(
                id="10101010-2",
                name="Clodomiro",
                email="clodo.silva@survival.com"
            )
        )

        print(f"Message sent:\n{MessageToJson(CSmessage)}\n")

        CSresponse = CSstub.add_course(CSmessage)

        print(f"Message received:\n{MessageToJson(CSresponse)}\n")

        if int(json.loads(MessageToJson(CSresponse))["statusCode"]) != 10:
            failed = True

    return failed


# called just in case the saga fails at some point
def saga_compensating_transaction():
    with (grpc.insecure_channel("localhost:50051") as channel):
        DSstub = DSpb2_grpc.DeliveryServiceStub(channel)

        DSmessage = DSpb2.DSCourseUser(
            id="TF2002",
            course_name="Backend Python",
            user=DSpb2.DSUser(
                id="10101010-2",
                name="Clodomiro",
                email="clodo.silva@survival.com"
            )
        )

        print(f"Message sent:\n{MessageToJson(DSmessage)}\n")

        # call remote method
        DSresponse = DSstub.undeliver_course(DSmessage)

        print(f"Message received:\n{MessageToJson(DSresponse)}\n")

    with (grpc.insecure_channel("localhost:50050") as channel):
        CSstub = CSpb2_grpc.CourseServiceStub(channel)

        CSmessage = CSpb2.CSCourseUser(
            id="TF2002",
            course_name="Backend Python",
            user=CSpb2.CSUser(
                id="10101010-2",
                name="Clodomiro",
                email="clodo.silva@survival.com"
            )
        )

        print(f"Message sent:\n{MessageToJson(CSmessage)}\n")

        CSresponse = CSstub.remove_course(CSmessage)

        print(f"Message received:\n{MessageToJson(CSresponse)}\n")


if __name__ == "__main__":
    saga_failed = course_saga()

    if saga_failed:
        saga_compensating_transaction()

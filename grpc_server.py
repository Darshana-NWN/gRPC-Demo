import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc

# Mock data
USERS = [
    {"id": i, "name": f"User {i}", "email": f"user{i}@example.com",
     "phone": f"555-000{i}", "address": f"{i} Main St", "city": "CityX",
     "country": "CountryX", "age": 20 + i}
    for i in range(1, 101)
]

class UserServicer(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        user = next((u for u in USERS if u["id"] == request.id), None)
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        return user_pb2.User(**user)

    def ListUsers(self, request, context):
        limit = request.limit if request.limit > 0 else 10
        users = [user_pb2.User(**u) for u in USERS[:limit]]
        return user_pb2.ListUsersResponse(users=users)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

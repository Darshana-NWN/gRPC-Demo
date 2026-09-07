import time
import requests
import grpc
import user_pb2
import user_pb2_grpc
import json

# Configuration
NUM_REQUESTS = 1000
USER_ID = 42

# REST benchmarks
def benchmark_rest():
    times = []
    total_bytes = 0

    url = "http://127.0.0.1:8000"

    # Warmup
    requests.get(f"{url}/user/{USER_ID}")

    start = time.time()
    for _ in range(NUM_REQUESTS):
        resp = requests.get(f"{url}/user/{USER_ID}")
        times.append(resp.elapsed.total_seconds() * 1000)
        total_bytes += len(resp.content)
    end = time.time()

    return {
        "name": "REST",
        "total_time": (end - start) * 1000,
        "avg_time": sum(times) / len(times),
        "total_bytes": total_bytes,
        "avg_bytes": total_bytes / NUM_REQUESTS
    }

# gRPC benchmarks
def benchmark_grpc():
    times = []
    total_bytes = 0

    channel = grpc.insecure_channel("127.0.0.1:50051")
    stub = user_pb2_grpc.UserServiceStub(channel)

    # Warmup
    stub.GetUser(user_pb2.GetUserRequest(id=USER_ID))

    start = time.time()
    for _ in range(NUM_REQUESTS):
        req_time = time.time()
        resp = stub.GetUser(user_pb2.GetUserRequest(id=USER_ID))
        times.append((time.time() - req_time) * 1000)
        total_bytes += len(resp.SerializeToString())
    end = time.time()

    channel.close()

    return {
        "name": "gRPC",
        "total_time": (end - start) * 1000,
        "avg_time": sum(times) / len(times),
        "total_bytes": total_bytes,
        "avg_bytes": total_bytes / NUM_REQUESTS
    }

def print_results(rest_result, grpc_result):
    print("\n" + "="*60)
    print(f"BENCHMARK RESULTS ({NUM_REQUESTS} requests each)")
    print("="*60)

    print(f"\n{'Protocol':<15} {'Total (ms)':<15} {'Avg (ms)':<15} {'Total (KB)':<15} {'Avg (bytes)':<15}")
    print("-"*70)

    for result in [rest_result, grpc_result]:
        print(f"{result['name']:<15} {result['total_time']:<15.2f} {result['avg_time']:<15.4f} "
              f"{result['total_bytes']/1024:<15.2f} {result['avg_bytes']:<15.2f}")

    # Calculate speedup
    speedup = rest_result['avg_time'] / grpc_result['avg_time']
    size_reduction = (1 - grpc_result['avg_bytes'] / rest_result['avg_bytes']) * 100

    print("\n" + "-"*70)
    print(f"gRPC is {speedup:.1f}x faster")
    print(f"gRPC payload is {size_reduction:.1f}% smaller")
    print("="*60 + "\n")

if __name__ == "__main__":
    print(f"Starting benchmark... ({NUM_REQUESTS} requests to GetUser({USER_ID}))")
    print("Make sure REST server (port 8000) and gRPC server (port 50051) are running!")

    try:
        rest_result = benchmark_rest()
        print("✓ REST benchmark complete")
    except Exception as e:
        print(f"✗ REST benchmark failed: {e}")
        exit(1)

    try:
        grpc_result = benchmark_grpc()
        print("✓ gRPC benchmark complete")
    except Exception as e:
        print(f"✗ gRPC benchmark failed: {e}")
        exit(1)

    print_results(rest_result, grpc_result)

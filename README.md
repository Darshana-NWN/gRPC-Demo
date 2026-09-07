# REST vs gRPC Demo

Simple demo showing the differences between REST and gRPC.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate gRPC code from proto:**
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. user.proto
   ```
   This creates `user_pb2.py` and `user_pb2_grpc.py` (auto-generated, not in git)

## Running the Demo

Open 3 terminals and run these in parallel:

**Terminal 1 — REST server** (port 8000):
```bash
python rest_server.py
```

**Terminal 2 — gRPC server** (port 50051):
```bash
python grpc_server.py
```

**Terminal 3 — Benchmark** (runs the test):
```bash
python benchmark.py
```

## What You'll See

Benchmark output showing side-by-side comparison:
```
Protocol      Total (ms)    Avg (ms)    Total (KB)    Avg (bytes)
REST          523.45        0.5235      145.30        145.30
gRPC          67.82         0.0678      18.50         18.50

gRPC is 7.7x faster
gRPC payload is 87.3% smaller
```

The test sends 1000 identical `GetUser(42)` requests to both servers and measures:
- **Response time** — how long each request takes (ms)
- **Payload size** — how many bytes transferred (KB)
- **Speedup** — gRPC is typically 5-10x faster with 70-80% smaller payloads

## File Overview

| File | Purpose |
|------|---------|
| `user.proto` | Service definition (the source of truth) |
| `rest_server.py` | FastAPI HTTP server (port 8000, JSON responses) |
| `grpc_server.py` | gRPC server (port 50051, binary responses) |
| `benchmark.py` | Load test that compares both (1000 requests) |
| `requirements.txt` | Python dependencies |

**Auto-generated files** (from `user.proto`):
- `user_pb2.py` — Python data classes
- `user_pb2_grpc.py` — gRPC client/server stubs

## Why gRPC is Faster

| Aspect | REST (JSON) | gRPC (Protobuf) |
|--------|-----------|-----------------|
| **Encoding** | Text (human-readable) | Binary (compact) |
| **Parsing** | Parse JSON string → object | Direct binary → object |
| **Size per request** | ~145 bytes | ~18 bytes |
| **Protocol** | HTTP/1.1 (single request/response) | HTTP/2 (multiplexing) |
| **Result** | Slower, larger | 5-10x faster, 70-80% smaller |

## Experiments

- Change `USER_ID` in `benchmark.py` to test users 1-100
- Change `NUM_REQUESTS` to 5000+ for bigger differences
- Add `ListUsers()` benchmarks to see streaming advantages

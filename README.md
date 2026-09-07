# REST vs gRPC Demo

Simple demo showing the differences between REST and gRPC.

## Setup

```bash
pip install -r requirements.txt
```

## Running the Demo

1. **Start REST server** (Terminal 1):
   ```bash
   python rest_server.py
   ```
   Server runs on `http://127.0.0.1:8000`

2. **Start gRPC server** (Terminal 2):
   ```bash
   python grpc_server.py
   ```
   Server runs on `127.0.0.1:50051`

3. **Run benchmark** (Terminal 3):
   ```bash
   python benchmark.py
   ```

## What You'll See

The benchmark sends 1000 identical requests to both servers and compares:
- **Response time** (ms)
- **Payload size** (bytes)
- **Speedup** (how much faster gRPC is)

## Why the Differences?

| Aspect | REST (JSON) | gRPC (Protobuf) |
|--------|-----------|-----------------|
| **Format** | Text-based | Binary |
| **Parsing** | Parse JSON string | Direct binary read |
| **Size** | Verbose | Compact |
| **Protocol** | HTTP/1.1 | HTTP/2 |
| **Setup** | Simple | More code |

## Try It!

Modify `USER_ID` in `benchmark.py` to test different users (1-100).

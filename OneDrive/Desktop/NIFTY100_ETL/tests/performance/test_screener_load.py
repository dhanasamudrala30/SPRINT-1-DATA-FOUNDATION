import time
import threading
import requests


URL = "http://127.0.0.1:8000/api/v1/screener"

results = []
lock = threading.Lock()


def make_request(request_number):
    start = time.perf_counter()

    try:
        response = requests.get(
            URL,
            params={"min_roe": 15},
            timeout=10,
        )

        elapsed = time.perf_counter() - start

        with lock:
            results.append({
                "request": request_number,
                "status": response.status_code,
                "time": elapsed,
            })

    except Exception as error:
        elapsed = time.perf_counter() - start

        with lock:
            results.append({
                "request": request_number,
                "status": "ERROR",
                "time": elapsed,
                "error": str(error),
            })


def main():
    threads = []

    overall_start = time.perf_counter()

    for i in range(1, 11):
        thread = threading.Thread(
            target=make_request,
            args=(i,),
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    overall_time = time.perf_counter() - overall_start

    print("=" * 60)
    print("DAY 43 — SCREENER LOAD TEST")
    print("=" * 60)

    for result in sorted(results, key=lambda x: x["request"]):
        print(
            f"Request {result['request']:2d} | "
            f"Status: {result['status']} | "
            f"Time: {result['time']:.3f}s"
        )

    successful = [
        r for r in results
        if r["status"] == 200
    ]

    print("=" * 60)
    print(f"Completed requests : {len(results)}/10")
    print(f"Successful requests: {len(successful)}/10")
    print(f"Total elapsed time : {overall_time:.3f}s")

    if successful:
        avg_time = sum(
            r["time"] for r in successful
        ) / len(successful)

        max_time = max(
            r["time"] for r in successful
        )

        print(f"Average response   : {avg_time:.3f}s")
        print(f"Slowest response   : {max_time:.3f}s")

    print("=" * 60)

    assert len(results) == 10
    assert len(successful) == 10
    assert overall_time < 10


if __name__ == "__main__":
    main()
import time
import csv
from pathlib import Path
from src.image_annotator import annotate_images

def benchmark(input_dir, output_path, scale=None, trials=1):
    """Benchmark annotation performance and log results."""
    results = None
    times = []
    for _ in range(trials):
        start_time = time.time()
        # Pass only 'scale' images
        results = annotate_images(input_dir, output_path, limit=scale)
        end_time = time.time()
        times.append(end_time - start_time)

    avg_time = sum(times) / len(times)
    per_image = avg_time / len(results) if results else 0
    return len(results), avg_time, per_image

if __name__ == "__main__":
    input_dir = "data/images"
    output_path = "data/image_output.json"

    print("🚀 Running benchmarks...\n")

    scales = [10, 20, 50]
    log_path = Path("data/benchmark_results.csv")

    with open(log_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["num_images", "avg_time_sec", "time_per_image_sec"])

        for scale in scales:
            print(f"🔍 Benchmarking with {scale} images...")
            num_images, avg_time, per_image = benchmark(input_dir, output_path, scale=scale, trials=1)

            writer.writerow([num_images, f"{avg_time:.2f}", f"{per_image:.2f}"])
            print(f"✅ {num_images} images → {avg_time:.2f} sec total "
                  f"({per_image:.2f} sec/image)\n")

    print(f"📊 Benchmark results saved to {log_path}")

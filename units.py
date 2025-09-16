def progress_bar(progress, total):
    percent = (progress / total) * 100
    bar = "#" * int(percent // 2)
    print(f"\r[{bar:<50}] {percent:.2f}%", end="")

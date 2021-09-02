import filecmp

from main import initialize_cpu

result_file = f"result.txt"

for i in range(5):
    j = i+1
    input_file = f"tests/in{j}.txt"
    output_file = f"tests/out{j}.txt"

    initialize_cpu(input_file)

    result = filecmp.cmp(output_file, result_file, shallow=False)
    if result:
        print(f"[SUCCESS] TEST {j} SUCCEEDED. IDENTICAL FILES!")
    else:
        print(f"[FAIL] TEST {j} FAILED. FILES ARE DISTINCT!")

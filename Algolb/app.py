from flask import Flask, render_template, request

app = Flask(__name__)

# ----------- DSA ALGORITHMS ----------- #
def bubble_sort(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            steps.append(arr.copy())
    return steps

def insertion_sort(arr):
    steps = []
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            steps.append(arr.copy())
        arr[j + 1] = key
        steps.append(arr.copy())
    return steps

def selection_sort(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append(arr.copy())
    return steps

def merge_sort(arr):
    steps = []
    def merge_sort_recursive(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort_recursive(arr[:mid])
        right = merge_sort_recursive(arr[mid:])
        return merge(left, right)

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
            steps.append(result + left[i:] + right[j:])
        result.extend(left[i:])
        result.extend(right[j:])
        steps.append(result.copy())
        return result

    merge_sort_recursive(arr)
    return steps

def quick_sort(arr):
    steps = []
    def quick_sort_recursive(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_recursive(arr, low, pi - 1)
            quick_sort_recursive(arr, pi + 1, high)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append(arr.copy())
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append(arr.copy())
        return i + 1

    quick_sort_recursive(arr, 0, len(arr) - 1)
    return steps

def radix_sort(arr):
    steps = []
    def counting_sort(exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        for i in range(n):
            index = arr[i] // exp
            count[index % 10] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        i = n - 1
        while i >= 0:
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            i -= 1
        for i in range(n):
            arr[i] = output[i]
            steps.append(arr.copy())

    max1 = max(arr)
    exp = 1
    while max1 // exp > 0:
        counting_sort(exp)
        exp *= 10
    return steps

# ----------- ROUTES ----------- #
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualize', methods=['POST'])
def visualize():
    algo = request.form['algorithm']
    user_input = request.form['array']

    try:
        arr = list(map(int, user_input.split(',')))
    except:
        return render_template('result.html', steps=["❌ Invalid input. Please enter integers separated by commas."], algo="Error")

    if algo == 'bubble_sort':
        steps = bubble_sort(arr)
    elif algo == 'insertion_sort':
        steps = insertion_sort(arr)
    elif algo == 'selection_sort':
        steps = selection_sort(arr)
    elif algo == 'merge_sort':
        steps = merge_sort(arr)
    elif algo == 'quick_sort':
        steps = quick_sort(arr)
    elif algo == 'radix_sort':
        steps = radix_sort(arr)
    else:
        steps = ['❌ Algorithm not implemented yet']

    return render_template('result.html', steps=steps, algo=algo)

import os

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

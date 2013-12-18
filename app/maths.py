def sign(x):
    return -1.0 if x < 0.0 else 1.0

def clamp(x, x1, x2):
    return min(max(x, x1), x2)

# Credit to dgc on Stack Overflow
# https://stackoverflow.com/a/31125282

import math

# A map of rgb points in your distribution
# [distance, (r, g, b)]
# distance is percentage from left edge
heatmap = [
    [0.0, (42 / 255, 187 / 255, 194 / 255)],  # 2abbc2
    [0.35, (203 / 255, 214 / 255, 18 / 255)],  # cbd612
    [0.70, (238 / 255, 139 / 255, 24 / 255)],  # ee8b18
    [1.00, (255 / 255, 0 / 255, 0 / 255)],  # ff0000
]  # linear-gradient(90deg, rgba(42,187,194,1) 0%, rgba(203,214,18,1) 35%, rgba(238,139,24,1) 70%, rgba(255,0,0,1) 100%);


def gaussian(x, a, b, c, d=0):
    return a * math.exp(-((x - b) ** 2) / (2 * c ** 2)) + d


def pixel(x, width=100, map=[], spread=1):
    width = float(width)
    r = sum([gaussian(x, p[1][0], p[0] * width, width / (spread * len(heatmap))) for p in heatmap])
    g = sum([gaussian(x, p[1][1], p[0] * width, width / (spread * len(heatmap))) for p in heatmap])
    b = sum([gaussian(x, p[1][2], p[0] * width, width / (spread * len(heatmap))) for p in heatmap])
    return min(1.0, r), min(1.0, g), min(1.0, b)

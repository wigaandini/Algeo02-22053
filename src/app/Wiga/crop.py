import numpy as np

def get_stacked_histograms(data1, data2, data3, bins=30):
    """
    Compute stacked histograms for three sets of data.

    Parameters:
    - data1, data2, data3 (array-like): The data for each histogram.
    - bins (int, optional): Number of bins in the histogram. Default is 30.

    Returns:
    - hist1, bin_edges1 (tuple): Histogram values and bin edges for data1.
    - hist2, bin_edges2 (tuple): Histogram values and bin edges for data2.
    - hist3, bin_edges3 (tuple): Histogram values and bin edges for data3.
    """
    hist1, bin_edges1 = np.histogram(data1, bins=bins)
    hist2, bin_edges2 = np.histogram(data2, bins=bins)
    hist3, bin_edges3 = np.histogram(data3, bins=bins)

    return (hist1, bin_edges1), (hist2, bin_edges2), (hist3, bin_edges3)

# Example usage:
# Replace data1, data2, and data3 with your own data
data1 = np.random.randn(1000)
data2 = np.random.randn(1000) + 3
data3 = np.random.randn(1000) - 3

histogram_values = get_stacked_histograms(data1, data2, data3)

# Access the histogram values and bin edges for each dataset
hist1, bin_edges1 = histogram_values[0]
hist2, bin_edges2 = histogram_values[1]
hist3, bin_edges3 = histogram_values[2]

print(f"Histogram 1 values: {hist1}")
print(f"Histogram 1 bin edges: {bin_edges1}")

print(f"Histogram 2 values: {hist2}")
print(f"Histogram 2 bin edges: {bin_edges2}")

print(f"Histogram 3 values: {hist3}")
print(f"Histogram 3 bin edges: {bin_edges3}")

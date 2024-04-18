import numpy as np
import portion as P



def cleanNumericalValues(values: list) -> list:
    return [value for value in values if isinstance(value, (int, float))]



def categorizeCuantile(values : list = [],
                       value: float = 0,
                       cuantiles: list = [],
                       tag: str = ""):

    values = cleanNumericalValues(values)

    if len(cuantiles) > 1:
        intervals = [P.open(-P.inf, np.percentile(values, cuantiles[0]))] +\
                    [P.closedopen(np.percentile(values, left),
                                  np.percentile(values, right)) \
                     for left, right in zip(cuantiles[:-1],
                                            cuantiles[1:])] +\
                    [P.closedopen(np.percentile(values, cuantiles[-1]), P.inf)]
    else:
        intervals = [P.open(-P.inf, np.percentile(values, cuantiles[0])),
                     P.closedopen(np.percentile(values, cuantiles[0]), P.inf)]

    for index, interval in enumerate(intervals):

        if value in interval:
            return f"{tag}_{index}to{index + 1}"



def categorizeMedian(values: list, value: float) -> str: return categorizeCuantile(values, value, [50], "median")
def categorizeTertile(values: list, value: float) -> str: return categorizeCuantile(values, value, [33.3, 66.6], "tertile")
def categorizeQuartile(values: list, value: float) -> str: return categorizeCuantile(values, value, [25, 50, 75], "quartile")
def categorizeQuintile(values: list, value: float) -> str: return categorizeCuantile(values, value, [20, 40, 60, 80], "quintile")
def categorizeSextile(values: list, value: float) -> str: return categorizeCuantile(values, value, [16.6, 33.3, 50, 66.6, 83.3], "sextile")
def categorizeSeptile(values: list, value: float) -> str: return categorizeCuantile(values, value, [14.2, 28.5, 42.8, 57.1, 71.4, 85.7], "septile")
def categorizeOctile(values: list, value: float) -> str: return categorizeCuantile(values, value, [12.5, 25, 37.5, 50, 62.5, 75, 87.5], "octile")
def categorizeDecile(values: list, value: float) -> str: return categorizeCuantile(values, value, [10, 20, 30, 40, 50, 60, 70, 80, 90], "decile")

def calculateMinimum(values: list) -> float: return np.min(cleanNumericalValues(values))
def calculateMaximum(values: list) -> float: return np.max(cleanNumericalValues(values))
def calculateMedian(values: list) -> float: return np.median(cleanNumericalValues(values))
def calculateMean(values: list) -> float: return np.mean(cleanNumericalValues(values))
def calculateMode(values: list) -> float: return np.mode(cleanNumericalValues(values))
def calculateVariance(values: list) -> float: return np.var(cleanNumericalValues(values))
def calculateStandardDeviation(values: list) -> float: return np.std(cleanNumericalValues(values))
def calculateSkewness(values: list) -> float: return np.skew(cleanNumericalValues(values))
def calculateKurtosis(values: list) -> float: return np.kurtosis(cleanNumericalValues(values))
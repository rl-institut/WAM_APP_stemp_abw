// Get color and step values as associated array
function getColorValues(schema, min, max, step, reverse) {

    // Get the sum of steps by step (interval)
    var sumSteps = parseInt((max - min) / step);
    // Get dividable interval step from steps
    // This is necessary, if "((max - min) / step)" produced rest
    var stepInterval = (max - min) / sumSteps;

    // Get colors for schema
    var colors = chroma.scale(schema).colors(sumSteps + 1);

    // Reverse colors if reverse value is true
    if (reverse == "true") {
        colors = colors.reverse();
    }

    // Combine colors and values of step intervals
    var colorsAndStepValues = {};
    colorsAndStepValues['values'] = [];
    var base = min;
    for (var i = 0; i < colors.length; i++) {
        colorsAndStepValues['values'][parseInt(base)] = colors[i];
        base = parseFloat(base) + stepInterval;
    }

    // Add max value
    colorsAndStepValues['max'] = max;

    return colorsAndStepValues;
}

// Get explicit color value from associated array and
// supplied averaged value
function getColor(colorVals, averagedValue) {
    for (var stepVal in colorVals['values']) {
        if (averagedValue <= stepVal) {
            return colorVals['values'][stepVal];
        }
        // Check if averageValue exceeds max value.
        if (averagedValue > colorVals['max']) {
            return colorVals['values'][colorVals['max']];
        }
    }
    // No color found - return '#FFFFFF'.
    // This should never happen.
    return '#FFFFFF';
}

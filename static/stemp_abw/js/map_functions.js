// Get color and step values as associated array
function getColorValues(schema, min, max, step, reverse) {

    // Convert to floats
    min = parseFloat(min);
    max = parseFloat(max);
    step = parseFloat(step);

    // Get number if digits to round resulting range values below
    var numberOfDigits = Math.ceil(Math.log(step + 1) / Math.LN10);

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
        colorsAndStepValues['values'][parseFloat(base)] = colors[i];
        base = parseFloat((parseFloat(base) + stepInterval).toFixed(numberOfDigits));
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

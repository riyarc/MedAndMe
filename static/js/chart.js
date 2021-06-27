(function () {
  // Get a data set.  10 points.
  function _getData () {
    return d3.range(10).map(function(i) {return _getDataPoint(i)})
  }

  // Get a single point of data.
  function _getDataPoint(i) {
    return {x: i/10, y: (Math.random(i/3) + 1) / 2}
  }

  // Slide a point to the left.
  function _slideDataPoint(datum, i) {
    return {x: (i-1)/10, y:datum.y}
  }

  // Add a data point to the right of the graph and slide the line to the
  // left.
  function addData() {
    // Grab the path
    var path = d3.select("path")
    // Grab the data from the path
    var data = path[0][0].__data__

    // Slap a new random point to the end of the data
    data.push(_getDataPoint(data.length))
    // Get rid of the first point
    // data.shift()

    // Adjust the X value for each point
    for (i = 0; i < data.length; i++) {
      data[i] = _slideDataPoint(data[i], i)
    }

    // Apply the new data to the path and re-draw. 
    path
      .data([data])
      .transition()
        .duration(1000)
        // Use a linear easing to keep an even scroll
        .ease("linear")
        .attr("d", d3.svg.line()
          .x(function(d) {return x(d.x)})
          .y(function(d) {return y(d.y)})
          // I'm not sure if this is the interpolation that works best, but I
          // can't find a better one...
          .interpolate("basis")
        )   

  }

function updateLine() {
addData();
data.shift();
}

  // Set up the parameters of the chart object.
  var width = 550,
      height = 275,
      x = d3.scale.linear().domain([0, 1]).range([0, width]),
      y = d3.scale.linear().domain([0, 1]).range([height, 0]);

  // Create the chart in its initial state
  d3.select("body")
    .data([_getData()])
    .append("svg:svg")
      .attr("width",  width)
      .attr("height", height)
    .append("svg:path")
      .attr("class", "line")
      .attr("d", d3.svg.line()
        .x(function(d) { return x(d.x); })
        .y(function(d) { return y(d.y); })
        .interpolate("basis")
      );

  // Add a new data point every second.
  window.setInterval(updateLine, 1000)

})()
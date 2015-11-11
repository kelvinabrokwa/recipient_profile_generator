/* eslint camelcase: [0] */
var fs = require('fs');
var path = require('path');
var jsdom = require('jsdom');
var xmlserializer = require('xmlserializer');
var Promise = require('promise');
var fetchRecipients = require('./fetch_recipients');

fetchRecipients()
  .then(generateRandomData)
  .then(writeChartToDisk)
  .catch(function(err) { console.log(err); });

function generateRandomData() {
  return new Promise(function(resolve) {
    resolve({});
  });
}

function writeChartToDisk(i, data) {
  if (!i) i = 0;
  jsdom.env({
    features: { QuerySelector: true },
    html: '<!DOCTYPE html>',
    script: [ 'http://d3js.org/d3.v3.min.js' ],
    done: function(err, window) {
      if (err) return;
      var svg = getChart(window, data[i]);
      fs.writeFileSync(
        path.join(__dirname, '..', 'graphics', 'spider.svg'),
        xmlserializer.serializeToString(svg),
        { encoding: 'utf-8' }
      );
      if (i < data.length) writeChartToDisk(++i);
    }
  });
}

function getChart(window, data) {

  var d3 = window.d3;
  //var PX_RATIO = 4 / 3;

  data = d3.range(16).map(function(i) {
    return { type: i };
  });

  var w = 600,
      h = 600;

  var PI = Math.PI;
  var n = data.length;

  var COLOR = '#161f34';

  var CENTER_CIRCLE_RADIUS = 100;
  var CHILD_RADIUS = 30;

  var svg = d3.select('body').append('svg')
    .attr('width', w)
    .attr('height', h);

  svg.append('g').selectAll('line')
      .data(data)
    .enter().append('svg:line')
      .attr('class', 'child')
      .attr('x1', w / 2)
      .attr('y1', h / 2)
      .attr('x2', function(d, i) {
        // draw to the edge of the outer circles
        var angle = (2 * PI / n) * i;
        var x1 = w / 2;
        var y1 = h / 2;
        var x2 = Math.cos((2 * PI / n) * i) * 200 + (h / 2) - Math.cos(100);
        var y2 = Math.sin((2 * PI / n) * i) * 200 + (h / 2) - Math.sin(100);
        var dist = Math.sqrt(Math.pow((x1 - x2), 2) + Math.pow((y1 - y2), 2));
        var radius = CHILD_RADIUS;
        var hypo = dist - radius;
        var x = x1 + hypo * Math.cos(angle);
        return x;
      })
      .attr('y2', function(d, i) {
        // draw to the edge of the outer circles
        var angle = (2 * PI / n) * i;
        var x1 = w / 2;
        var y1 = h / 2;
        var x2 = Math.cos((2 * PI / n) * i) * 200 + (h / 2) - Math.cos(100);
        var y2 = Math.sin((2 * PI / n) * i) * 200 + (h / 2) - Math.sin(100);
        var dist = Math.sqrt(Math.pow((x1 - x2), 2) + Math.pow((y1 - y2), 2));
        var radius = CHILD_RADIUS;
        var hypo = dist - radius;
        var y = y1 + hypo * Math.sin(angle);
        return y;
      })
      .attr('stroke', '#000')
      .attr('stroke-width', 2);

  svg.append('g').append('circle')
    .attr('cx', w / 2)
    .attr('cy', h / 2)
    .attr('r', CENTER_CIRCLE_RADIUS)
    .attr('fill', COLOR);

  svg.append('g').selectAll('circle.child')
      .data(data)
    .enter().append('svg:circle')
      .attr('class', 'child')
      .attr('cx', function(d, i) { return Math.cos((2 * PI / n) * i - PI / 2) * 200 + (w / 2); })
      .attr('cy', function(d, i) { return Math.sin((2 * PI / n) * i - PI / 2) * 200 + (h / 2); })
      .attr('r', CHILD_RADIUS)
      .attr('fill', COLOR)
      .attr('opacity', function(d, i) { return 1 - (0.5 * (i / n)); });

  svg.append('g').selectAll('.label')
      .data(data)
    .enter().append('text')
      .attr('x', function(d, i) { return Math.cos((2 * PI / n) * i - PI / 2) * 200 + (w / 2); })
      .attr('y', function(d, i) { return Math.sin((2 * PI / n) * i - PI / 2) * 200 + (h / 2); })
      .text(function(d) { return d.type; });

  svg.append('g')
    .append('text')
      .text('Influence in Addressing')
      .attr('x', w / 2)
      .attr('y', h / 2);
  svg.append('g')
    .append('text')
      .text('Different Problem Areas')
      .attr('x', w / 2)
      .attr('y', 20 + h / 2);

  d3.selectAll('text')
    .style('fill', '#fff')
    .style('font-family', 'Open Sans')
    .style('text-anchor', 'middle');

  return window.document.getElementsByTagName('svg')[0];
}


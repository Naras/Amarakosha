sentence = sessionStorage.getItem("sentence"); // "रामः गच्छति";
// sentence = "रामः अर्घ्येण ऋषिं पूजयति ।";
document.getElementById("sentence").innerHTML = sentence;
// graphs_string = document.getElementById("graphs_string");
graphs = sessionStorage.getItem("graphs");
// graphs = graphs_string.innerHTML; 
graphs_parsed = JSON.parse(graphs);
// graphs_string.parentNode.removeChild(graphs_string);
// console.log("JSON parsed", typeof graphs_parsed, graphs_parsed);
no = -1;
drawGraphs(graphs_parsed);
  
function drawGraphs(graphs) {
  graphs.forEach(graph => {
    no += 1; 
    // graph = graphs[no]; //console.log(no, graph);

  var svg = d3.select("svg"),
      width = +svg.attr("width") + no * 400,
      height = +svg.attr("height");

var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));

var link = svg.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
    .attr("stroke-width", 2)
    ;

var node = svg.append("g")
    .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
    .enter().append("circle").attr("r", 10).call(d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended))
    ;
  
var nodelabel = svg.append("g")
    .selectAll("text")
    .data(graph.nodes)
    .enter().append("text")
    .text(function(d) { return d.id; })
    .attr("class", "nodelabel")
    ;

nodelabel
    .style("text-anchor", "end");


node.append("title").text(function(d) { if (d.role=="Verb") result = d.purusha + "\n" + d.vacana; else result = d.linga + "\n" + d.vibhakti + "\n" + d.vacana; return result; });

var linklabel = svg.append("g")
    .selectAll("text")
    .data(graph.links)
    .enter().append("text")
    .text(function(d) { return d.key; })
    .attr("class", "linklabel")

linklabel
    .style("text-anchor", "middle");


simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .distance(150)
      .links(graph.links);

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
    
    nodelabel
        .attr("x", function(d) { return d.x; })
        .attr("y", function (d) { return d.y; });
    
    linklabel
        .attr("x", function(d) { return (d.source.x + d.target.x) / 2; })
        .attr("y", function (d) { return (d.source.y + d.target.y) / 2; });
  }

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}
 }); // forEach
}

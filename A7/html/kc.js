
function graph(dataset){
	var w = 960,
		h = 500

	var vis = d3.select("body").append("svg:svg")
		.attr("width", w)
		.attr("height", h);

	d3.json(dataset, function(json) {
		var force = d3.layout.force()
			.nodes(json.nodes)
			.links(json.links)
			.gravity(.05)
			.distance(100)
			.charge(-200)
			.size([w, h])
			.start();

		var link = vis.selectAll("line.link")
			.data(json.links)
		  .enter().append("svg:line")
			.attr("class", "link")
            .style("stroke-width", function(d) { return Math.sqrt(d.weight); });

		var node = vis.selectAll("g.node")
			.data(json.nodes)
		  .enter().append("svg:g")
			.attr("class", "node")
			.call(force.drag);

		node.append("circle")
			.attr("r", function(d) { return d.size; })
			.style("fill", "steelblue");

		node.append("svg:text")
			.attr("class", "nodetext")
			.attr("dx", 16)
			.attr("dy", ".35em")
                        .text(function(d) { return d.id });
			
				  
		force.on("tick", function() {
		  link.attr("x1", function(d) { return d.source.x; })
			  .attr("y1", function(d) { return d.source.y; })
			  .attr("x2", function(d) { return d.target.x; })
			  .attr("y2", function(d) { return d.target.y; });

		  node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
		});
	});
}

function chooseClub(){
  var dataset = "kc.json";
  d3.select("svg")
       .remove();
  myGraph = graph(dataset);
  }
function chooseSplit(){
  var dataset = "split.json";
  d3.select("svg")
       .remove();
  myGraph = graph(dataset);
  }  
 
var dataset = "kc.json";
var myGraph = graph(dataset);


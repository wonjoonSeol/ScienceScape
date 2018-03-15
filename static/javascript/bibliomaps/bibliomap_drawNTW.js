function drawNTW(nodeA, linkA, what, where, thrN, thrL, moduleForce){

  var nodeArray=nodeA.filter(function(d){return d.size>thrN})
  var linkArray=linkA.filter(function(d){return (d.source.size>thrN && d.target.size>thrN && d.weight >thrL)})

  // attribute to each nodes the filtered links
  linkArray.forEach(function(d){ 
      sourceNode = nodeArray.filter(function(n) { return n.name === d.source.name; })[0];
      targetNode = nodeArray.filter(function(n) { return n.name === d.target.name; })[0];
      sourceNode.links.push(targetNode.name);
      targetNode.links.push(sourceNode.name); 
  })
  // remove nodes without links
  nodeArray=nodeArray.filter(function(d){return d.links.length>0})
  d3.select("#coocnetwkompt").html(nodeArray.length+" out of the "+(nodeA.length>95?'top 100':nodeA.length))
  d3.select("#coocnetwkomptB").html((nodeA.length>95?'top 100':''))

	var WIDTH=d3.select(where).node().getBoundingClientRect().width
	var HEIGHT=d3.select(where).node().getBoundingClientRect().height
	var activeNode=undefined;


  // Variables keeping graph state
  var currentOffset = { x : 0, y : 0 };
  var currentZoom = 1.0;
  var SHOW_THRESHOLD=1.05;

	// The D3.js scales
	var xScale = d3.scale.linear()
	  .domain([0, WIDTH])
	  .range([0, WIDTH]);
	var yScale = d3.scale.linear()
	  .domain([0, HEIGHT])
	  .range([0, HEIGHT]);
	var zoomScale = d3.scale.linear()
	  .domain([1,6])
	  .range([1,6])
	  .clamp(true);

  // A scale for node radius
  var sizemax=Math.max.apply( null, nodeArray.map( function(n) {return n.size;} ) );  
  var node_size = d3.scale.pow().exponent(0.5)
    .domain([1, sizemax])
    .range([2,20])
    .clamp(true);

  // A scale for edge width
  var linkmax=Math.max.apply( null, linkArray.map( function(n) {return n.weight;} ) );
  var edge_width = d3.scale.pow().exponent(1)
    .domain([0, (0.1*linkmax+0.9)])
    .range([0.2, 4])
    .clamp(true);

  // colors
  var color = d3.scale.category20().domain(d3.range(30)); 

  // positions
  nodeArray.forEach(function(n){n.x=Math.floor(Math.random() * 100)*WIDTH/100; n.y=Math.floor(Math.random() * 100)*HEIGHT/100;})

  // start force
  var force = d3.layout.force()
  SGcharge=50000*moduleForce*linksArray.length/Math.pow(nodeArray.length,3)
  force
    .gravity(0.2)
    .charge(-SGcharge)
    .distance(20)
    .size( [WIDTH, HEIGHT] )
    .nodes(nodeArray)
    .links(linkArray)
    .linkStrength(function(link) { return (5*link.weight/ linkmax);})
    .start()


  //-------------------------------
  // COMMUNITY
  //-------------------------------
  var node_data = nodeArray.map(function (d) {return d.name});
  var edge_data = linkArray.map(function (d) {return {source: d.source.name, target: d.target.name, weight: d.weight}; });
  var community = jLouvain().nodes(node_data).edges(edge_data);
  var result  = community();
  nodeArray.forEach(function (n) {
    n.group = result[n.name]
  });


  /* --------------------------------------------------------------------- */
  /* ----------------- DRAW NTW ------------------------------------------ */
  /* --------------------------------------------------------------------- */ 
	d3.select(where).selectAll("svg").remove();
	var svg = d3.select(where).append("svg")
	  .attr('xmlns','http://www.w3.org/2000/svg')
	  .attr("width", WIDTH)
	  .attr("height", HEIGHT)
	  .attr("id",what+"_graph")
	  .attr("viewBox", "0 0 " + WIDTH + " " + HEIGHT )
	  .attr("preserveAspectRatio", "xMidYMid meet")
	  .style("background-color", "white") //"#f4f4f4"

    var networkGraph = svg.append('svg:g').attr('class', what+'grpParent');

    // links: simple lines
    var graphLinks = networkGraph.append('svg:g')//.attr('class','grp gLinks')
      .selectAll("line")
      .data(linkArray)
      .enter().append("line")
      .attr('id', function(d) { return what+"_e" + d.source.name + '-' + d.target.name; } )
      .style('stroke-width', function(d) {return edge_width(d.weight);} )
      .attr("class", "link");

    // nodes: an SVG circle
    var graphNodes = networkGraph.append('svg:g')//.attr('class','grp gNodes')
      .selectAll("circle")
      .data( nodeArray, function(d){return d.name} )
      .enter().append("svg:circle")
      .attr('id', function(d) { return what+"_c" + d.name; } )
      .attr('r', function(d) { return node_size(d.size); } )
      .style("fill", function(d){return color(d.group)})
      .attr('pointer-events', 'all')  
      .on("mouseover", function(d) { highlightGraphNode(d,true,this);})
      .on("mouseout", function(d) { highlightGraphNode(d,false,this);  })
      .call(force.drag);

    // labels: a group with two SVG text: a title and a shadow (as background)
    var graphLabels = networkGraph.append('svg:g').attr('class','grp gLabel')
      .selectAll("g.label")
      .data( nodeArray, function(d){return d.name} )
      .enter().append("svg:g")
      .attr('id', function(d) { return what+"_l" + d.name; } )
      .attr('class','label');
   
    /*var shadows = graphLabels.append('svg:text')
      .attr('text-anchor','middle')
      .attr('pointer-events', 'none') // they go to the circle beneath
      .attr('id', function(d) { return what+"_lb" + d.name; } )
      .attr('class','nshadow')
      .text( function(d) { return d.label; } );*/

    var labels = graphLabels.append('svg:text')
      .attr('text-anchor','middle')
      .attr('pointer-events', 'none') // they go to the circle beneath
      .attr('id', function(d) { return what+"_lf" + d.name; } )
      .attr('class','nlabel')
      .style('font-size', function(d){ return (0.4+0.5*Math.pow(d.size/sizemax,0.5))+"vw"})
      .text( function(d) { return d.label; } );

    svg.call(
    	d3.behavior.zoom()
         .x(xScale)
         .y(yScale)
         .scaleExtent([1, 2])
         .on("zoom", doZoom) 
        )
    .on("dblclick.zoom", null);  

    /* --------------------------------------------------------------------- */
    /* ----------------- HIGHLIGHT ----------------------------------------- */
    /* --------------------------------------------------------------------- */ 
    function highlightGraphNode( node, on ){ 
      /* Select/unselect a node in the network graph.
       Parameters are: 
       - node: data for the node to be changed,  
       - on: true/false to show/hide the node */
      
      // If we are to activate a cluster, and there's already one active, first switch that one off  
      if( on && activeNode !== undefined ) { highlightGraphNode( activeNode, false );}

      // opacity low for everybody (will be put higher for selected node and siblings below)
      opac=on?0.35:1
      nodeArray.forEach(function(d){d3.select("#"+what+"_c"+d.name).style("opacity", opac);})
      nodeArray.forEach(function(d){d3.select("#"+what+"_l"+d.name).style("opacity", (on?0:0.5));})
      linkArray.forEach(function(d){d3.select("#"+what+"_e"+d.source.name+"-"+d.target.name).style("opacity", opac)})

      // locate the SVG nodes: circle & label group
      circle = d3.select( '#'+what+'_c' + node.name );
      label  = d3.select( '#'+what+'_l' + node.name );

      // activate/deactivate the node itself
      circle.classed( 'main', on ).style("opacity", 1);
      label.style("opacity", on?1:0.5);
      label.classed( 'on', on || currentZoom >= SHOW_THRESHOLD );
      label.selectAll('text').classed( 'main', on );

      // activate all siblings
      Object(node.links).forEach( function(nm) {
        //.. circle      
        d3.select("#"+what+"_c"+nm).classed( 'sibling', on ).style("opacity", 1);
        //.. labels
        label = d3.select('#'+what+'_l'+nm);
        label.style("opacity", on?0.8:0.5)
        label.classed( 'on', on || currentZoom >= SHOW_THRESHOLD );
        label.selectAll('text.nlabel').classed( 'sibling', on );
        label.selectAll('text.nshadow').classed( 'nshadowB', on );
        //.. links  
        d3.select("#"+what+"_e"+node.name+'-'+nm).classed('linking', on).style("opacity", 1)
        d3.select("#"+what+"_e"+nm+'-'+node.name).classed('linking', on).style("opacity", 1)
      })      

      // set the value for the current active cluster
      activeNode=on?node:undefined;
    }

    /* --------------------------------------------------------------------- */
    /* ----------------- REPOSITION (DRAG / ZOOM / FORCE) ------------------ */
    /* --------------------------------------------------------------------- */ 
    function repositionGraph( off, z, mode ) {
      
      // drag: translate to new offset
      if( off !== undefined && (off.x != currentOffset.x || off.y != currentOffset.y ) ) {
        g = d3.select('g.'+what+'grpParent')
          g.attr("transform", function(d) { return "translate("+off.x+","+off.y+")" } );
          currentOffset.x = off.x;
          currentOffset.y = off.y;
      }
 
      // zoom: get new value of zoom
      if( z === undefined ) {
        if( mode != 'tick' )
          return;   // no zoom, no tick, we don't need to go further
        z = currentZoom;
      }
      else
        currentZoom = z;
        // prep matrice of transform
        za=z;zb=0;zc=0;
        zd=0;ze=z;zf=0;
        //.. rotation
        myROT=0;
        myHSYM=0;
        myVSYM=0;
        za=z*Math.cos(myROT*Math.PI/180);
        zb=z*Math.sin(myROT*Math.PI/180);
        zc=z*WIDTH/2*(1-Math.cos(myROT*Math.PI/180))-z*HEIGHT/2*Math.sin(myROT*Math.PI/180);
        zd=-z*Math.sin(myROT*Math.PI/180);
        ze=z*Math.cos(myROT*Math.PI/180);
        zf=z*HEIGHT/2*(1-Math.cos(myROT*Math.PI/180))+z*WIDTH/2*Math.sin(myROT*Math.PI/180);
        //..symmetries       
        if (myHSYM%2 ==1){za=-za;zb=-zb;zc=z*WIDTH-zc;}
        if (myVSYM%2 ==1){zd=-zd;ze=-ze;zf=z*HEIGHT-zf;}    
   
        // do transformation
        graphLinks
          .attr("x1", function(d) { return za*(d.source.x)+zb*(d.source.y)+zc; })
          .attr("y1", function(d) { return zd*(d.source.x)+ze*(d.source.y)+zf; })
          .attr("x2", function(d) { return za*(d.target.x)+zb*(d.target.y)+zc; })
          .attr("y2", function(d) { return zd*(d.target.x)+ze*(d.target.y)+zf; });
        graphNodes.attr("transform", function(d) { return "translate("+(za*d.x+zb*d.y+zc)+","+(zd*d.x+ze*d.y+zf)+")" } );
        graphLabels.attr("transform", function(d) { return "translate("+(za*d.x+zb*d.y+zc)+","+(zd*d.x+ze*d.y+zf)+")" } );

    // end function
    }

   // ------------
   // Perform drag
     
    function dragmove(d) {
      offset = { x : currentOffset.x + d3.event.dx, y : currentOffset.y + d3.event.dy };
      repositionGraph( offset, undefined, 'drag' );
    }
  
   // ------------
   // semantic zoom: nodes do not change size, but get spread out or stretched together as zoom changes)
     
    function doZoom( increment ) {
      var newZoom = increment === undefined ? d3.event.scale : zoomScale(currentZoom+increment);
      if( currentZoom == newZoom )
        return;  // no zoom change
      // See if we cross the 'show' threshold in either direction
      if( currentZoom<SHOW_THRESHOLD && newZoom>=SHOW_THRESHOLD )
        svg.selectAll("g.label").classed('on',true);
      else if( currentZoom>=SHOW_THRESHOLD && newZoom<SHOW_THRESHOLD )
        svg.selectAll("g.label").classed('on',false);


      // Compute the new offset, so that the graph center does not move
      var zoomRatio = newZoom/currentZoom;
      var newOffset = { x : currentOffset.x*zoomRatio + WIDTH/2*(1-zoomRatio), y : currentOffset.y*zoomRatio + HEIGHT/2*(1-zoomRatio) }; 

      // Reposition the graph
      repositionGraph( newOffset, newZoom, "zoom" );
    }

    // --------------
    // process events from the force-directed graph 
    force.on("tick", function() {
      repositionGraph(undefined,undefined,'tick');
    });


}

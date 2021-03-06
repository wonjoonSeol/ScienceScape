var graphs = [];

/**
 * Start or Stop force atlas functionality provided by sigma.js
 *
 * @param  {element}    HTML element 
 * @return {void}
 */
function startStopForceAtlas2(element){
	
	var edgeWeight = parseFloat(document.getElementById("edge-weight").value);
	var iterations = parseInt(document.getElementById("iterations").value);
	var gravityValue = parseFloat(document.getElementById("gravity").value);
	var scalingValue = parseFloat(document.getElementById("scaling").value);	
	
	if(!edgeWeight){
		edgeWeight = 0;
	}
	
	if(!iterations){
		iterations = 1;
	}
	
	if(!gravityValue){
		gravityValue = 1;
	}
	
	if(!scalingValue){
		scalingValue = 1;
	}
	
	console.log("Force Atlas 2: edgeWeight: " + edgeWeight + " iterations: "+ iterations +" gravity: " + gravityValue + " scaling: " + scalingValue);
	
	if(graphs.length > 0){
		if (!graphs[0].isForceAtlas2Running()){
		//start spacialization
			for (i=0 ; i<graphs.length; i++) {
				graphs[i].startForceAtlas2({worker: true, barnesHutOptimize: false, iterationsPerRender: iterations, scalingRatio: scalingValue, edgeWeightInfluence: edgeWeight, gravity: gravityValue});
			}
			element.innerHTML="<i class=\"material-icons left\">stop</i>Stop Force Atlas 2";

		} else {
		//stop spatialsation
		for (i = 0 ; i<graphs.length; i++) {
			graphs[i].stopForceAtlas2();
		}
			element.innerHTML="<i class=\"material-icons left\">play_arrow</i>Start Force Atlas 2";
		}
	}

}

/**
 * Rearrage each node coordinates into circle
 *
 * @return {void}
 */
function rearrageIntoCircle() {
	console.log("Rearrange circle pressed");
	if(graphs.length > 0){
		for (i=0 ; i<graphs.length ; i++) {
			var counter = 0;
			var numberOfNodes = graphs[i].graph.nodes().length;
			graphs[i].graph.nodes().forEach(function(n) {
			  n.x = 100 * Math.cos(2 * counter * Math.PI / numberOfNodes);
	    	  n.y = 100 * Math.sin(2 * counter * Math.PI / numberOfNodes);
			  counter++;
	      });
	      graphs[i].killForceAtlas2();
	           graphs[i].refresh();
		}
	}
}

/**
 * Turn on and off edges of produced graph
 *
 * @param {checkbox}    checkbox element
 * @return {void}
 */
function turnOnOffEdges(checkBox) {
	console.log("ToggleEdges pressed: " + checkBox.checked);
	if(graphs.length > 0){
		if (!checkBox.checked) {
			for (i=0 ; i<graphs.length ; i++) {
				graphs[i].settings('drawEdges', false);
				graphs[i].refresh();
			}
		} else {
			for (i=0 ; i<graphs.length ; i++) {
				graphs[i].settings('drawEdges', true);
				graphs[i].refresh();
			}
		}
	}
}



var graphs = [];
function startStopForceAtlas2(element){
	console.log("no. graphs: " + graphs.length)
	if(graphs.length > 0){
		if (!graphs[0].isForceAtlas2Running()){
		//start spacialization
			for (i=0 ; i<graphs.length; i++) {
				graphs[i].startForceAtlas2({worker: true, barnesHutOptimize: false});
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

function rearrageIntoCircle(element) {
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



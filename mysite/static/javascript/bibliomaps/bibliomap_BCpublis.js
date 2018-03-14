/* ---------------------------------------------------------------------------
   (c) BiblioMap, 2017
   Author: Sebastian Grauwin
   website: sebastian-grauwin.com
   --------------------------------------------------------------------------- */


// -------------------------------------------------------------------
// Some initial variables
var layout_option = 'FORCE'
var stuff_to_search = undefined;
var sf = undefined;
var myParam=''
var myHSYM=0
var myVSYM=0
var myROT=0
var stopstart=0
var mycolor='originaltopic'
var heatmapcolor=['#d73027','#f46d43','#fdae61','#fee090','#ffffbf','#e0f3f8','#abd9e9','#74add1','#4575b4']//  from colorBrewer 9-class RdYlBu
var mycolorvalues=[0,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5,1]
var itemfoos={'AU':['Author', 'Most Frequent Authors', 'Authors'], 'K':['Keyword', 'Most Frequent Keywords', 'Keywords'], 'TK':['Title Word', 'Most Frequent Title Words', 'Title Words'], 'S':['Subject', 'Most Frequent Subject Categories', 'Subject Categories'], 'J':['Journal', 'Most Frequent Journal Sources'], 'I':['Institution', 'Most Frequent Institution'], 'C':['Country', 'Most Frequent Countries', 'Countries'], 'R':['Reference', 'Most Frequent References', 'References'], 'RJ':['Ref Source', 'Most Frequent References\' Sources'], 'MRP':['Most Representative Papers', 'Most Representative Papers'], 'MCP':['Most Cited Papers', 'Most Cited Papers'], 'MCAU':['Most Cited Authors', 'Most Cited Authors']}
var searchdict = {}
var input=document.getElementById("MYsearch")
var awesomplete = new Awesomplete(input, { maxItems: 20})
var GLOB=[0,0,0] //  # of nodes, # of links, tot weight in ref states
var RTU={} // records how much time each ref is used
var QQQ = 0;
/*-------------------------------------------------------------------------------------------------------*/
/*-------------------------------------------------------------------------------------------------------*/

function outputPosition (){
  // type "outputPosition();" in the console to get a pop-up giving you the position of the nodes on the screen. Copy paste them in the defaultVAR file if you want to use them as basis for the static version
  console.log(myPos)
}
function outputParam (){
  // type "outputParam();" in the console to get a pop-up giving you some parameters used on the current visualization. Copy paste them in the defaultVAR file if you want to use them as basis for the static version
  alert(myParam)
}

// Get the current size & offset of the browser's viewport window
function getViewportSize( w ) {
    var w = w || window;
    if( w.innerWidth != null ) 
      return { w: w.innerWidth, 
          h: w.innerHeight,
          x : w.pageXOffset,
          y : w.pageYOffset };
    var d = w.document;
    if( document.compatMode == "CSS1Compat" )
      return { w: d.documentElement.clientWidth,
          h: d.documentElement.clientHeight,
          x: d.documentElement.scrollLeft,
          y: d.documentElement.scrollTop };
    else
      return { w: d.body.clientWidth, 
          h: d.body.clientHeight,
          x: d.body.scrollLeft,
          y: d.body.scrollTop};
  }

/*-------------------------------------------------------------------------------------------------------*/
/*-------------------------------------------------------------------------------------------------------*/

// Do the stuff -- to be called after D3.js has loaded
function doBCPviz() {
  // initialize in case of change of corpus
  awesomplete = new Awesomplete(input, { maxItems: 20})
  GLOB=[0,0,0] //  # of nodes, # of links, tot weight in ref states
  RTU={} // records how much time each ref is used

  // search stuff
  sel = '<select id="mysearchfield" style="width:100%;">'
  keepitem.forEach(function(elt){
    sel += '<option value="'+elt+'">'+itemfoos[elt][2]+'</option>'
  })
  sel += '</select>' 
  d3.select("#selectsearchfield").html(sel) 

  // zoom threshold to see labels
  showthr=1.1

  // PREP html string for level and layout options
  thehtml = '<div id="options" class="c_options">'

  // ...fixed or dynamic
  thehtml += '<b style="margin-right:5px;">Select Layout:</b><br/>'
  thehtml += '<span id="FIXED" style="padding:5px;border-top-left-radius:50px;border-bottom-left-radius:50px;" onclick="layout_option=\'FIXED\';updateA()">Static</span>'  
  thehtml += '<span id="FORCE" style="padding:5px;border-top-right-radius:50px;border-bottom-right-radius:50px;" onclick="layout_option=\'FORCE\';updateA()">Dynamic</span></div>'  
  // ... add level and layout controls in the html page
  d3.select("#options").html(thehtml);
  // prep search dict for autocomplete (main update is launch from that fonction)
  uploaditemsforsearch()

}// end of D3ok()

function onlyUnique(value, index, self) { 
    return self.indexOf(value) === index;
}

function uploaditemsforsearch(){
  aux1=['K', 'S', 'C', 'R', 'AU'].filter(function(x){ return keepitem.indexOf(x)>-1})
  //{'K':[], 'TK':[], 'S':[], 'J':[], 'I':[], 'C':[], 'R':[], 'RJ':[], 'MRP':[], 'MCP':[], 'MCAU':[]}
  searchdict={};aux1.forEach(function(x){ searchdict[x]=[] })
  d3.json(datafile,function(data) {
    // read all items
    data.nodes.forEach(function(d){
      aux1.forEach(function(x){ d.stuff[x].forEach(function(elt){searchdict[x].push(elt)}) })
      // record times of used of each R
      d.stuff['R'].forEach(function(elt){
        if (!(elt in RTU)){RTU[elt]=0}
        RTU[elt]+=1
      })
    })
    // remove duplicates
    aux1.forEach(function(x){ searchdict[x]=searchdict[x].filter(onlyUnique) })

    // record references numbers
    GLOB[0]=data.nodes.length
    GLOB[1]=data.links.length
    GLOB[2]=0
    data.links.forEach(function(l){ GLOB[2]+=l.weight})

    // output the number of publis in the network
    d3.select("#Nbc").html(data.nodes.length)

    // put that command in this loop to ensure the parameter have been taken into account (the d3 reading function is asynchronous)
    update();
  })

}

/*-------------------------------------------------------------------------------------------------------*/
/*-------------------------------------------------------------------------------------------------------*/


function update() {  
  // initiate auto complete search form
  awesomplete.list=searchdict[document.getElementById("mysearchfield").value]

  //...FILTERS
  thehtml = '<table>'
  // ... nodes "number of refs" filter
  thehtml += '<tr><td>Min. number of refs nR (node)</td>'
  thehtml += '<td><input type="range" id="NRrange" min="' + NRrange[0] + '" max="' + NRrange[1] + '" value="' + NRrange[2] + '" step="1"/></td>'
  thehtml += '<td style="text-align:right"><span id="theNRrange">'+NRrange[2]+'</span></td></tr>'
  // ... link weight filter
  thehtml += '<tr><td>Min. weight &omega; (link)</td>'
  thehtml += '<td><input type="range" id="Wrange" min="' + Wrange[0] + '" max="' + Wrange[1] + '" value="' + Wrange[2] + '" step="0.01"/></td>'
  thehtml += '<td style="text-align:right"><span id="theWrange">'+Wrange[2]+'</span></td></tr>'
  // ... link NC filter
  thehtml += '<tr><td>Min. number of shared refs (link)'
  thehtml += '<td><input type="range" id="NCrange" min="' + NCrange[0] + '" max="' + NCrange[1] + '" value="' + NCrange[2] + '" step="1"/></td>'
  thehtml += '<td style="text-align:right"><span id="theNCrange">'+NCrange[2]+'</span></td></tr>'
  // ... RTU filter
  thehtml += '<tr><td>Min. RTU (link)'
  thehtml += '<td><input type="range" id="RTUrange" min="' + RTUrange[0] + '" max="' + RTUrange[1] + '" value="' + RTUrange[2] + '" step="1"/></td>'
  thehtml += '<td style="text-align:right"><span id="theRTUrange">'+RTUrange[2]+'</span></td></tr>'
  // ... Dy filter
  if (DYrange[1]>0){
    thehtml += '<tr><td>Max. &Delta;y (link)'
    thehtml += '<td><input type="range" id="DYrange" min="' + DYrange[0] + '" max="' + DYrange[1] + '" value="' + DYrange[2] + '" step="1"/></td>'
    thehtml += '<td style="text-align:right"><span id="theDYrange">'+DYrange[2]+'</span></td></tr>'
  }
  //
  thehtml += '</table>'
  // ... display % remaining
  thehtml += '<table style="width:100%"><tr><th>% Nodes</th><th>% Links</th><th>% Link weight</th><th>Q</th></tr><tr><td style="text-align:right"><span id="pc_nodes"></span></td><td style="text-align:right"><span id="pc_links"></span></td><td style="text-align:right"><span id="pc_linksW"></span></td><td style="text-align:right"><span id="QQQ"></span></td></tr></table>'

  //
  d3.select("#filters").html(thehtml);

  //...FORCE PARAM
  thehtml = '<table>'
  thehtml+= '<tr><td><i>Gravity force</i></td><td><input id="force_grav" style="width:50px" type="number" min=0 step=0.1 value="'+ forceparam[0] +'" ></td></tr>'
  thehtml+= '<tr><td><i>Repulsive force</i></td><td><input id="force_charge" style="width:50px" type="number"  max=0 step=100 value="'+ forceparam[1] +'" ></td></tr>'
  thehtml+= '<tr><td><i>Typical distance</i></td><td><input id="force_dist" style="width:50px" type="number"  min=0 step=5 value="'+ forceparam[2] +'" ></td></tr>'
  thehtml+= '<tr><td><i>Attractive force proportionnal to link weight</i></td><td><input type="checkbox" id="force_link" style="width:50px" checked></td></tr>'
  thehtml += '</table>'
  d3.select("#forceparam").html(thehtml);

  //... RESET ALL
  d3.select("#reset").html('<button>Default parameters</button>');

  // plot the network
  updateA();

}// end of update


/*-------------------------------------------------------------------------------------------------------*/
/*-------------------------------------------------------------------------------------------------------*/

function updateA(){
  // ... add label selector 
  thehtml = '<select id="mylabel" >'
  thehtml += '<option value="TI" selected>the publication\'s title</option>'
  thehtml += '<option value="J">the journal</option>'
  thehtml += '<option value="1AU">the first author</option>'
  thehtml += '<option value="PY">the publication year</option>' 
  thehtml += '<option value="S">the subject(s)</option>'
  thehtml += '<option value="id">unique identifiers</option>'
  thehtml += '<option value="group">community group</option>'
  thehtml += '</select>'
  d3.select('#selectlabel').html(thehtml) 

  // ... add color selector 
  /*
  thehtml = '<select id="mycolor" >'
  thehtml += '<option value="topic" selected>research topics</option>'
  thehtml += '<optgroup label="Scopus categories">'
  for (k = 0; k < LIST_DISC[level_option].length; k++){
    thehtml += '<option value="DISC'+k+'">% of '+LIST_DISC[level_option][k][0]+'</option>'
  }
  thehtml += '</optgroup>'
  thehtml += '</select>'
  d3.select('#selectcolor').html(thehtml) 
  */

  // close info panel in case it was previously opened
  d3.select('div#clusterInfo').attr('class','panel_off');

  // deal with level and layout options + parameters
  d3.select('span#FIXED').attr('class', (layout_option == 'FIXED')?'active':'')
  d3.select('span#FORCE').attr('class', (layout_option == 'FORCE')?'active':'')

  var minS=0//document.getElementById("Srange").value;
  var minW=0//Math.pow(10,document.getElementById("Wrange").value);
  
  // Some constants for zoom and adjust to screen size
  s = getViewportSize();
  if (s.w > s.h*8/6){
    var WIDTH = 0.95*s.h*8/6; 
    var HEIGHT = 0.95*s.h;
  }
  else {
    var WIDTH = 0.95*s.w; 
    var HEIGHT = 0.95*s.w*6/8;    
  }

  SHOW_THRESHOLD = showthr;

  // Variables keeping graph state
  var activeCluster = undefined;
  var currentOffset = { x : 0, y : 0 };
  var currentZoom = 1.0;
  
  
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

  var color = d3.scale.category20().domain(d3.range(30)); 

  function colorValue(f){
    for (jk = 0; jk < 9; jk++){ 
      if (f>=mycolorvalues[jk] && f<mycolorvalues[jk+1]  ){return (8-jk);}
      if (f===1){return 0;}
    }
  }

  /* ---------------------------------------------------------------------  */


  // Cluster panel: the div into which the cluster details info will be written
  clusterInfoDiv = d3.select("#clusterInfo");

  // Prep content for the Info panel with cluster details.
  function getclusterInfo( n ) {
      //*********
      // info to display on html page
      //*********

      info = '<div>'
      // close button
      info+='<div style="position:fixed; width:30px; margin-left:-15px; margin-top:-11px; padding-bottom:2px; text-align:center; font-size:18px; font-weight:500; color:black; cursor:pointer; background-color: #ddd; border-radius:0 0 3px 0;" onClick="clusterInfoDiv.html(\'\').attr(\'class\',\'panel_off\');">x</div>'

      // general info

      info += '<div class="stuff" style="text-align:right;margin-top:10px;font-size:18px"><b>'+ n.title+'</b></div>'
      info += '<div class="stuff" style="text-align:right;font-size:13px;"><span style="opacity:0.4"><i>Published in</i></span> ' + n.journal + '<br/></div>'
      info += '<div class="stuff" style="text-align:right;font-size:13px;"><span style="opacity:0.4"><i>Type:</span> </i>'+ n.doctype +', <span style="opacity:0.4"><i>Publication year:</i></span> ' + n.year + '<br/></div><br/>'

      // selector
      /*sel = '<select id="myjump" style="width:100%">'
      keepitem.forEach(function(elt){sel += '<option value="'+elt+'">'+itemfoos[elt][2]+'</option>'})
      sel += '</select>'
      info += '<div class="stuff" style=margin-top:5px;font-size:13px"><strong>Jump to:</strong><br/>'+sel+'</div>'
      */

      // all tables
      info += '<div class="stuff" style="font-size:11px;">'
      keepitem.forEach(function(elt){
        // most used items
        if(elt.length<3){info += itemsTablesP(n.stuff[elt], elt, itemfoos[elt][0],itemfoos[elt][2])}
      })
      info += '</div>'         

      // end
      info+='</div>'
    return info;
  }

  //---------------------
  function auxSTS(ee,sts){
    foo=ee.toLowerCase().indexOf(sts);
    if (foo>-1){
      e=ee.substr(0,foo) + '<FONT style="BACKGROUND-COLOR: yellow">'+ ee.substr(foo,sts.length)  + '</FONT>' + ee.substr(foo+sts.length,ee.length)
    }
    else {e=ee}
    return e
  }

  //---------------------

  function itemsTablesP(stuff,acro,txt,txtt) {
    mytable = '<table style="width:100%">'
    mytable+="<tr><th>"+"</th></tr>"
    mytable+="<tr><th>"+txt+"</th></tr>"
    stuff.forEach(function(elt) { 
      ee=(acro==sf)?auxSTS(elt,stuff_to_search):elt
      ee=(acro=='R' && RTU[elt]>=2)?'<strong>'+ee+'</strong>'+'  <span style="color:blue">[RTU='+RTU[elt]+']</span>':ee
      mytable+="<tr><td>"+ee+"</td></tr>"
    })
    mytable += '</table><br/>'
    return mytable
   }

  //---------------------

  function signsymbol(x){
    plus =  '&plus;' //'&#8593;' '&#43' '&gt'; 
    minus = '&minus;' // &#8595;' '&#45' '&lt;';
    neutral = '=' //&#8776;'
    if (x>25){symb=plus+plus+plus}
    if (x>15 && x<=25){symb=plus+plus}
    if (x>5 && x<=15){symb=plus}  
    if (x>-5 && x<5){symb=neutral}
    if (x<-5 && x>=-15){symb=minus}
    if (x<-15 && x>=-25){symb=minus+minus}
    if (x<-25){symb=minus+minus+minus}    
    return symb
}
  
  function itemsTables(stuff,acro,txt,txtt) {
    mytable = '<table style="width:100%">'
    mytable+="<colgroup><col span='1' style='width: 72%;'><col span='1' style='width: 14%;'><col span='1' style='width: 14%;'></colgroup>"
    mytable+='<tr><th colspan="2" align="center" style="font-size:12px;">' + txtt + '</th><th style="text-align:right"><span id="info_'+acro+'" class="infobulle">?</span></th></tr>'
    mytable+="<tr><th>"+txt+"</th><th align='right'>f(%)</th><th align='center'>&sigma;</th></tr>"
    stuff.forEach(function(elt) { 
      ee=(acro==sf)?auxSTS(elt[0],stuff_to_search):elt[0]
      mytable+="<tr><td>"+ee+"</td><td align='right' >"+elt[1]+"</td><td align='center'>"+signsymbol(elt[2])+"</td></tr>"
    })
    mytable += '</table><br/>'
    return mytable
   }

  //---------------------

  function authorsTables(stuff,acro, txt) {
    mytable = '<table style="width:100%">'
    mytable+='<tr><th style="font-size:12px;">'+txt+'<span id="info_'+acro+'" style="float:right;padding:0 0.1em;" class="infobulle">?</span></th></tr>'
    mytable+="<tr><th>Author</th></tr>"
    stuff.forEach(function(elt) { 
      ee=(acro==sf)?ee=auxSTS(elt[0],stuff_to_search):elt[0]
      if (elt[2]>1){pp = ' papers'}
      else {pp = ' paper'}
      mytable+='<tr><td><span class="title"><a href="' + wwwlink(elt[0]) + '" target="new">' + ee + "</a></span><span class='nums'>"+ elt[2] + pp +" / " + elt[1] + " citations</span></td></tr>"      
    })
    mytable += '</table><br/>'
    return mytable
  }

  //---------------------

  function articlesTables(stuff,acro,txt,size) {
    ii=1;aux=true;
    mytable = '<table style="width:100%">'
    mytable+='<tr><th style="font-size:12px;">'+txt+'<span id="info_'+acro+'" style="float:right;padding:0 0.1em;" class="infobulle">?</span></th></tr>'
    mytable+="<tr><th>Paper</th></tr>"
    stuff.forEach(function(elt) { 
      if (aux){
        gg=(acro==sf)?auxSTS(elt[0],stuff_to_search):elt[0]
        ee=(acro==sf)?auxSTS(elt[1],stuff_to_search):elt[1] 
        mytable+='<tr><td><span class="title"><a href="' + wwwlink(elt[0]) + '" target="new">' + gg + "</a> ["+elt[6]+"]</span><br/><span class='source'>" + ee + " in <i>" + elt[2] + " (" + elt[3] + ")</i></span><span class='nums'>In-degree:"+ elt[5]+" ("+(100*elt[5]/size).toFixed(0)+"%), Times Cited:" + elt[4] + "</span></td></tr>"}
      ii+=1;
      if (ii === 11) {aux = false};
    })
    mytable += '</table><br/>'
    return mytable
  }

  function wwwlink(foo) {
    foo="https://scholar.google.com/scholar?hl=com&q="+foo.replace(' ','+');
    return foo
  }
  
  function mostsign(stuff){
    sig=-100;lab='';
    stuff.forEach(function(elt){if (elt[2]>sig){sig=elt[2];lab=elt[0]}
    })
    return lab
  }
  // --------------------------------------------------------------------- 

  d3.json(datafile,
    function(data) {

    // Add to the page the SVG element that will contain the cluster network
    var svg = d3.select("#biblioMap").append("svg")
    var force = d3.layout.force()

    // A scale for node radius 
    var node_size = d3.scale.linear()
      .domain([0, 1])
      .range([1,3])
      .clamp(true);

    //-------------------------------
    // NODES
    //-------------------------------  
    var nodeArray = [];
    function updatenodes(){    
      minNR=parseFloat(document.getElementById("NRrange").value);
      d3.select("#theNRrange").html(minNR)
      nodeArray = data.nodes.filter( function(d) { return (d.stuff.R.length >= minNR )  ; })
      //auxSize = Math.max.apply( null, nodeArray.map( function(n) {return n.size;} ) );

      //-------------------------------
      // POSITIONS
      //-------------------------------
      // read positions in default file
      DefinedPos.forEach(function (p){
        Node = nodeArray.filter(function(n) { return n.name === p[0].toString()  ; });
        if (Node.length > 0 ){
          if (!('myX' in Node[0])){
            Node[0].myX=p[1];
            Node[0].myY=p[2];
          }
        }
      })
      //nodeArray.forEach(function (n){n.myX=0;n.myY=0})

      // extract min / max values
      minX=Math.min.apply( null, nodeArray.map( function(n) {return n.myX;} ) );
      maxX=Math.max.apply( null, nodeArray.map( function(n) {return n.myX;} ) );
      minY=Math.min.apply( null, nodeArray.map( function(n) {return n.myY;} ) );
      maxY=Math.max.apply( null, nodeArray.map( function(n) {return n.myY;} ) );

      // scale for my position
      myposx = d3.scale.linear().domain([minX,maxX]).range([0.15*WIDTH,0.85*WIDTH]).clamp(true);
      myposy = d3.scale.linear().domain([minY,maxY]).range([0.05*HEIGHT,0.95*HEIGHT]).clamp(true);

      // give initial position
      nodeArray.forEach( function(n){n.x=myposx(n.myX); n.y=myposy(n.myY);});
    }
    updatenodes();
    
    //-------------------------------
    // LINKS
    //-------------------------------

    // filter the links (keep only those with kept nodes and weight > minW)
    // and update the nodes' lists of links
    var linkArray = [];
    var edge_width = d3.scale.pow().exponent(1)
    function updatelinks(){
	    linkArray = [];
	    minW=parseFloat(document.getElementById("Wrange").value);
      d3.select("#theWrange").html(minW.toFixed(2))
      minNC=document.getElementById("NCrange").value
      d3.select("#theNCrange").html(minNC)
      minRTU=document.getElementById("RTUrange").value
      d3.select("#theRTUrange").html(minRTU)
      if (DYrange[1]>0){
        maxDY=document.getElementById("DYrange").value
        d3.select("#theDYrange").html(maxDY)
      }
      else{maxDY=0}
      // create empty list of the nodes links
      nodeArray.forEach(function(n){n.links=[];});
      //
	    data.links.forEach(function(e) { 
	      var sourceNode = nodeArray.filter(function(n) { return n.name === e.source; });
	      var targetNode = nodeArray.filter(function(n) { return n.name === e.target; });
        if((sourceNode.length >0) & (targetNode.length >0)){
          if (minRTU>2){
            aux=sourceNode[0].stuff['R'].filter(function(ref){return ((targetNode[0].stuff['R'].indexOf(ref)>-1) && RTU[ref]>=minRTU) })
            auxNC=aux.length
            auxweight=auxNC / Math.sqrt((sourceNode[0].stuff['R'].length * targetNode[0].stuff['R'].length))
          }
          else {auxweight=e.weight; auxNC=e.nc;}
          //
  	      if ( (auxweight > minW) & (auxNC >= minNC) & ( Math.abs(sourceNode[0].year-targetNode[0].year) <=maxDY) ) {
  	        linkArray.push({source: sourceNode[0], target: targetNode[0], weight: auxweight});
  	        sourceNode[0].links.push(targetNode[0].name);
  	        targetNode[0].links.push(sourceNode[0].name);
  	      }
        }
	    }); 

      // filter nodes without links
      nodeArray=nodeArray.filter(function(n){return n.links.length>0})

	    // A scale for edge width
	    edge_width = d3.scale.pow().exponent(1)
	      .domain([0, 1] )
	      .range([0.2, 3])
	      .clamp(true);

	    // redraw network
      force.stop()
	    redraw_graph();
      if (layout_option === 'FIXED'){force.start()}
      if (layout_option === 'FORCE'){
        force.links(linkArray);
        force.start()
        d3.select('#STARTSTOP').style("background-color","#0095D7")
        stopstart=1
      }
      updatecommunity();
    }
    updatelinks();
    d3.select("#Wrange").on('change', function(){updatenodes();updatelinks();updateforceini();})
    d3.select("#NCrange").on('change', function(){updatenodes();updatelinks();updateforceini();})
    d3.select("#NRrange").on('change', function(){updatenodes();updatelinks();updateforceini();})
    d3.select("#RTUrange").on('change', function(){updatenodes();updatelinks();updateforceini();})
    d3.select("#DYrange").on('change', function(){updatenodes();updatelinks();updateforceini();})

    //-------------------------------
    // FORCE
    //-------------------------------
    // Add the node & link arrays to the layout, and start the D3.js force-directed layout
    // and add specific drag & zoom behaviours 
    function updateforceparam(){
        force
          .gravity(document.getElementById("force_grav").value)
          .charge(document.getElementById("force_charge").value)
          .distance(document.getElementById("force_dist").value)
          .size( [WIDTH, HEIGHT] )
        if (document.getElementById("force_link").checked){force.linkStrength(function(link) { return (link.weight);}) }
        else {force.linkStrength(1) }
        force.start()
        if (layout_option=="FORCE" && stopstart%2==0){
          d3.select('#STARTSTOP').style("background-color","#0095D7")
          stopstart=1
        }
    }

    // update the force param
    updateforceparam();
    d3.select("#force_grav").on('change', function(){updateforceparam();})
    d3.select("#force_charge").on('change', function(){updateforceparam();})
    d3.select("#force_dist").on('change', function(){updateforceparam();})
    d3.select("#force_link").on('change', function(){updateforceparam();})
    d3.select("#reset").on('click', function(){
      document.getElementById("force_grav").value=forceparam[0]
      document.getElementById("force_charge").value=forceparam[1]
      document.getElementById("force_dist").value=forceparam[2]
      document.getElementById("force_link").checked=true
      updateforceparam();
    })

    function updateforce(){
        if(stopstart % 2 == 0){force.start(); d3.select('#STARTSTOP').style("background-color","#0095D7")}
        if(stopstart % 2 == 1){force.stop(); d3.select('#STARTSTOP').style("background-color","#E2E2E2")}
        stopstart+=1
        //network_energy()
    }

    function updateforceini(){
      if (layout_option === 'FORCE'){
      stopstart=0
      force
        .nodes(nodeArray)
        .links(linkArray)
        .start()
        updateforce();
        // start/stop buttons
        d3.select('#STARTSTOP')
        .on('click',function(){ updateforce();})      
      }

      if (layout_option === 'FIXED'){
      force
        .start()
      svg.call( d3.behavior.drag()
        .on("drag",dragmove))       
      stopstart=0
      d3.select('#STARTSTOP')
        .style("background-color","#E2E2E2")
        .on('click',function(){
          layout_option = 'FORCE'; 
          updateA();  
        })               
      }

      svg.call( d3.behavior.zoom()
        .x(xScale)
        .y(yScale)
        .scaleExtent([1, 5])
        .on("zoom", doZoom) 
        ).on("dblclick.zoom", null);
    }
    updateforceini();

    //compute energy
    function network_energy(){
    	energy=0
        p_grav = document.getElementById("force_grav").value
        p_charge = document.getElementById("force_charge").value
        p_dist = document.getElementById("force_dist").value	
        pplink = document.getElementById("force_link").checked
        nodeArray.forEach(function(d){
        	energy += -p_grav*Math.sqrt(Math.pow(d.x-WIDTH/2,2)+Math.pow(d.y-HEIGHT/2,2))
        	nodeArray.filter(function(n){return n.name > d.name}).forEach(function(n){
        		energy += p_charge/Math.sqrt(Math.pow(d.x-n.x,2)+Math.pow(d.y-n.y,2))
        	})
        })
        linkArray.forEach(function(l){
        	ene = (pplink==true?l.weight:1)*Math.pow((Math.sqrt(Math/pow(l.source.x-l.target.x,2)+Math.pow(l.source.y-l.target.y,2))-p_dist),2)
        	energy += ene
        })
    	//console.log(energy/nodeArray.length**2)
    }

    //-------------------------------
    // LAYOUT
    //-------------------------------
    // ------- Create the elements of the layout (links, nodes, labels) ------

    function redraw_graph(){
		d3.select("#biblioMap").selectAll("svg").remove()
		svg = d3.select("#biblioMap").append("svg")
		  .attr('xmlns','http://www.w3.org/2000/svg')
		  .attr("width", WIDTH)
		  .attr("height", HEIGHT)
		  .attr("id","graph")
		  .attr("viewBox", "0 0 " + WIDTH + " " + HEIGHT )
		  .attr("preserveAspectRatio", "xMidYMid meet");

        networkGraph = svg.append('svg:g').attr('class','grpParent');

	    // links: simple lines
	    graphLinks = networkGraph.append('svg:g').attr('class','grp gLinks')
	      .selectAll("line")
	      .data(linkArray)
	      .enter().append("line")
	      .attr('id', function(d) { return "e" + d.source.name + '-' + d.target.name; } )
	      .style('stroke-width', function(d) { return edge_width(d.weight);} )
	      .attr("class", "link");

	    // nodes: an SVG circle
	    graphNodes = networkGraph.append('svg:g').attr('class','grp gNodes')
	      .selectAll("circle")
	      .data( nodeArray, function(d){return d.name} )
	      .enter().append("svg:circle")
	      .attr('id', function(d) { return "c" + d.name; } )
	      .attr('r', function(d) { return node_size(1); } )
	      .style("fill", function(d) { return d.ccolor;})
	      .attr('pointer-events', 'all') 
	      .on("click", function(d) { showClusterPanel(d); highlightGraphNode(d,true,this); } ) //
	      .on("mouseover", function(d) { 
	      	if (stopstart%2==1){force.start()}
	      	if (clusterInfoDiv.attr('class') === 'panel_off') { highlightGraphNode(d,true,this);  }} )
	      .on("mouseout", function(d) { if (clusterInfoDiv.attr('class') === 'panel_off') { highlightGraphNode(d,false,this);  }} )
	      .call(force.drag);

	    // labels: a group with two SVG text: a title and a shadow (as background)
	    graphLabels = networkGraph.append('svg:g').attr('class','grp gLabel')
	      .selectAll("g.label")
	      .data( nodeArray, function(d){return d.name} )
	      .enter().append("svg:g")
	      .attr('id', function(d) { return "l" + d.name; } )
	      .attr('class','label');

	    labels = graphLabels.append('svg:text')
	      .attr('text-anchor','middle')
	      .attr('pointer-events', 'none') // they go to the circle beneath
	      .attr('id', function(d) { return "lf" + d.name; } )
	      .attr('class','nlabel')
        .style('font-size', '10px')
	      .text( function(d) { return d.labelb; } );

      // compute and output % of remaining nodes / links
      d3.select("#pc_nodes").html((100*nodeArray.length/GLOB[0]).toFixed(2))
      d3.select("#pc_links").html((100*linkArray.length/GLOB[1]).toFixed(2))
      aux=0;
      linkArray.forEach(function(l){ aux+=l.weight})
      d3.select("#pc_linksW").html((100*aux/GLOB[2]).toFixed(2))

	  }

    //-------------------------------
    // LABELS
    //-------------------------------     

    updatelabel();
    d3.select('#mylabel').on('change',function(){updatelabel();});
    function updatelabel(){
      mylabel=document.getElementById("mylabel").value;
      if (mylabel==='id'){nodeArray.forEach(function(n){n.labelb=n.name});} 
      if (mylabel==='group'){nodeArray.forEach(function(n){n.labelb=n.group});} 
      if (mylabel==='PY'){nodeArray.forEach(function(n){n.labelb=n.year});} 
      if (mylabel==='TI'){nodeArray.forEach(function(n){n.labelb=n.title.slice(0,30)+'...'; });}
      if (mylabel==='S'){nodeArray.forEach(function(n){n.labelb=n.stuff.S[0]; });}
      if (mylabel==='J'){nodeArray.forEach(function(n){n.labelb=n.journal; });}
      if (mylabel==='1AU'){nodeArray.forEach(function(n){n.labelb=n.firstAU; });}  
      labels.text( function(d) { return d.labelb; } );
      //shadows.text( function(d) { return d.labelb; } );
      if (activeCluster != undefined){showClusterPanel( activeCluster );}
    }

    //-------------------------------
    // COLORS
    //------------------------------- 
    // redo searches in case a layout change has induced an "updateA()" (eg switch between topic and subtopics, since it can impact the color)
    if (stuff_to_search !== undefined){ searchStuff (stuff_to_search, nodeArray);}

    d3.select('#mycolor').on('change',function(){updatecolor();});
    d3.select("#SHOWPCcheckbox").on("change", function(){switchlabels();} ); 
    updatecolor();

    function updatecolor(){
      if (mycolor==='originaltopic'){
        nodeArray.forEach(function(n){n.ccolor=color(n.id_top)} )
        d3.select("#Searchcbar").style("display","none");
        document.getElementById("SHOWPCcheckbox").checked=false;
      };
      if (mycolor==='topic'){
        nodeArray.forEach(function(n){n.ccolor=color(n.group)} )
        d3.select("#Searchcbar").style("display","none");
        document.getElementById("SHOWPCcheckbox").checked=false;
      };
      if (mycolor==='search'){
        nodeArray.forEach(function(n){n.ccolor=n.search[0]?heatmapcolor[colorValue(n.search[1]/100)]:'#f0f0f0'} )
        //d3.select("#Searchcbar").style("display","block");
      };
      /*
      for (k = 0; k < LIST_DISC[level_option].length; k++){
        if (mycolor===('DISC'+k)){
          kk=parseInt(mycolor.replace('DISC',''));
          nodeArray.forEach(function(n){n.ccolor=heatmapcolor[colorValue(n.freqS[kk]/n.size)]});  
          d3.select("#showPC").style("display","block");     
        }
      } 
      */           
      nodeArray.forEach(function(n){d3.select("#c"+n.name).style("fill", n.ccolor);})
      switchlabels(); 
    } 

    function switchlabels(){
      //var mycolor=document.getElementById("mycolor").value;
      if (document.getElementById("SHOWPCcheckbox").checked){
        labels.text( function(d) { return (d.search[0]?'':'<')+d.search[1]+'%'; } );
        //shadows.text( function(d) { return (d.search[0]?'':'<')+d.search[1]+'%'; } );        
        /*if(mycolor.indexOf('SUB')>-1){
          kk=parseInt(mycolor.replace('SUBDISC',''));
          labels.text( function(d) { return ((100*d.freqS2[kk]/d.size).toFixed(2)+'%'); } );
          shadows.text( function(d) { return ((100*d.freqS2[kk]/d.size).toFixed(2)+'%'); } );
        }
        else{
          kk=parseInt(mycolor.replace('DISC',''));
          labels.text( function(d) { return ((100*d.freqS[kk]/d.size).toFixed(2)+'%'); } );
          shadows.text( function(d) { return ((100*d.freqS[kk]/d.size).toFixed(2)+'%'); } );
        }*/
      }
      else{
        labels.text( function(d) { return d.labelb; } );
        //shadows.text( function(d) { return d.labelb; } );
      }
    }

    //-------------------------------
    // COMMUNITY
    //-------------------------------
    function updatecommunity(){
      var node_data = nodeArray.map(function (d,i) { d.newid=i; return d.newid});
      var edge_data = linkArray.map(function (d) {return {source: d.source.newid, target: d.target.newid, weight: d.weight}; });
      var community = jLouvain().nodes(node_data).edges(edge_data);
      var result  = community();

      nodeArray.forEach(function (n) {n.group = result[n.newid]});
      d3.select("#QQQ").html(QQQ.toFixed(3))
      mycolor='topic'
      updatecolor();

    }

    /* --------------------------------------------------------------------- */
    /* ----------------- FIRST ITERATION LOADED ---------------------------- */
    /* --------------------------------------------------------------------- */
    d3.select("#loading").remove()

    /* --------------------------------------------------------------------- */
    /* ----------------- SEARCH -------------------------------------------- */
    /* --------------------------------------------------------------------- */   
     
    // do search if new search typed in
    d3.select('#MYsearch').on('keydown',function(event){
      if(d3.event.keyCode === 13){
        // close autocomplete form if open
        awesomplete.close()
        //do search part
        stuff_to_search = document.getElementById("MYsearch").value.toLowerCase();
        if (stuff_to_search === ''){stuff_to_search=undefined}
        if (stuff_to_search !== undefined){ searchStuff(stuff_to_search, nodeArray);}
        else { 
            d3.select('#SearchRes').html('')
            mycolor='topic';
            updatecolor();
        }  
      }
    })
    // reset search stuff if form is empty
    d3.select('#MYsearch').on('keyup',function(event){
      if(d3.event.keyCode === 8 || d3.event.keyCode === 46 ){
        if(document.getElementById("MYsearch").value==''){
          d3.select('#SearchRes').html('')
          mycolor='topic';
          updatecolor();        
        }
      }
    })
    d3.select('#mysearchfield').on('change', function(){updatesearchdict(); searchStuff(stuff_to_search, nodeArray)})

    // do search if element is selected in autocomplete form
    document.querySelector('#MYsearch').addEventListener('awesomplete-selectcomplete', function(evt){
      stuff_to_search = document.getElementById("MYsearch").value.toLowerCase();
      searchStuff(stuff_to_search, nodeArray)
    })


    // update lsit of autocomplete form 
    function updatesearchdict(){
      awesomplete.list=searchdict[document.getElementById("mysearchfield").value]
    }
    
    /********************* aux functions *************************************/
    function mycheckP(stuff, sts){  
      res=false; ff=0;
      stuff.forEach(function (elt){ 
        if ( (elt.toLowerCase() == sts)  ){  
          res=true;
          ff=100
        } 
      })

      return [res,ff];
    }
    

    /********************* perform search *************************************/
    // search the typed characters in most frequent items of the nodes
    function searchStuff (sts, nodeArray){
      // ini
      graphNodes.classed( 'found', false )
      sf=document.getElementById("mysearchfield").value;
      d3.select("#searchlegend").html(sts)

      // look for stuff and return freq by node
      nodeArray.forEach(function(n){ n.search=mycheckP(n.stuff[sf], sts); })

      // how much hits did we get?
      foundNodes=[];
      nodeArray.forEach( function(n){ if (n.search[0]){foundNodes.push(n.name)} })    
      var mylength = foundNodes.length;

      // at what level are we?
      truc=' publication'
      function suff(L){str=''; if(L>1){str='s';} return str}

      // where was the stuff found?
      if (mylength === 0){
        searchRes = '<br/><i>No results found at this level.</i>'
        mycolor='topic'
        updatecolor();
      }
      else {
        searchRes = '<br/><i>Found in ' + mylength + truc + suff(mylength) + '!<br/>'
        //foundNodes.forEach(function(nm){d3.select( '#c' + nm ).classed( 'found', true ) })
        mycolor='search';
        updatecolor();
      }
      // display searRes
      searchRes += '<button id="resetSearch" class="emptyb" style="width:40.5%;font-size: 11px;">Clear search</button>'
      d3.select('#SearchRes').html('')

      if (stuff_to_search!== undefined){
        d3.select('#SearchRes').html(searchRes)
        d3.select('#ElsewSearch')
          .on('click',function(){
             update();
          })        
        d3.select('#resetSearch')
          .on('click',function(){
            stuff_to_search=undefined;
            document.getElementById("MYsearch").value=''
            //graphNodes.classed( 'found', false )
            d3.select('#SearchRes').html('')
            mycolor='topic';
            updatecolor();
            if (activeCluster != undefined){showClusterPanel( activeCluster )}
          })
      }
      // reload cluster panel info
      if (activeCluster != undefined){showClusterPanel( activeCluster )}
    }

    /* --------------------------------------------------------------------- */
    /* ----------------- HIGHLIGHT & INFO PANE----------------------------- */
    /* --------------------------------------------------------------------- */ 
    
    // -----------------------------------
    function highlightGraphNode( node, on )
    { 
      /* Select/unselect a node in the network graph.
       Parameters are: 
       - node: data for the node to be changed,  
       - on: true/false to show/hide the node */
      
      // If we are to activate a cluster, and there's already one active, first switch that one off  
      if( on && activeCluster !== undefined ) { highlightGraphNode( activeCluster, false );}

      // opacity low for everybody (will be put higher for selected node and siblings below)
      opac=on?0.15:1
      nodeArray.forEach(function(d){d3.select("#c"+d.name).style("opacity", opac)})
      nodeArray.forEach(function(d){d3.select("#l"+d.name).style("opacity", on?0:0.5);})
      linkArray.forEach(function(d){d3.select("#e"+d.source.name+"-"+d.target.name).style("opacity", opac)})

      // locate the SVG nodes: circle & label group
      circle = d3.select( '#c' + node.name );
      label  = d3.select( '#l' + node.name );

      // activate/deactivate the node itself
      circle.classed( 'main', on ).style("opacity", 1);
      label.style("opacity",  on?1:0.5);
      label.classed( 'on', on || currentZoom >= SHOW_THRESHOLD );
      label.selectAll('text').classed( 'main', on );

      // activate all siblings
      Object(node.links).forEach( function(nm) {
        //.. circle      
        d3.select("#c"+nm).classed( 'sibling', on ).style("opacity", 1);
        //.. labels
        label = d3.select('#l'+nm);
        label.style("opacity",  on?0.7:0.5);
        label.classed( 'on', on || currentZoom >= SHOW_THRESHOLD );
        label.selectAll('text.nlabel').classed( 'sibling', on );
        label.selectAll('text.nshadow').classed( 'nshadowB', on );
        //.. links  
        d3.select("#e"+node.name+'-'+nm).classed('linking', on).style("opacity", 1)
        d3.select("#e"+nm+'-'+node.name).classed('linking', on).style("opacity", 1)
      })      

      // set the value for the current active cluster
      activeCluster=on?node:undefined;
    }

    //----------------------------------
    // Show the cluster details panel for a given node   
    function showClusterPanel( node ) {
      // Fill it and display the panel
      clusterInfoDiv  
      .html( getclusterInfo(node,nodeArray) )
      .attr("class","panel_on");
    }

    /* --------------------------------------------------------------------- */
    /* ----------------- FOR OUTPUT POSITIONS / PARAMS --------------------- */
    /* --------------------------------------------------------------------- */
    //use 'outputPosition();' in the console log to see them, then copy-paste it 
    force.on("end", function() {
      // At this point layout do not move anymore
      console.log("ready to export params/positions");
      // get positions
      myPos=''
      ff=[];
      nodeArray.forEach(function (n){
        ff.push('['+ n.name + ',' + Math.round(n.x*10)/10 + ',' + Math.round(n.y*10)/10 + ']');
      })  
      myPos='"positions":['+ff.join(',')+']';
      // get parameters
      auxSize = Math.max.apply( null, nodeArray.map( function(n) {return n.size;} ) );
      auxminLinkWeight = Math.min.apply( null, linkArray.map( function(n) {return n.weight;} ) );
      min_alpha=Math.log(auxminLinkWeight)/Math.log(10);min_alpha=Math.ceil(min_alpha*10)/10;
      auxmaxLinkWeight = Math.max.apply( null, linkArray.map( function(n) {return n.weight;} ) );
      max_alpha=Math.log(auxmaxLinkWeight)/Math.log(10);max_alpha=Math.ceil(max_alpha*10)/10;
      thrW=Math.log(minW)/Math.log(10);thrW=Math.round(thrW*100)/100;
      myParam='"maxNodeSize":'+auxSize;
      myParam+=',\n"maxLinkWeight":'+auxmaxLinkWeight;
      myParam+=',\n"Wrange":['+min_alpha+','+max_alpha+','+thrW+'],';
    });


    /* --------------------------------------------------------------------- */
    /* ----------------- EXPORT GRAPH -------------------------------------- */
    /* --------------------------------------------------------------------- */

    exportPNG = function(){
      doc=d3.select('#graph').style("background-color", 'white');;
      doc=document.getElementById("graph");
      saveSvgAsPng(doc, "graph.png");
      // export colorbar if exists
      if (d3.select('#Searchcbar').style("display")=='block'){
        docb=document.getElementById("cbar");
        saveSvgAsPng(docb, "cbar.png");
      }
    } 
    d3.select('#export').html('<button onclick="exportPNG()">as PNG</button>')


    /* --------------------------------------------------------------------- */
    /* ----------------- TRANSFORM POSITIONS ------------------------------- */
    /* --------------------------------------------------------------------- */

    //...MODIF LAYOUT
    thehtml='<button style="color:#2671a9">&#9658;</button>'

    d3.select("#hsym").html(thehtml)
      .attr('pointer-events', 'all')         
      .on("click",function(){myHSYM+=1;doZoom(0.0001);})

    d3.select("#vsym").html(thehtml)
      .attr('pointer-events', 'all')         
      .on("click",function(){myVSYM+=1;doZoom(0.0001);})

    d3.select("#rotation").html(thehtml)
      .attr('pointer-events', 'all')                  
      .on("click",function(){myROT+=parseInt(document.getElementById("rot").value);doZoom(0.0001);}) 

    d3.select("#resetLayout").html(thehtml)
      .attr('pointer-events', 'all') 
      .on("click",function(){
        myHSYM=0;myVSYM=0;myROT=0;
        doZoom(0.0001);
      })  

    //... LABELS
    d3.select('#labfontsize').html(thehtml)
      .attr('pointer-events', 'all')         
      .on("click",function(){
        labels.style("font-size",(document.getElementById("FS").value/10) +'vw')
        shadows.style("font-size",(document.getElementById("FS").value/10) +'vw')
      })  

    d3.select('#labfontstyle').html(thehtml)
      .attr('pointer-events', 'all')         
      .on("click",function(){
        fsty=document.getElementById("FSTYLE").value;
        if (fsty=='n'){myweight='normal';mystyle='normal'}
        if (fsty=='b'){myweight='bold';mystyle='normal'}
        if (fsty=='i'){myweight='normal';mystyle='italic'}
        if (fsty=='bi'){myweight='bold';mystyle='italic'}
        labels.style("font-weight",myweight)
        shadows.style("font-weight",myweight)
        labels.style("font-style",mystyle)
        shadows.style("font-style",mystyle)      
      })  

    d3.select("#resetFormat").html(thehtml)
      .attr('pointer-events', 'all') 
      .on("click",function(){
        document.getElementById("FS").value=10;
        document.getElementById("FSTYLE").value='n';
        labels.style("font-weight",'normal')
        labels.style("font-style",'normal')
        labels.style("font-size","1vw")
        shadows.style("font-weight",'normal')
        shadows.style("font-style",'normal')
        shadows.style("font-size","1vw")
      })   


    /* --------------------------------------------------------------------- */
    /* ----------------- REPOSITION ---------------------------------------- */
    /* --------------------------------------------------------------------- */
    /* Move all graph elements to its new positions. Triggered:
       - on node repositioning (as result of a force-directed iteration)
       - on translations (user is panning)
       - on zoom changes (user is zooming)
       - on explicit node highlight (user clicks in a cluster panel link)
       Set also the values keeping track of current offset & zoom values */
    
    function repositionGraph( off, z, mode ) {
      
      // drag: translate to new offset
      if( off !== undefined && (off.x != currentOffset.x || off.y != currentOffset.y ) ) {
        g = d3.select('g.grpParent')
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
           

    /* --------------------------------------------------------------------- */
    /* -----------------DRAG and ZOOM -------------------------------------- */
    /* --------------------------------------------------------------------- */

    // Perform drag 
    function dragmove(d) {
      offset = { x : currentOffset.x + d3.event.dx, y : currentOffset.y + d3.event.dy };
      repositionGraph( offset, undefined, 'drag' );
    }   

    // ---------------------------------------------------------------------
    // semantic zoom: nodes do not change size, but get spread out or stretched together as zoom changes)
     
    function doZoom( increment ) {
      newZoom = increment === undefined ? d3.event.scale : zoomScale(currentZoom+increment);
      if( currentZoom == newZoom )
        return;  // no zoom change
      // See if we cross the 'show' threshold in either direction
      if( currentZoom<SHOW_THRESHOLD && newZoom>=SHOW_THRESHOLD )
        svg.selectAll("g.label").classed('on',true);
      else if( currentZoom>=SHOW_THRESHOLD && newZoom<SHOW_THRESHOLD )
        svg.selectAll("g.label").classed('on',false);

      // See what is the current graph window size
      s = getViewportSize();
      width  = s.w<WIDTH  ? s.w : WIDTH;
      height = s.h<HEIGHT ? s.h : HEIGHT;

      // Compute the new offset, so that the graph center does not move
      zoomRatio = newZoom/currentZoom;
      newOffset = { 
        x : currentOffset.x*zoomRatio + width/2*(1-zoomRatio),
        y : currentOffset.y*zoomRatio + height/2*(1-zoomRatio) 
      };  

      // Reposition the graph
      repositionGraph( newOffset, newZoom, "zoom" );
    }

    // ------------------------------------------
    // process events from the force-directed graph 
    force.on("tick", function() {
      repositionGraph(undefined,undefined,'tick');
    });


  });

} // end of update



/*-------------------------------------------------------------------------------------------------------*/
/*-------------------------------------------------------------------------------------------------------*/

// INFOBULLES
function prep_infobulle(myid,mymsg){
  ttb = d3.select("#tooltip_bulle").attr("class", "tooltip_bulle").style("opacity", 0);
  var deltax=(myid=="#info_search")?-70:-390
  var deltay=(myid=="#info_search")?10:45

  d3.select(myid)
    .on("mouseover", function() {
      ttb.transition()
        .duration(200)
        .style("opacity", .95)       
      ttb.html(mymsg)
           .style("left", (d3.event.pageX + deltax) + "px")
           .style("top", (d3.event.pageY + deltay) + "px");  
    })
    .on("mouseout", function(d) {
        ttb.transition().duration(10).style("opacity", 0);
    }); 
}

/*-------------------------------------------------------------------------------------------------------*/
/*-------------------------------------------------------------------------------------------------------*/


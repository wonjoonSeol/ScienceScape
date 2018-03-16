/* ---------------------------------------------------------------------------
   (c) BiblioMaps, 2017
   Author: Sebastian Grauwin
   website: sebastian-grauwin.com
   --------------------------------------------------------------------------- */

/*-------------------------------------------------------------------------------------------------------*/
/*-------------------------------------------------------------------------------------------------------*/
function doCDviz(){
  //width stuff
  foo=d3.select('#headermenu').node().getBoundingClientRect().width-240
  d3.select("#container").style("width", foo+"px")
  d3.select("#redocloud").style("left", (250+0.40*foo)+"px")
  d3.select("#slider").style("left", (250+0.40*foo)+"px")
  //height stuff
  foo=window.innerHeight-50
  d3.select("#container").style("height", foo+"px")
  d3.select("#sidepanel").style("height", foo+"px")
  d3.select("#listTAB").style("height", (foo-42)+"px")
  d3.select("#graph").style("height", (foo-42)+"px").style("width", "100%")
  d3.select("#slider").style("top", (foo-20)+"px")

  var alpha = 0
  var filename = ''
  fields=['AU','CU','DT','I','K','LA','J','Y','R','RJ','S']; //['AK','AU','CU','DT','I','K','LA','J','Y','R','RJ','S','S2','TK'];
  graph_type=['custom','science'];
  items={'AU':'author','CU':'country/territory','I':'institution','DT':'document type','LA':'language','Y':'publication year','S':'subject category','S2':'subject subcategory','J':'publication source','K':'keyword','AK':'authors\' keyword','TK':'title word','R':'reference','RJ':'reference source'};
  itemsB={'AU':'authors','CU':'countries/territories','CI':'cities','I':'institutions','DT':'document types','LA':'languages','Y':'publication years','S':'subject categories','S2':'subject subcategories','J':'publication sources','K':'keywords','AK':'authors\' keywords','TK':'title words','R':'references','RJ':'reference sources'};
  file={'AU':'authors','CU':'countries','I':'institutions','DT':'doctypes','LA':'languages','Y':'years','S':'subjects','S2':'subjects2','J':'journals','K':'keywords','AK':'authorskeywords','R':'references','RJ':'refjournals'};
  file={'AU':'authors','CU':'countries','I':'institutions','DT':'doctypes','LA':'languages','Y':'years','S':'subjects','J':'journals','K':'keywords','AK':'authorskeywords','TK':'titlewords','R':'references','RJ':'refjournals'};
  country_code={'Canada': 'CAN', 'East Timor': 'TLS', 'Turkmenistan': 'TKM', 'United States of America': 'USA', 'United States': 'USA', 'Lithuania': 'LTU', 'Cambodia': 'KHM', 'Ethiopia': 'ETH', 'Swaziland': 'SWZ', 'Argentina': 'ARG', 'Bolivia': 'BOL', 'Cameroon': 'CMR', 'Burkina Faso': 'BFA', 'Ghana': 'GHA', 'Saudi Arabia': 'SAU', 'Slovenia': 'SVN', 'Guatemala': 'GTM', 'Bosnia and Herzegovina': 'BIH', 'Guinea': 'GIN', 'Germany': 'DEU', 'Spain': 'ESP', 'Liberia': 'LBR', 'Netherlands': 'NLD', 'Pakistan': 'PAK', 'Oman': 'OMN', 'Zambia': 'ZMB', 'Greenland': 'GRL', 'French Guiana': 'GUF', 'New Zealand': 'NZL', 'Yemen': 'YEM', 'Jamaica': 'JAM', 'Albania': 'ALB', 'West Bank': 'PSE', 'Nicaragua': 'NIC', 'United Arab Emirates': 'ARE', 'Uruguay': 'URY', 'India': 'IND', 'Azerbaijan': 'AZE', 'Lesotho': 'LSO', 'Republic of Serbia': 'SRB', 'Kenya': 'KEN', 'South Korea': 'KOR', 'Tajikistan': 'TJK', 'Turkey': 'TUR', 'Afghanistan': 'AFG', 'Bangladesh': 'BGD', 'Mauritania': 'MRT', 'Solomon Islands': 'SLB', 'Kyrgyzstan': 'KGZ', 'Mongolia': 'MNG', 'Mongol Peo Rep': 'MNG', 'France': 'FRA', 'Rwanda': 'RWA', 'Namibia': 'NAM', 'Somalia': 'SOM', 'Peru': 'PER', 'Laos': 'LAO', 'Norway': 'NOR', 'Malawi': 'MWI', 'Benin': 'BEN', 'Western Sahara': 'ESH', 'Cuba': 'CUB', 'Montenegro': 'MNE', 'Republic of the Congo': 'COG', 'Rep Congo': 'COG', 'Togo': 'TGO', 'China': 'CHN', 'Peoples R China': 'CHN', 'Armenia': 'ARM', 'Dominican Republic': 'DOM', 'Ukraine': 'UKR', 'Somaliland': '-99', 'Finland': 'FIN', 'Libya': 'LBY', 'Indonesia': 'IDN', 'Central African Republic': 'CAF', 'Cent Afr Republ': 'CAF', 'United States': 'USA', 'Sweden': 'SWE', 'Belarus': 'BLR', 'Mali': 'MLI', 'Russia': 'RUS', 'Bulgaria': 'BGR', 'Romania': 'ROU', 'Angola': 'AGO', 'Portugal': 'PRT', 'Trinidad and Tobago': 'TTO', 'Cyprus': 'CYP', 'Qatar': 'QAT', 'Malaysia': 'MYS', 'Austria': 'AUT', 'Vietnam': 'VNM', 'Mozambique': 'MOZ', 'UK': 'GBR', 'Hungary': 'HUN', 'Niger': 'NER', 'Brazil': 'BRA', 'Falkland Islands': 'FLK', 'The Bahamas': 'BHS', 'Panama': 'PAN', 'Guyana': 'GUY', 'Costa Rica': 'CRI', 'Luxembourg': 'LUX', 'Ivory Coast': 'CIV', 'Cote Ivoire':'CIV', 'Nigeria': 'NGA', 'Ecuador': 'ECU', 'Czech Republic': 'CZE', 'Brunei': 'BRN', 'Australia': 'AUS', 'Iran': 'IRN', 'USA': 'USA', 'Algeria': 'DZA', 'El Salvador': 'SLV', 'Chile': 'CHL', 'Puerto Rico': 'PRI', 'Belgium': 'BEL', 'Thailand': 'THA', 'Haiti': 'HTI', 'Belize': 'BLZ', 'Sierra Leone': 'SLE', 'Georgia': 'GEO', 'Gambia': 'GMB', 'Philippines': 'PHL', 'Guinea Bissau': 'GNB', 'Moldova': 'MDA', 'Morocco': 'MAR', 'Croatia': 'HRV', 'United Republic of Tanzania': 'TZA', 'Tanzania': 'TZA', 'Switzerland': 'CHE', 'Iraq': 'IRQ', 'Chad': 'TCD', 'Estonia': 'EST', 'Kosovo': '-99', 'Mexico': 'MEX', 'Lebanon': 'LBN', 'Northern Cyprus': '-99', 'South Africa': 'ZAF', 'Uzbekistan': 'UZB', 'Tunisia': 'TUN', 'Djibouti': 'DJI', 'Colombia': 'COL', 'Burundi': 'BDI', 'Slovakia': 'SVK', 'Taiwan': 'TWN', 'Fiji': 'FJI', 'Madagascar': 'MDG', 'Italy': 'ITA', 'Bhutan': 'BTN', 'Sudan': 'SDN', 'Nepal': 'NPL', 'Democratic Republic of the Congo': 'COD', 'Dem Rep Congo': 'COD', 'Suriname': 'SUR', 'Kuwait': 'KWT', 'Israel': 'ISR', 'Iceland': 'ISL', 'Venezuela': 'VEN', 'Senegal': 'SEN', 'Papua New Guinea': 'PNG', 'Zimbabwe': 'ZWE', 'Jordan': 'JOR', 'Vanuatu': 'VUT', 'Denmark': 'DNK', 'Kazakhstan': 'KAZ', 'Poland': 'POL', 'Eritrea': 'ERI', 'Ireland': 'IRL', 'Uganda': 'UGA', 'New Caledonia': 'NCL', 'Macedonia': 'MKD', 'North Korea': 'PRK', 'Paraguay': 'PRY', 'Latvia': 'LVA', 'South Sudan': 'SSD', 'Japan': 'JPN', 'Syria': 'SYR', 'Honduras': 'HND', 'Myanmar': 'MMR', 'Equatorial Guinea': 'GNQ', 'Egypt': 'EGY', 'French Southern and Antarctic Lands': 'ATF', 'United Kingdom': 'GBR', 'Antarctica': 'ATA', 'Greece': 'GRC', 'Sri Lanka': 'LKA', 'Gabon': 'GAB', 'Botswana': 'BWA'}

  // input some general data
  d3.json(dirdatafreqs+'DISTRIBS_itemuse.json', function(data) {
    database=data.database.toLowerCase();
    Npapers=data.N;
    probas_items={'AU':data.pAU,'CU':data.pCU,'I':data.pI,'DT':data.pDT,'LA':data.pLA,'Y':data.pY,'S':data.pS,'J':data.pJ,'K':data.pK,'AK':data.pAK,'TK':data.pTK,'R':data.pR,'RJ':data.pRJ};
    probas_publis={'AU':data.qAU,'CU':data.qCU,'I':data.qI,'DT':data.qDT,'LA':data.qLA,'Y':data.qY,'S':data.qS,'J':data.qJ,'K':data.qK,'AK':data.qAK,'TK':data.qTK,'R':data.qR,'RJ':data.qRJ};
    if (database=='scopus'){probas_items['S2']=data.pS2; probas_publis['S2']=data.qS2;}
    d3.json(dirdatafreqs+'coocnetworks.json', function(data) {Znodes = data.nodes; Zlinks = data.links; dotheviz();})
  })

}


// Do the stuff -- to be called after D3.js has loaded
function dotheviz() {
  //---------------------------------
  //------------------ select items to analyze / graph type
  //---------------------------------
  function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }
  thehtml = '<select id="selectITEM" style="width:170px;" >'
  fields.filter(function(f){return  (f!='S2' || database=='scopus') ; }).forEach(function(f){thehtml+='<option value="'+f+'" '+(field_option==f?'selected':'')+'>'+capitalizeFirstLetter(items[f])+'</option>'})
  thehtml += '</select>'
  d3.select('#itemselection').html(thehtml) 
  d3.select('#selectITEM').on('change',function(){update();})

  thehtml = '<select id="selectGRAPH" style="width:170px;" >'
  thehtml += '<option value="custom" '+(graph_option=='custom'?'selected':'')+'>Custom</option>'
  thehtml += '<option value="science" '+(graph_option=='science'?'selected':'')+'>Distributions</option>'
  thehtml += '</select>'
  d3.select('#graphselection').html(thehtml) 
  d3.select('#selectGRAPH').on('change',function(){update();})

  foo='<select id="selectSORTtab" style="width:170px;" >'
  foo+='<option value="NB" selected>Record count</option>'
  foo+='<option value="ITEM">Item</option>'
  foo+='</select>'
  d3.select('#sortTAB').html(foo)  

  //...
  d3.select('#NUMPUB').html(Npapers)
  prep_infobulle("#info_fs", "Items from that field will be listed on the left panel in numeric order, based on the number of documents in which they appear.")
  prep_infobulle("#info_gt", "Choose between different options:<br/><ul><li>The \"Custom\" option will display the information in the left panel in a custom representation (either a co-occurrence network, a pie chart, a word cloud or a map)</li><li>The \"Distributions\" option will produce a histogram of the number of items per publication and a cumulative distribution graph displaying the number of items appearing in at least <i>x</i> documents, for varying <i>x</i>. This last graph use logarithmic scales on both axes, which is useful to recognize power law relationships, appearing as straight lines.</li></ul>")
  prep_infobulle("#info_sl", "We only display items appearing more than <i>x</i> times, the threshold <i>x</i> being chosen so that the length of the list is less than 10000.")
  update();
} // end of D3ok()


// INFOBULLES
function prep_infobulle(myid,mymsg){
  ttb = d3.select("#tooltip_bulle").attr("class", "tooltip_bulle").style("opacity", 0);
  d3.select(myid)
    .on("mouseover", function() {
      ttb.transition()
        .duration(200)
        .style("opacity", 1)       
      ttb.html(mymsg)
           .style("left", (d3.event.pageX + 10) + "px")
           .style("top", (d3.event.pageY -20) + "px");  
    })
    .on("mouseout", function(d) {
        ttb.transition().duration(10).style("opacity", 0);
    }); 
}

// Do the "real" stuff once the selection has been made
function update() {
  //---------------------------------
  //------------------ select options
  //---------------------------------
  field_option=document.getElementById("selectITEM").value;
  graph_option=document.getElementById("selectGRAPH").value;
  filename=file[field_option];

  //---------------------------------
  //------------------ deal with list
  //---------------------------------
  function prepList(stuff){
    d3.select("#noneAV").style("opacity", 0)
    // prep table with data
    mytable = '<table style="width:99%;table-layout:fixed;margin-left:1%;font-size:'+(field_option.indexOf('R')>-1?'0.75':'0.95')+'em;">'
    //mytable+="<colgroup><col ><col style='width:33%;'><col style='width: 20%;'><col style='width: 20%;'></colgroup>"
    mytable+='<tr><th align="left" style="width:7%;" >Rank</th><th align="left" style="width:63%;">Item='+items[field_option]+'</th><th align="right" style="width:15%;">Record count</th><th align="right" style="width:15%;">% of '+Npapers+'</th></tr>'
    sortby=document.getElementById("selectSORTtab").value;
    if(sortby=="ITEM"){stuff.sort(function(a, b){ return (b[1].toLowerCase() > a[1].toLowerCase()) ? -1:1 ; })}
    if(sortby=="NB"){stuff.sort(function(a, b){ if(a[2]==b[2]){return ((b[1].toLowerCase() > a[1].toLowerCase()) ? -1:1)} else {return (b[2] - a[2]);} })}
    stuff.forEach(function(elt) { 
      ee=(elt[3]<0.01)?'&epsilon;':elt[3];
      if (elt[1]=="none available"){d3.select("#noneAV").html("<strong>Note: this data is NOT available/existing for "+elt[3]+" % of the publications in the studied corpus.</strong>").style("opacity", 1)}
      else{mytable+="<tr><td>"+elt[0]+"</td><td style=\"width:63%;\">"+elt[1]+"</td><td align='right' >"+elt[2]+"</td><td align='right'>"+ee+"</td></tr>"}
    })
    mytable += '</table>'

    // fancy decorum
    mylist  = ''
    mylist += mytable

    // output
    d3.select('#listTAB').html(mylist).property("scrollTop", 0);
    return
  }
  
  d3.select("#titleTAB").html("<i>List of " + itemsB[field_option] + " in corpus</i>")
  stuff=[]
  d3.csv(dirdatafreqs+'freq_'+filename+'.dat', function(err,data) {
    data.forEach(function(d,i){
      // use this to declare the format (string or float) of the data
      stuff.push([i+1,d.item,+d.count,+d.f])
    })
  // output the list and scroll to top
  d3.select('#selectSORTtab').on('change',function(){prepList(stuff);}) 
  prepList(stuff)
  

  //---------------------------------
  //------------------ deal with graph
  //---------------------------------
  alpha = 0
  draw_graph();

  })
} // end of update()

function draw_graphA(){
  alpha=document.getElementById("range").value;
  draw_graph()
}


//do the graph
function draw_graph(){
  if(graph_option==='science'){VIZscience()}
  if(graph_option==='custom' && ['K','AK','TK','S','R','RJ'].indexOf(field_option) >-1){VIZnetwork()}
  if(graph_option==='custom' && ['AU','J','I','S2'].indexOf(field_option) >-1){VIZwordcloud()}
  if(graph_option==='custom' && field_option==='CU'){VIZmap()}
  if(graph_option==='custom' && field_option==='Y'){VIZpubyears()}
  if(graph_option==='custom' && (field_option==='DT' || field_option==='LA')){VIZpiechart()}
  //if(graph_option==='custom' && ['K','AK','TK','S','S2','R','RJ','AU','J','I','CI'].indexOf(field_option) >-1){VIZtreemap()}
}

///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////

function VIZscience(){

  mycond=(field_option==='AU' || field_option==='CU' || field_option==='I' || field_option==='K' || field_option==='AK' || field_option==='TK' || field_option==='S' || field_option==='S2' || field_option==='R' || field_option==='RJ')

  var margin = {top: (30+(mycond?0:d3.select('#graph').node().getBoundingClientRect().height*0.2)), right: 100, bottom: 60, left: 120},
  width = d3.select('#graph').node().getBoundingClientRect().width - margin.left - margin.right,
  height = d3.select('#graph').node().getBoundingClientRect().height*(0.5+(mycond?0:0.2)) - margin.top - margin.bottom; 

  // setup plot    
  d3.select("#graph").html('').style("background",'white')    // start from clean slate
  d3.select("#slider").html('')    // remove slider if exists
  d3.select("#redocloud").html('')
  d3.select("#custominfo").html("").style("opacity", 0);

  //... graph title
  d3.select("#titleGRAPH").html("<i>Distributions</i>")     // 

  // add the tooltip area to the webpage
  var tooltip = d3.select("#tooltip")
    .attr("class", "tooltip")
    .style("opacity", 0);


  //////////////// cumulative distrib
  // initiate svg 
  var svg = d3.select("#graph")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", 
              "translate(" + margin.left + "," + margin.top + ")");

  // setup x
  var xValue = function(d) { return d.x;}, // data -> value
    xScale = d3.scale.log().range([1, width]),  // value -> display
    xMap = function(d) { return xScale(xValue(d));}, // data -> display
    xAxis = d3.svg.axis().scale(xScale).orient("bottom");

  // setup y
  var yValue = function(d) { return d.y;}, // data -> value
    yScale = d3.scale.log().range([height,0]), // value -> display
    yMap = function(d) { return yScale(yValue(d));}, // data -> display
    yAxis = d3.svg.axis().scale(yScale).orient("left");

  // input the data
  data = []
  for (var i = 0; i < probas_items[field_option][0].length; i++) {
    data.push({x: probas_items[field_option][0][i], y: probas_items[field_option][1][i]});
  }

  // Scale the range of the data
  xMaxPow=d3.max(data, function(d) {return Math.ceil(Math.log(d.x)/Math.log(10)); });
  yMaxPow=d3.max(data, function(d) {return Math.ceil(Math.log(d.y)/Math.log(10)); });
  xScale.domain([1, Math.pow(10,xMaxPow)]); 
  yScale.domain([1, Math.pow(10,yMaxPow)]); 

  xAxis.ticks(xMaxPow);
  yAxis.ticks(yMaxPow);

  // draw dots
  svg.selectAll(".dot")
    .data(data)
  .enter().append("circle")
    .attr("class", "dot")
    .attr("r", 4.1)
    .attr("cx", xMap)
    .attr("cy", yMap)
    .on("mouseover", function(d) {
        tooltip.transition()
          .duration(200)
          .style("opacity", .95);
        if (yValue(d)>1){aaa=itemsB[field_option];} else{aaa=items[field_option];} 
        if (xValue(d)>1){bbb=' records';} else{bbb=' record';}   
        tooltip.html(yValue(d) +' '+ aaa+ ' appear'+(yValue(d)==1?'s':'')+' in at least ' + xValue(d) + bbb)
             .style("left", (d3.event.pageX - 155) + "px")
             .style("top", (d3.event.pageY -20) + "px");
        d3.select(this).attr("r", 6).style("fill", "steelblue");    
    })
    .on("mouseout", function(d) {
        tooltip.transition()
             .duration(10)
             .style("opacity", 0);
        d3.select(this).attr("r", 4.1).style("fill", "#81BEF7");      
    });

  // Add a title
  var title = svg.append("text")
    .attr("x", width/2)             
    .attr("y", 0)
    //.attr("text-anchor", "middle")  
    .style("font-size", "1.2em")
    .style("font-style", "italic")
    .style("text-anchor", "middle")
    .style("fill", "gray") 
    .style("opacity", 0.9)  
    .text("Cumulative distribution of occurrences of "+itemsB[field_option]);

  svg.append("g")            // Add the X Axis
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .append("text")
      .attr("class", "label")
      .attr("x", 15)
      .attr("y", -6)
      .style("text-anchor", "start")
      .text("# of occurrences");

  svg.append("g")            // Add the Y Axis
    .attr("class", "y axis")
    .call(yAxis) 
    .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("x", -height+25)
      .attr("dy", ".71em")
      .style("text-anchor", "start")
      .text("# of "+itemsB[field_option]);

  //////////////// how many items by publis?
  if( field_option==='AU' || field_option==='CU' || field_option==='I' || field_option==='K' || field_option==='AK' || field_option==='TK' || field_option==='S' || field_option==='S2' || field_option==='R' || field_option==='RJ'){
    // initiate svg 
    var svgQ = d3.select("#graph")
      .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
      .append("g")
          .attr("transform", 
                "translate(" + margin.left + "," + (margin.top) + ")");

    // setup x
    var xValue = function(d) { return d.x;}, // data -> value
      xScale = d3.scale.linear().range([0, width]),  // value -> display
      xMap = function(d) { return xScale(xValue(d));}, // data -> display
      xAxis = d3.svg.axis().scale(xScale).orient("bottom");

    // setup y
    var yValue = function(d) { return d.y;}, // data -> value
      yScale = d3.scale.linear().range([height,0]), // value -> display
      yMap = function(d) { return yScale(yValue(d));}, // data -> display
      yAxis = d3.svg.axis().scale(yScale).orient("left").innerTickSize(-width);
    yAxis.ticks(6)

    // input the data
    data = []
    excess=0
    auxtot=0
    excessthr={'AU':20,'CU':10,'I':20,'DT':5,'LA':5,'Y':5,'S':20,'S2':20,'J':5,'K':20,'AK':20,'TK':20,'R':100,'RJ':50}
    for (var i = 0; i < probas_publis[field_option][0].length; i++) {
      myx=probas_publis[field_option][0][i];myy=probas_publis[field_option][1][i];
      if (myx<excessthr[field_option]){data.push({x:myx , y: myy*100.0/Npapers })}
      else{excess+=myy}
      auxtot+=myy
    }
    if (excess>0){data.push({x:excessthr[field_option], y: excess*100.0/Npapers })}
    if (auxtot<Npapers){data.push({x:0, y: (Npapers-auxtot)*100.0/Npapers })}

    // Scale the range of the data
    xMax=d3.max(data, function(d) {return d.x});
    yMax=d3.max(data, function(d) {return d.y });
    xScale.domain([-0.5, xMax+0.5]); 
    yScale.domain([0, Math.ceil(yMax)]); 

    // draw dots
    svgQ.selectAll(".dot")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return xScale(d.x-0.5); })
      .attr("width", width/(xMax+1))
      .attr("y", function(d) { return yScale(d.y); })
      .attr("height", function(d) { return height - yScale(d.y); })
      .on("mouseover", function(d) {
          tooltip.transition()
            .duration(200)
            .style("opacity", .95);
          if (xValue(d)>1){aaa=itemsB[field_option];} else{aaa=items[field_option];}    
          tooltip.html(Math.round(yValue(d)*Npapers/100)+' of the publications ('+yValue(d).toFixed(1)+'%) have '+ xValue(d) +' '+ aaa + (xValue(d)==excessthr[field_option]?' or more':''))
               .style("left", (d3.event.pageX - 155) + "px")
               .style("top", (d3.event.pageY -20) + "px");
          d3.select(this).attr("r", 6).style("fill", "steelblue");    
      })
      .on("mouseout", function(d) {
          tooltip.transition()
               .duration(10)
               .style("opacity", 0);
          d3.select(this).attr("r", 4.1).style("fill", "#81BEF7");      
      });

    // Add a title
    var title = svgQ.append("text")
      .attr("x", width/2)             
      .attr("y", -10)
      //.attr("text-anchor", "middle")  
      .style("font-size", "1.2em")
      .style("font-style", "italic")
      .style("text-anchor", "middle")
      .style("fill", "gray") 
      .style("opacity", 0.9)  
      .text("Histogram of number of "+itemsB[field_option]+" per publication");

    svgQ.append("g")            // Add the X Axis
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .append("text")
        .attr("class", "label")
        .attr("x", width)
        .attr("y", -6 )
        .style("text-anchor", "end")
        .text("# of "+itemsB[field_option]);

    svgQ.append("g")            // Add the Y Axis
      .attr("class", "y axis")
      .call(yAxis) 
      .append("text")
        .attr("class", "label")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("x", 0)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("% of publications");
  }

}
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
function VIZnetwork(){

  // start from clean slate 
  d3.select("#graph").html('').style("background",'white')
  d3.select("#slider").html('')    // remove slider if exists 
  d3.select("#tooltip").style("opacity", 0);
  d3.select("#redocloud").html('')
  // custom info
  thehtml="<strong>Co-"+(field_option[0]=='R'?'citations':'occurrences')+" network</strong><br/> <ul style='padding-left:15px;'><li>Each circle <i>c</i> represents a different "+items[field_option]+", with the circle's sizes being proportional to its frequency of use <i>f<sub>c</sub></i> in the studied corpus. </li><li>Each line reflects the link strength between two "+itemsB[field_option]+", the strength being defined as the normalized fraction of times these two "+itemsB[field_option]+" appear together in a publication: <i>S<sub>c1c2</sub> = f<sub>c1c2</sub> / &Sqrt;(f<sub>c1</sub>f<sub>c2</sub>)</i>.<br/> Here, we only show links with S > "+fooTHR[field_option]+".</li><li>The nodes' colors emphasize groups of "+itemsB[field_option]+" significantly linked to each other.</li></ul>"
  thehtml += '<strong>Fine-tuning</strong>'
  thehtml += '<table style="margin-left:12px;">'
  thehtml += '<tr><td >Link threshold</td><td style="padding-right:3px;"><input id="foobarTHR" style="width:50px" type="number" min=0 step=0.01 value="'+ fooTHR[field_option] +'"></td><td><div id="info_linkthr" class="infobulle">?</div></td></tr>'
  thehtml += '<tr><td style="padding-right:5px;">Repulsive force</td><td><input id="foobarForce" style="width:50px" type="number" min=0 step=0.1 value="'+ fooForce[field_option] +'"></td><td><div id="info_repforce" class="infobulle">?</div></td></tr>'
  thehtml += '</table>'
  d3.select("#custominfo").html(thehtml).style("opacity", 1);
  prep_infobulle("#info_linkthr", "The network will show links with strength S greater than this value.")
  prep_infobulle("#info_repforce", "Normalized repulsive force used in the force-based layout algorithm. Typically, you may increase or decrease this value to increase or decrease the spatial range of the network.")

  d3.select("#foobarTHR").on('change',function(){fooTHR[field_option]=document.getElementById("foobarTHR").value; VIZnetwork()})
  d3.select("#foobarForce").on('change',function(){fooForce[field_option]=document.getElementById("foobarForce").value; VIZnetwork()})

  // prep data
  nodesArray=[]
  Znodes.filter(function(elt){return elt.type==field_option}).forEach(function(d, i){ nodesArray.push({name:i, label:d.item, group:i, size:d.size, links:[]}) })
  linksArray=[]
  Zlinks.filter(function(elt){return elt.type==field_option}).forEach(function(d){ 
    sourceNode = nodesArray.filter(function(n) { return n.name === d.source; })[0];
    targetNode = nodesArray.filter(function(n) { return n.name === d.target; })[0];
    linksArray.push({source:sourceNode, target:targetNode, nco: d.Ncooc, weight:d.Ncooc/Math.sqrt(sourceNode.size*targetNode.size)})   
  })

  //... graph title
  d3.select("#titleGRAPH").html("<i>"+(field_option=='S'?'Subject categories':'Top 100 '+itemsB[field_option])+' co-'+(field_option[0]=="R"?'citations':'occurrences')+' network'+"</i>")  

  // draw co-occurrence network
  drawNTW(nodesArray, linksArray, 'xx', "#graph", 0, fooTHR[field_option], fooForce[field_option])  

}
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
function VIZwordcloud(){
  // start from clean slate 
  d3.select("#graph").html('').style("background",'white')
  d3.select("#slider").html('')    // remove slider if exists 
  d3.select("#tooltip").style("opacity", 0);
  d3.select("#redocloud").html('');
  d3.select("#custominfo").html("").style("opacity", 0);

  // prep data
  var frequency_list=[];maxsize=0;
  d3.csv(dirdatafreqs+'freq_'+filename+'.dat', function(err,data) {
      data.forEach(function(d, i) {
        if(d.item[0]!='[' && d.item!='none available'){
          if(maxsize==0){maxsize=d.count}
          if(i<100){frequency_list.push({"text": d.item, "size": (5+30*Math.pow(d.count/maxsize,0.5))});}
      }
      });
    updateWORDCLOUD(frequency_list) 
  })
  
  function updateWORDCLOUD(frequency_list){
    d3.select("#graph").html('').style("background",'white')

    WIDTH=d3.select("#graph").node().getBoundingClientRect().width
    HEIGHT=d3.select("#graph").node().getBoundingClientRect().height

    var colorWC = d3.scale.linear()
          .domain([0,1,2,5,10,20,100])
          .range(['#192934','#124569','#165581','#1F77B4','#5B97C0', '#64A6D4', '#9DB8CB'])

    d3.layout.cloud()
          .size([(WIDTH-20), (HEIGHT-10)])
          .words(frequency_list)
          .rotate(0)
          .fontSize(function(d) { return d.size; })
          .on("end", draw)
          .start();

    d3.select("#redocloud")
      .html('<a><img src="img/update-icon.png" height="20px"/></a>')
      .on("mouseover", function() { d3.select("#redocloud").style("background-color",'#a4a4a4') })
      .on("click", function() {updateWORDCLOUD(frequency_list)  })
      .on("mouseout", function() { d3.select("#redocloud").style("background-color",'') })

    function draw(words) {
      var svg=d3.select("#graph").append("svg")
            .attr("width", WIDTH)
            .attr("height", HEIGHT)
            .attr("class", "wordcloud")
            //.style("background",'white')
      //... append word cloud
      svg.append("g")
            // without the transform, words words would get cutoff to the left and top, they would
            // appear outside of the SVG area
            .attr("transform", "translate("+(0.5*WIDTH)+","+0.5*HEIGHT+")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", function(d) { return d.size + "px"; })
            .style("fill", function(d, i) { return colorWC(i); })
            .style("text-anchor","middle")
            .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
            .text(function(d) { return d.text; });
      //... graph title
      d3.select("#titleGRAPH").html("<i>Word cloud of "+(words.length>95?'top 100 ':'top ')+itemsB[field_option]+"</i>")
    }
  }

}
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
function VIZmap(){
  // setup plot  
  var margin = {top: 30, right: 80, bottom: 30, left: 100},
  width = d3.select('#graph').node().getBoundingClientRect().width - margin.left - margin.right,
  height = d3.select('#graph').node().getBoundingClientRect().height - margin.top - margin.bottom;

  // start from clean slate  
  d3.select("#graph").html('').style("background",'white')
  d3.select("#slider").html('')    // remove slider if exists 
  d3.select("#redocloud").html('');
  d3.select("#custominfo").html("").style("opacity", 0);

  // add the tooltip area to the webpage
  var tooltip = d3.select("#tooltip")
      .attr("class", "tooltip")
      .style("opacity", 0);

  // graph title
  d3.select("#titleGRAPH").html("<i>Map of involved countries / territories</i>")

  // colors
  //color = ['#ffffe5', '#f7fcb9', '#d9f0a3', '#addd8e', '#78c679', '#41ab5d', '#238443', '#006837', '#004529'] // obtained from colorbrewer.YlGn[9]
  //color= ['#ffffd4', '#fed98e', '#fe9929', '#d95f0e', '#993404'] // colorbrewer.YlOrBr[5]
  //function colorValue(ff){return Math.floor(Math.pow(Math.min(ff,20),0.53))}
  colorC = ['#ffffd4','#fee391','#fec44f','#fe9929','#d95f0e','#993404'] // colorbrewer.YlOrBr[6]
  colorV = [0, 2, 5, 10, 20, 50, 100]
  function colorValue(ff){ ii=0; while(Math.min(ff,51) > colorV[ii+1]){ii+=1} return ii }

  // colorbar 
  HH=20;WW=198; nC=6
  thechtml = '<svg id="cbar" height="'+(HH+20)+'" width="'+(WW+20)+'">'
  for (k = 0; k < nC; k++) {
    thechtml += '<polygon points="'+(k*WW/nC+5)+','+0+','+(k*WW/nC+5)+','+(HH)+','+((k+1)*WW/nC+5)+','+(HH)+','+((k+1)*WW/nC+5)+',0" style="fill:'+colorC[k]+';" />'
    thechtml += '<text x="'+((k)*WW/nC+5)+'" y="'+(HH+13)+'" fill="black" style="text-anchor: middle; font-size:8px;">'+(colorV[k]).toFixed((k==1 || k==2)?1:0)+'%</text>'
  }
  thechtml += '<text x="'+(WW+5)+'" y="'+(HH+13)+'" fill="black" style="text-anchor: middle; font-size:8px;">100%</text>'
  thechtml += '</svg>'
  //d3.select("#mycolorbar").html(thechtml);

  // input the data
  d3.csv(dirdatafreqs+'freq_'+filename+'.dat', function(err,rdata) {
    myfills={};mydata={};
    rdata.forEach(function(d){
      code=country_code[d.item];
      mydata[code]= {fillKey: code, Fpapers:d.f};
      myfills[code]= colorC[colorValue(d.f)];
    })
    for (var CU in country_code){
      code = country_code[CU]
      if ((code in mydata)===false){
        mydata[code]= {fillKey: code, Fpapers:0};
        myfills[code]= colorC[colorValue(0)];
      }
    }
    // set up world map
    thehtml='<div id="MAPcontainer" style="position:relative;left:1%;top:12%;width:98%;height:60%;padding-top:0%;padding-bottom:15%;background:lightblue;"></div><div style="position:relative;left:1%;width:93%;margin-top:0;padding-left:5%;background:lightblue;"><strong>Publications in which a country is involved</strong><br/>'+thechtml+'</div>' 
    d3.select('#graph').html(thehtml).style("background",'white')
    var map = new Datamap({
      element: document.getElementById('MAPcontainer'),
      fills: myfills,
      data: mydata,
      geographyConfig: {
        popupTemplate: function(geo, data) {
            if (data.Fpapers >0.01){return ['<div class="hoverinfo"><strong>' + data.Fpapers + '% of documents have an affiliation in <i>' + geo.properties.name + '</i></strong></div>'];}
            else {return ['<div class="hoverinfo"><strong> < 0.01% of documents have an affiliation in <i>' + geo.properties.name + '</i></strong></div>'];}
        },
        highlightFillColor: 'lightgreen',
        highlightBorderColor: 'green'
      }
    }); 

  })
}

///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
function VIZpubyears(){
  // setup plot  
  var margin = {top: (0.2*d3.select('#graph').node().getBoundingClientRect().height + 30), right: 80, bottom: 30, left: 100},
  width = d3.select('#graph').node().getBoundingClientRect().width - margin.left - margin.right,
  height = 0.7*d3.select('#graph').node().getBoundingClientRect().height - margin.top - margin.bottom;

  // start from clean slate  
  d3.select("#graph").html('').style("background",'white')
  d3.select("#slider").html('')    // remove slider if exists 
  d3.select("#redocloud").html('')
  d3.select("#custominfo").html("").style("opacity", 0);

  // add the tooltip area to the webpage
  var tooltip = d3.select("#tooltip")
      .attr("class", "tooltip")
      .style("opacity", 0);

  // start svg  
  var svg = d3.select("#graph")
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");   

  // graph title
  d3.select("#titleGRAPH").html("<i>Number of publications by year</i>")

  // setup x
  var xValue = function(d) { return d.x;}, // data -> value
      xScale = d3.scale.linear().range([0,width]),
      xAxis = d3.svg.axis().scale(xScale).orient("bottom").tickFormat(d3.format(".0f"));

  // setup y
  var yValue = function(d) { return d.y;}, // data -> value
    yScale = d3.scale.linear().range([height,0]), // value -> display
    yAxis = d3.svg.axis().scale(yScale).orient("left").innerTickSize(-width);

  // input the data
  d3.csv(dirdatafreqs+'freq_'+filename+'.dat', function(err,rdata) {
    data=[]
    rdata.forEach(function(d,i){
     // use this to declare the format (string or float) of the data
     if(d.count>0 ){ //Npapers/5000
       data.push({x: +d.item, y: +d.count})
     }
    })
    // Scale the range of the data
    xMin=d3.min(data, function(d) {return d.x; });
    xMax=d3.max(data, function(d) {return d.x; });

    // year selector
    thehtml = '<i>Show years from</i><br/><span id="PYymin"></span> <i>to</i> <span id="PYymax"></span>'
    d3.select('#slider').html(thehtml)
    fooy =  '<select id="selectPYymin" style="width:60px;" >'
    for (var yy = xMin; yy < xMax+1; yy++){fooy += '<option value="'+yy+'" '+((yy==xMin)?'selected':'')+'>'+yy+'</option>'}
    fooy += '</select>'
    d3.select('#PYymin').html(fooy) 
    d3.select('#selectPYymin').on('change',function(){updateXscales();})
    fooy =  '<select id="selectPYymax" style="width:60px;" >'
    for (var yy = xMin; yy < xMax+1; yy++){fooy += '<option value="'+yy+'" '+((yy==xMax)?'selected':'')+'>'+yy+'</option>'}
    fooy += '</select>'
    d3.select('#PYymax').html(fooy) 
    d3.select('#selectPYymax').on('change',function(){updateXscales();})

    function updateXscales(){
      // years range
      my_xMin=parseInt(document.getElementById("selectPYymin").value)
      my_xMax=parseInt(document.getElementById("selectPYymax").value)
      xScale.domain([my_xMin-0.5, my_xMax+0.5]); 
      xAxis.ticks(Math.min(my_xMax-my_xMin+1,7));  

      dataF=data.filter(function(d){return d.x<=my_xMax && d.x>=my_xMin})
      yMin=d3.min(dataF, function(d) {return d.y; });
      yPow=Math.floor(Math.log(yMin)/Math.log(10));
      yMin=Math.floor(yMin/Math.pow(10,yPow))*Math.pow(10,yPow);
      yMax=d3.max(dataF, function(d) {return d.y; });
      yPow=Math.floor(Math.log(yMax)/Math.log(10));
      yMax=Math.ceil(2*yMax/Math.pow(10,yPow))/2*Math.pow(10,yPow);
      yScale.domain([0,yMax]); 

      //remove previous bars / xAxis
      d3.selectAll('#mycurrentbars').remove() 
    
      // draw bars
      svg.selectAll(".dot")
        .data(dataF)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("id", "mycurrentbars")
        .attr("x", function(d) { return xScale(d.x-0.5); })
        .attr("width", width/(my_xMax-my_xMin+1))
        .attr("y", function(d) { return yScale(d.y); })
        .attr("height", function(d) { return height - yScale(d.y); })
        .on("mouseover", function(d) {
          tooltip.transition()
            .duration(200)
            .style("opacity", .9); 
          tooltip.html(d.y +' records published in ' + d.x)
               .style("left", (d3.event.pageX - 150) + "px")
               .style("top", (d3.event.pageY -20) + "px");
          d3.select(this).style("fill", "steelblue");    
      })
      .on("mouseout", function(d) {
          tooltip.transition()
               .duration(10)
               .style("opacity", 0);
          d3.select(this).style("fill", "#81BEF7");      
      });

      // Add the X Axis
      svg.append("g")            
        .attr("class", "x axis")
        .attr("id", "mycurrentbars")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        /*.append("text")
          .attr("class", "label")
          .attr("x", 15)
          .attr("y", -6)
          .style("text-anchor", "start")
          .text("Publication Year");*/

      // Add the Y Axis
      svg.append("g")            
        .attr("class", "y axis")
        .attr("id", "mycurrentbars")
        .call(yAxis) 
        .append("text")
          .attr("class", "label")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("x", 0) //-height + 25
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("Record count");   

    }

    // draw the data
    updateXscales();
   
  }) 
}
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
function VIZpiechart(){
  // setup plot  
  var margin = {top: 30, right: 80, bottom: 30, left: 100},
  width = d3.select('#graph').node().getBoundingClientRect().width - margin.left - margin.right,
  height = d3.select('#graph').node().getBoundingClientRect().height - margin.top - margin.bottom;

  // start from clean slate  
  d3.select("#graph").html('').style("background",'white')
  d3.select("#slider").html('')    // remove slider if exists 
  d3.select("#redocloud").html('')
  d3.select("#custominfo").html("").style("opacity", 0);

  // add the tooltip area to the webpage
  var tooltip = d3.select("#tooltip")
      .attr("class", "tooltip")
      .style("opacity", 0);

  // ... graph title
  d3.select("#titleGRAPH").html("<i>Pie Chart of the publications' "+itemsB[field_option]+"</i>")

  // ... slider 
  thehtml = '<i>Distort Pie Chart</i><br/><input type="range" id="range" min="0" max="1" value="'+alpha+'" step="0.01" onchange="draw_graphA()" />'
  d3.select('#slider').html(thehtml)

  // start svg
  var svg = d3.select("#graph")
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + (margin.left + width / 2) + ","  + (margin.top + 0.45*height) + ")");

  // some variables
  var radius = Math.min(width, height) / 2.5;
  var color = d3.scale.category20().domain(d3.range(20));  

  // prep pie
  var arc = d3.svg.arc()
      .outerRadius(radius - 10)
      .innerRadius(radius / 3);

  var pie = d3.layout.pie()
      .sort(null)
      .value(function(d) { return Math.pow(d.f,(1-alpha)); });

  // import data and draw pie
  d3.csv(dirdatafreqs+'freq_'+filename+'.dat', function(err,data) {
    data.forEach(function(d) {
      d.f = +Math.round(10000*d.count/Npapers)/100;
    });

    var g = svg.selectAll(".arc")
        .data(pie(data))
      .enter().append("g")
        .attr("class", "arc");

    g.append("path")
        .attr("d", arc)
        .style("fill", function(d) { return color(d.data.item); })
        .on("mouseover", function(d) {
          tooltip.transition()
            .duration(200)
            .style("opacity", .9); 
          if (field_option==='LA'){aaa='written in '} else{aaa='';}
          if (d.data.f>0){xxx=d.data.f} else{xxx='<0.01';}
          tooltip.html(xxx +'% of the documents are ' + aaa + d.data.item)
               //.style("background-color", "black")
               //.style("border", "5px solid "+color(d.data.item))
               .style("left", (d3.event.pageX + 10) + "px")
               .style("top", (d3.event.pageY -20) + "px");    
        })
        .on("mouseout", function(d) {
          tooltip.transition()
               .duration(10)
               .style("opacity", 0);     
        });
    
    g.append("text")
        .attr("transform", function(d) {
          var c = arc.centroid(d),
            x = c[0],
            y = c[1],
            // pythagorean theorem for hypotenuse
            h = Math.sqrt(x*x + y*y);
            return "translate(" + (x/h * radius*1.0) +  ',' + (y/h * radius*1.0) +  ")"; 
        })
        .attr("dy", ".35em")
        .attr("text-anchor", function(d) {
          // are we past the center?
          return (d.endAngle + d.startAngle)/2 > Math.PI ?
          "end" : "start";
        })
        .text(function(d) {if (Math.pow(d.data.f,(1-alpha))/Math.pow(100,(1-alpha)) >0.04){return d.data.item;} })
        .style("font-weight","bold")
        .style("font-size","10px")  
  });
}
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
function VIZtreemap(){
  // setup plot  
  var margin = {top: 30, right: 80, bottom: 30, left: 100},
  width = d3.select('#graph').node().getBoundingClientRect().width - margin.left - margin.right,
  height = d3.select('#graph').node().getBoundingClientRect().height - margin.top - margin.bottom;

  // start from clean slate  
  d3.select("#graph").html('').style("background",'white')
  d3.select("#slider").html('')    // remove slider if exists 
  d3.select("#redocloud").html('')
  d3.select("#custominfo").html("").style("opacity", 0);

  // add the tooltip area to the webpage
  var tooltip = d3.select("#tooltip")
      .attr("class", "tooltip")
      .style("opacity", 0);


  // heatmap color stuff
  //var heatmapcolor=['#d73027','#f46d43','#fdae61','#fee090','#ffffbf','#e0f3f8','#abd9e9','#74add1','#4575b4']
  //var mycolorvalues=[0,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5,1]
  var mycolorvalues=[0,0.01,0.05,0.1,0.5,1]
  heatmapcolor=['#d73027','#f46d43','#fdae61','#fee090','#ffffbf']
  function colorValue(f){
    for (jk = 0; jk < 5; jk++){ 
      if (f>=mycolorvalues[jk] && f<mycolorvalues[jk+1]  ){return (4-jk);}
      if (f===1){return 0;}
    }
  }

  var margin = {top: 40, right: 20, bottom: 30, left: 20},
  width = d3.select('#graph').node().getBoundingClientRect().width - margin.left - margin.right,
  height = d3.select('#graph').node().getBoundingClientRect().height - margin.top - margin.bottom;

  //... graph title  
  d3.select("#titleGRAPH").html("<i>"+"Top 100 " + itemsB[field_option]+"</i>")

  var treemap = d3.layout.treemap()
      .size([width, height])
      .sticky(true)
      .value(function(d) { return d.size; });

  var div = d3.select("#graph").append("div")
      .style("position", "absolute")
      .style("width", width + margin.left + margin.right)
      .style("height", height + margin.top + margin.bottom)
      .style("left", margin.left + "px")
      .style("top", margin.top + "px");

  Broot=[]
  d3.csv(dirdatafreqs+'freq_'+filename+'.dat', function(err,mydata) {
    mydata.forEach(function(d,i){
      if (i<100){
        Broot.push({"name":d.item,"size":d.f}) 
      }  
    })
    maxsize=mydata[0].f;
    minsize=mydata[Math.min(100,mydata.length-1)].f;
    root={"name":'corpus',"children":Broot}
    var node = div.datum(root).selectAll(".node")
        .data(treemap.nodes)
      .enter().append("div")
        .attr("class", "node")
        .call(position)
        .style("background", function(d){return heatmapcolor[colorValue((d.size-minsize)/(maxsize-minsize))] })
        .html(function(d) { return d.name + '<br/><div style="text-align:center">' +(d.size) + '%</div>'; })            
        .style("line-height", function(d){return 6+15*Math.pow(d.size/maxsize,0.9)+"px";})
        .style("font-size", function(d){return 4+12*Math.pow(d.size/maxsize,0.9)+"px";})
        .on("mouseover", function(d) {
          tooltip.transition()
            .duration(200)
            .style("opacity", .9);
          tooltip.html( '<i>' + d.name +'</i> appears in ' + d.size + '% of documents')
               .style("left", (d3.event.pageX - 150) + "px")
               .style("top", (d3.event.pageY -20) + "px")
               .style("font-size", "9pt");
          d3.select(this).style("background", "lightgreen");   
        })
        .on("mouseout", function(d) {
          tooltip.transition()
               .duration(10)
               .style("opacity", 0);
          d3.select(this).style("background", heatmapcolor[colorValue((d.size-minsize)/(maxsize-minsize))]);    //"#81BEF7"      
        });            
  })

  function position() {
    this.style("left", function(d) { return d.x + "px"; })
        .style("top", function(d) { return d.y + "px"; })
        .style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
        .style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; });
  }

}


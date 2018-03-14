function togglemenu(mytoggleID){
  //show right submenu
  d3.select("#toggleID1").attr( 'class', 'hidden_submenu')
  d3.select("#toggleID2").attr( 'class', 'hidden_submenu')
  d3.select("#toggleID3").attr( 'class', 'hidden_submenu')
  d3.select("#toggleID4").attr( 'class', 'hidden_submenu')
  d3.select("#toggleID"+mytoggleID).attr( 'class', 'active_submenu')

}
/*
$(document).ready(function() {
    console.log("page loaded..");
    document.getElementById("demo").innerHTML = "demo loaded";
});
*/

$(function () {
    $('[data-toggle="popover"]').popover()
})

function getSelectedText(elementId) {
    var elt = document.getElementById(elementId);

    if (elt.selectedIndex == -1)
        return null;

    return elt.options[elt.selectedIndex].text;
}

var plotGraphsElement = document.getElementById("plotGraphs");
plotGraphsElement.addEventListener("click", plotGraphsEventMethod, false);


var searchLogElement = document.getElementById("searchLogs");
searchLogElement.addEventListener("click", searchLogEventMethod, false);


function searchLogEventMethod(event) {
    var url = window.location.href;
    url = url.split('?')[0]
    event.preventDefault()
    var level = getSelectedText('id_level');
    var sensor = getSelectedText('id_sensor');
    var searchStr = document.getElementById('id_search_str').value;
    url = url + '?level='+ level;
    url = url + '&sensor='+ sensor;
    url = url + '&search_str='+ searchStr;
    //url = url + '&page=1';
    window.location.href = url;
}

function plotGraphsEventMethod(event) {
    var url = window.location.href;
    url = url.split('?')[0]
    event.preventDefault()
    var sensor = getSelectedText('id_sensor');
    var startDate = document.getElementById('id_start_date').value;
    var endDate = document.getElementById('id_end_date').value;
    url = url + '?sensor='+ sensor;
    url = url + '&start_date='+ startDate;
    url = url + '&end_date='+ endDate;
    window.location.href = url;
}


document.getElementById("searchLogs2").addEventListener("click", function(event){
    var url = window.location.href;
    url = url.split('?')[0]
    console.log('1 - ', url)
    //return null;
    event.preventDefault()
    //event.preventDefault()
    var level = getSelectedText('id_level');
    var sensor = getSelectedText('id_sensor');
    var searchStr = document.getElementById('id_search_str').value;
    console.log('level', level, sensor, searchStr);
    url = url + '?level='+ level;
    console.log('2 - ', url)
    url = url + '&sensor='+ sensor;
    console.log('3 - ', url)
    url = url + '&search_str='+ searchStr;
    //url = url + '&page=1';
    console.log('4 - ', url)
    window.location.href = url;
    console.log('url', window.location.href);
});



document.getElementById("plotGraphs1").addEventListener("click", function(event){
    var url = window.location.href;
    url = url.split('?')[0]
    console.log('1 - ', url)
    //return null;
    event.preventDefault()
    //event.preventDefault()
    var sensor = getSelectedText('id_sensor');
    var startDate = document.getElementById('id_start_date').value;
    var endDate = document.getElementById('id_end_date').value;
    console.log('level', sensor, startDate, endDate);
    url = url + '?sensor='+ sensor;
    console.log('3 - ', url)
    url = url + '&start_date='+ startDate;
    url = url + '&end_date='+ endDate;
    console.log('4 - ', url)
    window.location.href = url;
    console.log('url', window.location.href);
});



document.getElementById("searchLogs1").addEventListener("click", function(event){
    var url = window.location.href;
    url = url.split('?')[0]
    console.log('1 - ', url)
    //return null;
    event.preventDefault()
    //event.preventDefault()
    var level = getSelectedText('id_level');
    var sensor = getSelectedText('id_sensor');
    var searchStr = document.getElementById('id_search_str').value;
    console.log('level', level, sensor, searchStr);
    url = url + '?level='+ level;
    console.log('2 - ', url)
    url = url + '&sensor='+ sensor;
    console.log('3 - ', url)
    url = url + '&search_str='+ searchStr;
    //url = url + '&page=1';
    console.log('4 - ', url)
    window.location.href = url;
    console.log('url', window.location.href);
});

function searchLogs1() {
    var url = window.location.href;
    console.log('button clicked. ' + url)
    url = url + '?page=2';
    //window.location.href = url;
    // Edit "action" of the form
    console.log('action - ' + document.getElementById("searchLogForm").action)
    document.getElementById("searchLogForm").action = url;
    console.log('action - ' + document.getElementById("searchLogForm").action)
    //alert('new url - ' + url)
    window.location.href = url;
}

function getForm() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("demo").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "ajax-about", true);
    xhttp.send();
}


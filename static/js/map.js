var map, infowindow, geocoder, service;
var searchString = '';
var address = 'México, Yucatán, Mérida';
var numPlaces = 0;
var cont = 0;
var data = [];
var markers = [];
var ended = true;
var emailUrl = '';
var running = false;
var details = [];
var explored = [];

var fieldsToShow = [
  'name', 'formatted_address', 'formatted_phone_number', 'email', 'website', 'opening_hours',
  'types', 'reviews', 'user_ratings_total', 'photos', 'rating'

];

var fieldNames = {
  'address_components':'Work line #3',
  'adr_address':'Work line #2',
  'formatted_address':'Work line #1',
  'geometry':'geometry',
  'icon':'image',
  'id':'id',
  'name':'Organization name',
  'opening_hours':'Open Times & Service Availability',
  'place_id':'place_id',
  'reference':'reference',
  'scope':'scope',
  'types':'Organization tag 1',
  'url':'Other web site',
  'utc_offset':'utc_offset',
  'vicinity':'Postal line #1',
  'html_attributions':'Postal line #2',
  'email':'Work email',
  'reviews':'Organization tag 2',
  'user_ratings_total':'Organization tag 3',
  'formatted_phone_number':'Work phone',
  'international_phone_number':'Home phone',
  'photos':'photos',
  'rating':'Organization tag 4',
  'website':'Work web site',
  'permanently_closed':''
};

function download() {
  jsonToCsv();
  document.getElementById('downlink').click();
  /*
  if (document.getElementById('downlink')) {
    document.getElementById('downlink').click();
  }
  */
}

function initMap() {
  var pyrmont = {lat: 23.662, lng: -102.528};
  map = new google.maps.Map(document.getElementById('map'), {
    center: pyrmont,
    zoom: 5,
    styles: [{
      stylers: [{ visibility: 'simplified' }]
    }, {
      elementType: 'labels',
      stylers: [{ visibility: 'off' }]
    }]
  });

  geocoder = new google.maps.Geocoder();
  infowindow = new google.maps.InfoWindow();
  service = new google.maps.places.PlacesService(map);

  map.addListener('idle', performSearch);
}

function geoCodingCallback(results, status) {
  if (status === google.maps.GeocoderStatus.OK) {
    map.setCenter(results[0].geometry.location);
    map.setZoom(12);
    pyrmont = results[0].geometry.location;
    performSearch();
    // service.nearbySearch({location: pyrmont, radius: 5000, keyword: searchString}, placesCallback);
  } else {
    alert('Geocode was not successful for the following reason: ' + status);
  }
}

function placesCallback(results, status, pagination) {
  if (status === google.maps.places.PlacesServiceStatus.OK) {
    numPlaces += results.length;
    for (var i = 0; i < results.length; i++) {
      service.getDetails({placeId: results[i].place_id}, detailsCallback);
    }
    if (pagination.hasNextPage) {
      pagination.nextPage();
    } else {
      ended = true;
    }
  }
}

function detailsCallback(place, status) {
  if (status === google.maps.places.PlacesServiceStatus.OK) {
    /*
    var marker = new google.maps.Marker({
      map: map,
      position: place.geometry.location
    });
    google.maps.event.addListener(marker, 'click', function() {
      infowindow.setContent(place.name);
      infowindow.open(map, this);
    });
    markers.push(marker);
    */
    place['email'] = []
    if (place['website'] != undefined && place['website']) {
      console.log('Extracting mails from: ' + place['website']);
      $.getJSON('../cse?site=' + place['website'], function(res){
        console.log(res['value']);
        place['email'] = res['value'];
        data.push(place);
        console.log('GOOD ' + (++cont));
        runDetails();
      });
    } else {
      data.push(place);
      console.log('GOOD ' + (++cont));
      runDetails();
    }
  } else {
    console.log('BAD ' + (++cont));
    runDetails();
  }
  /*
  cont++;
  console.log(cont);
  console.log(data.length);
  //console.log(numPlaces);
  if (ended && cont == numPlaces) {
    document.getElementById('gp_loading').style.display = 'none';
  }
  */
}

function jsonToCsv() {
  var headers = [];
  var csvData = [];
  var csvText = '';
  for (var i in data) {
    csvData[i] = [];
    for (var k in fieldsToShow) {
      var j = fieldsToShow[k];
      var index = headers.indexOf(j);
      index = index!=-1?index:(headers.push(j)-1);
      console.log(j);
      var fieldValue = formatData(data[i], j);
      console.log(fieldValue);
      fieldValue = fieldValue.split('"').join('""');
      csvData[i][index] = '"' + fieldValue + '"';
    }
  }
  var keys = []
  for (var i in headers) {
    var header = headers[i];
    if (fieldNames[header] != undefined) {
      keys.push(fieldNames[header]);
    } else {
      keys.push(header);
    }
  }
  csvText = keys.join(',');
  for (var i in csvData) {
    csvText += '\n' + csvData[i].join(',');
  }
  var uri = 'data:text/csv;charset=utf-8,' + escape(csvText);
  var link = document.getElementById('downlink');
  if (!link) {
    link = document.createElement("a");    
    link.appendChild(document.createTextNode("Download"));
    link.id = 'downlink';
    link.href = uri;
    link.download = 'results.csv';
    document.getElementById('floating-panel').appendChild(link);
  } else {
    link.href = uri;
  }
  // document.getElementById('bt_gp_do').style.display = 'inline-block';
  // document.getElementById('gp_loading').style.display = 'none';
}

function formatData(row, i) {
  var value = '';
  switch (i) {
    case 'address_components':
      var coma = '';
      for (var j in row[i]) {
        value = value + coma + row[i][j]['long_name'];
        coma = ', ';
      }
      break;
    case 'adr_address':
      value = row[i].replace(/<\/?[^>]+(>|$)/g, "");
      break;
    case 'geometry':
      value = '';
      break;
    case 'types':
      var value = '';
      var coma = '';
      for (var j in row[i]) {
        value = value + coma + row[i][j];
        coma = ', ';
      }
      break;
    case 'photos':
      var value = '';
      var coma = '';
      for (var j in row[i]) {
        value = value + coma + row[i][j]['html_attributions'];
        coma = '\n';
      }
      break;
    case 'reviews':
      var value = '';
      var coma = '';
      for (var j in row[i]) {
        value = value + coma + row[i][j]['text'];
        coma = '\n';
      }
      break;
    case 'opening_hours':
      var value = '';
      var coma = '';
      for (var j in row[i]['weekday_text']) {
        var val = row[i]['weekday_text'][j];
        val = val.replace('\u2013', '-');
        value = value + coma + val;
        coma = ', ';
      }
      break;
    default:
      if (row[i] != undefined) {
        value = JSON.stringify(row[i]);  
      }
      break;
  }
  return value;
}

function clearMarkers() {
  while (markers.length > 0) {
    var marker = markers.pop();
    marker.setMap(null);
  }
}

function createMarker(place) {
  var placeLoc = place.geometry.location;
  var marker = new google.maps.Marker({
    map: map,
    position: place.geometry.location
  });

  google.maps.event.addListener(marker, 'click', function() {
    infowindow.setContent(place.name);
    infowindow.open(map, this);
  });
}

function search() {
  // document.getElementById('bt_gp_do').style.display = 'none';
  // document.getElementById('gp_loading').style.display = 'inline-block';
  data = [];
  details = [];
  explored = [];
  cont = 0;
  numPlaces = 0;
  ended = true;
  clearMarkers();
  address = document.getElementById('where').value;
  searchString = document.getElementById('what').value;
  if (address && searchString) {
    geocoder.geocode({'address': address}, geoCodingCallback);  
  } else {
    alert('Please fill the requiered fields.');
  }
}

function addMarker(place) {
  var marker = new google.maps.Marker({
    map: map,
    position: place.geometry.location,
    icon: {
      url: 'http://maps.gstatic.com/mapfiles/circle.png',
      anchor: new google.maps.Point(10, 10),
      scaledSize: new google.maps.Size(10, 17)
    }
  });
  markers.push(marker);

  google.maps.event.addListener(marker, 'click', function() {
    service.getDetails(place, function(result, status) {
      if (status !== google.maps.places.PlacesServiceStatus.OK) {
        console.error(status);
        return;
      }
      infowindow.setContent(result.name);
      infowindow.open(map, marker);
    });
  });
}

function callback(results, status) {
  if (status !== google.maps.places.PlacesServiceStatus.OK) {
    console.error(status);
    return;
  }
  numPlaces += results.length;
  for (var i = 0, result; result = results[i]; i++) {
    addMarker(result);
    if (explored.indexOf(results[i].place_id) == -1) {
      explored.push(results[i].place_id);
      details.push(results[i].place_id);  
    }
  }
  if (!running) {
    runDetails(); 
  }
}

function runDetails() {
  var placeId = details.shift();
  if (placeId) {
    running = true;
    document.getElementById('gp_lo').style.display = 'inline-block';
    document.getElementById('gp_co').innerHTML = 'Pending: ' + details.length;
    setTimeout(function(){
      service.getDetails({placeId: placeId}, detailsCallback);
    }, 1000);
  } else {
    running = false;
    document.getElementById('gp_lo').style.display = 'none';
  }
}

function performSearch() {
  if (searchString && address) {
    var request = {
      bounds: map.getBounds(),
      keyword: searchString
    };
    service.radarSearch(request, callback);
  }
}
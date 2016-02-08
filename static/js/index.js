jQuery(function($) {

  var objRes = null;
  var curId = null;

  var $bodyEl = $('body'),
      $sidedrawerEl = $('#sidedrawer'),
      $titleEls = $('strong', $sidedrawerEl);

  $('.js-show-sidedrawer').on('click', showSidedrawer);
  $('.js-hide-sidedrawer').on('click', hideSidedrawer);

  $('.bt').on('click', buttonActions);
  $('.lk').on('click', buttonActions);
  $('.sb').on('click', startSearch);
  $('.ka').on('click', killAll)
  $('.ks').on('click', killSelected)

  $titleEls
    .next()
    .hide();

  $titleEls.on('click', function() {
    $(this).next().slideToggle(200);
  });

  $('.dv').hide();

  var urls = {
    'wa':{
      'st': '/bots/wa/st',
      'se': '/bots/wa/se',
      'in': '/bots/wa/in',
      'ki': '/bots/wa/ki'
    },
    'sa':{
      'st': '/bots/sa/st',
      'se': '/bots/sa/se',
      'in': '/bots/sa/in',
      'do': '/bots/sa/do',
      'ki': '/bots/sa/ki'
    },
    'gp':{
      'st': '/bots/gp/st',
      'se': '/bots/gp/se',
      'in': '/bots/gp/in',
      'do': '/bots/gp/do'
    },
    'wm':{
      'st': '/bots/wm/st',
      'se': '/bots/wm/se',
      'in': '/bots/wm/in',
      'do': '/bots/wm/do',
      'ki': '/bots/wm/ki'
    }
  };

  function buttonActions() {
    var id = $(this).attr('id');
    if (id) {
      curId = id;
      var arrId = id.split('_');
      arrId[0] = 'dv';
      mui.tabs.activate('pane-justified-' + arrId[1]);
      var divId = arrId.join('_');
      var curObj = document.getElementById(divId);
      if (curObj) {
        $('.dv').hide();
        $(curObj).show();
        objRes = $('.res', curObj);
      }
      executeAction(id);
    }
  }

  function showSidedrawer() {
    // show overlay
    var options = {
      onclose: function() {
        $sidedrawerEl
          .removeClass('active')
          .appendTo(document.body);
      }
    };

    var $overlayEl = $(mui.overlay('on', options));

    // show element
    $sidedrawerEl.appendTo($overlayEl);
    setTimeout(function() {
      $sidedrawerEl.addClass('active');
    }, 20);
  }


  function hideSidedrawer() {
    $bodyEl.toggleClass('hide-sidedrawer');
  }

  function executeAction(id) {
    var arrId = id.split('_');
    $('.res').text('');
    switch (arrId[2]) {
      case 'st':
        getStatus(arrId[1]);
        break;
      case 'in':
        toggleInit(arrId[1]);
        break;
      case 'do':
        startDownload(arrId[1]);
        break;
      case 'se':
        actionSearch(arrId[1]);
        break;
    }
  }

  function actionSearch(section) {
    switch (section) {
      case 'gp':
        if (document.getElementById('map') == undefined) {
          $('#mapDiv').append('<div id="map"></div><script id="mapScript" src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAiXqbxr9TDiRHzdMgHhE3XfpMyOmX9nYU&callback=initMap&signed_in=true&libraries=places,visualization" async defer></script>');
          $('#bt_gp_do').show();
        }
        break;
    }
  }

  function getUrl(action, section) {
    var url = urls[section][action];
    return url;
  }

  function printCallback(response) {
    $(objRes).html(JSON.stringify(response));
    takeAction(response);
    console.log(response);
  }

  function takeAction(response) {
    var exit = '';
    var arrId = curId.split('_');
    if (arrId[1] == 'sa' && arrId[2] == 'do') {
      exit = 'File is not yet ready. Wait some minutes meanwhile the first part is ready.';
      if (response.status) {
        if (response.value == 'FINISHED') {
          exit = '<a target="_blank" href="/' + response.status + '">Download complete file</a>';
        } else {
          exit = '<a target="_blank" href="/' + response.status + '">Download partial file</a>';
        }
      }
      $(objRes).html(exit);
    } else if (arrId[1] == 'wm' && arrId[2] == 'do') {
      exit = 'File is not yet ready. Wait some minutes meanwhile the first part is ready.';
      if (response.status) {
        if (response.value == 'FINISHED') {
          exit = '<a target="_blank" href="/' + response.status + '">Download complete file</a>';
        } else {
          exit = '<a target="_blank" href="/' + response.status + '">Download partial file</a>';
        }
      }
      $(objRes).html(exit);
    } else if (arrId[2] == 'st') {
      if (response.status == 'NOT_RUNNING') {
        exit = 'Bots are not running.';
      } else {
        exit = 'Bots that are running:<br>';
        var arrProc = response.status.split('\n');
        arrProc.pop();
        for (var i in arrProc) {
          exit += arrProc[i] + '<br>';
        }
      }
      $(objRes).html(exit);
    }
  }

  function getStatus(section) {
    var data = {};
    var url = getUrl('st', section);
    if (url) {
      $.getJSON(url, data, printCallback);
    }
  }

  function toggleInit(section) {
    var data = {};
    var url = getUrl('st', section);
    if (url) {
      $.getJSON(url, data, function(resp) {
        console.log(resp);
        if (resp.status == 'NOT_RUNNING') {
          $('#fk_' + section).hide();
          $('#rs_' + section + '_in').text('There are no bots running.');
        } else {
          $('#fk_' + section).show();
          var arrCmd = resp.status.split('\n');
          arrCmd.pop();
          $('#sl_' + section).empty();
          $.each(arrCmd, function(index, item) {
            $('#sl_' + section).append(new Option(item, item));
          });
        }
      });  
    }
  }

  function startDownload(section) {
    var data = {};
    var url = getUrl('do', section);
    if (url) {
      $.getJSON(url, data, printCallback);  
    }
  }

  function startSearch() {
    var arrId = this.id.split("_");
    var action = arrId[1];
    var data = getFormData("#fm_" + action);
    console.log(data);
    var url = getUrl('se', action);
    if (url) {
      $.getJSON(url, data, printCallback);  
    }
  }

  function killSelected() {
    var arrId = this.id.split("_");
    var action = arrId[1];
    var data = getFormData('#fk_' + action);
    console.log(data);
    var url = getUrl('ki', action);
    if (url) {
      $.getJSON(url, data, function(response) {
        $("#sl_" + action + " option[value='" + data['k'] + "']").remove();
        if ($("#sl_" + action + " option").length == 0) {
          $('#fk_' + action).hide();
        }
        printCallback(response);
      });
    }   
  }

  function killAll() {
    var arrId = this.id.split("_");
    var section = arrId[1];
    var url = getUrl('in', section);
    if (url) {
      $.getJSON(url, data, printCallback);
      $('#sl_' + section).empty();
      $('#fk_' + section).hide();
    }
  }

  function getFormData(formName){
    var unindexed_array = $(formName).serializeArray();
    var indexed_array = {};
    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });
    return indexed_array;
  }

});
$(function() {
	function init() {
		$('#Chat_Calendar').dtpicker();
		$('#Chat_Topbar_Left').on('click', function(e) {
			$('#Chat_Profile').toggle('slow');
		});
		$('#Dialog_Order_Close').on('click', function(e) {
			$('#Modal_Background').hide('slow');
			$('.Dialog').hide('slow');
		});
		$('#Modal_Background').on('click', function(e) {
			$('#Modal_Background').hide('slow');
			$('.Dialog').hide('slow');
		});
		$('#Dialog_Order_Button_Vertical').on('click', function(e) {
			$('#Dialog_Order_Vertical').toggle('slow');
		});
		$('#Dialog_Order_Vertical_Button_Cancel').on('click', function(e) {
			$('#Dialog_Order_Vertical').hide('slow');
		});
		$('#Dialog_Order_Vertical_Button_Save').on('click', function(e) {
			$('#Dialog_Order_Vertical').hide('slow');
		});
		$('.Chat_Message_Options_Create').on('click', function(e) {
			$('#Modal_Background').show('slow');
			$('#Dialog_Order').show('slow');
		});
		$('#Dialog_Order_Transfer_Dropdown').on('click', function(e) {
			$('#Dialog_Order_Transfer').toggle('slow');
		});
		$('#Dialog_Order_Transfer_Button_Cancel').on('click', function(e) {
			$('#Dialog_Order_Transfer').hide('slow');
		});
		$('#Dialog_Order_Transfer_Button_Save').on('click', function(e) {
			$('#Dialog_Order_Transfer').hide('slow');
		});
		$('.Ticket_Main').on('click', function(e) {
			$('.Container_Tickets').removeClass('Container_Tickets_Active');
			$(this).parent().addClass('Container_Tickets_Active');
			$('.Ticket_Secondary').removeClass('Ticket_Secondary_Selected');
		});
		$('.Ticket_Secondary').on('click', function(e) {
			if ($(this).hasClass('Ticket_Secondary_Selected')) {
				$(this).removeClass('Ticket_Secondary_Selected');	
			} else {
				$('.Ticket_Secondary').removeClass('Ticket_Secondary_Selected');
				$(this).addClass('Ticket_Secondary_Selected');
			}
		});
		$('.Suggestions_Button').on('click', function(e) {
			$('.Suggestions_Button').removeClass('Suggestions_Button_Selected');
			$(this).addClass('Suggestions_Button_Selected');
		});
		$('.Image_Toogleable').on('click', function(e) {
			var jQueryObj = $(this);
			var tmp = jQueryObj.attr('src');
		    jQueryObj.attr('src', jQueryObj.attr('togglesrc'));
		    jQueryObj.attr('togglesrc', tmp);
		});
		function deleteMovement(e) { $(this).parent().parent().remove(); }
		$('.Dialog_Order_Movement_Remove').on('click', deleteMovement);
		$('#Dialog_Order_Button_Movement').on('click', function(e) {
			$('#Dialog_Order_Movements').append('<div class="Dialog_Order_Movement"><div class="Dialog_Order_Movement_Left"><div class="Dialog_Order_Movement_Tag" contenteditable="true">CUANDO</div><div class="Dialog_Order_Movement_Value" contenteditable="true">Justo ahora</div></div><div class="Dialog_Order_Movement_Right"><div class="Dialog_Order_Movement_Tag" contenteditable="true">CONCEPTO</div><div class="Dialog_Order_Movement_Strong" contenteditable="true">$1</div><span class="icon-eliminar Image_Remove Dialog_Order_Movement_Remove"></span></div></div>');
			$('.Dialog_Order_Movement_Remove').on('click', deleteMovement);
		});
		$('#Message_Schedule').on('click', function(e) {
			if ($('#Message_Schedule').hasClass('Image_Programar_Active')) {
				$('#Message_Schedule').removeClass('Image_Programar_Active');
			} else {
				$('#Modal_Background').show('slow');
				$('#Dialog_Schedule').show('slow');
			}
		});
		$('#Dialog_Order_Button_Schedule').on('click', function(e) {
			$('#Modal_Background').hide('slow');
			$('.Dialog').hide('slow');
			$('#Message_Schedule').addClass('Image_Programar_Active');
		});
	}

	init();
});
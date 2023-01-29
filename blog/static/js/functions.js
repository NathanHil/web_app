//=============//
//	Functions	//
//=============//
console.log("Loading functions.js...");

/*---------------------*/
/* AJAX form functions */
/*---------------------*/
var loadingAnimation = '<div class="loading-container"><div class="lds-default"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div></div>';

window.showHidePlatSelector = function() {
	if ($("#id_milestone").val() == "VerticalLaunch") {
		$('#id_plat').parent().show();
		$('#id_plat').removeAttr('disabled');
		$('#id_plat').attr('data-error', 'This field is required.');
		$('#id_plat>option[value=""]:not(:first),#id_plat>option:not([value]):not(:first)').remove();
		if (!$("#id_milestone").parents().find(".js-item-create-form").length > 0) {
			$("#id_community").removeAttr('disabled');
			$("#id_community").attr('readonly', 'readonly');
		}
	}
	else {
		$('#id_plat>option').removeAttr('selected');
		if ($('#id_plat>option[value=""],#id_plat>option:not([value])').length == 0) {
			$('#id_plat').append('<option value>---------</option>');
		}
		$('#id_plat>option[value=""]:first,#id_plat>option:not([value]):first').attr('selected', true);
		$('#id_plat').parent().hide();
		$('#id_plat').attr('disabled','');
		$('#id_plat').removeAttr('required');
		$('#id_plat').removeAttr('data-error');
	}
}

window.loadForm = function() { // Receive form from the specific page and button clicked and populate it on the page
	console.log("loading form...");
	var btn = $(this);
	console.log("Modal open - background scroll disabled.")
	$("html").addClass('no-scroll');
	$.ajax({
		url: btn.attr("data-url"),
		type: 'get',
		dataType: 'json',
		beforeSend: function() {
			$("#modal-item .modal-content").html(loadingAnimation);
			$("#modal-item").modal("show");
		},
		success: function(data) {
			console.log("Form loaded.");
			$("#modal-item .modal-content").html(data.html_form);
			if(btn.hasClass("subtable-button")) {
				$(".js-item-update-form").addClass("subtable-form");
			}
			$(".modal-content #errorBlock").remove();
			showHidePlatSelector();
		},
		statusCode: {
			403: function() {
				$('.modal-content').html('<div class="modal-header"></div><div id="errorBlock"></div>');
				$(".modal-content .modal-header").html("<h2>ERROR - 403 Forbidden</h2>");
				$(".modal-content #errorBlock").html("You do not have permission to access this page or data. If you think this is incorrect, please contact your system administrator.");
				$(".modal-content #errorBlock").show();
			},
			404: function() {
				$('.modal-content').html('<div class="modal-header"></div><div id="errorBlock"></div>');
				$(".modal-content .modal-header").html("<h2>ERROR - 404 Not Found</h2>");
				$(".modal-content #errorBlock").html("The requested data was not found on the server");
				$(".modal-content #errorBlock").show();
			},
			500: function() {
				$('.modal-content').html('<div class="modal-header"></div></div><div id="errorBlock"></div>');
				$(".modal-content .modal-header").html("<h2>ERROR - 500 Server Error</h2>");
				$(".modal-content #errorBlock").html("An error occurred on the server. Please try again later. If the problem persists, contact your system administrator");
				$(".modal-content #errorBlock").show();
			}
		},
		error : function(jqXHR, textStatus, errorThrown) {
			console.log("jqXHR ERROR: "+jqXHR);
			console.log("Text Status ERROR: "+textStatus);
			console.log("ERROR Thrown: "+errorThrown);
		}
	});
};

window.saveForm = function () { // Verify data in the form and submit it
	console.log('Saving form...')
	var form = $(this);
	var updateTableClass = $(this).attr("id");
	var tableIsSub = (form.hasClass("subtable-form")) ? true : false;
	var parentOfSub = $("#item-table .parent.active");

	$('.modal-content').append('<div id="errorBlock"></div>');
	$(".modal-body input").attr('readonly', true);
	$(".modal-body select").attr('readonly', true);
	if (form.hasClass("js-item-delete-form")) {
		$(".modal-body").remove();
	}
	$(".modal-footer").html(loadingAnimation);

	$.ajax({
		url: form.attr("action"),
		data: form.serialize(),
		type: form.attr("method"),
		dataType: 'json',
		success: function (data) {
			if (data.form_is_valid) {
				// $('.modal-body').hide();
				// $("#modal-item").modal("hide");
				// Reload the page when filter
				if (window.location.href.includes("?")) {
					location.reload();
				}
				else { // No filter; reload just the table with new data
					console.log("no filter applied; reload table");
					console.log("Background scroll enabled.");
					$("html").removeClass('no-scroll');
					if (!tableIsSub) { // NOT subtable: update table
						$("#item-table."+updateTableClass).html(data.html_item_list);
					}
					// Hide modal
					$('.modal-body').hide();
					$("#modal-item").modal("hide");
					console.log("Modal closed; Background scroll enabled.");
					$("html").removeClass('no-scroll');
					// Reload subtable whether editing parent OR sub
					parentOfSub.each(updateSubtable);
				}
				// get rid of repeated pagination and div space
				$("#item-table."+updateTableClass+" .pagination").last().remove();
				$("#item-table."+updateTableClass+" .col-md-12").last().remove();
			}
			else {
				$("#modal-item .modal-content").html(data.html_form);
			}
		},
		error : function(data, textStatus, errorThrown) {
			console.log("data ERROR: "+data);
			// console.log("Text Status ERROR: "+textStatus);
			// console.log("ERROR Thrown: "+errorThrown);
			$(".modal-content .modal-header").html("<h2>ERROR - "+errorThrown+"</h2>");
			$(".modal-content .modal-body").hide();
			console.log(data);
			$("#errorBlock").text(data.responseJSON.error.message);
			$(".modal-content #errorBlock").show();
			$(".modal-content .modal-footer").remove();
		}
	});
	return false;
};

window.loadIframe = function(e) {
	e.preventDefault();
	console.log("loading iframe...");
	var btn = $(this);
	$("#modal-item").modal("show");
	$("#modal-item .modal-content").html("<div class='modal-header'><button type='button' class='close' data-dismiss='modal' aria-label='Close'><span aria-hidden='true'><i class='fas fa-times'></i></span></button></div><iframe id='importIframe' width='100%' height='100%' src="+btn.attr('data-url')+" frameborder='0'></iframe>");
};

window.submitIframeForm = function(e) { // iFrame forms need to submit without navigating the parent page away
	e.preventDefault();
	// $("#importMessage").html(loadingAnimation);
	if (!$('#importData').get(0).files.length) {
		e.preventDefault();
		$("#importMessage").hide();
		$("#importMessage").html('<div id="errorBlock" style="display:none;"><h3>There was a problem importing your file</h3><h5>Please select a valid .csv file to import<br>Double check your file and try again</h5></div>');
		$("#errorBlock").css("background", "#f0f0f0");
		$("#errorBlock").hide();
		$("#importMessage").fadeIn(300);
		$("#errorBlock").fadeIn(300);
		$("#errorBlock").delay(5000).fadeOut(3000);
	}
	else {
		window.parent.$("#importIframe").css("height", "64vh");
		// Disable button and update text
		$(this).find("#importFormSubmit").html("Submiting Import...");
		$(this).find("#importFormSubmit").css("background-color", "#28a745");
		$(this).find("#importFormSubmit").prop("disabled",true);
		$("#errorBlock").css("background", "#f0f0f0");
		// Message to user to inform that data submits in background
		this.submit();
	}
}


window.updateSubtable = function() { // When updating subtable, load data into rows and run showHideSubtable
	var rowID = $(this).attr("id"); 
	var id = rowID.replace('_row','');
	$(".subtable .table-data").slideUp(200);
	$(".subtable").slideUp(200);
	$("#item-table > tr").removeClass('active');

	$("#"+id+"-subtable").remove();
	$("#"+rowID+" .js-view-accordion").each(showHideSubTable);
};

window.showHideSubTable = function() { // New function to load, add, and display accordion below table row
	console.log("showing subtable..")
	var id = $(this).attr("id");
	var rowID = id+"_row"; 
	var requestURL = $(this).attr("action");
	var clickedRow = $("#"+rowID);
	var subTableRow = $("#"+id+"-subtable");

	$(".paleblue tr:not(#"+rowID+")").removeClass('active');

	if ( subTableRow.length < 1 ) { // does not exist OR subtable has been updated
		// (re)create subtable and show it
		$("#"+rowID).after("<tr class='subtable' id='"+id+"-subtable' style='display:none;'><td colspan='20'><div class='table-data' style='display:none;'><h3 id='subtable-header'></h3></div></td></tr>");
		// Add temporary loading animation
		$("#"+id+"-subtable .table-data").html(loadingAnimation);
		$("#"+id+"-subtable").fadeIn(200);
		$("#"+id+"-subtable .table-data").slideDown(200);

		$.ajax({
			url: requestURL,
			type: "GET",
			dataType: 'text',
			success: function (data) {
				// Populate the subtable with the data
				$("#"+id+"-subtable .table-data").html(data);
				// Hide all the other open "subtables"
				clickedRow.addClass("active");
				$(".subtable:not(#"+id+"-subtable) .table-data").slideUp(200);
				$(".subtable:not(#"+id+"-subtable)").fadeOut(200);
				// Add flag to each subtable button to inform later functions that a subtable is being interracted with
				$(".subtable .btn").each(function() {
					$(this).addClass("subtable-button");
				});
			},
			error : function(jqXHR, textStatus, errorThrown) {
				console.log("jqXHR ERROR: "+jqXHR);
				console.log("Text Status ERROR: "+textStatus);
				console.log("ERROR Thrown: "+errorThrown);
			}
		});
	} 
	else { // subtable already exists
		// currently open -- close it
		if (clickedRow.hasClass("active")) {
			// Deactivate parent
			// console.log("This parent is ACTIVE ==> deactivating...'");
			clickedRow.removeClass("active");
			// Collapse subtable
			// console.log("This parent's subtable is OPEN ==> closing...'");
			$(".subtable .table-data").slideUp(200);
			$(".subtable").fadeOut(200); // collapse all subtables
		}
		// currently closed -- open it
		else {
			// Activate parent
			// console.log("This parent is DEACTIVE ==> activating...");
			clickedRow.addClass("active");
			// Open subtable
			// console.log("This subtable is CLOSED ==> opening...");
			$(".subtable .table-data").slideUp(200);
			$(".subtable").fadeOut(200);
			subTableRow.fadeIn(200);
			$("#"+id+"-subtable .table-data").slideDown(200);
		}
	}
};

function loadRelatedData(selectedValue, url, relatedFieldId) { // Get data related to a specified dropdown selection in form and populate additional form selection
	console.log("loading data for "+$(this).attr("id"));
	var ajaxData = [];
	var urlList = [];
	var relatedFieldIdList = [];

	// Turn URL and field ID into arrays for ajax function to use properly
	if ($.type(url) != "array" && $.type(relatedFieldId) != "array") {
		console.log('Converting to array...');
		urlList.push(url);
		relatedFieldIdList.push(relatedFieldId);
	}
	else { // URL and Field ID are already arrays
		urlList = url;
		relatedFieldIdList = relatedFieldId;
	}
	// Only run the ajax if the url list and the field ID lists are the same size
	if (urlList.length == relatedFieldIdList.length) {
		console.log("building ajaxData "+urlList.length);
		$.each(urlList, function(index) {
			// Build list with tuples of url and field ID data for ajax to recurse through
			ajaxData.push([ urlList[index], relatedFieldIdList[index] ]);
		});
		// Run ajax per each form selector that needs data
		doAjax(0, ajaxData, selectedValue);
	}
}

function doAjax(arrCount, ajaxData, selectedValue) { // Get data to populate form selector dropdown associated with 'selectedValue'
	if(arrCount < ajaxData.length) {
		// Form field that is getting updated is the second in the tuple at index 'arrCount' of ajaxData
		var relatedField = $(ajaxData[arrCount][1]);
		// Add loading animation when loading plans associated with the selected plat
		relatedField.html(loadingAnimation);

		// Get the data related to the selected form field asynchronously
		$.ajax({
			url: ajaxData[arrCount][0],
			data: {
				// add the community id to the GET parameters
				'community': selectedValue 
			},
			success: function (data) { // 'data' is the return of the 'load_' view function
				if (data == "") {
					relatedField.html("<p style='color: grey;font-style: italic;'>No "+relatedField.attr('name')+"s found for this</p>");
				}
				else {
					// replace the contents of the field input with the data that came from the server
					relatedField.html(data);
				}
				arrCount += 1;
				doAjax(arrCount, ajaxData, selectedValue);
			},
			error : function(jqXHR, textStatus, errorThrown) {
				relatedField.html("<p style='color: grey;font-style: italic;'>Please select a Community to view Plans</p>");
				console.log("jqXHR ERROR: "+jqXHR);
				console.log("Text Status ERROR: "+textStatus);
				console.log("ERROR Thrown: "+errorThrown);
			}
		});
	}
}

window.submitTieout = function() { // Update tieout and close all open subsections
	$("table.tieout_table tbody.accordion").removeClass("open");
	$("table.tieout_table tr.accordion_header").removeClass("open");
	// Replace page with loading animation to keep from unwanted changes
	$(".tieout_loading_block").html(loadingAnimation);
	$(".tieout_loading_block").show();
}

window.toggleSubTable = function(evt) {
	// If the current open dropdown is clicked, close it
	if ($(this).parent().hasClass("open")) {
		$(this).parent().removeClass("open");
	}
	// If a different dropdown is clicked, close all others and open new one
	else {
		$(".dropdown-check-list").removeClass("open");
		$(this).parent().addClass("open");
	}
}

window.closeDropdownOnOuterClick = function(e) {
	// Re-enable body scroll when click outside modal when modal is open
	if ( $("body").hasClass("modal-open") && $(e.target).parents(".modal-dialog").length === 0) {
		console.log("Modal closed; Background scroll re-enabled.");
		$("html").removeClass('no-scroll');
	}
	// Close the filter dropdown if click is outside of it
	if ( $(e.target).parents(".dropdown-check-list").length === 0 ) {
		$(".dropdown-check-list").removeClass("open");
	}
	// Close accordion on open/close button
	if ( $(e.target).parents(".dropbtn").length === 0 && !$(e.target).hasClass("dropbtn")) {
		$(".accordion_header .dropbtn").removeClass("open");
	}
}

window.openTieoutModal = function(e) {
	var modal_table = $(".modal-content."+e.target.id).html();
	$("#modal-item").modal("show");
	$("#modal-item .modal-content").html(modal_table);
	$("#modal-item .modal-header").html('<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true"><i class="fas fa-times"></i></span></button><h2>'+e.target.value+' Breakdown</h2>');
}

window.toggleAccordion = function(e) {
	// Do not expand accordion if associated menu is clicked
	if ( $(e.target).prop("tagName") != "TR" 
		&& $(e.target).prop("tagName") != "TD" 
		&& $(e.target).prop("tagName") != "H3") 
		{ return; }

	var accName = $(this).attr('id');

	$("table.tieout_table tbody.accordion:not(."+accName+")").removeClass("open");
	$("table.tieout_table tr.accordion_header:not(#"+accName+")").removeClass("open");
	$("table.tieout_table tbody."+accName).toggleClass("open");
	$("table.tieout_table tr#"+accName).toggleClass("open");
	// Scroll the page to the header selected
	$([document.documentElement, document.body]).animate({
        scrollTop: $("#headerText").offset().top,
        easing: 'linear'
    }, 300);
}

window.openTieoutMenu = function(e) {
	// Dropdown menus expand on click, and close on outer click or repeated click of menu button
	if ($(e.target).prop("tagName") == "I") {
		$(".accordion_header .dropbtn:not(."+$(e.target).attr("for")+")").removeClass("open");
		$(e.target).toggleClass("open");
	}
}

function confirmCompleteAllDialog(message, id, name) { // When marking all tieout items complete, request verification from user
	$.confirm({
		title: 'Are you sure?',
		content: 'Do you want to complete all '+name+'?',
		type: 'blue',
		buttons: {
			ok: {
				text: "Yes",
				btnClass: 'btn-primary',
				keys: ['enter'],
				action: function(){
					$('.'+id+' input[name*="complete"]').each(function(i) {
						if (!$(this).prop('disabled')) {
							console.log(this.checked);
							$(this).prop('checked', true);
							updateTieoutCompleteCounter();
						}
					});
				}
			},
			cancel: function(){
				console.log('The user clicked "Cancel"');
			}
		}
	});
}

window.checkAllComplete = function(e) { // User marks all tieout items complete
	var id =	$(e.target).attr("id");
	confirmCompleteAllDialog("Are you sure you want to complete all "+id+"?", id, $('#'+id+'.accordion_header h3').html());
}

/*---------------------------*/
/* Update page items on load */
/*---------------------------*/
window.updateTieoutCompleteCounter = function() { // Count completed tieout items and update the counter on the page
	$("table.tieout_table tr.accordion_header").each(function() {
		var acc = $(this).next();
		var errorCount = acc.find(".error_msg.active").length
		var completeCount = acc.find("input:checkbox[name*='complete']:checked").length;
		var totalCount = acc.find("input:checkbox[name*='complete']").length;
		// Completed count
		$(this).find(".complete_count").text(completeCount+" / "+totalCount);
		// Warning icon and count
		if (errorCount > 0) {
			$(this).find(".warning_count").text(" "+errorCount);
		}
		else {
			$(this).find(".warning_count").hide();
			$(this).find(".tieout_warning_icon").hide();
		}
		if (completeCount == totalCount) {
			$(this).find(".complete_count").css('color', 'green');
		}
		else {
			$(this).find(".complete_count").css('color', '#b7b7b7');
		}
	});
}

console.log("functions.js complete");
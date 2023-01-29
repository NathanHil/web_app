window.onLoadScripts = function() {

	console.log("Loading onLoad...");

	// Define loading animation variable HTML
	var loadingAnimation = '<div class="loading-container"><div class="lds-default"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div></div>';

	//=====================//
	// Pre-defined scripts //
	//=====================//
	
	$.fn.digits = function() {
		return this.each(function(){ 
			$(this).val( $(this).val().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,")); 
		});
	}


	//=====================//
	// Run on load scripts //
	//=====================//

	// Populate tag with currentUrl id with the current page URL
	$("#currentUrl").html($(location).attr('href'));

	// Add body class 404 if page not found
	if ($("#not-found-bg").length > 0) {
		$('body').addClass('not_found');
	}

	// Add table headers to row items for mobile view
	$("table.paleblue > tbody > tr > td").each(function () {
		var $label = $("table.paleblue thead tr th a").eq($(this).index()).html();
		if ($label != "undefined") {
			$(this).attr("label",$label);
		}
	});

	// Check if page loading is in iframe
	if (self != top) {
		console.log("loading iframe");
		$('html').addClass("iframe");
	}

	// Reload table-display page if form within iframe is submitted successfully
	if (window.parent.$('#modal-item').hasClass("submitted")) {
		window.parent.$("#modal-item").modal("hide");
		window.parent.location.reload();
	}

	// Create formatted dropdown for check box drop down selector
	$("div.checkItems").each(function( i ) { 
		// Get container created by CheckBoxSelectMultiple in filters
		var checkList = $(this);
		// Populate the dropdown label using the first classname set in filters
		var dropdownName = checkList.attr("class").split(/\s+/)[0];
		// Wrap list in collapsible container
		checkList.wrap('<div id="checkListWrapper_'+i+'" class="dropdown-check-list check-list_'+i+'" tabindex="100"></div>');
		var wrapper = $('#checkListWrapper_'+i);
		// Create clickable element outside of hidden container
		wrapper.prepend('<span class="anchor openBtn" id="check-list_'+i+'">Select '+dropdownName+'(s)</span>');
	});

	// Show "clear filters" button if a filter is applied
	if (window.location.href.includes("?") && !window.location.href.includes("?page=")) {
		$( "<div><a href='"+window.location.pathname+"' class='clear-filters'>Clear filters</a></div>" ).insertBefore( ".table-filter .btn.btn-primary" );
	}

	// Add tieout breakdown button to tieout table(s)
	if (window.location.href.includes("tieout")) {
		$(".tieout_table >tbody .form_row").each(function() {
			var table_name = $(this).find("td:first-child >input:last-child").attr('class');
			var has_cc_mapping = $(this).find("td[class*='has_cc_mapping'] input").val();
			console.log("CC Mapping for "+table_name+": "+has_cc_mapping);
			if (table_name.length > 0) {
				$(this).find(">:first-child").append('<a type="button" data-url="breakdown/?table_name='+table_name+'" value="'+table_name+'" class="open-tieout-modal  js-create-item" id="'+table_name.toLowerCase().replace(" ","_")+'_table">View transactions</a>');
			}
			if (has_cc_mapping == "True") {
				$(this).find(">:first-child").append('<a type="button" data-url="cc_breakdown/?mapping='+table_name+'" value="'+table_name+'" title="View Cost Code breakdown table" class="open-tieout-modal  js-create-item" id="'+table_name.toLowerCase().replace(" ","_")+'_table">View Cost Code breakdown</a>');
			}
		});
	}
	// Tieout Table data formatting
	$('.tieout_table').find('.date').each(function() {
		$(this).clone().attr('type','date').insertAfter($(this)).prev().remove();
	});
	$('.tieout_table').find('.decimal').digits();
	$('.tieout_table').find('.integer').digits();
	// Tieout Progress Bar
	$(".tieout_progress_table tr").each(function(e) {
		var barComplete = $(this).find('td.completed_tasks').html();
		var barMax = $(this).find("td.total_tasks").html();
		var barWidth = Math.round((barComplete/barMax)*100);
		var widthCSS = barWidth.toString()+'%';
		console.log("Complete percent: "+widthCSS);
		$(this).find('td .progress_bar').css('width',  widthCSS);
		$(this).find('td .tieout_progress .complete').html(barComplete);
		// $(this).find('td .tieout_progress .total').html(barMax);
		if (barWidth < 100) {
			$(this).find('td .progress_bar').css('background-color','');
		}
		// Style past-due assignments
		console.log($(this).find("td.past_due").text().includes("False"));
		if ($(this).find("td.past_due").text().includes("False")) {
			$(this).find("td.past_due").text("On Schedule");
			$(this).find("td.past_due").css('color','green');
		} else {
			$(this).find("td.past_due").text("Past Due");
			$(this).find("td.past_due").css('color','#e73700');
		}
	});
	// Tieout seperate accordion sections
	$("table.tieout_table tbody").each(function(e) {
		var $name = $(this).attr('name').toLowerCase();
		var $class = $(this).attr("class").substring($(this).attr("class").indexOf(" ")+1);
		var $warn = "All warnings must be resolved before "+$name+" section can be completed";
		$(this).before("<tr class='accordion_header' id='"+$class+"'><td><i class='fas fa-bars menu_btn dropbtn dropdown "+$class+"' for='"+$class+"'><div class='dropdown_menu'><div class='tieout_menu_item check_all_complete' id='"+$class+"'>Check all complete</div></div></i><h3>"+$name+"</h3><div class='complete_count'></div><i class='fas fa-exclamation-triangle tieout_warning_icon' title='"+$warn+"'></i><div class='warning_count' title='"+$warn+"'></div></td></tr>");
	});
	$('.tieout_table .form_row:has(> td > input.error_msg.active)').css('background','rgb(241 233 210)');

	//====================//
	//  Auto run Scripts  //
	//====================//
	// Update the count field for each tieout item
	updateTieoutCompleteCounter();
	// Hide plat field in milestone form until vertical launch is selected
	showHidePlatSelector();


	//===================//
	//    Event hooks    //
	//===================//
	$(document).on('submit', '.js-import-form', submitIframeForm);
	// Toggle open and close list on button click event
	$(document).on('click', '.openBtn', toggleSubTable);
	// Close list if click anywhere outside dropdown
	$(document).mouseup(closeDropdownOnOuterClick);
	// Open tieout modal
	$(document).on('click', '.open-tieout-modal', openTieoutModal);
	$(document).on('click', '.modal-footer .close-btn', function() {$('html').removeClass('no-scroll');});
	$(document).on('click', '.modal-header .close', function() {$('html').removeClass('no-scroll');});
	// Accordion functionality
	$(document).on('click', '.accordion_header', toggleAccordion);
	$(document).on('click', '.accordion_header .dropbtn', openTieoutMenu);
	$(document).on('click', '.dropdown_menu .check_all_complete', checkAllComplete)
	$(document).on('click', '.tieout_table .form_row input[name*="complete"]', updateTieoutCompleteCounter);
	// Create modal form
	$(document).on('click', '.js-create-item', loadForm);
	$(document).on('submit', '#modal-item .js-item-create-form', saveForm);
	// Update modal form
	$(document).on('click', '#item-table .js-update-item', loadForm);
  	$(document).on('submit', '#modal-item .js-item-update-form', saveForm);
	// Delete item modal form
	$(document).on('click', '#item-table .js-delete-item', loadForm);
	$(document).on('submit', '#modal-item .js-item-delete-form', saveForm);
	// View Associated Table accordion
	$(document).on('click', '.js-view-accordion', showHideSubTable);
	// Import item modal
	$(document).on('click', '.js-import', loadIframe);
	// Master Loan get related form list data
	$(document).on('change', 
		'#masterloanpackage #id_community', 
		{ // Data dictionary
			url:'/ajax/load-platplans/', 
			relatedFieldId:'#id_platplans'
		}, 
		function(event) {
			loadRelatedData($(this).val(), event.data.url, event.data.relatedFieldId);
		} 
	);
	// Proforma get related form list data
	$(document).on('change', 
		'#proformamilestone #id_community', 
		{ // Data dictionary
			url:['/ajax/load-communityplats/', '/ajax/load-communityplans/'], 
			relatedFieldId:['#id_plat', '#id_communityplans']
		}, 
		function(event) {
			// Must use anonymouse function to run other functions with arguments 
			loadRelatedData($(this).val(), event.data.url, event.data.relatedFieldId);
		}
	);
	// Disable plat field if plat is not selected in milestone
	$(document).on('change', '#id_milestone', showHidePlatSelector);
	// Submit tieout
	$(document).on('click', '.submit_tieout', submitTieout);
	
	console.log('onLoad Complete.');
}

$( document ).ready(onLoadScripts);
$( document ).on('readyAgain', onLoadScripts);

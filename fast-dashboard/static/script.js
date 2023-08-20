$(function () {
	var start = moment().subtract(29, "days");
	var end = moment();

	function cb(start, end) {
		console.log(start, end);

		const startFormatted = start.format("MMMM D, YYYY HH:MM");
		const startISO = start.toISOString();
		const endFormatted = end.format("MMMM D, YYYY HH:MM");
		const endISO = end.toISOString();
		$("#reportrange span").html(startFormatted + " - " + endFormatted);
		console.log(startISO, endISO);
		fetchNew(startISO, endISO);
	}

	$("#reportrange").daterangepicker(
		{
			startDate: start,
			timePicker: true,
			endDate: end,
			autoUpdateInput: false,
			ranges: {
				Today: [moment(), moment()],
				Yesterday: [moment().subtract(1, "days"), moment().subtract(1, "days")],
				"Last 7 Days": [moment().subtract(6, "days"), moment()],
				"Last 30 Days": [moment().subtract(29, "days"), moment()],
				"This Month": [moment().startOf("month"), moment().endOf("month")],
				"Last Month": [
					moment().subtract(1, "month").startOf("month"),
					moment().subtract(1, "month").endOf("month"),
				],
			},
		},
		cb
	);

	cb(start, end);
});

function fetchNew(new_start_date, new_end_date) {
	const queryParams = new URLSearchParams(window.location.search);

	queryParams.set("start_date", new_start_date);
	queryParams.set("end_date", new_end_date);

	const newUrl = `${window.location.pathname}?${queryParams.toString()}`;

	console.log(newUrl);
}

function getAllQueryParams() {
	var queryParams = {};
	var queryString = window.location.search.substring(1);
	var queryParamsArray = queryString.split("&");

	for (var i = 0; i < queryParamsArray.length; i++) {
		var param = queryParamsArray[i].split("=");
		queryParams[param[0]] = decodeURIComponent(param[1]);
	}

	return queryParams;
}

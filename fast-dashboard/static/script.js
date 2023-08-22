let startISO, endISO;
$(function () {
	var start = moment().subtract(29, "days");
	var end = moment();

	function cb(start, end) {
		startISO = start.toISOString();
		endISO = end.toISOString();
		$("#reportrange span").html(
			start.format("MMMM D, YYYY hh:mm A") +
				" - " +
				end.format("MMMM D, YYYY hh:mm A")
		);
		fetchLatest();
	}

	$("#reportrange").daterangepicker(
		{
			startDate: start,
			endDate: end,
			timePicker: true,
			timePicker24Hour: true,
			ranges: {
				Today: [moment().startOf("day"), moment().endOf("day")],
				Yesterday: [
					moment().subtract(1, "days").startOf("day"),
					moment().subtract(1, "days").endOf("day"),
				],
				"Last 7 Days": [
					moment().subtract(6, "days").startOf("day"),
					moment().endOf("day"),
				],
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

async function fetchLatest(page = 1) {
	const sensorType = document.getElementById("sensorType").value;
	const sensorId = document.getElementById("sensorID").value;
	console.log(sensorType, startISO, endISO, sensorId, page);

	const queryParams = new URLSearchParams({
		sensor_id: sensorId,
		sensor_type: sensorType,
		start_date: startISO,
		end_date: endISO,
		page: page,
	});

	const url = `/filter?${queryParams}`;

	try {
		const response = await fetch(url);

		if (!response.ok) {
			throw new Error(`HTTP error! Status: ${response.status}`);
		}

		const htmlContent = await response.text();

		const resultContainer = document.getElementById("content");
		resultContainer.innerHTML = htmlContent;
	} catch (error) {
		console.error("Error fetching data:", error);
	}
}

let startISO, endISO;


/*
function responsible for daterangepicker
*/
$(function (start, end, last) {
	var start = moment().subtract(29, "days");
	var end = moment();

	function cb(start, end, last = "") {
		startISO = start.toISOString();
		endISO = end.toISOString();
		console.log("Lastt val", last);

		$("#reportrange span").html(
			start.format("MMMM D, YYYY hh:mm A") +
				" - " +
				end.format("MMMM D, YYYY hh:mm A")
		);
		fetchLatest((page = 1), (last = last));
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

	cb(start, end, last);
});



function titleCase(str) {
	str = str.toLowerCase().split(" ");
	for (var i = 0; i < str.length; i++) {
		str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
	}
	return str.join(" ");
}

/**
 * The function fetchLatest is an asynchronous function that fetches data from a server based on user
 * input and updates the HTML content of a content element with the fetched data.
 * @param [page=1] - The page parameter is used to specify the page number of the data to fetch. It is
 * an optional parameter with a default value of 1.
 * @param [last] - The "last"  parameter is used for redis caching 
 */
async function fetchLatest(page = 1, last = "") {
	const sensorType = document.getElementById("sensorType").value;
	const sensorId = document.getElementById("sensorID").value;
	console.log(sensorType, startISO, endISO, sensorId, page);

	const queryParams = new URLSearchParams({
		sensor_id: sensorId,
		sensor_type: sensorType,
		start_date: startISO,
		end_date: endISO,
		page: page,
		last: last,
	});

	const url = `/filter?${queryParams}`;

	try {
		const response = await fetch(url);

		if (!response.ok) {
			throw new Error(`HTTP error! Status: ${response.status}`);
		}

		const htmlContent = await response.text();

		if (sensorType) {
			document.getElementById("currentSensorType").textContent =
				titleCase(sensorType);
		} else {
			document.getElementById("currentSensorType").textContent =
				titleCase("all sensors types");
		}

		const resultContainer = document.getElementById("content");
		resultContainer.innerHTML = htmlContent;
	} catch (error) {
		console.error("Error fetching data:", error);
	}
}

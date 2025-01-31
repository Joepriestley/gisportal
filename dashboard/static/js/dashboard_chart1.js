
document.addEventListener("DOMContentLoaded", async () => {
  try {
    let response = await fetch("http://127.0.0.1:9008/globetudes/forest/");
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    let data = await response.json();
    console.log("API Response:", data); // Debugging step

    // Ensure 'features' array exists in response
    if (!data.features || !Array.isArray(data.features)) {
      throw new Error("Expected 'features' array in response but got something else.");
    }

    // Extract data from 'properties'
    let labels = data.features.map(row => row.properties.forest_nam);
    let data1 = data.features.map(row => row.properties.superficie);

    // Ensure the canvas exists
    const canvas = document.getElementById("lineChart");
    if (!canvas) {
      throw new Error("Canvas element with ID 'lineChart' not found.");
    }
    const ctx = canvas.getContext("2d");

    // Call function to create the chart
    createChart(ctx, labels, data1, "Forest Area (sq km)");

  } catch (error) {
    console.error("Error fetching data:", error);
  }
});

// Function to create Chart
function createChart(ctx, labels, data, dataName) {
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: dataName,
        data: data,
        backgroundColor: "rgba(35, 81, 34, 0.8)",
        borderColor: "rgba(41,155,99,1)",
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

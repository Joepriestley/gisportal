let myChart;
let jsonData;

const setChartType = (chartType) => {
    if (myChart) {
        myChart.destroy();
    }

    const canvas = document.getElementById("lineChart");
    const ctx = canvas.getContext("2d");

    createChart(ctx, jsonData.features.map(row => row.properties.forest_nam), 
                jsonData.features.map(row => row.properties.superficie), 
                "Forest Area (sq km)", chartType);
};

document.addEventListener("DOMContentLoaded", async () => {
    try {
        let response = await fetch("http://127.0.0.1:9008/globetudes/forest/");
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        let data = await response.json();
        console.log("API Response:", data); 

        jsonData = data;

        if (!data.features || !Array.isArray(data.features)) {
            throw new Error("Expected 'features' array in response but got something else.");
        }

        let labels = data.features.map(row => row.properties.forest_nam);
        let dataValues = data.features.map(row => row.properties.superficie);

        const canvas = document.getElementById("lineChart");
        if (!canvas) {
            throw new Error("Canvas element with ID 'lineChart' not found.");
        }
        const ctx = canvas.getContext("2d");

        createChart(ctx, labels, dataValues, "Forest Area (sq km)", "bar");

    } catch (error) {
        console.error("Error fetching data:", error);
    }
});

function createChart(ctx, labels, data, dataName, chartType) {
    myChart = new Chart(ctx, {
        type: chartType,
        data: {
            labels: labels,
            datasets: [{
                label: dataName,
                data: data,
                backgroundColor: chartType === "pie" ? 
                    ["#388E3C", "#F57C00", "#D32F2F", "#1976D2", "#7B1FA2", "#FFEB3B", "#8BC34A","#8BC36A"] 
                    : "rgba(35, 81, 34, 0.8)",
                borderColor: chartType === "pie" ? 
                    ["#2E7D32", "#E65100", "#C62828", "#1565C0", "#6A1B9A", "#FBC02D", "#689F38"] 
                    : "rgba(41, 155, 99, 1)",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: "top"
                }
            },
            scales: chartType === "pie" ? {} : {
              x:{
                title:{
                  display:true,
                  text:"Forest Name",
                  color:"red",
                  font:{
                    family:"Comic sans MS3",
                    size:15,
                    weight:"bold",
                    lineHeight:1.5
                  }
                }
              },
                y: {
                    beginAtZero: true,
                    title:{
                      display:true,
                      text:"Superficie (km²)",
                      color:"red",
                      font:{
                        family:"Comic Sans MS",
                        size:10,
                        weight:"bold",
                        lineHeight:1.2
                      }
                    }
                }
            }
        }
    });
}
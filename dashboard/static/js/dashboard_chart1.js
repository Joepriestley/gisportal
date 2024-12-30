const ctx = document.getElementById('lineChart');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul','Aug', 'Sept', 'Oct','Nov','Dec'],


      datasets: [{
        label: 'Data',
        data: [2500,6000,2050,1900,2030,1905,2800,2300,2900,9000,1200,3000],
        backgroundColor:['rgba(85,85,85,1)'

        ],

        borderColor:['rgba(41,155,99)'

        ],
        borderWidth: 1
      }],

    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      },

      responsive:true
    }
    
  });
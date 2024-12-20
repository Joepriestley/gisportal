const pieChart = document.getElementById('doughnut').getContext('2d');
new Chart(pieChart, {
  type: 'doughnut',
  data: {
    labels: ['Academic', 'Non-academic', 'Administrator', 'Others'], // Fixed typo
    datasets: [{
      label: 'Employees',
      data: [2500, 6000, 2050, 1900],
      backgroundColor: [
        'rgba(45,115,99,1)',
        'rgba(50,162,235,1)',
        'rgba(225,206,86,1)',
        'rgba(120,46,139,1)'
      ],
      borderColor: [
        'rgba(45,115,99,1)',
        'rgba(50,162,235,1)',
        'rgba(225,206,86,1)',
        'rgba(120,46,139,1)'
      ],
      borderWidth: 1
    }]
  },
  options: {
    responsive: true
  }
});

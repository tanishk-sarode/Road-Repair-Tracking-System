function viewReport() {
    const reportContainer = document.getElementById('reportContainer');
    
    // Simulate a report generation
    const report = `
      <h3>Monthly Report</h3>
      <p><strong>Total Complaints:</strong> 30</p>
      <p><strong>Resolved Complaints:</strong> 20</p>
      <p><strong>Pending Complaints:</strong> 10</p>
      <p><strong>Total Resources Used:</strong> 80 Machines, 40 Personnel</p>
    `;
    
    // Display the generated report
    reportContainer.innerHTML = report;
  }
  
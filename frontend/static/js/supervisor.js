const complaintsContainer = document.getElementById('complaintsContainer');

// Dummy complaints from supervised area
let complaints = [
  { id: 1, title: "Broken Streetlight", desc: "Streetlight not working in Block C", area: "Block C", accepted: false },
  { id: 2, title: "Water Leakage", desc: "Main pipeline leaking in Sector 4", area: "Sector 4", accepted: false }
];

function renderComplaints() {
  complaintsContainer.innerHTML = '';

  complaints.forEach((complaint, index) => {
    if (complaint.accepted) return;

    const div = document.createElement('div');
    div.className = 'complaint';

    div.innerHTML = `
      <h3>${complaint.title}</h3>
      <p>${complaint.desc}</p>
      <p><strong>Area:</strong> ${complaint.area}</p>
      <input type="text" placeholder="Type of Work" class="typeInput" />
      <input type="number" placeholder="No. of Machines" class="machineInput" />
      <input type="number" placeholder="No. of Personnel" class="personnelInput" />
      <select class="priorityInput">
        <option value="" disabled selected>Select Priority</option>
        <option value="1">1 (High)</option>
        <option value="2">2 (Medium)</option>
        <option value="3">3 (Low)</option>
      </select>
      <button class="accept-btn" onclick="acceptComplaint(${index}, this)">Accept</button>
    `;

    complaintsContainer.appendChild(div);
  });
}

function acceptComplaint(index, btn) {
  const parent = btn.parentElement;
  const type = parent.querySelector('.typeInput').value.trim();
  const machines = parent.querySelector('.machineInput').value.trim();
  const personnel = parent.querySelector('.personnelInput').value.trim();
  const priority = parent.querySelector('.priorityInput').value;

  if (!type || !machines || !personnel || !priority) {
    alert("Please fill all fields before accepting!");
    return;
  }

  complaints[index].accepted = true;
  complaints[index].details = {
    type,
    machines: parseInt(machines),
    personnel: parseInt(personnel),
    priority: parseInt(priority)
  };

  alert("Complaint Accepted!");
  renderComplaints();
}

renderComplaints();

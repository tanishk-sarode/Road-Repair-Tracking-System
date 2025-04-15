// const form = document.getElementById('newComplaintForm');
// const list = document.getElementById('complaintList');

// let complaints = [
//   { title: 'Streetlight not working', desc: 'Streetlight near block A is off', location: 'Block A' },
//   { title: 'Water leakage', desc: 'Pipe leak near park', location: 'Central Park' }
// ];

// function renderComplaints() {
//   list.innerHTML = '';
//   complaints.forEach((c, index) => {
//     const li = document.createElement('li');

//     li.innerHTML = `
//       <input type="text" value="${c.title}" />
//       <textarea>${c.desc}</textarea>
//       <input type="text" value="${c.location}" />
//       <button class="edit-btn" onclick="updateComplaint(${index}, this)">Save</button>
//     `;

//     list.appendChild(li);
//   });
// }

// function updateComplaint(index, btn) {
//   const inputs = btn.parentElement.querySelectorAll('input, textarea');
//   complaints[index] = {
//     title: inputs[0].value,
//     desc: inputs[1].value,
//     location: inputs[2].value
//   };
//   alert('Complaint updated!');
// }

// form.addEventListener('submit', (e) => {
//   e.preventDefault();
//   const title = document.getElementById('title').value;
//   const desc = document.getElementById('description').value;
//   const location = document.getElementById('location').value;

//   complaints.push({ title, desc, location });
//   form.reset();
//   renderComplaints();
// });

// renderComplaints();

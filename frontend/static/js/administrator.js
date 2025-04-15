let totalMachines = 100;
let totalPersonnel = 50;

function updateResource(type, value) {
  if (type === 'machines') {
    totalMachines = value;
    document.getElementById('totalMachines').innerText = totalMachines;
  } else if (type === 'personnel') {
    totalPersonnel = value;
    document.getElementById('totalPersonnel').innerText = totalPersonnel;
  }
}

function editResource(type) {
  const newValue = prompt(`Enter new value for total ${type === 'machines' ? 'Machines' : 'Personnel'}:`, type === 'machines' ? totalMachines : totalPersonnel);
  
  if (newValue && !isNaN(newValue) && newValue >= 0) {
    updateResource(type, newValue);
  } else {
    alert("Please enter a valid number greater than or equal to 0.");
  }
}

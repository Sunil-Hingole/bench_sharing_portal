// form-handler.js

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('submitButton').addEventListener('click', function() {
        const name = document.getElementById('name').value;
        const resoursetypeid = document.getElementById('resoursetypeid').value;
        const resoursetypeText = document.getElementById('resoursetypeid').options[document.getElementById('resoursetypeid').selectedIndex].text;
        const description = document.getElementById('description').value;
        const available_from = document.getElementById('available_from').value;
        const booked_by = document.getElementById('booked_by').value;
        const booked_at = document.getElementById('booked_at').value;

        if (name && resoursetypeid && description && available_from) {
            const table = document.getElementById('recordsTable').getElementsByTagName('tbody')[0];
            const newRow = table.insertRow();

            newRow.insertCell(0).innerText = name;
            newRow.insertCell(1).innerText = resoursetypeText;
            newRow.insertCell(2).innerText = description;
            newRow.insertCell(3).innerText = available_from;
            newRow.insertCell(4).innerText = booked_by;
            newRow.insertCell(5).innerText = booked_at;

            document.getElementById('resourceForm').reset();
        } else {
            alert('Please fill out all required fields.');
        }
    });
});

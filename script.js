document.addEventListener('DOMContentLoaded', () => {
    const tableContainer = document.getElementById('periodic-table-container');
    const detailsContainer = document.getElementById('element-details-container');
    const defaultDetailsContent = `
        <h2>Element Details</h2>
        <p>Click on an element to see its details.</p>
    `;

    let elementsData = []; // Initialize as an empty array

    function displayElementDetails(element) {
        if (element) {
            detailsContainer.innerHTML = `
                <h2>${element.name} (${element.symbol})</h2>
                <p><strong>Atomic Number:</strong> ${element.atomicNumber}</p>
                <p><strong>Atomic Mass:</strong> ${element.mass}</p>
                <p><strong>Type:</strong> ${element.type}</p>
                <p><strong>Description:</strong> ${element.description || 'No description available.'}</p>
            `;
        } else {
            detailsContainer.innerHTML = defaultDetailsContent;
        }
    }

    function createPeriodicTable(elements) {
        tableContainer.innerHTML = ''; // Clear any existing content

        elements.forEach(element => {
            const elementDiv = document.createElement('div');
            elementDiv.classList.add('element');
            // Convert type to lowercase and replace spaces with hyphens for CSS class
            elementDiv.classList.add(element.type.toLowerCase().replace(/ /g, '-')); 
            
            // Use row and column data for positioning
            elementDiv.style.gridRowStart = element.row;
            elementDiv.style.gridColumnStart = element.column;

            elementDiv.innerHTML = `
                <div class="atomic-number">${element.atomicNumber}</div>
                <div class="symbol">${element.symbol}</div>
                <div class="name">${element.name}</div>
            `;

            elementDiv.addEventListener('click', () => {
                displayElementDetails(element);
            });

            tableContainer.appendChild(elementDiv);
        });
    }

    // Initial setup
    displayElementDetails(null); // Show default message

    // Fetch element data from elements.json
    fetch('elements.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            elementsData = data;
            createPeriodicTable(elementsData);
        })
        .catch(error => {
            console.error('Error fetching element data:', error);
            tableContainer.innerHTML = '<p>Error loading elements. Please try again later.</p>';
        });
});

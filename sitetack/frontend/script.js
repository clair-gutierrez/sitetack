function submitData() {
    var formData = {
        ptm: document.getElementById('ptm').value,
        label: document.getElementById('label').value,
        organism: document.getElementById('organism').value,
        text: document.getElementById('text').value
    };

    fetch('/submit/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => {
        // Check if the response is ok (status in the range 200-299)
        if (!response.ok) {
            // If not ok, return the response as JSON to process the error
            return response.json().then(errorData => {
                throw errorData; // Throw an error with the error data
            });
        }
        // If response is ok, return it as JSON
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        document.getElementById('thresholdControl').style.display = 'block';
        window.originalData = data;
        displayResultsWithHighlighting(data, parseFloat(document.getElementById('threshold').value));
        createJsonDownloadLink(data);
        createCSVDownloadLink(data);
    })
    .catch((error) => {
        console.error('Error:', error);
        // Display the error message on the webpage
        displayErrorMessage(error); // Implement this function to show the error
    });
}

function loadExample() {
    const fastaExample = `>RNase_1
KESRAKKFQRQHMDSDSSPSSSSTYCNQMMRRRNMTQGRCKPVNTFVHEPLVDVQNVCFQ
QEKVTCKNGQGNCYKSNSSMHITDCRLTNGSRYPNCAYRTSPKERHIIVACEGSPYVPVH
FDASVEDST`;
    document.getElementById('text').value = fastaExample;
}


function displayErrorMessage(error) {
    let errorMessage = "An error occurred.";
    if (error.detail && error.detail.length > 0) {
        errorMessage = error.detail.map(e => e.msg).join('\n');
    }
    
    // Create a Bootstrap alert div and set its content
    const alertDiv = document.createElement('div');
    alertDiv.classList.add('alert', 'alert-danger');
    alertDiv.setAttribute('role', 'alert');
    alertDiv.textContent = errorMessage;
    
    // Clear previous messages and append the new one
    const resultsElement = document.getElementById('results');
    resultsElement.innerHTML = ''; // Clear previous content
    resultsElement.appendChild(alertDiv); // Append the new alert div
}

function jsonToCSV(jsonData) {
    // Define CSV headers
    const csvHeaders = 'sequence name,site,amino acid,probability\n';
    // Convert JSON data to CSV
    let csvRows = jsonData.sequence_predictions.flatMap(seqPrediction => 
        seqPrediction.site_predictions.map(site => 
            `${seqPrediction.sequence_name},${site.site},${site.amino_acid},${site.probability.toFixed(4)}`
        )
    ).join('\n');

    return csvHeaders + csvRows;
}

function createCSVDownloadLink(data) {
    const csvString = jsonToCSV(data);
    const blob = new Blob([csvString], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);

    // Remove any existing CSV download links
    const existingLink = document.getElementById('downloadCSVLink');
    if (existingLink) {
        existingLink.remove();
    }

    // Create download link and append it to the body or a specific element
    const link = document.createElement('a');
    link.id = 'downloadCSVLink'; // Assign an ID for potential removal or styling
    link.href = url;
    link.download = 'predictionResults.csv'; // Suggest a filename for the download
    link.textContent = 'Download CSV Data'; // Text for the link
    link.classList.add('btn', 'btn-success', 'mt-3', 'button-spacing'); // Adds Bootstrap button classes

    // Append the link to the new container
    document.getElementById('downloadButtonsContainer').appendChild(link);
}

function createJsonDownloadLink(data) {
    const jsonString = JSON.stringify(data, null, 2); // Beautify the JSON string
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    // Remove any existing download links
    const existingLink = document.getElementById('downloadLink');
    if (existingLink) {
        existingLink.remove();
    }

    // Create download link and append it to the body or a specific element
    const link = document.createElement('a');
    link.id = 'downloadLink'; // Assign an ID for potential removal or styling
    link.href = url;
    link.download = 'predictionResults.json'; // Suggest a filename for the download
    link.textContent = 'Download JSON Data'; // Text for the link
    link.classList.add('btn', 'btn-info', 'mt-3', 'button-spacing'); // Adds Bootstrap button classes

    // Append the link to the new container
    document.getElementById('downloadButtonsContainer').appendChild(link);
}

function displayResultsWithHighlighting(data, threshold) {
    let formattedResults = '';
    data.sequence_predictions.forEach(seqPrediction => {
        // Process each sequence to potentially highlight certain amino acids
        let sequenceWithHighlights = highlightSequence(seqPrediction.sequence, seqPrediction.site_predictions, threshold);
        formattedResults += `Sequence Name: ${seqPrediction.sequence_name}\nSequence: ${sequenceWithHighlights}\n\n`;
    });
    document.getElementById('results').innerHTML = formattedResults;
}

function highlightSequence(sequence, sitePredictions, threshold) {
    // Convert sequence into an array of characters for easy manipulation
    let sequenceChars = sequence.split('');
    // Iterate over site predictions and apply highlights as needed
    sitePredictions.forEach(site => {
        if (site.probability > threshold) {
            // Wrap the character in a span with a style for highlighting
            sequenceChars[site.site - 1] = `<span class="bg-warning">${sequenceChars[site.site - 1]}</span>`; // Uses Bootstrap's warning background color
        }
    });
    // Join the characters back into a string and return
    return sequenceChars.join('');
}

document.getElementById('loadExampleLink').addEventListener('click', loadExample);

document.getElementById('threshold').addEventListener('input', function() {
    document.getElementById('thresholdValue').textContent = this.value;
    if (window.originalData) { // Check if the original data is available
        displayResultsWithHighlighting(window.originalData, parseFloat(this.value));
    }
});


// Chemical structures for each PTM, cropped from Figure_S1.2 and served out of
// /frontend/structures/. Keyed by PtmKind member name, which is what the dropdown
// puts in option.value (see setupDropdown below) and which differs from the display
// name for several PTMs -- e.g. N6_ACETYLATION_K is shown as "Acetylation (K)".
const PTM_STRUCTURES = {
    PHOSPHORYLATION_ST: [
        { file: 'phospho-S.png', caption: 'Serine (S)' },
        { file: 'phospho-T.png', caption: 'Threonine (T)' },
    ],
    PHOSPHORYLATION_Y: [
        { file: 'phospho-Y.png', caption: 'Tyrosine (Y)' },
    ],
    N_LINKED_GLYCOSYLATION_N: [
        { file: 'nglyc-N.png', caption: 'Asparagine (N)' },
    ],
    O_LINKED_GLYCOSYLATION_ST: [
        { file: 'oglyc-S-GlcNAc.png', caption: 'Ser-GlcNAc' },
        { file: 'oglyc-T-GlcNAc.png', caption: 'Thr-GlcNAc' },
        { file: 'oglyc-S-GalNAc.png', caption: 'Ser-GalNAc' },
        { file: 'oglyc-T-GalNAc.png', caption: 'Thr-GalNAc' },
    ],
    UBIQUITINATION_K: [
        { file: 'ubiquitin-K.png', caption: 'Lysine (K)' },
    ],
    SUMOYLATION_K: [
        { file: 'sumo-K.png', caption: 'Lysine (K)' },
    ],
    N6_ACETYLATION_K: [
        { file: 'acetyl-K.png', caption: 'Lysine (K)' },
    ],
    METHYLATION_K: [
        { file: 'methyl-K-mono.png', caption: 'Monomethyl' },
        { file: 'methyl-K-di.png', caption: 'Dimethyl' },
        { file: 'methyl-K-tri.png', caption: 'Trimethyl' },
    ],
    METHYLATION_R: [
        { file: 'methyl-R-mono.png', caption: 'Monomethyl' },
        { file: 'methyl-R-adma.png', caption: 'Asymmetric dimethyl' },
        { file: 'methyl-R-sdma.png', caption: 'Symmetric dimethyl' },
    ],
    PYRROLIDONE_CARBOXYLIC_ACID_Q: [
        { file: 'pyroglutamyl-Q.png', caption: 'Glutamine (Q)' },
    ],
    S_PALMITOYLATION_C: [
        { file: 'palmitoyl-C.png', caption: 'Cysteine (C)' },
    ],
    HYDROXYPROLINE_P: [
        { file: 'hydroxy-P.png', caption: 'Proline (P)' },
    ],
    HYDROXYLYSINE_K: [
        { file: 'hydroxy-K.png', caption: 'Lysine (K)' },
    ],
};

const PTM_STRUCTURE_PATH = '/frontend/structures/';

function showStructureModal(src, title) {
    const image = document.getElementById('ptmStructureModalImage');
    const label = document.getElementById('ptmStructureModalLabel');
    if (!image || !label) {
        console.warn('sitetack: missing structure modal markup (stale cached page?)');
        return;
    }
    // Bootstrap's JS drives the modal. If the CDN failed the thumbnails are still
    // usable, so degrade quietly rather than throwing.
    if (typeof jQuery === 'undefined' || !jQuery.fn || !jQuery.fn.modal) {
        console.warn('sitetack: Bootstrap modal unavailable; cannot enlarge structure');
        return;
    }
    image.src = src;
    image.alt = 'Chemical structure of ' + title;
    label.textContent = title;
    jQuery('#ptmStructureModal').modal('show');
}

// Render the chemical structures for the selected PTM. Called by setupDropdown on
// page load and on every change of the PTM dropdown.
function renderPtmStructures(ptmKey, ptmName) {
    const container = document.getElementById('ptm_structures');
    if (!container) {
        console.warn('sitetack: missing element #ptm_structures (stale cached page?)');
        return;
    }
    container.innerHTML = '';

    const structures = PTM_STRUCTURES[ptmKey];
    if (!structures) {
        return;
    }

    structures.forEach(structure => {
        const figure = document.createElement('figure');
        figure.className = 'ptm-structure';

        const title = structure.caption
            ? `${ptmName} — ${structure.caption}`
            : ptmName;

        const image = document.createElement('img');
        image.src = PTM_STRUCTURE_PATH + structure.file;
        image.alt = 'Chemical structure of ' + title;
        image.title = 'Click to enlarge';
        // Drop the figure entirely rather than leaving a broken-image icon.
        image.onerror = () => figure.remove();
        image.addEventListener('click', () => showStructureModal(image.src, title));
        figure.appendChild(image);

        // A caption only earns its place when it tells two structures apart. For
        // single-structure PTMs the dropdown label already names the residue.
        if (structures.length > 1) {
            const caption = document.createElement('figcaption');
            caption.textContent = structure.caption;
            figure.appendChild(caption);
        }

        container.appendChild(figure);
    });
}


document.addEventListener('DOMContentLoaded', function () {
// Generalized function to initialize the dropdowns and their descriptions.
// onSelect is optional and runs only for dropdowns that need extra work when the
// selection changes -- currently just the PTM one, which renders structures.
function setupDropdown(endpoint, selectElementId, descriptionElementId, onSelect) {
    const selectElement = document.getElementById(selectElementId);
    const descriptionElement = document.getElementById(descriptionElementId);
    // Cache the payload fetched below so that changing the selection does not
    // re-request the endpoint every single time.
    let entries = null;

    // Function to fetch data (organisms/labels) and populate the select dropdown
    function fetchData() {
        fetch(endpoint)
            .then(response => response.json())
            .then(data => {
                entries = data;
                for (const key in data) {
                    if (data.hasOwnProperty(key)) {
                        const option = document.createElement('option');
                        option.value = key;
                        option.textContent = data[key].name;
                        selectElement.appendChild(option);
                    }
                }
                // Update description for the initially selected option
                updateDescription();
            })
            .catch(error => console.error(`Error fetching data from ${endpoint}:`, error));
    }

    // Function to update the description based on the currently selected option
    function updateDescription() {
        if (!entries) {
            return;
        }
        const selectedValue = selectElement.value;
        const entry = entries[selectedValue];
        if (!entry) {
            return;
        }
        descriptionElement.textContent = entry.description;
        if (onSelect) {
            onSelect(selectedValue, entry.name);
        }
    }

    // Initial fetch of data to populate the select element
    fetchData();

    // Event listener to update the description when a new option is selected
    selectElement.addEventListener('change', updateDescription);
}

// Setup for the PTM dropdown, which also renders the PTM's chemical structures
setupDropdown('/ptms', 'ptm', 'ptm_description', renderPtmStructures);

// Setup for the organisms dropdown
setupDropdown('/organisms', 'organism', 'organism_description');

// Setup for the labels dropdown
setupDropdown('/labels', 'label', 'label_description');
});

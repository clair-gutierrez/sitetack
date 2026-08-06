// Frontend for the hidden pyrophosphorylation page.
//
// All fetch URLs are RELATIVE so they resolve under the page's unguessable
// prefix (e.g. /pyrophos-<token>/submit/) without hardcoding the token here.
// The page is always served with a trailing slash, so relative paths are safe.
//
// Every submission returns three scores per site -- one from each cohort model
// (general / ck2 / other) -- plus a "routed" value picking the cohort matching
// the site's own +3 motif. The charts are drawn as inline SVG rather than with a
// plotting library: the server pins an old dependency set, and an SVG the user
// can right-click and save is the whole requirement here.

var COHORT_COLOURS = {
    general: '#4C72B0',
    ck2: '#C44E52',
    other: '#55A868',
    routed: '#8172B2'
};

var COHORT_ORDER = ['general', 'ck2', 'other'];

function submitData() {
    var formData = {
        model: document.getElementById('model').value,
        text: document.getElementById('text').value
    };

    fetch('submit/', {
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
        document.getElementById('viewControls').style.display = 'block';
        window.originalData = data;
        renderAll(data);
        createJsonDownloadLink(data);
        createCSVDownloadLink(data);
    })
    .catch((error) => {
        console.error('Error:', error);
        // Display the error message on the webpage
        displayErrorMessage(error); // Implement this function to show the error
    });
}

function renderAll(data) {
    var threshold = parseFloat(document.getElementById('threshold').value);
    var cohort = document.getElementById('highlightCohort').value;
    displayResultsWithHighlighting(data, threshold, cohort);
    drawCharts(data, threshold);
    drawTables(data, threshold);
}

function scoreFor(site, cohort) {
    return cohort === 'routed' ? site.routed : site.scores[cohort];
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
    document.getElementById('charts').innerHTML = '';
    document.getElementById('tables').innerHTML = '';
}

function jsonToCSV(jsonData) {
    // One row per site, carrying every cohort's score so the CSV is a complete
    // record of the submission.
    const csvHeaders = 'sequence name,site,amino acid,ck2 motif,general,ck2,other,routed\n';
    let csvRows = jsonData.sequences.flatMap(seq =>
        seq.sites.map(site =>
            [
                seq.sequence_name,
                site.site,
                site.amino_acid,
                site.is_ck2_motif,
                site.scores.general.toFixed(4),
                site.scores.ck2.toFixed(4),
                site.scores.other.toFixed(4),
                site.routed.toFixed(4)
            ].join(',')
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

function displayResultsWithHighlighting(data, threshold, cohort) {
    let formattedResults = '';
    data.sequences.forEach(seq => {
        let sequenceWithHighlights = highlightSequence(seq.sequence, seq.sites, threshold, cohort);
        formattedResults += `Sequence Name: ${seq.sequence_name}\nSequence: ${sequenceWithHighlights}\n\n`;
    });
    document.getElementById('results').innerHTML = formattedResults;
}

function highlightSequence(sequence, sites, threshold, cohort) {
    // Convert sequence into an array of characters for easy manipulation
    let sequenceChars = sequence.split('');
    sites.forEach(site => {
        if (scoreFor(site, cohort) > threshold) {
            // Wrap the character in a span with a style for highlighting
            sequenceChars[site.site - 1] = `<span class="bg-warning">${sequenceChars[site.site - 1]}</span>`;
        }
    });
    // Join the characters back into a string and return
    return sequenceChars.join('');
}

// ---------------------------------------------------------------------------
// Charts
// ---------------------------------------------------------------------------

function svgElement(name, attributes) {
    var node = document.createElementNS('http://www.w3.org/2000/svg', name);
    for (var key in attributes) {
        if (attributes.hasOwnProperty(key)) {
            node.setAttribute(key, attributes[key]);
        }
    }
    return node;
}

function drawCharts(data, threshold) {
    var container = document.getElementById('charts');
    container.innerHTML = '';

    data.sequences.forEach(function (seq, index) {
        var card = document.createElement('div');
        card.classList.add('card', 'mb-4');

        var header = document.createElement('div');
        header.classList.add('card-header', 'py-2');
        header.innerHTML = '<strong>' + seq.sequence_name + '</strong> &mdash; ' +
            seq.sites.length + ' target sites, ' +
            seq.sites.filter(function (s) { return s.is_ck2_motif; }).length + ' CK2-motif';
        card.appendChild(header);

        var body = document.createElement('div');
        body.classList.add('card-body');
        var svg = buildChart(seq, threshold);
        body.appendChild(svg);
        body.appendChild(buildChartDownload(svg, seq.sequence_name, index));
        card.appendChild(body);

        container.appendChild(card);
    });
}

function buildChart(seq, threshold) {
    var width = 900;
    var height = 260;
    var margin = { top: 16, right: 16, bottom: 40, left: 46 };
    var plotWidth = width - margin.left - margin.right;
    var plotHeight = height - margin.top - margin.bottom;
    var length = seq.sequence.length;

    var svg = svgElement('svg', {
        width: '100%',
        viewBox: '0 0 ' + width + ' ' + height,
        preserveAspectRatio: 'xMidYMid meet',
        style: 'background: #fff;'
    });

    function xFor(site) {
        return margin.left + (length > 1 ? (site - 1) / (length - 1) : 0.5) * plotWidth;
    }
    function yFor(score) {
        return margin.top + (1 - score) * plotHeight;
    }

    // Axes and gridlines.
    [0, 0.25, 0.5, 0.75, 1].forEach(function (value) {
        var y = yFor(value);
        svg.appendChild(svgElement('line', {
            x1: margin.left, x2: margin.left + plotWidth, y1: y, y2: y,
            stroke: '#e6e6e6', 'stroke-width': 1
        }));
        var label = svgElement('text', {
            x: margin.left - 8, y: y + 4, 'text-anchor': 'end',
            'font-size': 10, fill: '#666'
        });
        label.textContent = value.toFixed(2);
        svg.appendChild(label);
    });

    // Threshold line.
    svg.appendChild(svgElement('line', {
        x1: margin.left, x2: margin.left + plotWidth,
        y1: yFor(threshold), y2: yFor(threshold),
        stroke: '#999', 'stroke-width': 1, 'stroke-dasharray': '4 3'
    }));

    // One polyline per cohort, plus a marker at each site.
    COHORT_ORDER.forEach(function (cohort) {
        var points = seq.sites.map(function (site) {
            return xFor(site.site) + ',' + yFor(site.scores[cohort]);
        }).join(' ');
        svg.appendChild(svgElement('polyline', {
            points: points, fill: 'none',
            stroke: COHORT_COLOURS[cohort], 'stroke-width': 1.6, 'stroke-opacity': 0.85
        }));
        seq.sites.forEach(function (site) {
            var marker = svgElement('circle', {
                cx: xFor(site.site), cy: yFor(site.scores[cohort]), r: 2.6,
                fill: COHORT_COLOURS[cohort], 'fill-opacity': 0.9
            });
            var title = svgElement('title', {});
            title.textContent = site.amino_acid + site.site +
                ' (' + (site.is_ck2_motif ? 'CK2 motif' : 'non-CK2') + ')  ' +
                cohort + ' = ' + site.scores[cohort].toFixed(4);
            marker.appendChild(title);
            svg.appendChild(marker);
        });
    });

    // Ticks along the bottom mark CK2-motif sites, so the routing is visible.
    seq.sites.forEach(function (site) {
        svg.appendChild(svgElement('line', {
            x1: xFor(site.site), x2: xFor(site.site),
            y1: margin.top + plotHeight + 2, y2: margin.top + plotHeight + 8,
            stroke: site.is_ck2_motif ? COHORT_COLOURS.ck2 : '#bbb', 'stroke-width': 1.4
        }));
    });

    // Axis frame.
    svg.appendChild(svgElement('line', {
        x1: margin.left, x2: margin.left + plotWidth,
        y1: margin.top + plotHeight, y2: margin.top + plotHeight,
        stroke: '#333', 'stroke-width': 1
    }));
    svg.appendChild(svgElement('line', {
        x1: margin.left, x2: margin.left,
        y1: margin.top, y2: margin.top + plotHeight, stroke: '#333', 'stroke-width': 1
    }));

    var xLabel = svgElement('text', {
        x: margin.left + plotWidth / 2, y: height - 6,
        'text-anchor': 'middle', 'font-size': 11, fill: '#333'
    });
    xLabel.textContent = 'Residue position (1 - ' + length + ');  ticks below the axis mark CK2-motif sites';
    svg.appendChild(xLabel);

    var yLabel = svgElement('text', {
        x: 12, y: margin.top + plotHeight / 2,
        'text-anchor': 'middle', 'font-size': 11, fill: '#333',
        transform: 'rotate(-90 12 ' + (margin.top + plotHeight / 2) + ')'
    });
    yLabel.textContent = 'Predicted probability';
    svg.appendChild(yLabel);

    // Legend.
    COHORT_ORDER.forEach(function (cohort, i) {
        var x = margin.left + 10 + i * 130;
        svg.appendChild(svgElement('line', {
            x1: x, x2: x + 18, y1: margin.top + 8, y2: margin.top + 8,
            stroke: COHORT_COLOURS[cohort], 'stroke-width': 2.4
        }));
        var text = svgElement('text', {
            x: x + 24, y: margin.top + 12, 'font-size': 11, fill: '#333'
        });
        text.textContent = cohort;
        svg.appendChild(text);
    });

    return svg;
}

function buildChartDownload(svg, sequenceName, index) {
    var link = document.createElement('a');
    link.textContent = 'Download chart (SVG)';
    link.classList.add('btn', 'btn-outline-secondary', 'btn-sm', 'mt-2');
    link.href = URL.createObjectURL(
        new Blob([new XMLSerializer().serializeToString(svg)], { type: 'image/svg+xml' })
    );
    link.download = 'pyrophos_' + (sequenceName || ('sequence' + index)).replace(/[^\w.-]+/g, '_') + '.svg';
    return link;
}

// ---------------------------------------------------------------------------
// Per-site table
// ---------------------------------------------------------------------------

function drawTables(data, threshold) {
    var container = document.getElementById('tables');
    container.innerHTML = '';

    data.sequences.forEach(function (seq) {
        var above = seq.sites.filter(function (site) {
            return COHORT_ORDER.some(function (c) { return site.scores[c] > threshold; });
        });

        var heading = document.createElement('h5');
        heading.classList.add('mt-4');
        heading.textContent = seq.sequence_name + ' — sites above ' + threshold.toFixed(2) +
            ' in any model (' + above.length + ')';
        container.appendChild(heading);

        if (above.length === 0) {
            var empty = document.createElement('p');
            empty.classList.add('text-muted');
            empty.textContent = 'No sites pass the threshold in any of the three models.';
            container.appendChild(empty);
            return;
        }

        var table = document.createElement('table');
        table.classList.add('table', 'table-sm', 'table-striped');
        table.innerHTML =
            '<thead><tr><th>Site</th><th>Motif</th>' +
            COHORT_ORDER.map(function (c) { return '<th>' + c + '</th>'; }).join('') +
            '<th>routed</th></tr></thead>';

        var tbody = document.createElement('tbody');
        above.forEach(function (site) {
            var cells = COHORT_ORDER.map(function (c) {
                var strong = site.scores[c] > threshold;
                return '<td' + (strong ? ' class="font-weight-bold"' : '') + '>' +
                    site.scores[c].toFixed(4) + '</td>';
            }).join('');
            var row = document.createElement('tr');
            row.innerHTML =
                '<td>' + site.amino_acid + site.site + '</td>' +
                '<td>' + (site.is_ck2_motif ? 'CK2' : 'non-CK2') + '</td>' +
                cells +
                '<td>' + site.routed.toFixed(4) + '</td>';
            tbody.appendChild(row);
        });
        table.appendChild(tbody);
        container.appendChild(table);
    });
}

// ---------------------------------------------------------------------------
// Wiring
// ---------------------------------------------------------------------------

document.getElementById('loadExampleLink').addEventListener('click', loadExample);

document.getElementById('threshold').addEventListener('input', function() {
    document.getElementById('thresholdValue').textContent = this.value;
    if (window.originalData) {
        renderAll(window.originalData);
    }
});

document.getElementById('highlightCohort').addEventListener('change', function () {
    if (window.originalData) {
        renderAll(window.originalData);
    }
});


document.addEventListener('DOMContentLoaded', function () {
    // Populate the label-variant dropdown and keep its description in sync.
    const selectElement = document.getElementById('model');
    const descriptionElement = document.getElementById('model_description');
    let modelData = {};

    function updateDescription() {
        const selected = modelData[selectElement.value];
        descriptionElement.textContent = selected ? selected.description : '';
    }

    fetch('models')
        .then(response => response.json())
        .then(data => {
            modelData = data.models || data;
            for (const key in modelData) {
                if (modelData.hasOwnProperty(key)) {
                    const option = document.createElement('option');
                    option.value = key;
                    option.textContent = modelData[key].name;
                    selectElement.appendChild(option);
                }
            }
            updateDescription();

            const legend = document.getElementById('cohortLegend');
            if (data.cohorts && legend) {
                legend.innerHTML = data.cohorts.map(function (cohort) {
                    return '<div><span style="display:inline-block;width:10px;height:10px;' +
                        'background:' + (COHORT_COLOURS[cohort.key] || '#666') + ';"></span> ' +
                        '<strong>' + cohort.name + '</strong> &mdash; ' + cohort.description +
                        '</div>';
                }).join('');
            }
        })
        .catch(error => console.error('Error fetching models:', error));

    selectElement.addEventListener('change', updateDescription);
});

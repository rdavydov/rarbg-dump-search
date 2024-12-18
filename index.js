document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('theme-switch');
    const body = document.body;

    // Check if the theme preference exists in localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        // Apply the saved theme preference
        body.classList.add(savedTheme);
        themeToggle.checked = savedTheme === 'theme-night';
    }

    themeToggle.addEventListener('change', function () {
        if (this.checked) {
            body.classList.remove('theme-day');
            body.classList.add('theme-night');
            // Save the theme preference to localStorage
            localStorage.setItem('theme', 'theme-night');
        } else {
            body.classList.remove('theme-night');
            body.classList.add('theme-day');
            // Save the theme preference to localStorage
            localStorage.setItem('theme', 'theme-day');
        }
    });

    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const resultsList = document.getElementById('results');
    const resultsHeader = document.getElementById('results-header');

    searchButton.addEventListener('click', function () {
        const query = searchInput.value.trim().replace(/\s/g, ' ');

        if (query) {
            fuzzySearch(query);
        } else displayResults(0);
    });

    searchInput.addEventListener('keyup', function (event) {
        const query = event.target.value.trim().replace(/\s/g, ' ');
        if (event.key === 'Enter')
            if (query) {
                fuzzySearch(query);
            } else displayResults(0);
    });

    function fuzzySearch(query) {
        resultsList.innerHTML = '<p>Searching...</p>';
        resultsHeader.textContent = 'Results';

        const url = decodeURL('aHR0cHM6Ly9yYXJiZy5tb29vLmNvbS8/cT0');
        fetch(url + query)
            .then(response => response.json())
            .then(data => {
                const results = data.results;
                displayResults(results);
            })
            .catch(error => {
                resultsList.innerHTML = `<p>Error searching: ${error}</p>`;
                console.error('Error searching:', error);
            });
    }

    function displayResults(results) {
        resultsList.innerHTML = '';

        if (results.length === 0 || !results) {
            resultsList.innerHTML = '<p>No results found</p>';
        } else {
            resultsHeader.textContent = `Results: ${results.length}`;

            results.forEach(result => {
                const magnetLink = document.createElement('a');
                magnetLink.href = result;
                magnetLink.onclick = function () {
                    this.style.color = "gray";
                }

                const dnStartIndex = result.indexOf('&dn=') + 4;
                const dnEndIndex = result.indexOf('&', dnStartIndex);
                const dn = dnEndIndex !== -1 ? result.substring(dnStartIndex, dnEndIndex) : result.substring(dnStartIndex);

                const li = document.createElement('li');
                li.appendChild(magnetLink);
                resultsList.appendChild(li);

                const magnetEmoji = document.createElement('span');
                magnetEmoji.textContent = '🧲';
                magnetEmoji.className = 'magnet-emoji';

                magnetLink.appendChild(document.createTextNode(dn));
                magnetLink.appendChild(magnetEmoji);
            });
        }
    }

    function decodeURL(encodedURL) {
        const decodedString = atob(encodedURL);
        return decodedString;
    }
});

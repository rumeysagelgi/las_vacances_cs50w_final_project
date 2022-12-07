document.addEventListener('DOMContentLoaded', function() {
    let timeout = null;
    document.querySelector('#search-form').addEventListener('submit', preventSubmit);
    const search = document.querySelector('#search-input');
    search.addEventListener('keyup', function(e) {
        clearTimeout(timeout);
        timeout = setTimeout(function () {
            search_suite(search.value)
        }, 200);
    })
});


function preventSubmit(form) {
    form.preventDefault();
}


function delay(fn, ms) {
    let timer = 0
    return function(...args) {
        clearTimeout(timer)
        timer = setTimeout(fn.bind(this, ...args), ms || 0)
    }
}


function search_suite(address) {
    fetch(`/get_suite?` + new URLSearchParams ({
        suite: address,
    }))
    .then(response => response.json())
    .then(data => {
        document.querySelector('#display').innerHTML = ''
        if (data.suites !== null) {
            load_suites(data);
        }
    })
}


function load_suites(list) {
    const display = document.querySelector('#display');
    display.innerHTML = ''
    list.forEach(element => {
        display.innerHTML = display.innerHTML + `
        <div class="display-item">
                <div class="display-image" onclick="openSuite(${element.id})">
                    <img id=img${element.id} src="${element.image}" alt="${element.title} image">
                </div>
                <div class="display-info">
                    <span class="display-title"><strong>${element.title}</strong></span>
                    <span class="display-address">(${element.address})</span>
                </div>
        </div>
        `;
        document.querySelector(`#img${element.id}`).addEventListener('load', () => resizeImage(document.querySelector(`#img${element.id}`)));
    });
}


function resizeImage(image) {
    const aspectRatio = image.naturalWidth / image.naturalHeight;

    // If image is landscape
    if (aspectRatio > 1) {
        image.style.minWidth = 'unset';
        image.style.maxHeight = '100%';
    };
}


function openSuite(id) {
    let url = window.location.origin
    window.location.href = (`${url}/suite/${id}`);
}

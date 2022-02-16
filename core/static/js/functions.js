function getCars(page) {
    let url = `${page ? page : "?" + (location.search.slice(1) != '' ? location.search.slice(1) : 'page=1')}`
    window.history.pushState({page: "another"}, "another page", `${url}`)
    $.getJSON(`http://127.0.0.1:8000/api/v1/${url}`, function (data) {
        if (!("error" in data)) {
            createCarList(data)
        }
    })
}

function createCarList(data) {
    let firstRow = `<div class="row">`
    let secondRow = `<div class="row">`
    data.results.map((car, i) => {
        if (i < 4) {
            firstRow += `
                    <div class="col-3 div-car">
                        <img src="${car.image}" class="d-block w-100">
                        <h4 class="pl-15 mt-15">${car.brand} ${car.model}</h4>
                        <div class="row mt-15">
                            <div class="col-7 pr-0">
                                <p class="pl-15"><i class="far fa-stop-circle"></i> ${car.exchange}</p>
                            </div>
                            <div class="col-5 pl-0" align="end">
                                <p class="pr-15"><i class="fas fa-gas-pump"></i> ${car.fuel}</p>
                            </div>
                        </div>
                        
                        <div class="row mt-15">
                            <div class="col-6">
                                <p class="pl-15"><i class="far fa-calendar-alt"></i> ${car.year}</p>
                            </div>
                            <div class="col-6" align="end">
                                <p class="pr-15"><i class="fas fa-tachometer-alt"></i> ${car.kms} Km</p>
                            </div>
                        </div>
        
                        <h4 id="price-${car.id}" class="pl-15 bt-5">${formatPrice(car.price)}</h4>
                    </div>
                    `
        } else {
            secondRow += `
                    <div class="col-3 div-car">
                        <img src="${car.image}" class="d-block w-100">
                        <br><h4 class="pl-15">${car.brand} ${car.model}</h4>
                        <div class="row">
                            <div class="col-7 pr-0">
                                <p class="pl-15"><i class="far fa-stop-circle"></i> ${car.exchange}</p>
                            </div>
                            <div class="col-5 pl-0" align="end">
                                <p class="pr-15"><i class="fas fa-gas-pump"></i> ${car.fuel}</p>
                            </div>
                        </div>
                        
                        <div class="row bt-45 wd-100">
                            <div class="col-6">
                                <p class="pl-15"><i class="far fa-calendar-alt"></i> ${car.year}</p>
                            </div>
                            <div class="col-6 pr-0" align="end">
                                <i class="fas fa-tachometer-alt"></i> ${car.kms} Km
                            </div>
                        </div>
        
                        <h4 id="price-${car.id}" class="pl-15 bt-5">${formatPrice(car.price)}</h4>
                    </div>
                    `
        }
    })

    let carsContainer = document.getElementById('container-cars');
    carsContainer.innerHTML = firstRow
    carsContainer.innerHTML += secondRow

    if (data.links.total >= 1) {
        let pag = document.getElementById('paginator');
        let pagProdText = ""
        pagProdText += `
                    <nav aria-label="Page navigation">
                        <ul class="pagination justify-content-center">
                            <li class="page-item ${data.links.previous == null ? "disabled" : ""} ">
                                <a class="page-link" onclick="updateFilter('?page=1')" tabindex="-1" ${data.links.previous === null ? 'aria-disabled="true"' : ''} >&laquo;</a>
                            </li>
                `
        for (let i = 1; i <= data.links.total; i++) {
            pagProdText += `
                        <li class="page-item ${data.links.current === i ? 'active' : ''}"><a class="page-link" onclick="updateFilter('?page=${i}')">${i}</a></li>
                    `
        }

        pagProdText += `
                        <li class="page-item ${data.links.next == null ? "disabled" : ""}">
                            <a class="page-link" onclick="updateFilter('?page=${data.links.total}')">&raquo;</a>
                        </li>
                    </ul>
                </nav>
                `
        pag.innerHTML = pagProdText
    }
}



function formatPrice(price) {
    let newPrice = parseFloat(price).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    return newPrice
}

function updateFilter(page) {
    if (!page) { page = '?page=1' }
    let url = `${page ? page : '?page=1'}${checkOrder() + checkAllFilters()}`
    getCars(url)
}

function checkOrder() {
    let order = document.getElementById('inputOrder').selectedIndex;
    if (order === 1) {
        return '&order=ASC';
    } else if (order === 2) {
        return '&order=DESC';
    }
    return ""
}

function getCategories() {
    $.getJSON(`http://127.0.0.1:8000/api/v1/categorys/`, function (data) {
        if (!("error" in data)) {
            let inputCategory = document.getElementById('inputCategory')
            let txt = '';
            data.map((category, i) => {
                txt += `<option value="${i}">${category.category}</option>`
            })
            inputCategory.innerHTML += txt
        }
    })
}

function getColors() {
    $.getJSON(`http://127.0.0.1:8000/api/v1/colors/`, function (data) {
        if (!("error" in data)) {
            let inputColor = document.getElementById('inputColor')
            let txt = '';
            data.map((color, i) => {
                txt += `<option value="${i}">${color.color}</option>`
            })
            inputColor.innerHTML += txt
        }
    })
}

function getBrands() {
    $.getJSON(`http://127.0.0.1:8000/api/v1/brands/`, function (data) {
        if (!("error" in data)) {
            let inputMarca = document.getElementById('inputMarca');
            let txt = '';
            data.map((car, i) => {
                txt += `<option value="${i}">${car.brand}</option>`
            })
            inputMarca.innerHTML += txt
        }
    })
}

function getModels() {
    let inputMarca = document.getElementById('inputMarca');
    let brand = inputMarca.options[inputMarca.selectedIndex].text;
    $.getJSON(`http://127.0.0.1:8000/api/v1/models/?brand=${brand}`, function (data) {
        if (!("error" in data)) {
            let inputMarca = document.getElementById('inputModel');
            let txt = '<option selected>Selecionar Modelo</option>';
            data.map((car, i) => {
                txt += `<option value="${i}">${car.model}</option>`
            })
            inputMarca.innerHTML = txt
        }
    })
}

function checkState() {
    let radio = document.querySelector('.state>.row');
    let newEnable = radio.querySelector('.new>#flexradioNew').checked;
    let usedEnable = radio.querySelector('.used>#flexradioUsed').checked;

    if (newEnable) {
        return "&state=new"
    } else if (usedEnable) {
        return "&state=used"
    }

    return ""
}

function checkBrand() {
    let brandDiv = document.getElementById('inputMarca');
    if (brandDiv.selectedIndex != 0) {
        return `&brand=${brandDiv.options[brandDiv.selectedIndex].text}`
    }
    return ""
}

function checkModel() {
    let modelDiv = document.getElementById('inputModel');
    if (modelDiv.selectedIndex != 0) {
        return `&model=${modelDiv.options[modelDiv.selectedIndex].text}`
    }
    return ""
}

function checkYear() {
    let minYear = document.getElementById('minYear').value;
    let maxYear = document.getElementById('maxYear').value;

    if (minYear != '' && maxYear != '') {
        return `&year=${minYear}-${maxYear}`
    } else if (minYear != '') {
        return `&year=${minYear}`
    } else if (maxYear != '') {
        return `&year=0-${maxYear}`
    }

    return ""
}

function checkPrice() {
    let minPrice = document.getElementById('minPrice').value;
    let maxPrice = document.getElementById('maxPrice').value;

    if (minPrice != '' && maxPrice != '') {
        return `&price=${minPrice}-${maxPrice}`
    } else if (minPrice != '') {
        return `&price=${minPrice}`
    } else if (maxPrice != '') {
        return `&price=0-${maxPrice}`
    }

    return ""
}

function checkColors() {
    let inputColor = document.getElementById('inputColor');
    if (inputColor.selectedIndex != 0) {
        return `&color=${inputColor.options[inputColor.selectedIndex].text}`
    }
    return ""
}

function checkCategory() {
    let inputCategory = document.getElementById('inputCategory');
    if (inputCategory.selectedIndex != 0) {
        return `&category=${inputCategory.options[inputCategory.selectedIndex].text}`
    }
    return ""
}

function checkExchanges() {
    let manual = document.getElementById('manual').checked;
    let automatico = document.getElementById('automatico').checked;
    let cvt = document.getElementById('cvt').checked;
    let semi = document.getElementById('semi-automatico').checked;
    let txt = ""

    if (manual) {
        txt = `&exchange=manual`
    }

    if (automatico) {
        if (txt != "") {
            txt += `/automatico`
        } else {
            txt = `&exchange=automatico`
        }
    }

    if (cvt) {
        if (txt != "") {
            txt += `/cvt`
        } else {
            txt = `&exchange=cvt`
        }
    }

    if (semi) {
        if (txt != "") {
            txt += `/semi-automatico`
        } else {
            txt = `&exchange=semi-automatico`
        }
    }
    return txt
}

function checkFuel() {
    let diesel = document.getElementById('diesel').checked;
    let gasolina = document.getElementById('gasolina').checked;
    let ag = document.getElementById('ag').checked;
    let alcool = document.getElementById('alcool').checked;
    let txt = ""

    if (diesel) {
        txt = `&fuel=diesel`
    }

    if (gasolina) {
        if (txt != "") {
            txt += `-gasolina`
        } else {
            txt = `&fuel=gasolina`
        }
    }

    if (ag) {
        if (txt != "") {
            txt += `-a/g`
        } else {
            txt = `&fuel=a/g`
        }
    }

    if (alcool) {
        if (txt != "") {
            txt += `-alcool`
        } else {
            txt = `&fuel=alcool`
        }
    }
    return txt
}

function checkDoors() {
    let portas2 = document.getElementById('portas-2').checked;
    let portas3 = document.getElementById('portas-3').checked;
    let portas4 = document.getElementById('portas-4').checked;
    let portas5 = document.getElementById('portas-5').checked;
    let txt = ""

    if (portas2) {
        txt = `&doors=2`
    }

    if (portas3) {
        if (txt != "") {
            txt += `-3`
        } else {
            txt = `&doors=3`
        }
    }

    if (portas4) {
        if (txt != "") {
            txt += `-4`
        } else {
            txt = `&doors=4`
        }
    }

    if (portas5) {
        if (txt != "") {
            txt += `-5`
        } else {
            txt = `&doors=5`
        }
    }
    return txt
}

function checkAllFilters() {
    let txt = ''
    txt = `${checkState()}${checkBrand()}${checkModel()}${checkYear()}${checkPrice()}${checkColors()}${checkCategory()}${checkExchanges()}${checkFuel()}${checkDoors()}`
    return txt
}

function createOfferList() {

    let carrousel = document.getElementById('carouselExampleCaptions');
    let txt = '<ol class="carousel-indicators">';
    let active = `
        <div class="carousel-inner">
            <div class="carousel-item active">
                <div class="row">
    `;
    let deactive = `
        <div class="carousel-item">
            <div class="row">
    `
    
    $.getJSON(`http://127.0.0.1:8000/api/v1/?page=1`, function (data) {
        if (!("error" in data)) {
            txt += `
            <li data-target="#carouselExampleCaptions" data-slide-to="1" class="active"></li>
            <li data-target="#carouselExampleCaptions" data-slide-to="2" class="active"></li>
            `
            data.results.map((car, i) => {
                if (i < 4) {

                    active += `
                        <div class="col-3">
                            <img src="${car.image}" class="d-block w-100">
                            <h5>${car.brand} ${car.model}</h5>
                            <div class="row">
                                <div class="col-4">
                                    <h6>${car.exchange}</h6>
                                </div>
                                <div class="col-4"></div>
                                <div class="col-4" align="end">
                                    <h6>${car.fuel}</h6>
                                </div>
                            </div>
                            <h4>R$ ${car.price} </h4>
                            <div class="row">
                                <div class="col-3">
                                    <h6>${car.year}</h6>
                                </div>
                                <div class="col-5"></div>
                                <div class="col-4" align="center">
                                    ${car.kms} Km
                                </div>
                            </div>
                        </div>
                    `
                } else {
                    deactive += `
                    <div class="col-3">
                        <img src="${car.image}" class="d-block w-100">
                        <h5>${car.brand} ${car.model}</h5>
                        <div class="row">
                            <div class="col-4">
                                <h6>${car.exchange}</h6>
                            </div>
                            <div class="col-4"></div>
                            <div class="col-4" align="end">
                                <h6>${car.fuel}</h6>
                            </div>
                        </div>
                        <h4>R$ ${car.price} </h4>
                        <div class="row">
                            <div class="col-3">
                                <h6>${car.year}</h6>
                            </div>
                            <div class="col-5"></div>
                            <div class="col-4" align="center">
                                ${car.kms} Km
                            </div>
                        </div>
                    </div>
                    `
                }
            })
            txt += `</ol>`
            active += `
                    </div>
                </div>
                    ${deactive}
                    </div>
                </div>
            </div>
            <a class="carousel-control-prev" href="#carouselExampleCaptions" role="button" data-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="sr-only">Previous</span>
            </a>
            <a class="carousel-control-next" href="#carouselExampleCaptions" role="button" data-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="sr-only">Next</span>
            </a>
            `
            txt += active
        carrousel.innerHTML = txt;
        }
    })
}

function getIndexBrands() {
    $.getJSON(`http://127.0.0.1:8000/api/v1/brands/`, function (data) {
        if (!("error" in data)) {
            let inputMarca = document.getElementById('inputMarca');
            let txt = '';
            data.map((car, i) => {
                txt += `<option value="${i}">${car.brand}</option>`
            })
            inputMarca.innerHTML += txt
        }
    })
}

function getIndexModels() {
    let inputMarca = document.getElementById('inputMarca');
    let brand = inputMarca.options[inputMarca.selectedIndex].text;
    $.getJSON(`http://127.0.0.1:8000/api/v1/models/?brand=${brand}`, function (data) {
        if (!("error" in data)) {
            let inputMarca = document.getElementById('inputModel');
            let txt = '<option selected>Selecionar Modelo</option>';
            data.map((car, i) => {
                txt += `<option value="${i}">${car.model}</option>`
            })
            inputMarca.innerHTML = txt
        }
    })
}

function getYearModels() {
    
    let inputYear = document.getElementById('inputYear');
    let txt = '<option selected>Ano..</option>';
    for (var i=22; i>0; i--) {
        txt += `<option value="${i}">${2000+i}</option>`
    }
    inputYear.innerHTML = txt
}

function checkIndexBrand() {
    let brandDiv = document.getElementById('inputMarca');
    if (brandDiv.selectedIndex != 0) {
        return `&brand=${brandDiv.options[brandDiv.selectedIndex].text}`
    }
    return ""
}

function checkIndexModel() {
    let modelDiv = document.getElementById('inputModel');
    if (modelDiv.selectedIndex != 0) {
        return `&model=${modelDiv.options[modelDiv.selectedIndex].text}`
    }
    return ""
}

function checkIndexYear() {
    let modelYear = document.getElementById('inputYear');
    if (modelYear.selectedIndex != 0) {
        return `&year=${modelYear.options[modelYear.selectedIndex].text}-${modelYear.options[modelYear.selectedIndex].text}`
    }
    return ""
}

function searchCars() {
    let url = `http://127.0.0.1:8000/estoque/?page=1${checkIndexBrand()}${checkIndexModel()}${checkIndexYear()}`
    window.location.href = url
}
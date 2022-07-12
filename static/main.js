async function submitForSimulation() {
    let data = {};
    $("#ac-calculate-form").serializeArray().map(function (x) {
        data[x.name] = x.value;
    });

    data = JSON.stringify(data)
    // console.log(data);

    // document.getElementById("ac-calculated-chance").outerHTML = "<div class=\"spinner-border\" role=\"status\" id=\"ac-calculated-chance\"></div>\n";
    document.getElementById("ac-calculated-chance").innerHTML = "<div class=\"spinner-border\" role=\"status\" id=\"ac-calculated-chance\"></div>\n";

    let api_address = "https://hutan-tft-calculator.herokuapp.com/api/tft/simulation"
    if (location.hostname === "localhost" || location.hostname === "127.0.0.1") {
        api_address = "http://127.0.0.1:5000/api/tft/simulation"
    }

    const response = await fetch(api_address, {
        method: "post",
        headers: {"Content-Type": "application/json"},
        body: data
    })

    if (!response.ok) {
        const message = `An error has occured: ${response.status}`;
        throw new Error(message);

    }

    const calculatedResult = await response.json();
    // console.log(calculatedResult)

    // document.getElementById("ac-calculated-chance").outerHTML = "<p id=\"ac-calculated-chance\"></p>\n";
    document.getElementById("ac-calculated-chance").innerHTML = calculatedResult["chance"];

    return false; //don't submit
}

async function submitForCalculation() {
    let data = {};
    $("#ac-calculate-form").serializeArray().map(function (x) {
        data[x.name] = x.value;
    });

    data = JSON.stringify(data)
    // console.log(data);

    // document.getElementById("ac-calculated-chance").outerHTML = "<div class=\"spinner-border\" role=\"status\" id=\"ac-calculated-chance\"></div>\n";
    document.getElementById("ac-calculated-chance").innerHTML = "<div class=\"spinner-border\" role=\"status\" id=\"ac-calculated-chance\"></div>\n";

    let api_address = "https://hutan-tft-calculator.herokuapp.com/api/tft/calculation"
    if (location.hostname === "localhost" || location.hostname === "127.0.0.1") {
        api_address = "http://127.0.0.1:5000/api/tft/calculation"
    }

    const response = await fetch(api_address, {
        method: "post",
        headers: {"Content-Type": "application/json"},
        body: data
    })

    if (!response.ok) {
        const message = `An error has occured: ${response.status}`;
        throw new Error(message);

    }

    const calculatedResult = await response.json();
    // console.log(calculatedResult)

    // document.getElementById("ac-calculated-chance").outerHTML = "<p id=\"ac-calculated-chance\"></p>\n";
    document.getElementById("ac-calculated-chance").innerHTML = calculatedResult["chance"];

    return false; //don't submit
}


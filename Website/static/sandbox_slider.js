// Code for the slider in the sandbox 
// https://refreshless.com/nouislider/ 


let slider = document.getElementById("sandbox_slider");

// Creating slider
noUiSlider.create(slider, {
    start: [25, 75],
    range: {
        min: 0,
        max: 100
    },
    connect: [true, true, true],
    format: wNumb({
        decimals: 0
    })
});

// Range colors
var connect = slider.querySelectorAll(".noUi-connect");
var ids = ["range_f", "range_c", "range_r"];

for (let i = 0; i < connect.length; i++) {
    connect[i].classList.add(ids[i]);
};


// the text elements that shows distribution
let textSpans = [
    document.getElementById("slider_f_value"),
    document.getElementById("slider_c_value"),
    document.getElementById("slider_r_value")
];

// When changing sliders, text is changed accordingly
slider.noUiSlider.on("update", function (values) {
    // Commoners
    textSpans[0].innerHTML = values[1] - values[0];
    // Fake news influencers
    textSpans[1].innerHTML = values[0];
    // Real news influencers
    textSpans[2].innerHTML = 100 - values[1];
});
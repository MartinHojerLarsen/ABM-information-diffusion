// Code for the slider in the sandbox 
// https://refreshless.com/nouislider/ 


let slider = document.getElementById("sandbox_slider");

noUiSlider.create(slider, {
    start: [25, 75],
    range: {
        min: 0,
        max: 100
    },
    connect: [true, true, true],
});


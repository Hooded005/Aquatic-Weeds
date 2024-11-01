document.addEventListener("DOMContentLoaded", function() {
  console.log("Test-Load");
});

const temp =document.getElementById('calculate-button');
temp.addEventListener("input", test());

function test(){
    console.log("Function Called")
};


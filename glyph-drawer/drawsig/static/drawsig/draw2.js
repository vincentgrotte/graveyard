//  author: 

//  TODOs
//  draw2.js -- More shapes

/*
/   GLOBAL VARIABLES
*/
var vowels = ["a", "e", "i", "o", "u"];
var consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z'];
var canvas = document.getElementById("canvas_x");
var ctx = canvas.getContext("2d");
var shape = "9-TS";
var centers = [];

/*                        ----- A SQUARE -----
*
*                [50, 25],      [150, 25],      [250, 25],
*                                
*                
*                [50, 75],       [150, 75],      [250, 75],
*                
*                
*                [50, 125],      [150, 125],     [250, 125],
*
*
*                wqwetrqtwreqtewtqwtuyetiruotyertieryeoryppuotuiyiuopityopuptiydgafgsdgafsdagdgasdfgkjdfhgjkldhldzxcnvxbnzcxncxvbnvmbcvvbnmvbmadsdasdasdaqweqweqweiuyoiutoiutjkgkljcXZCxzlkjgdslfjkgadsoioavshvbvnunkgnbmxfgbvyjuwemjfuvnrhyvbtygbjuhmnikjymkouomkfbdgyfcdk
*
*/

/*
*   Shapes hard-coded as arrays of coordinates
*/
function computeCenters() {
    centers = [];
    var x = 150;
    var y = 75;
    var yd = 50;
    var xd = 100;
    switch (shape) {
        case "9-TS":
            centers = [
                [50,25], [150,25], [250,25], [250,75], [250,125], [150,125], [50,125], [50,75], [x,y]
            ];
            break;
        case "quad":
            centers = [
                [50,25], [250,25], [250,125], [50,125], [50,25], [150,75]   
            ];
            break;
        case "qent":
            centers = [
                [x, y-yd], 
                [x+(yd*zr('s',2)), y+(yd*zr('c',2))],
                [x+(yd*zr('s',4)), y-(yd*zr('c',1))],
                [x-(yd*zr('s',4)), y-(yd*zr('c',1))],
                [x-(yd*zr('s',2)), y+(yd*zr('c',2))],
                [x, y]
            ];
            break;
        case "pent":
            centers = [
                [x, y-yd], 
                [x+(xd*zr('s',2)), y+(yd*zr('c',2))],
                [x+(xd*zr('s',4)), y-(yd*zr('c',1))],
                [x-(xd*zr('s',4)), y-(yd*zr('c',1))],
                [x-(xd*zr('s',2)), y+(yd*zr('c',2))],
                [x, y]
            ];
            break;
    }
}

function zr(trig, x) {
    switch (trig) {
        case "s":
            console.log(Math.sin((x*Math.PI)/5));
            return Math.sin((x*Math.PI)/5);
            break;
        case "c":
            console.log(Math.cos((x*Math.PI)/5));
            return Math.cos((x*Math.PI)/5);
            break;
    }
}

function clearAll() {
    document.getElementById("intent").value = "";
    document.getElementById("intent_novowels").innerHTML = "";
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function drawSigil() {
    var intentNoVowels = [];
    var intentAsChars = document.getElementById("id_intent").value.toLowerCase().split("");
    for (i = 0; i < intentAsChars.length; i++) {
        if (!(vowels.includes(intentAsChars[i])) && (/^[a-zA-Z]+$/.test(intentAsChars[i]))) {
            intentNoVowels.push(intentAsChars[i]);
        }
    }
    document.getElementById("intent_novowels").innerHTML = intentNoVowels.join("").toUpperCase();
    var intent = intentNoVowels.join("");
    computeCenters();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    var initialCenter = getCenter(intent[0]);

    ctx.moveTo(initialCenter[0], initialCenter[1]);
    for (i = 1; i < intent.length; i++) {
        var nextCenter = getCenter(intent[i]);
        ctx.lineTo(nextCenter[0], nextCenter[1]);
    }
    ctx.stroke();
}

function setShape(s) {
    shape = s;
    document.getElementById("shape_status").innerHTML = shape;
}

/*
*   Encode characters as numbers in lexographic order
*/
function getCenter(character) {
    var index = (consonants.indexOf(character) % centers.length);
    return centers[index];
}

//  TODO
//  - Submits intent to backend
function save() {
    var confirm = window.confirm("Would you like me to remember this?")
    if (confirm) {
        document.getElementById("intent_form").submit();
    }
}

//  TODO
//  - Displays all saved intentions in backend
function toggleSaveList() {
    var x = document.getElementById("save_list");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function load(sigil, shape) {
    setShape(shape);
    document.getElementById("id_intent").value = sigil;
    drawSigil();
}


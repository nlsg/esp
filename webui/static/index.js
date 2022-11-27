import { h, Component, render } from 'https://unpkg.com/preact?module';
let HOST = "http://192.168.43.31:5000/"

function initHttp(url, onLoad) {
  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", url, true);
  xhttp.onload = ()=> {
    let resp = JSON.parse(xhttp.response)
    onLoad(resp)}
  xhttp.send();
}

let constructText = (pin, val) => `pin: ${pin} value: ${val}`

function updatePinIO(path, pin) {
  return () => {
    initHttp(HOST + `${path}/${pin}`, (response) => {
      console.log(`${path}/`)
      console.log(response)
      $(`#gpio-header-Val-${pin}`).data("io")(response.value)
      })
  }
}

let PINS = [2, 14, 16, 17, 18, 19, 21, 22, 23]

window.tag = (tag, props, inner="") => {
  if (!tag) return
  var propStr = ""
  if (props) for (const key in props)
    propStr += ` ${key}='${props[key]}'`
  return `<${tag}${propStr}>${inner}</${tag}>`
}

function initGPIO(){

}
function initGPIOs(){
  for (let i in PINS){
    let header = (key, val) => {
      let id = `#gpio-header-${key}-${pin}`
      return $(tag("span", {id: id.slice(1)},`${key}: ${val}`))
        .css({paddingLeft: "10%"})
        .data({io: (value) => {
          console.log(value)
          $(id).text(`${key}: ${value}`)}})
    }
    let pin = PINS[i]
    let attributes = (type) => {return {id:`gpio-${type}-${pin}`, class: "grid-item"} }
    $("#gpio-container").append(
      $(tag("div",{id:`gpio-header-${pin}`}))
        .append(header("Pin", pin))
        .append(header("Val", "-"))
        .append(header("Type", "-"))
        .append(header("Pull", "-"))
        .append($(tag("span", {},`ref: -`)).css({float: "right"}))
    ).append(
      $(tag("div",{id:`gpio-${pin}`, border: "20px"}))
        .append($(tag("button", attributes("pin"),`pin: ${pin}`))
                .click(updatePinIO("api/gpio/set", `${pin}`)))
        .append($(tag("button", attributes("val"),`val: -`)))
        .append($(tag("button", attributes("type"),`type: -`)))
        .click(updatePinIO("api/gpio/get", `${pin}`))
    )
    updatePinIO("api/gpio/get", `${PINS[i]}`)()
  }
}

window.toggleHeader = () => {
  var x = document.getElementById("myLinks");
  if (x.style.display === "block") {
    x.style.display = "none";
  } else {
    x.style.display = "block";
  }
}

window.ESP = HOST
window.initGPIOs = initGPIOs
initGPIOs()
$( function() {
  $("#screen").tabs()
  $("#gpio-container").accordion()
})
initGPIOs()

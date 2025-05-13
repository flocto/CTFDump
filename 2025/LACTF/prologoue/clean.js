let elements = document.getElementsByClassName("blocklyPath blocklyBlockBackground");

for (let i = 0; i < elements.length; i++) {
    // remove attributes if fill and stroke are both FFFFFF
    if (elements[i].getAttribute("fill") === "#FFFFFF" && elements[i].getAttribute("stroke") === "#FFFFFF") {
        elements[i].removeAttribute("stroke");
        elements[i].removeAttribute("fill");
        elements[i].removeAttribute("fill-opacity");
        // console.log(elements[i]);

    }
    // get g > rect from parent
    let parent = elements[i].parentElement;
    let rect = parent.getElementsByTagName("rect")[0];
    if (rect) {
        // remove rect if fill is FFFFFF
        if (rect.getAttribute("fill") === "#FFFFFF") {
            rect.remove();
            // console.log(rect);
        }
    }
}
const minValue = 1
const maxValue = 8


/**
 * Function that check if input value is in valid range
 * @param {Object} event
 */
function checkInput(event){
    let element = event.target
    if (element.value == ""){
        return
    }
    
    if (element.value < minValue){
        element.value = minValue
    } else if (element.value > maxValue){
        element.value = maxValue
    }
}

/**
 * Function that moves the focus based on input
 * @param {Object} event 
 */
function moveFocus(event){
    let element = event.target
    if (event.code=="ArrowLeft" && (element.value != '' || element.value != null)) {
        previousFocus(element)
        return
    }

    if (event.key >= minValue && event.key <= maxValue) {
        nextFocus(element)
    }
}

/**
 * function that moves focus to next element
 * @param {Object} element 
 */
function nextFocus(element){
    let nextSibling = element.nextElementSibling
    if (nextSibling.type == 'submit') {
        return
    }
    nextSibling.focus()
}

/**
 * Function that moves focus to previous element
 * @param {Object} element 
 */
function previousFocus(element){
    let previousSibling = element.previousElementSibling
    if (previousSibling == null || previousSibling == '') {
        return
    }
    previousSibling.focus()
}


// Event listeners
document.querySelectorAll(".letter-input").forEach(element=>
    element.addEventListener('input', Event=>checkInput(Event))
)

document.querySelectorAll(".letter-input").forEach(element=>
    element.addEventListener('keyup', Event=>moveFocus(Event))
)

/**
 * Used to ensure the input is not out of possible Values
 * 
 * @param element 
 */

function checkInput(element){
    if (element.value == ""){
        return
    }

    if (element.value < 1){
        element.value = 1
    } else if (element.value > 8){
        element.value = 8
    }
}

/**
 * Focuses on the next Input
 * 
 * @param enabledInput int, for focusing on precise input
 */
focusIndex = 1
function moveFocus(enabledInput){
    element = document.getElementsByClassName("letter-input")

    if (focusIndex >= element.length + enabledInput*4){
        return
    }
    if (focusIndex % 4 == 0){
        return
    }

    element[focusIndex + enabledInput*4].focus()
    focusIndex++
}

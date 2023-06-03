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


focusIndex = 1
function moveFocus(){
    element = document.getElementsByClassName("letter-input")
    console.log(element);

    if (focusIndex >= element.length){
        return
    }

    element[focusIndex].focus()
    focusIndex++
}
let optionResult = 0;

function clicked_advertising(){
    document.getElementById("zatemnenie").style.display = "block";
    document.body.style.overflow = "hidden";
};

function clicked_button(item){
    var valueInput = item.previousElementSibling.value;
    var answerInput = item.parentNode.parentNode.parentNode.children[1].children[0].getElementsByClassName('article__task__block__answer')[0].children[1].textContent; item.previousElementSibling.setAttribute('placeholder','Your Answer');
    valueInput = valueInput.replace(",",".");
    if ((isNaN(valueInput) == false) && (valueInput.trim() != '')){
        item.parentNode.parentNode.children[1].style.display = "block";
        item.parentNode.children[0].value = "";
        valueInput = valueInput.replace(".",",");
        if (valueInput != answerInput) {
            item.parentNode.parentNode.children[1].style.color = "red";
            item.parentNode.parentNode.children[1].innerHTML = "Incorrect answer";
        } else {
            item.parentNode.parentNode.children[1].style.color = "green";
            item.parentNode.parentNode.children[1].innerHTML = "Correct answer";
        }
    } else {
        item.parentNode.parentNode.children[1].style.display = "none"; 
        item.parentNode.children[0].value = ""; item.previousElementSibling.setAttribute('placeholder','Enter the number!');

    }
};

function clicked_accordion(item){
    if (item.parentNode.children[1].style.maxHeight != "") {
        item.parentNode.children[2].style.display = "flex";
    } else {
        item.parentNode.children[2].style.display = "none";
        item.parentNode.children[2].children[1].style.display = "none";
        item.parentNode.children[2].children[0].children[0].value = "";
    }
};

function close_panel(item){
    var panel = item.nextElementSibling;
    item.classList.toggle("active");
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
  };

function clicked_button_option(item){
    var valueInput = item.previousElementSibling.value;
    var answerInput = item.parentNode.parentNode.parentNode.children[1].textContent; item.previousElementSibling.setAttribute('placeholder','Your Answer');
    valueInput = valueInput.replace(",",".");
    if ((isNaN(valueInput) == false) && (valueInput.trim() != '')){
        item.parentNode.parentNode.children[1].style.display = "block";
        if (item.parentNode.children[0].value == answerInput){
            optionResult++  
        }
        document.getElementById("progress-bar").value += 1;
        if (document.getElementById("progress-bar").value == 11) {
            document.getElementById("option_result_btn").style.display = "block";
        }
        document.getElementById("result").innerHTML = optionResult;
        item.parentNode.children[0].value = "";
        valueInput = valueInput.replace(".",","); 
        item.parentNode.parentNode.children[1].style.color = "white";
        item.parentNode.parentNode.children[1].innerHTML = "Your answer has been accepted.";
        item.parentNode.style.display = "none";

    } else {
        item.parentNode.parentNode.children[1].style.display = "none"; 
        item.parentNode.children[0].value = ""; item.previousElementSibling.setAttribute('placeholder','Enter the number!');

    }
};

function clicked_button_option_result(item){
    document.getElementById("option_result_btn").style.display = "none";
    document.getElementsByClassName("option_result")[0].style.display = "block";
};

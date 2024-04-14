/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//todo
const inputBox = document.getElementById("input-box");
const listContainer = document.getElementById("list-container");
function addTask(){
    if(inputBox.value === ''){
        alert("You must write something!");
    }
    else{
        let li = document.createElement("li");
        li.innerHTML = inputBox.value;
        listContainer.appendChild(li);
        let span = document.createElement("span");
        span.innerHTML = "\u00d7";
        li.appendChild(span);
    }
    inputBox.value='';
    
    saveData();
}


listContainer.addEventListener("click",function(e){
    if(e.target.tagName === "LI"){
        e.target.classList.toggle("checked");
        saveData();
    }
    else if(e.target.tagName === "SPAN"){
        e.target.parentElement.remove();
        saveData();
    }
},false);

function saveData(){
    localStorage.setItem("data",listContainer.innerHTML);
}
function showTask(){
    listContainer.innerHTML=localStorage.getItem("data");
}
showTask();




///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//for meditation:
const circleProgress = document.querySelector('.circle-progress');
const numberOfBreaths = document.querySelector('.breath-input');
const start = document.querySelector('.start');
const instructions = document.querySelector('.instructions');
const breathText = document.querySelector('.breaths-text');
let breathsLeft = 3;

numberOfBreaths.addEventListener('change',()=>{
    breathsLeft=numberOfBreaths.value;
    breathText.innerText=breathsLeft;
});


const growCircle = ()=>{
    circleProgress.classList.add('circle-grow');
    setTimeout(()=>{
        circleProgress.classList.remove("circle-grow");
    },8000);
};

const breathTextUpdate = () =>{
    breathsLeft--;
    breathText.innerText=breathsLeft;
    instructions.innerText="Breath in";
    setTimeout(() => {
        instructions.innerText="Hold Breath";
        setTimeout(()=>{
            instructions.innerText="exhale slowly";
        },4000)
    }, 4000);
}


const breathingApp = ()=>{
    const breathingAnimation = setInterval(()=>{
        if(breathsLeft===0){
            clearInterval(breathingAnimation);
            instructions.innerText="Breathing session completed. Click 'Begin' to start again";
            start.classList.remove("button-inactive");
            breathsLeft=numberOfBreaths.value;
            breathText.innerHTML=breathsLeft;
            return;
        }
        growCircle();
        breathTextUpdate();
    },12000)
}
start.addEventListener('click',()=>{
    growCircle();
    breathTextUpdate();
    breathingApp(); 
});

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//swiper
var swiper = new Swiper(".mySwiper", {
    slidesPerView: 1,
    spaceBetween: 30,
    loop: true,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });
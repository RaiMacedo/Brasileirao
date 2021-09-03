function Mudadiv(){
    var cond = document.getElementById("info").selectedIndex
    if(cond == 1){
        document.getElementById("div1").style.display = "none";
        document.getElementById("div2").style.display = "none";
        document.getElementById("div0").style.display = "initial";
    }

    if(cond == 2){
        document.getElementById("div0").style.display = "none";
        document.getElementById("div2").style.display = "none";
        document.getElementById("div1").style.display = "initial";
    }
    
    if(cond == 3){
        document.getElementById("div0").style.display = "none";
        document.getElementById("div1").style.display = "none";
        document.getElementById("div2").style.display = "initial";
    }

    
}

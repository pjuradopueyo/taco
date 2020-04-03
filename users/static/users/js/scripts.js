  alert("Muchachooo");

/* 
function clapCounter() {
  console.log("Contando...");
  var claps = 1;
  var maxTime;
  var clapTimer;
  var init;

  $('.clap').click(function () {
    
    clearTimeout(clapTimer);
    if (claps == 1) {
      maxTime = setTimeout(sendApplause(), 60000); 
      init = Date.now();     
    }
    claps += 1;
    clapTimer = setTimeout(sendApplause(), 5000);

  });
  

  function sendApplause() {
    clearTimeout(clapTimer);
    var totalTime = (Date.npw() - init)/1000;
    alert(claps + " - " + totalTime);

  }
} */
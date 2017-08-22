var args = require('system').args;
var page = require('webpage').create();
var fs = require('fs');
var number = 100;
// Find the address given as parameter
var address = '';
args.forEach(function(arg, i) {
  if(i == 1) {
    address = arg;
  }
});


// Count how many boards are in the page
var countItens = function(){
  var reg = new RegExp('_tw _2k', 'g');
  var count = page.content.match(reg);
  if (count) { return count.length;}
  return 0
}

//Collect the page data
page.open(address, function (status) {

    if (status === "success") {
        window.setInterval(function() {
//            console.log("Now items : "+countItens());
            if (number > countItens()){
                page.evaluate(function() {
                    window.document.body.scrollTop = document.body.scrollHeight;
                });

            }
            else{
                console.log(page.content);
                page.render("page200.png");
                phantom.exit();
            }
        }, 500);

    }

});


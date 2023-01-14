$(document).ready(function() {
   $('body').html(function(i,val){
        return val.replace(/\$/g,"<span class ='dollarsign'>$</span>");
    });
});


$('h1').on('click', function(){
    $(this).toggleClass('turnBlue')})

$(document.documentElement).html(function(i,val){
    return val.replace(/\$/g,"<span class ='dollasign'>$</span>");
});

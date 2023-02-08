var acceptedCookies = Cookies.get('accepted_cookies');
if (acceptedCookies === undefined) {
Cookies.set('accepted_cookies', "false");
}

$(document).ready(function() {
  // Get the value of 'accepted_cookies'
  var acceptedCookies = Cookies.get('accepted_cookies');
//  console.log(Cookies.get('accepted_cookies')) --for testing

  if (acceptedCookies !== "true") {
    // stops scrolling
    $('html, body').css({overflow: 'hidden', height: '100%'});

    $('#cookie-banner').show();

  } else {
    // unstops scrolling
    $('html, body').css({overflow: 'auto', height: 'auto'});
  }

  $('#accept-cookies').click(function() {
    // Set the custom cookie 'accepted_cookies' to true
    Cookies.set('accepted_cookies', "true", { expires: 365 });
    $('#cookie-banner').hide();
    // unstops scrolling
    $('html, body').css({overflow: 'auto', height: 'auto'});
  });

  $('#learn-more-link').click(function(e) {
    e.preventDefault();
    $('#cookie-banner-details').toggle();
  });

  $('#decline-cookies').click(function() {
    // unstops scrolling
    $('html, body').css({overflow: 'auto', height: 'auto'});
    if (confirm("Are you sure you want to decline cookies? This will greatly limit the functionality of our website.")) {
      Cookies.remove('accepted_cookies');
      document.cookie = "_ga=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      var cookies = document.cookie.split(";");
      //loop through the cookies and get rid of google analytics cookies
        for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i];
          var eqPos = cookie.indexOf("=");
          var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
          if (name.startsWith("_ga_")) {
            document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
          }
        }
      $('#cookie-banner').hide();
    }
  });

});

;(function ($, window, undefined) {

  /* Javascript masterminded by Kevin Xu <kevin@imkevinxu.com> */
  $('.signup form').each(function() {
    var form = $(this);
    form.on('submit', function(e) {
      e.preventDefault();
      form.next().fadeOut();
      form.next().next().fadeOut();
      form.find('.loader').fadeIn();
      $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        success: function (data) {
          if (data['status'] === "success") {
            if (form.data('position') === "bottom") {
              $('.top.signup form').fadeOut();
            }
            form.fadeOut();
            form.next().delay(400).fadeIn();
          } else {
            form.next().next().fadeIn();
          }
        },
        error: function (data) {
          form.next().next().fadeIn();
        }
      });
    });
  });

  $('.top .email').on('focus', function() {
    $('.more-info').fadeIn();
  });

  $('.type').each(function() {
    $(this).on('click', function() {
      $('.type_other').val('');
      $('.type').removeClass('focus');
      $(this).toggleClass('focus');
      $("input[value="+$(this).data('type')+"]").click();
    });
  });

  $('.type_other').on('focus', function() {
    $('.type').removeClass('focus');
    $("input[type=radio]").prop('checked', false);
  });

  /* -----------------------------------------
     ZURB FOUNDATION INITIALIZERS
  ----------------------------------------- */

  var $doc = $(document);
  var Modernizr = window.Modernizr;

  $(document).ready(function() {
    $.fn.foundationAlerts           ? $doc.foundationAlerts() : null;
    $.fn.foundationButtons          ? $doc.foundationButtons() : null;
    $.fn.foundationAccordion        ? $doc.foundationAccordion() : null;
    $.fn.foundationNavigation       ? $doc.foundationNavigation() : null;
    $.fn.foundationTopBar           ? $doc.foundationTopBar() : null;
    $.fn.foundationCustomForms      ? $doc.foundationCustomForms() : null;
    $.fn.foundationMediaQueryViewer ? $doc.foundationMediaQueryViewer() : null;
    $.fn.foundationTabs             ? $doc.foundationTabs({callback : $.foundation.customForms.appendCustomMarkup}) : null;
    $.fn.foundationTooltips         ? $doc.foundationTooltips() : null;
    $.fn.foundationMagellan         ? $doc.foundationMagellan() : null;
    $.fn.foundationClearing         ? $doc.foundationClearing() : null;
    $.fn.placeholder                ? $('input, textarea').placeholder() : null;
  });

  // Hide address bar on mobile devices (except if #hash present, so we don't mess up deep linking).
  if (Modernizr.touch) {
    $(window).load(function () {
      setTimeout(function () {
        window.scrollTo(0, 1);
      }, 0);
    });
  }

  /* -----------------------------------------
     AUTO-SETS CSRF TOKEN FOR AJAX CALLS
  ----------------------------------------- */

  // Acquiring CSRF token and setting it to X-CSRFToken header for AJAX POST Request
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type)) {
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
      }
    }
  });

})(jQuery, this);
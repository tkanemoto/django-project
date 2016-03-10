var preferences = {};

$(function() {
  $(document).ready(function() {
    if ($('#navigation')) {
      $('#navigation > li > a').each(function(index, element) {
        var classes = $(element).attr('class').split(' ');
        for (var key in classes) {
          if ($('body').hasClass(classes[key])) {
            $(element).parent().addClass('active');
            break;
          }
        }
      });
    }
    //$('.nav .dropdown, .btn-group').mouseenter(function(){ if (!$(this).hasClass('open')) { $('> a.dropdown-toggle', this).click(); }});
    $('.tooltip').tooltip();
    $('.popover').popover();
    $("*[rel=popover]").popover();
    $('.dropdown-menu.prevent-dismissal').on('click', function(event){
      if (event.target.tagName != 'A') {
        event.stopPropagation();
      }
    });
    $('img.lazy').lazyload({ skip_invisible: false });
    $('.ajax[data-url]').each(function(index, element) { ajaxFragment(element); });
  });
});

/*
 * AJAX form submission
 *
 * Data attributes
 *  data-success-url
 *    The URL to redirect to after successful form submission
 *  data-action
 *    Preferred over the action attribute if set
 *  data-target
 *    The selector for the element to load the result into.
 *  data-no-redirect
 *    If set, there will be no URL transition. If data-target is set
 *    the content of the response to the form submission will be loaded
 *    into data-target.
 *  data-refresh-target
 *    If set, reload this part of the page using ajaxFragment.
 *  data-loading-target
 *    Selector of element shown during request.
 */
$(document).on('submit.tk.ajaxform', 'form.ajax-form', function(e) {
  e.preventDefault()
  if ($(this).attr('method') == 'get') {
    loadUrl($(this).attr('action') + '?' + $(this).serialize())
    return false
  }
  var form = $(this)
  if (form.is('[disabled]')) return false
  var action = form.data('action') ? form.data('action') : form.attr('action')
  $('input[type=submit], button[type=submit], fieldset', form).attr('disabled', 'disabled')
  form.attr('disabled', 'disabled')
  $(form.attr('data-loading-target'), form).show()
  clearErrors(form)
  $.post(action, $(this).serialize())
  .done(function(data){
    form.trigger('success.ajaxform', data)
  })
  .fail(function(response){
    showFormErrors(response, form)
    form.trigger('error.ajaxform')
  })
  .always(function(){
    $(form.attr('data-loading-target'), form).hide()
    $('input[type=submit], button[type=submit], fieldset', form).removeAttr('disabled').removeClass('disabled')
    form.removeAttr('disabled')
  })
  return false
})

$(document).on('success.ajaxform', 'form', function(e, data){
  var $this = $(this)
  ajaxFormSuccess($this, data)
  $this.trigger('postsuccess.ajaxform')
})

// Submit form on change for form.ajax-form-submit-on-change
$(document).on('change.tk.ajaxform', 'form.ajax-form.ajax-form-submit-on-change input, form.ajax-form.ajax-form-submit-on-change select', function(){
  $(this).closest('form').submit()
})

// Allow alternative actions to be set on buttons in forms
// a[data-action=<name>] sets action to be @form[data-action-<name>]
$(document).on('click.tk.alternativeformaction', 'form a[data-action]', function(e){
  var $this = $(this)
  var name = $this.data('action')
  var $form = $this.closest('form')
  if ($form.is('[data-action-' + name + ']')) {
    var url = $form.data('action-' + name)
    var urlOriginal = $form.data('action')
    var noRedirect = $this.data('action-' + name + '-no-redirect')
    var target = $this.data('action-' + name + '-target')
    var noRedirectOriginal = $form.data('no-redirect')
    var targetOriginal = $form.data('target')
    if (typeof noRedirect != 'undefined') {
      $form.data('no-redirect', noRedirect)
    }
    if (typeof target != 'undefined') {
      $form.data('target', target)
    }
    if (name == 'preview') {
      $form.append($('<input type="hidden" name="preview" value="preview">'))
    }

    $form.off('postsuccess.ajaxform.alternativeformaction').on('postsuccess.ajaxform.alternativeformaction', function() {
      if (typeof noRedirect != 'undefined') {
        if (typeof noRedirectOriginal == 'undefined') {
          $form.removeAttr('data-no-redirect').removeData('no-redirect')
        } else {
          $form.data('no-redirect', noRedirectOriginal)
        }
      }
      if (typeof target != 'undefined') {
        if (typeof targetOriginal == 'undefined') {
          $form.removeAttr('data-target').removeData('target')
        } else {
          $form.data('target', targetOriginal)
        }
      }
      if (name == 'preview') {
        $form.find('input[name=preview][type=hidden]').remove()
      }
      $form.data('action', urlOriginal)
    })
    $form.data('action', url).submit()
  }
})
/*
 * Programmatical page transition
 */
function loadUrl(url) {
  if (typeof url == 'undefined') {
    url = window.location.href
  }

  // Check special cases
  // - Ajax modals (#modal/...)
  // - Fragment AJAXing (#id:<id>/...)
  if (url.match(/^#modal\//)) {
    $.ajaxModal({url: url.replace('#modal', '')})
    return
  } else if (m = url.match(/^#id:([^\/]+)\//)) {
    var $e = $('#' + m[1])
    $e.attr('data-url', url.replace('#id:' + m[1], ''))
    ajaxFragment($e)
    return
  }

  // Convert canonical URL to absolute URL (e.g. '/projects/foobar')
  url = url.replace(window.location.protocol + '//' + window.location.host, '')

  // Catch transitions that only change the hash
  var hashOnly = false
  var currHash = window.location.hash
  var currPath = window.location.pathname + window.location.search
  if (url.length && url[0] == '#' && currHash != url) {
    hashOnly = true
  } else {
    if (url.indexOf('#') != -1) {
      var newHash = url.substring(url.indexOf('#'))
      var newPath = url.substring(0, url.indexOf('#'))
    } else {
      var newHash = ''
      var newPath = url
    }
    if (newPath == currPath  && newHash != currHash) {
      hashOnly = true
    }
  }

  if (hashOnly) {
    window.location.href = url
    return
  }

  if (preferences.ui_bool_use_pjax) {
    var replace = url == window.location.href;
    $.pjax({ url: url, container: '#pjax-container', replace: replace });
    pollNotifications();
  } else {
    if (url[0] == '/') {
      url = window.location.protocol + '//' + window.location.host + url;
    }
    if (url == window.location.href) {
      window.location.reload();
    } else {
      window.location.href = url
    }
  }
}

/*
 * Fetch an HTML fragment using AJAX into [data-url] elements
 * @TODO: turn into jQuery plugin
 */
function ajaxFragment(element) {
  var $e = $(element).closest('[data-url]');
  var ajax_url = $e.attr('data-url');
  $e.addClass('ajax-loading').removeClass('ajax');  // don't issue ajax request multiple times
  $e.load(ajax_url, function(res, status) {
    $e.addClass('ajax-loaded').removeClass('ajax-loading');
    if (status == 'error') {
      var url = $e.attr('data-url');
      $e.html(
        '<div class="alert alert-warning">Error loading <code>' + url + '</code>' +
        '<a class="pull-right" href="javascript:;" onclick="ajaxFragment(this);">Retry</a></div>');
    } else {
      if (!$e.closest('#page > .tooltip.in, #page > .popover.in').length) {
        cleanUI();
      }
      refreshUI($e);
    }
  });
}

/*
 * Handle possible page transitions based on the data attributes on `form`.
 * For data-no-redirect="true" elements, the `data` argument must be given
 * to set the HTML of data-target directly.
 */
function ajaxFormSuccess(form, data) {
  var successUrl = form.data('success-url') || window.location.href
  var target = form.data('target') || null
  var noRedirect = form.data('no-redirect') || false
  var refreshTarget = form.data('refresh-target') || null

  if (successUrl == '__absolute_url__' && typeof data.absolute_url != 'undefined') {
    successUrl = data.absolute_url
  }
  if (refreshTarget && $(refreshTarget).length) {
    ajaxFragment($(refreshTarget))
  }
  if (target) {
    if (target == '__parent__') {
      var $target = form.parent()
    } else {
      var $target = $(target)
      if ($target.length != 1) {
        $target = form.closest(target)
      }
    }
    if (noRedirect) {
      $target.html(data)
      if ($target.find('> form').length == 1) {
        $target.find('> form').trigger('invalidated.cmweb.ui')
      } else {
        $target.trigger('invalidated.cmweb.ui')
      }
    } else {
      $target.attr('data-url', successUrl)
      ajaxFragment($target.get(0))
      pollNotifications()
    }
  } else {
    if (!noRedirect && !refreshTarget) {
      loadUrl(successUrl)
    }
  }
}


// Extend Bootstrap behaviour with ajaxFragment

$(document).on('show.bs.tab', '[data-url]', function(e) {
  var url = $(this).data('url')
  var target = $(e.target).data('target') || $(e.target).attr('href')
  $(target).attr('data-url', url).removeClass('ajax-loaded')
  ajaxFragment($(target))
})

/*
 * Form error handling
 */

function setFieldError(key, message) {
  var $g = $('#id_' + key).closest('.form-group')
  $g.addClass('has-error has-feedback')
  $g.find('.form-status').html(message).show()
  $g.find('.form-control-feedback').show()
  $g.show()
}

function setErrorAlert($mbody, msg) {
  if (typeof msg == 'undefined') {
    msg = 'There were errors in the input.  Please check the items annotated in red.'
  }
  $('.status', $mbody).addClass('alert alert-danger').html(msg)
}

function showFormErrors(response, $mbody) {
  var text = ''
  try {
    var errors = JSON.parse(response.responseText)
    if (errors.length == 1 && typeof errors[0] == 'string') {
      text = errors[0]
    } else {
      for (var i = 0; i < errors.length; i++) {
        for (var key in errors[i]) {
          if (/-__all__$/.test(key)) {
            var selector = '.form-status-' + key.replace(/-__all__$/, '')
            $(selector).html(errors[i][key]).show()
          } else if (key != '__all__') {
            setFieldError(key, errors[i][key]);
          } else {
            text = errors[i][key];
          }
        }
      }
    }
  } catch(e) {
    text = response.responseText;
  }
  var msg = 'The request could not be processed'
  if (text.length) {
    msg = msg + ": <pre class='bg-primary bg-console'>" + text + "</pre>"
  }
  setErrorAlert($mbody, msg)
}

function clearErrors($mbody) {
  $('.status', $mbody)
    .html('')
    .removeClass('alert alert-danger')
  $('.form-group', $mbody)
    .removeClass('has-error')
    .removeClass('has-feedback')
  $('.form-status', $mbody).html('').hide()
  $('.form-group', $mbody)
    .find('.form-control-feedback').hide()
  $('.form-group-hidden', $mbody).hide()
}

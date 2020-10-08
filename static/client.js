// client-side js
// run by the browser each time your view template is loaded

// by default, you've got jQuery,
// add other scripts at the bottom of index.html

$(function() {
  console.log('hello world :o')
  
  $.get('/enlace', function(dreams) {
    dreams.forEach(function(dream) {
      $('<li></li>').text(dream).appendTo('ul#enlace')
    })
  })

  $('form').submit(function(event) {
    event.preventDefault()
    var dream = $('input').val()
    $.post('/enlace?' + $.param({dream: dream}), function() {
      $('<li></li>').text(dream).appendTo('ul#enlace')
      $('input').val('')
      $('input').focus()
    })
  })

})

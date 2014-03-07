jQuery(function() {
  jQuery('.refresh-widget').click(function(){
    jQuery(this).addClass('refreshing');
    jQuery(this).parent().parent().find('.widget-data').slideUp(150).load(jQuery(this).attr('data-url'), function() {
      jQuery(this).delay(150).slideDown(200);
      jQuery(this).parent().parent().find('.refresh-widget').removeClass('refreshing');
    });

    var objToday = new Date(),
      weekday = new Array('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'),
      dayOfWeek = weekday[objToday.getDay()],
      dayOfMonth = objToday.getDate(),
      months = new Array('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'),
      curMonth = months[objToday.getMonth()],
      curYear = objToday.getFullYear(),
      curHour = objToday.getHours(),
      curMinute = objToday.getMinutes(),
      curSeconds = objToday.getSeconds(),
      curZone = objToday.getTimezoneOffset();
    var rightnow = dayOfWeek + ", " + dayOfMonth + " " + curMonth + " " + curYear + " " + curHour + ":" + curMinute + ":" + curSeconds;

    jQuery(this).parent().find('abbr.timeago').remove();
    jQuery(this).parent().prepend('<abbr class="timeago">asd</div>');
    jQuery(this).parent().find('abbr.timeago').attr('title', rightnow).text(rightnow).timeago();
  });

  jQuery("abbr.timeago").timeago();
  
});
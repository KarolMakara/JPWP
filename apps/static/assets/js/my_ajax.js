$(document).ready(function() {
    updateTable();
    md.initDashboardPageCharts();
  });
  setInterval(updateTable, 2000);

function updateTable() {
        $.ajax({
            url: '/notifications-data',
            type: 'POST',
            data: {

            },
            success: function(response) {

              var notifications = response.notifications;
              console.log(notifications)
    
              $('#notifications').empty();

              $('#notifications_count').empty();
              $('#notifications_count').append(notifications[0].count)

              notifications.forEach(function(notification) {
                if (notification.message.includes('Daily')){
                  $('#notifications').append(`
                    <a class="dropdown-item text-success" href="report">${notification.message}</a>
                 `);
                }
              });
              

    
              notifications.forEach(function(notification) {
                  var danger = '';
                  if (notification.message.includes('Missed')){
                    danger = 'text-danger';
                  }
                  if (!notification.message.includes('Daily')){
                    $('#notifications').append(`
                    <a class="dropdown-item ${danger}" href="/notifications/mark-as-seen/${notification.id}">${notification.message}</a>
                  `);
                  }
                
              });
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    }


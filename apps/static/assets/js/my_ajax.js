$(document).ready(function() {
    // Javascript method's body can be found in assets/js/demos.js
    md.initDashboardPageCharts();
    updateTable();

  });

  setInterval(updateTable, 10000);

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
                var danger = '';
                  if (notification.message.includes('Missed')){
                    danger = 'text-danger';
                  }
                  $('#notifications').append(`
                   <a class="dropdown-item ${danger}" href="/notifications/mark-as-seen/${notification.id}">${notification.message}</a>
                  `);
              });
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    }


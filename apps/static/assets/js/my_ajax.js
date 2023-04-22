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
                // Send any necessary data to the view
                // ...
            },
            success: function(response) {
              // Update the table with the new data
              var notifications = response.notifications; // <-- get the notifications data
              console.log(notifications)
    
              // Clear the existing rows from the table
              $('#notifications').empty();

              $('#notifications_count').empty();
              $('#notifications_count').append(notifications[0].count)
    
              // Append the updated rows to the table
              notifications.forEach(function(notification) {
                  $('#notifications').append(`
                   <a class="dropdown-item" href="/notifications/mark-as-seen/${notification.id}/">${notification.message}</a>
                  `);
              });
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    }


function startTimer() {
      var timerDisplay = document.getElementById('total-time-left');
      var time = 59; // Set the initial time to 59 seconds

      function updateTimer() {
        var minutes = Math.floor(time / 60);
        var seconds = time % 60;

        // Format the time as "mm:ss"
        var timeString = (minutes < 10 ? '0' : '') + minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
        timerDisplay.textContent = timeString;

        if (time <= 0) {
          // Timer has reached 00:00, you can add code to handle this event
          timerDisplay.textContent = '00:00';
          clearInterval(timerInterval);
        } else {
          time--; // Decrease the time by 1 second
        }
      }

      updateTimer(); // Call the function immediately to display the initial time
      var timerInterval = setInterval(updateTimer, 1000); // Update the timer every 1 second
    }

    startTimer();
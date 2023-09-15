
function loadCandleData() {
  if (document.getElementById('myDiv')) {
    // Send a GET request to fetch initial data
    fetch(candleInfoUrl)
      .then(response => {
        if (response.status === 200) {
          return response.json();
        } else {
          throw new Error(`HTTP Error: ${response.status}`);
        }
      })
      .then(data => processData(data))
      .catch(error => {
        console.error('Error:', error);
        
      });
  }
}

// POST request when the form is submitted
function makeplot() {
  const form = document.getElementById('candleChartForm');

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault(); 

      const formData = new FormData(this);
      console.log(formData);

      // Extract data from form to render details on screen
      const currency1 = formData.get('currency1');
      const currency2 = formData.get('currency2');
      const dateTime1 = formData.get('dateTime1');
      const dateTime2 = formData.get('dateTime2');
      const periods = formData.get('timeFrame');

      const currency1Display = document.getElementById('currency1Display');
      const currency2Display = document.getElementById('currency2Display');
      const dateTime1Display = document.getElementById('dateTime1Display');
      const dateTime2Display = document.getElementById('dateTime2Display');
      const periodDisplay = document.getElementById('timeFrameDisplay')

      if (currency1Display && currency2Display && dateTime1Display && dateTime2Display) {
        currency1Display.textContent = currency1;
        currency2Display.textContent = currency2;
        dateTime1Display.textContent = dateTime1;
        dateTime2Display.textContent = dateTime2;
        periodDisplay.textContent = periods;
      }

      // Send form data to the server using AJAX
      fetch(candleInfoUrl, {
        method: 'POST',
        body: formData,
      })
        .then(response => {
          if (response.status === 200) {
            console.log(response.status);
            return response.json();
          } else {
            throw new Error(`HTTP Error: ${response.status}`);
          }
        })
        .then(data => processData(data))
        .catch(error => {
          console.error('Error:', error);
          
        });
    });
  }
}

function processData(data) {
  console.log(data)
  const errorBanner = document.getElementById('errorBanner');
  const myDiv = document.getElementById('myDiv');

  if (data === 400 || data === 429 ) {
    console.log(data)
    myDiv.style.display = 'none';

    if (data === 400) {
      console.log("Trading pair is not found")
      displayErrorBanner("Trading pair is not found");
    } else if (data === 429) {
      console.log(`Reached request limit, wait a minute since your last request`)
      displayErrorBanner(`Reached request limit, wait a minute from your last request`);
    } else {
      displayErrorBanner("An unknown error occurred");
    }
  } 
  else {
    var data_open = [],
      data_close = [],
      data_high = [],
      data_low = [],
      data_volume = [],
      data_count = [],
      dates = [];

    for (var i = 0; i < data.length; i++) {
      row = data[i];
      data_open.push(parseFloat(row["price_open"]));
      data_close.push(parseFloat(row["price_close"]));
      data_high.push(parseFloat(row["price_high"]));
      data_low.push(parseFloat(row["price_low"]));
      data_volume.push(parseFloat(row["volume_traded"]));
      data_count.push(parseFloat(row["trades_count"]));
      var date = new Date(row["time_period_start"]);
      dates.push(date);
    }

    makePlotly(
      data_open,
      data_close,
      data_high,
      data_low,
      data_volume,
      data_count,
      dates
    );

  myDiv.style.display = 'block';
  }
}

function displayErrorBanner(message) {
  console.log(message)
  const errorBanner = document.getElementById('errorBanner');
  if (errorBanner) {
    errorBanner.textContent = message;
    errorBanner.style.display = 'block';

    errorBanner.style.backgroundColor = '#ff0000'; 
    errorBanner.style.color = '#FFC107'; 
    errorBanner.style.padding = '50px'; 
    errorBanner.style.margin = '150px auto'; 
    errorBanner.style.border = '3px solid #000000'; 
    errorBanner.style.borderRadius = '15px';  

    errorBanner.style.fontSize = '24px'; 
    errorBanner.style.fontWeight = 'bold';
  }
}

function makePlotly(
  data_open,
  data_close,
  data_high,
  data_low,
  data_volume,
  data_count,
  data_dates
) {
  var trace = {
    open: data_open,
    high: data_high,
    low: data_low,
    close: data_close,
    volume: data_volume,
    count: data_count,
    x: data_dates,

    increasing: {line: {color: 'black'}},
  decreasing: {line: {color: 'red'}},

  type: 'candlestick',
  xaxis: 'x',
  yaxis: 'y'

  };

  var data = [trace];

  var firstXValue = trace.x[0];
  var lastXValue = trace.x[trace.x.length - 1];

  var layout = {
    dragmode: 'zoom',
    showlegend: false,
    xaxis: {
      title: 'Date',
      range: [firstXValue, lastXValue]
    },
    yaxis: {
      autorange: true,
    }
  };

  Plotly.newPlot("myDiv", data, layout);
}

window.addEventListener('DOMContentLoaded', loadCandleData);

makeplot();
